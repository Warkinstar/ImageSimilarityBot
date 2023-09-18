import telebot


bot = telebot.TeleBot("6548015444:AAGe-BAM0B9wJdnglW5m3JCZV1i-BQTIVks")

@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text.lower() == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)
