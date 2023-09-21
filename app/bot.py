import telebot
import os
from calc_image_hash import calc_image_hash
from compare_hash import compare_hash
import uuid


bot = telebot.TeleBot(
    "6548015444:AAGe-BAM0B9wJdnglW5m3JCZV1i-BQTIVks"
)  # Ваш ключ чат-бота


# Путь для сохранения фотографий шаблона стеллажа
template_images_path = "../template_images/"

# Хранилище хешей
hash_storage = {}


@bot.message_handler(content_types=["text", "photo"])
def handle_template_image(message):

    if message.text:
        bot.send_message(
            message.from_user.id,
            "Загрузите фотографию, а затем другую фотографию для сравнения",
        )
    if message.photo:

        try:
            # Получаем информацию о фотографии
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            file_path = file_info.file_path

            # Скачиваем фотографию шаблона стеллажа
            downloaded_file = bot.download_file(file_path)

            # Генерируем уникальное имя файла
            file_extension = os.path.splitext(file_path)[-1]
            unique_filename = template_images_path + str(uuid.uuid4()) + file_extension

            # Сохраняем фотографию в папку template_images_pash
            with open(unique_filename, "wb") as new_file:
                new_file.write(downloaded_file)

            # Вычисляем хеш
            image_hash = calc_image_hash(unique_filename)

            # Если фото еще не загружено
            if len(hash_storage) == 0:
                hash_storage["photo_1"] = image_hash
                bot.send_message(
                    message.from_user.id,
                    "Первая фотография загружена",
                )

            else:
                hash_storage["photo_2"] = image_hash
                bot.send_message(message.from_user.id, "Вторая фотография загружена")

            if len(hash_storage) == 2:
                # Вычисляем разницу между хешами
                hash1 = list(hash_storage.values())[0]
                hash2 = list(hash_storage.values())[1]
                difference = compare_hash(hash1, hash2)
                in_percent = int((difference / 64) * 100)
                hash_storage.clear()  # Очистить хеш хранилище
                bot.send_message(
                    message.from_user.id,
                    f"Разница между хешами: {difference}; отличие {in_percent} %",
                )

        except Exception as e:
            bot.send_message(
                message.from_user.id,
                "Произошла ошибка при сохранении фотографии: " + str(e),
            )


bot.polling(none_stop=True, interval=0)
