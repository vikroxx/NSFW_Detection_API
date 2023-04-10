from config import MAX_IMAGE_SIZE
from random import randint
import aiohttp
import aiofiles

import base64
import numpy as np
from PIL import Image
from io import BytesIO
import cv2

MAX_IMAGE_SIZE = MAX_IMAGE_SIZE * 1000000


async def download_image(url):
    file_name = f"{randint(6969, 6999)}.jpg"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                if int(resp.headers['Content-Length']) > MAX_IMAGE_SIZE:
                    return False
                f = await aiofiles.open(file_name, mode='wb')
                await f.write(await resp.read())
                await f.close()
            else:
                return False
    return file_name


def pad_base64(encoded_image):
    padding = 4 - (len(encoded_image) % 4)
    if padding < 4:
        encoded_image += "=" * padding
    return encoded_image

def process_base64_image(encoded_image, target_size=(224, 224)):
    base64_data = encoded_image
    decoded_image = base64.b64decode(base64_data)
    # nparr = np.frombuffer(decoded_image, np.uint8)

    # Convert the decoded image bytes to a PIL image object
    img = Image.open(BytesIO(decoded_image))

    img1 = img.resize((600,600), Image.NEAREST)
    # Resize the image to the target size
    img = img.resize(target_size, Image.NEAREST)

    # Convert the PIL image object to a NumPy array
    img_array = np.asarray(img)
    img_array1 = np.asarray(img1)

    # Normalize the image data by dividing each pixel value by 255
    # img_array = img_array / 255.0
    bgr_img_array = img_array1[:, :, ::-1]

    return img_array, bgr_img_array


def detect_faces(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces
