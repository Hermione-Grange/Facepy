# Добавим необходимый объект из модуля telegram.ext
from telegram.ext import CommandHandler
from telegram.ext import Application, MessageHandler, filters
import asyncio
#import face_recognition
import random


parametr = ""
list_of_famous_people = []
f = open('famous_people.txt', encoding="utf8")
lines = f.readlines()
for i in range(len(lines)):
    line = lines[i].rstrip('\n')
    list_of_famous_people.append(line)


def quiz2():
    a = random.randint(0, 2)
    url_photo = list_of_famous_people[a].split(", ")[1]
    return url_photo

async def question(update, context):
    url_photo = quiz2()
    await update.message.reply_photo(photo=url_photo)


# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я веселый бот Том! Напиши команду /help, чтобы узнать какие у меня функции есть)")


async def help(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Как мною пользоваться? "
                                    "У меня есть несколько функций: \n"
                                    "/quiz -- запускает викторину, в которой я буду предлагать тебе фотографии известных "
                                    "людей, а ты отгадывать кто это \n"
                                    "/guess -- присылай фотографию мне и я угадаю кто на ней изображен!"
                                    )


async def quiz(update, context):
    """Отправляет сообщение когда получена команда /quiz"""
    parametr = "qiuz"
    await update.message.reply_text("Угадай личность! вопросов будет 3")
    await question(update, context)


async def echo2(update, context):
    file = update.message.photo[-1]
    await update.message.reply_photo(photo=file)

def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token('6025902268:AAGQYal13ICn7AR9u0rOu2Rj3IpmxfULGfw').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("quiz", quiz))
    text_handler2 = MessageHandler(filters.PHOTO, echo2)

    application.add_handler(text_handler2)

    # Запускаем приложение.
    application.run_polling()

# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    quiz2()
    main()