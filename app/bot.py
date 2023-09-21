import telebot
import os
from image_hash import CalcImageHash, CompareHash
import uuid


bot = telebot.TeleBot("6548015444:AAGe-BAM0B9wJdnglW5m3JCZV1i-BQTIVks")


# Путь для сохранения фотографий шаблона стеллажа
template_images_path = "../template_images/"

# Хранилище хешей
hash_storage = {}


@bot.message_handler(content_types=["text", "photo"])
def handle_template_image(message):

    if message.text:
        bot.send_message(
            message.from_user.id,
            "Загрузите фотографию стеллажа-шаблона, а затем фотографию стеллажа для сравнения",
        )
    if message.photo:
        print(hash_storage)
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

            # Сохраняем фотографию на сервере
            with open(unique_filename, "wb") as new_file:
                new_file.write(downloaded_file)

            image_hash = CalcImageHash(unique_filename)
            print(hash_storage)

            if len(hash_storage) == 0:
                hash_storage["rack_template"] = image_hash
                bot.send_message(
                    message.from_user.id,
                    "Фотография шаблона стеллажа успешно загружена.",
                )
                print(hash_storage)
            else:
                hash_storage["rack"] = image_hash
                bot.send_message(message.from_user.id, "Фотография стеллажа загружена")

            print(hash_storage)
            if len(hash_storage) == 2:
                # Вычисляем разницу между хешами
                hash1 = list(hash_storage.values())[0]
                hash2 = list(hash_storage.values())[1]
                difference = CompareHash(hash1, hash2)
                in_percent = int((difference / 64) * 100)
                hash_storage.clear()  # Очистить хеш хранилище
                bot.send_message(
                    message.from_user.id,
                    f"Разница между хешами: {difference}; отличие {in_percent} %",
                )
            print(hash_storage)

        except Exception as e:
            bot.send_message(
                message.from_user.id,
                "Произошла ошибка при сохранении фотографии: " + str(e),
            )


bot.polling(none_stop=True, interval=0)
