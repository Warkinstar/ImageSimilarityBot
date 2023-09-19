import telebot
import os


bot = telebot.TeleBot("6548015444:AAGe-BAM0B9wJdnglW5m3JCZV1i-BQTIVks")


# Путь для сохранения фотографий шаблона стеллажа
template_images_path = "../template_images/"

@bot.message_handler(content_types=["photo"])
def handle_template_image(message):
    try:
        # Получаем информацию о фотографии
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        # Скачиваем фотографию шаблона стеллажа
        downloaded_file = bot.download_file(file_path)

        # Генерируем уникальное имя файла
        file_extension = os.path.splitext(file_path)[-1]
        unique_filename = template_images_path + str(message.from_user.id) + file_extension

        # Сохраняем фотографию на сервере
        with open(unique_filename, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.send_message(message.from_user.id, "Фотография шаблона стеллажа успешно сохранена.")

    except Exception as e:
        bot.send_message(message.from_user.id, "Произошла ошибка при сохранении фотографии: " + str(e))

bot.polling(none_stop=True, interval=0)