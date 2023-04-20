import face_recognition
from requests import get
import numpy

known_encodings = []
list_of_famous_people = []
f = open('famous_people.txt', encoding="utf-8-sig")
lines = f.readlines()
for i in range(len(lines)):
    line = lines[i].rstrip('\n')
    list_of_famous_people.append(line)


def making_face_encoding():
    global known_encodings
    for i in range(len(list_of_famous_people)):
        url_photo = list_of_famous_people[i].split(", ")[1]
        response = get(url_photo)
        with open("tmp" + str(i) + ".jpg", "wb") as img_file:
            img_file.write(response.content)
        img_file = open("tmp" + str(i) + ".jpg", "rb")
        known_image = face_recognition.load_image_file(img_file)
        face_encoding = face_recognition.face_encodings(known_image)[-1]
        known_encodings.append(face_encoding)
        print("Encoded " + str(i + 1) + " of " + str(len(list_of_famous_people)) + " faces.")


making_face_encoding()
numpy.save("face_encoding", known_encodings, allow_pickle=True, fix_imports=True)
