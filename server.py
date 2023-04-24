# Добавим необходимый объект из модуля telegram.ext
from telegram.ext import CommandHandler
from telegram.ext import Application, MessageHandler, filters
import face_recognition
import random
from requests import get
from PIL import Image, ImageDraw
import cv2
#from face_encoding import *
import numpy as np

eyebrows_color = (68, 54, 39, 128)
lips_color = (150, 0, 0, 128)
eyes_color = (0, 0, 0, 30)
eyeliner_color = (0, 0, 0, 255)
eyeliner_width = 2
red = (150, 0, 0, 128)
green = (119, 221, 119, 128)
blue = (14, 77, 146, 128)
picture = "карандаш"
parametr = ""
count = 0
known_encodings = []
list_of_famous_people = []
f = open('famous_people.txt', encoding="utf-8-sig")
lines = f.readlines()
for i in range(len(lines)):
    line = lines[i].rstrip('\n')
    list_of_famous_people.append(line)


def making_quiz_photos():
    global a
    a = random.randint(0, len(list_of_famous_people))
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
    global parametr
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
                                    "/guess -- присылай фотографию мне и я угадаю кто на ней изображен! \n"
                                    "/search --  пришли мне имя и фамилию человека, а я тебе пришлю его фотографию) \n"
                                    "/makeup -- сделает макияж. \n"
                                    "/sketching -- обработает фотографию под рисунок"
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
    elif parametr == "guess":
        await update.message.reply_text("Загрузи фото!)")
    elif parametr == "search":
        await searching_photo(update, context)
    elif parametr == "makeup":
        await getting_parametres(update, context)
    elif parametr == "sketching":
        await getting_parametres_of_picture(update, context)
    else:
        await echo(update, context)


async def quiz(update, context):
    """Отправляет сообщение когда получена команда /quiz"""
    global parametr
    global  count
    count = 0
    parametr = "quiz"
    await update.message.reply_text("Угадай личность! вопросов будет 3")
    await question(update, context)


async def guess(update, context):
    global parametr
    parametr = "guess"
    await update.message.reply_text("Пришлите фотографию, и я угадаю, кто это!")


async def loading_picture(update, context):
    obj = await context.bot.getFile(update.message.photo[-1].file_id)
    file = get(obj.file_path)
    print("Get user image " + str(file))
    with open('mytmp.jpg', 'wb') as f:
        f.write(file.content)
    img_file = open("mytmp.jpg", "rb")
    return img_file


async def getting_photo(update, context):
    global parametr
    if parametr == "guess":
        try:
            img_file = await loading_picture(update, context)
            fc_image = face_recognition.load_image_file(img_file)
            face_encoding = face_recognition.face_encodings(fc_image)[-1]
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            face_distance = face_distances.min()
            count = 0
            for i in range(len(face_distances)):
                count += 1
                if face_distances[i] == face_distance:
                    break
            name = list_of_famous_people[count - 1].split(", ")[0]
            if face_distance < 0.5:
                await update.message.reply_text("Это точно " + name + "!")
            elif face_distance > 0.5 and face_distance < 0.59:
                await update.message.reply_text("Наверное, это " + name + ".")
            else:
                await update.message.reply_text("Я не знаю кто это((")
            print("face distance of " + name + " is " + str(face_distance))
        except:
            print("processing failed")
            await update.message.reply_text("Хмм... Не могу обработать это изображение!")
    elif parametr == "makeup":
        await making_up_photo(update, context)
    elif parametr == "sketching":
        await making_sketching(update, context)
    else:
        await update.message.reply_text("Я не знаю что вы хотите. Вызовите, пожалуйста, одну из моих команд!)")


async def search(update, context):
    global parametr
    parametr = "search"
    await update.message.reply_text("Введите, пожалуйста, имя и фамилию известной личности, и я вам выдам ее фотографию.")


async def searching_photo(update, context):
    user_text = update.message.text
    for i in range(len(list_of_famous_people)):
        if user_text == list_of_famous_people[i].split(", ")[0]:
            url_photo = list_of_famous_people[i].split(", ")[1]
            await update.message.reply_photo(photo=url_photo)
            return
    await update.message.reply_text("Извините, такого человека я не знаю...")


async def makeup(update, context):
    global parametr
    parametr = "makeup"
    await update.message.reply_text("Пришли мне фотографию, и я сделаю макияж!) "
                                    "Вы можете указать какой цвет губ, глаз, поводки глаз, бровей, толщину подводки вы хотите."
                                    "пишите, например, глаза красные")


async def getting_parametres(update, context):
    global lips_color
    global eyes_color
    global eyeliner_color
    global eyeliner_width
    global eyebrows_color
    user_text = update.message.text
    user_text_list = user_text.split(" ")
    if "губы" in user_text_list:
        if user_text_list[1] == "красные":
            lips_color = red
        if user_text_list[1] == "зеленые":
            lips_color = green
        if user_text_list[1] == "голубые":
            lips_color = blue
    elif "глаза" in user_text_list:
        if user_text_list[1] == "красные":
            eyes_color = red
        if user_text_list[1] == "зеленые":
            eyes_color = green
        if user_text_list[1] == "голубые":
            eyes_color = blue
    elif "брови" in user_text_list:
        if user_text_list[1] == "красные":
            eyebrows_color = red
        if user_text_list[1] == "зеленые":
            eyebrows_color = green
        if user_text_list[1] == "голубые":
            eyebrows_color = blue
    elif "подводка глаз" in user_text_list:
        if user_text_list[1] == "красная":
            eyeliner_color = red
        if user_text_list[1] == "зеленая":
            eyeliner_color = green
        if user_text_list[1] == "голубая":
            eyeliner_color = blue
    elif "толщина подводки глаз" in user_text_list:
        eyeliner_width = user_text_list[3]


async def making_up_photo(update, context):
    file = await loading_picture(update, context)
    image = face_recognition.load_image_file(file)
    face_landmarks_list = face_recognition.face_landmarks(image)
    print("LANDMARK_LIST -- ", face_landmarks_list)

    pil_image = Image.fromarray(image)
    for face_landmarks in face_landmarks_list:
        d = ImageDraw.Draw(pil_image, 'RGBA')

        # Make the eyebrows into a nightmare
        d.polygon(face_landmarks['left_eyebrow'], fill=eyebrows_color)
        d.polygon(face_landmarks['right_eyebrow'], fill=eyebrows_color)
        d.line(face_landmarks['left_eyebrow'], fill=eyebrows_color, width=2)
        d.line(face_landmarks['right_eyebrow'], fill=eyebrows_color, width=2)

        # Gloss the lips
        d.polygon(face_landmarks['top_lip'], fill=lips_color)
        d.polygon(face_landmarks['bottom_lip'], fill=lips_color)
        d.line(face_landmarks['top_lip'], fill=lips_color, width=2)
        d.line(face_landmarks['bottom_lip'], fill=lips_color, width=2)

        # Sparkle the eyes
        d.polygon(face_landmarks['left_eye'], fill=eyes_color)
        d.polygon(face_landmarks['right_eye'], fill=eyes_color)

        # Apply some eyeliner
        d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=eyeliner_color, width=eyeliner_width)
        d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=eyeliner_color, width=eyeliner_width)

        pil_image.save("mytmp1.jpg")
        await update.message.reply_photo(photo="mytmp1.jpg")

async def getting_parametres_of_picture(update, context):
    global picture
    user_text = update.message.text
    if "карандаш" in user_text:
        picture = "карандаш"
    elif "тушь" in user_text:
        picture = "тушь"
    elif "акварель" in user_text:
        picture = "акварель"
    else:
        await update.message.reply_text("Не понял(... Можно рисунок тушью, акварелью или карандашом.")


async def sketching(update, context):
    global parametr
    parametr = "sketching"
    await update.message.reply_text("Пришли мне фотографию, напиши какой рисунок хочешь (акварельный, тушью или карандашом) и я пришлю тебе модифицированную фотографию")

async def making_sketching(update, context):
    global picture
    await loading_picture(update, context)
    img = cv2.imread("mytmp.jpg")
    if picture == "акварель":
        # effect of watercolor image
        watercolour_image = cv2.stylization(img, sigma_s=10, sigma_r=0.45)
        cv2.imwrite('mytmp1.jpg', watercolour_image)
        await update.message.reply_photo(photo='mytmp1.jpg')
    elif picture == "карандаш":
        # effect of pencil sketch
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_invert = cv2.bitwise_not(gray_img)
        img_smoothing = cv2.GaussianBlur(img_invert, (25, 25), sigmaX=100, sigmaY=100)
        final_img = cv2.divide(gray_img, 255 - img_smoothing, scale=255)
        cv2.imwrite('mytmp1.jpg', final_img)
        await update.message.reply_photo(photo='mytmp1.jpg')
    elif picture == "тушь":
        # effect of ink
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_invert = cv2.bitwise_not(gray_img)
        img_smoothing = cv2.GaussianBlur(img_invert, (25, 25), sigmaX=100, sigmaY=100)
        final_img = cv2.divide(gray_img, 255 - img_smoothing, scale=255)
        img_smoothing = cv2.GaussianBlur(final_img, (25, 25), sigmaX=1, sigmaY=0.1)
        cv2.imwrite('mytmp1.jpg', (20 * 255) / (256 - img_smoothing))
        await update.message.reply_photo(photo='mytmp1.jpg')


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token('6025902268:AAGQYal13ICn7AR9u0rOu2Rj3IpmxfULGfw').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CommandHandler("guess", guess))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(CommandHandler("makeup", makeup))
    application.add_handler(CommandHandler("sketching", sketching))
    application.add_handler(MessageHandler(filters.TEXT, get_answer))
    application.add_handler(MessageHandler(filters.PHOTO, getting_photo))


    # Запускаем приложение.
    application.run_polling()

# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    print("Load encodings...")
    known_encodings = np.load("face_encoding.npy")
    print(known_encodings)
    main()