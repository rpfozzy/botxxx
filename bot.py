import telebot

# Вставьте сюда ваш токен
API_TOKEN = '6487715421:AAG4WeqsWG_8FkxQbbbZbHDqeDadF-0Ir1g'

bot = telebot.TeleBot(API_TOKEN)

# ID стикера, который нужно отправить
STICKER_ID = 'CAACAgUAAxkBAAIC3WayOjLJBeRRcNJMudxAOATGtyOqAAJKBwACL3PQVBb_4XVqltbqNQQ'

@bot.message_handler(func=lambda message: message.text == '😈')
def send_sticker(message):
    bot.send_sticker(message.chat.id, STICKER_ID)

if __name__ == '__main__':
    bot.polling(none_stop=True)