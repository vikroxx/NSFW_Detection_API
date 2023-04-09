from config import MAX_IMAGE_SIZE
from random import randint
import aiohttp
import aiofiles

import base64
import numpy as np
from PIL import Image
from io import BytesIO


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
    # Ensure the base64 string has correct padding
    # encoded_image = pad_base64(encoded_image)

    # # Decode the base64 encoded image
    # decoded_image = base64.b64decode(encoded_image)

    base64_data = encoded_image
    decoded_image = base64.b64decode(base64_data)
    # nparr = np.frombuffer(decoded_image, np.uint8)

    # Convert the decoded image bytes to a PIL image object
    img = Image.open(BytesIO(decoded_image))

    # Resize the image to the target size
    img = img.resize(target_size, Image.NEAREST)

    # Convert the PIL image object to a NumPy array
    img_array = np.asarray(img)

    # Normalize the image data by dividing each pixel value by 255
    img_array = img_array / 255.0

    return img_array


