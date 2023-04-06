# Добавим необходимый объект из модуля telegram.ext
from telegram.ext import CommandHandler
from telegram.ext import Application, MessageHandler, filters
from datetime import date
import datetime
#import face_recognition




# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я веселый бот Том!")


async def help(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def quiz(update, context):
    """Отправляет сообщение когда получена команда /quiz"""
    await update.message.reply_text("Давай поиграм в викторину?!)")

def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token('6025902268:AAGQYal13ICn7AR9u0rOu2Rj3IpmxfULGfw').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("quiz", quiz()))


    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()