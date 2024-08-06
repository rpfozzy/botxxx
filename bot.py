import telebot

# Вставьте сюда ваш токен
API_TOKEN = '6487715421:AAG4WeqsWG_8FkxQbbbZbHDqeDadF-0Ir1g'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    # Получаем файл_id стикера
    file_id = message.sticker.file_id

    # Получаем файл по file_id
    file_info = bot.get_file(file_id)

    # Формируем URL для скачивания файла
    sticker_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}"

    # Отправляем ссылку пользователю
    bot.reply_to(message, sticker_url)

if __name__ == '__main__':
    bot.polling(none_stop=True)