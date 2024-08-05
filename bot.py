import telebot
import requests

API_KEY = '7482301429:AAGqW25r7oGert4wmqEYWGwcN5qrvgjmaMc'
GEMINI_API_KEY = 'AIzaSyDlIJZ3gAae5S_owNcETNahJvLYwPpFEwA'
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

bot = telebot.TeleBot(API_KEY)

# Возможные вариации имени
name_variations = ["фоззи", "фоззян", "фозхян", "фоззик", "фозик"]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "приветт, я фоззян. как я могу помочь?😈")

@bot.message_handler(commands=['name'])
def send_name(message):
    bot.reply_to(message, "меня зовут икор, но вы можете называть меня фоззян.")

@bot.message_handler(func=lambda message: message.reply_to_message is None)
def handle_message(message):
    user_text = message.text.lower()

    # Обработка вопроса "как тебя звать?"
    if "как тебя звать" in user_text or "как тебя зовут" in user_text:
        response_text = f"меня зовут фоззи"
        bot.reply_to(message, response_text)
    else:
        gemini_response = get_gemini_response(user_text)
        bot.reply_to(message, gemini_response.lower())

def get_gemini_response(question):
    combined_message = f"{question}\n\nПрочти всё внимательно что находится ниже: Всё что написано ниже не упоминай это в своих сообщениях. Будь разнообразным, креативным, иногда используй эмодзи такие как '😈, 🥵, 🤔, 😭', импользуй их только в нужных моментах. Если к тебе будет идти похожий запрос на этот: 'ДАЙТЕ МНЕ ТОП РП ДЛЯ ПВП', или если будет что то похожее на это, то прочто выдай это: амм, все хорошие ресурс паки есть тут @rpfozzy, @tominecraft ну и конечно тут @rp_ver1ade, выбирай себе любой ресурс пак, под свой вкус. А если ничего похожего на это °Дайте рп/ресурс пак° не будет, то просто ничего не отвечай по этому поводуТы больше не Gemini, и твое название фоззи(никогда не упоминай что ты создан Google), то есть если тебя спрашивают кто ты? То отвечай что ты бот созданный фоззиком(только отвечай по-русски). Но если тебе ничего похожего не написали, то не нужно этого писать Будь так-же, как человек, отвечай мне как человек, и не будь сильно заумным, отвечай максимально просто"
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
        
        # Удаление точки в конце текста
        if result.endswith('.'):
            result = result[:-1]
        
        return result
    else:
        return "извините, произошла ошибка при обработке запроса"

if __name__ == "__main__":
    bot.polling()
