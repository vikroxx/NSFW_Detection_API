from config import MAX_IMAGE_SIZE
from random import randint
import aiohttp
import aiofiles
import cv2
import numpy as np
from datetime import datetime
import base64
from PIL import Image
from io import BytesIO
import json
from datetime import datetime
import pytz


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
    print(img.size)
    img = crop_image_to_square(img)
    print(img.size)

    img1 = img.resize((300,300), Image.NEAREST)
    # Resize the image to the target size
    img = img.resize(target_size, Image.NEAREST)

    # Convert the PIL image object to a NumPy array
    img_array = np.asarray(img)
    img_array1 = np.asarray(img1)

    # Normalize the image data by dividing each pixel value by 255
    # img_array = img_array / 255.0
    bgr_img_array = img_array1[:, :, ::-1]

    return img_array, bgr_img_array


def process_base64_image_ios(encoded_image, target_size=(224, 224)):
    base64_data = encoded_image
    decoded_image = base64.b64decode(base64_data)
    # nparr = np.frombuffer(decoded_image, np.uint8)

    # Convert the decoded image bytes to a PIL image object
    img = Image.open(BytesIO(decoded_image))
    print(img.size)
    img = crop_image_to_square(img)
    print(img.size)

    # Rotate the image 90 degrees clockwise
    img = img.rotate(-90)

    img1 = img.resize((300,300), Image.NEAREST)
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


def crop_image_to_square(img):
    width, height = img.size
    
    if height > width:
        # Calculate the difference in height and divide by 2
        delta = (height - width) // 2
        
        # Crop the image from the top and bottom
        cropped_img = img.crop((0, delta, width, height - delta))
        
    elif width > height:
        # Calculate the difference in width and divide by 2
        delta = (width - height) // 2
        
        # Crop the image from the sides
        cropped_img = img.crop((delta, 0, width - delta, height))
        
    else:
        # Image is already square, no cropping needed
        cropped_img = img

    return cropped_img




def save_image_with_dict(image, features_dict, output_dir):
    # Create a black 300x300 image for the bottom part
    black_bg = np.zeros((300, 300), dtype=np.uint8)

    # Convert dictionary to JSON-formatted string with indentation
    json_text = json.dumps(features_dict, indent=2)
    
    # Split the JSON-formatted string into lines
    lines = json_text.split('\n')

    # Write the lines on the black background
    y = 20
    for line in lines:
        cv2.putText(black_bg, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        y += 20

    # Convert the black background to a 3-channel image
    black_bg = cv2.cvtColor(black_bg, cv2.COLOR_GRAY2BGR)

    # Concatenate the original image and the black background with text
    combined_image = np.concatenate((image, black_bg), axis=0)

    # Create the output file name with the current date, time, and milliseconds

    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).strftime("%Y%m%d_%H%M%S_%f")[:19]
    
    # local_timezone = datetime.now().astimezone().tzinfo
    # current_time = datetime.now(local_timezone).strftime("%Y%m%d_%H%M%S_%f")[:19]

    file_name = f"{output_dir}/image_{current_time}.jpg"

    # Save the combined image to the specified directory
    cv2.imwrite(file_name, combined_image)




