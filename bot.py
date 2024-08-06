import telebot
import requests
import logging

API_KEY = 'YOUR_API_KEY'
GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY'
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

bot = telebot.TeleBot(API_KEY)
admin_user_id = 1653222949  # ID to send error messages to

# Logging setup
logger = logging.getLogger('telegram_bot')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler('bot_errors.log')
handler.setLevel(logging.ERROR)
logger.addHandler(handler)

# Возможные вариации имени
name_variations = ["фоззянка", "фоззянко", "фоззхюшка", "фоззяха", "фозиха"]

# ID пользователей и их специальные сообщения
special_users = {
    1420106372: "Пиши как мудрый философкий миллиардер...",
    1653222949: "Тебя если что звать фоззянка...",
    893032579: "Мой ник мордер...",
    6183589990: "Я кираше и я люблю жрать кириешки..."
}

# Словарь соответствия эмодзи и стикеров
emoji_to_sticker = {
    '😈': 'CAACAgIAAxkBAAEBGKFhIysEOpUO28QhFz_Wr3mAiDe4bwAC2gADrWW8FG0My60vh47aHgQ',
    '🥵': 'CAACAgIAAxkBAAEBGKNhIytcFY6u9YZcS7UozZhXh30yxAAC8QADrWW8FPZmIo5UFLtoHgQ',
    '🤔': 'CAACAgIAAxkBAAEBGKZhIyvQutHfGVKyA5U0KzNid7kPxQACvgADrWW8FCbcdkhlq7fdHgQ',
    '😭': 'CAACAgIAAxkBAAEBGKphIyy11bkJwSvIS8rkPa7ApwmOxQACxgADrWW8FBB2kISQ4bZlHgQ',
    '🤩': 'CAACAgIAAxkBAAEBGKphIyy11bkJwSvIS8rkPa7ApwmOxQACxgADrWW8FBB2kISQ4bZlHgQ'
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "приветт, я фоззянка. как я могу помочь?😈")

@bot.message_handler(commands=['name'])
def send_name(message):
    bot.reply_to(message, "меня зовут юлэй, но вы можете называть меня фоззян.")

@bot.message_handler(func=lambda message: message.reply_to_message is None)
def handle_message(message):
    try:
        user_text = message.text.lower()
        user_id = message.from_user.id

        bot.send_chat_action(message.chat.id, 'typing')  # Показываем статус "печатает"

        # Обработка ключевых слов
        if any(keyword in user_text for keyword in ["рп", "ресурс пак", "топ", "пвп", "текстур пак"]):
            response_text = "@rpfozzy, @tominecraft, @rp_ver1ade"
            bot.reply_to(message, response_text)
        elif "как тебя звать" in user_text or "как тебя зовут" in user_text:
            response_text = f"меня зовут фоззхянка"
            bot.reply_to(message, response_text)
        elif user_text.startswith('.'):
            if user_id in special_users:
                gemini_response = get_gemini_response_special(user_text, special_users[user_id])
            else:
                gemini_response = get_gemini_response(user_text)
            gemini_response = gemini_response.replace('*', '')  # Удаление символов "*"
            bot.reply_to(message, gemini_response.lower())

            # Анализ и отправка стикера
            send_sticker_if_emoji_present(message.chat.id, gemini_response)
    except Exception as e:
        handle_error(e)

def get_gemini_response(question):
    combined_message = f"{question}\n\nПрочти всё внимательно что находится ниже: ..."
    payload = {
        "contents": [{
            "parts": [{
                "text": combined_message
            }]
        }]
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(f'{GEMINI_API_URL}?key={GEMINI_API_KEY}', json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        result = data['candidates'][0]['content']['parts'][0]['text']
        if result.endswith('.'):
            result = result[:-1]
        return result
    else:
        return "извините, произошла ошибка при обработке запроса"

def get_gemini_response_special(question, special_message):
    combined_message = f"{question}\n\n{special_message}"
    payload = {
        "contents": [{
            "parts": [{
                "text": combined_message
            }]
        }]
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(f'{GEMINI_API_URL}?key={GEMINI_API_KEY}', json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        result = data['candidates'][0]['content']['parts'][0]['text']
        if result.endswith('.'):
            result = result[:-1]
        return result
    else:
        return "извините, произошла ошибка при обработке запроса"

def send_sticker_if_emoji_present(chat_id, response):
    for emoji, sticker_id in emoji_to_sticker.items():
        if emoji in response:
            bot.send_sticker(chat_id, sticker_id)
            break

def handle_error(error):
    error_message = f"Error: {error}"
    bot.send_message(admin_user_id, error_message)
    logger.error(error_message)

if __name__ == "__main__":
    bot.polling(none_stop=True)