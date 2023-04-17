# Добавим необходимый объект из модуля telegram.ext
from telegram.ext import CommandHandler
from telegram.ext import Application, MessageHandler, filters
import asyncio
#import face_recognition
import random


parametr = ""
count = 0
list_of_famous_people = []
f = open('famous_people.txt', encoding="utf8")
lines = f.readlines()
for i in range(len(lines)):
    line = lines[i].rstrip('\n')
    list_of_famous_people.append(line)


def making_quiz_photos():
    global a
    a = random.randint(0, 9)
    url_photo = list_of_famous_people[a].split(", ")[1]
    return url_photo

async def question(update, context):
    global count
    url_photo = making_quiz_photos()
    if parametr != "quiz3":
        await update.message.reply_photo(photo=url_photo)
    else:
        await update.message.reply_text("Вкиторина окончена!) Спасибо за участие! Вы ответили верно " + str(count) + " вопросов из 3")


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


async def echo(update, context):
    await update.message.reply_text(update.message.text)


async def checking_answer(update, context):
    global count
    user_text = update.message.text
    stroka = list_of_famous_people[a]
    spisok = stroka.split(", ")
    if user_text == spisok[0]:
        await update.message.reply_text("Да! Верно)")
        count += 1
    else:
        await update.message.reply_text("Увы и ах.. это неверный ответ. Это -- " + spisok[0] + ".")
    await question(update, context)


async def get_answer(update, context):
    global parametr
    if parametr == "quiz":
        await checking_answer(update, context)
        parametr = "quiz2"
    elif parametr == "quiz2":
        await checking_answer(update, context)
        parametr = "quiz3"
    elif parametr == "quiz3":
        await checking_answer(update, context)
        parametr = ""
    else:
        await echo(update, context)


async def quiz(update, context):
    """Отправляет сообщение когда получена команда /quiz"""
    global parametr
    parametr = "quiz"
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
    #pplication.add_handler((MessageHandler(filters.PHOTO, echo2))
    text_handler = MessageHandler(filters.TEXT, get_answer)
    application.add_handler(text_handler)


    # Запускаем приложение.
    application.run_polling()

# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    making_quiz_photos()
    main()