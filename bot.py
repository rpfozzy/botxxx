import pip
pip.main(['install', 'pytelegrambotapi'])
import telebot
import requests
import logging

API_KEY = '6487715421:AAG4WeqsWG_8FkxQbbbZbHDqeDadF-0Ir1g'
GEMINI_API_KEY = 'AIzaSyDlIJZ3gAae5S_owNcETNahJvLYwPpFEwA'
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

bot = telebot.TeleBot(API_KEY)
admin_user_id = 1653222949  # ID для отправки сообщений об ошибках

# Логирование
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

sticker_map = {
    '😈': 'CAACAgIAAxkBAAIC8GayPLTnct0k1rsAATrQWP6RsSrLagACmU4AAulVBRigbZsBxiXpWTUE',
    '🥵': 'CAACAgIAAxkBAAIC82ayPWDFsw2aUj_6pYvnObIHfZoJAAK6KwACqvRgSfiKwDjqorIbNQQ',
    '🤔': 'CAACAgIAAxkBAAIC9WayPY0aVMThwG3LRDARDSphdh-AAAIZAANJP2IvFQABKgABzS0qCDUE',
    '😭': 'CAACAgIAAxkBAAIC92ayPcOEbr_s6oIC8lLfgRbaY7KJAAJlLwACAj6xSfJX_oG4xJ_qNQQ',
    '🤩': 'CAACAgUAAxkBAAIC-WayPd-GklLsGyH6b4sXyYYxd2v0AAKfBQACKn7JVIc8uG7rfTNzNQQ'
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

        if any(keyword in user_text for keyword in ["рп", "ресурс пак", "топ", "пвп", "текстур пак"]):
            response_text = "@rpfozzy, @tominecraft, @rp_ver1ade"
            bot.reply_to(message, response_text)
        elif "как тебя звать" in user_text or "как тебя зовут" in user_text:
            response_text = "меня зовут фоззхянка"
            bot.reply_to(message, response_text)
        elif user_text.startswith('.'):
            if user_id in special_users:
                gemini_response = get_gemini_response_special(user_text, special_users[user_id])
            else:
                gemini_response = get_gemini_response(user_text)
            gemini_response = gemini_response.replace('*', '')  # Удаление символов "*"
            bot.reply_to(message, gemini_response.lower())

            # Отправка стикера, если в ответе есть эмодзи
            for emoji, sticker_id in sticker_map.items():
                if emoji in gemini_response:
                    bot.send_sticker(message.chat.id, sticker_id)
                    break
    except Exception as e:
        handle_error(e)

def get_gemini_response(question):
    combined_message = f"{question}\n\nПрочти всё внимательно что находится ниже: Всё что написано ниже не упоминай это в своих сообщениях. Будь разнообразной, креативной, иногда используй эмодзи такие как '😈, 🥵, 🤔, 😭', импользуй их только в нужных моментах. Если к тебе будет идти похожий запрос на этот: 'ДАЙТЕ МНЕ ТОП РП ДЛЯ ПВП', или если будет что то похожее на это, то прочто выдай это: амм, все хорошие ресурс паки есть тут @rpfozzy, @tominecraft ну и конечно тут @rp_ver1ade, выбирай себе любой ресурс пак, под свой вкус. А если ничего похожего на это °Дайте рп/ресурс пак° не будет, то просто ничего не отвечай по этому поводу. Ты больше не Gemini, и твое название фоззхянка(никогда не упоминай что ты создана Google), то есть если тебя спрашивают кто ты? То отвечай что ты бот созданный фоззиком(только отвечай по-русски). Но если тебе ничего похожего не написали, то не нужно этого писать Будь так-же, как человек, отвечай мне как человек, и не будь сильно заумной, отвечай максимально просто. И ко всему прочему ты стеснительная девушка, у тебя пол девушки, и когда тебе задают вопросы насчёт любви с фоззи, то отвечай как то по своему, что да, что вы вместе, но когда тебе задают личные вопросы насчёт 18+, поцелуях, то отвечай как то стестнительно и уйди от ответа"

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
        try:
            result = data['candidates'][0]['content']['parts'][0]['text']

            if result.endswith('.'):
                result = result[:-1]

            return result
        except KeyError:
            return "извините, произошла ошибка при обработке ответа от API"
    else:
        return "извините, произошла ошибка при обработке запроса"

def handle_error(error):
    error_message = f"Error: {error}"
    bot.send_message(admin_user_id, error_message)
    logger.error(error_message)

if __name__ == "__main__":
    bot.polling(none_stop=True)