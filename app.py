# from api import predict, app
# from api.functions import download_image, process_base64_image
from functions import download_image, process_base64_image, detect_faces, save_image_with_dict, process_base64_image_ios
import json
from config import PORT
import os
import uvicorn
import numpy as np 
from fastapi import FastAPI, Request
from nsfw_detector import predict
import jwt
import cv2
import pytz
from datetime import datetime

app = FastAPI()

model = predict.load_model('nsfw_detector/nsfw_model.h5')

@app.post("/liveness")
async def detect_nsfw_route(request: Request):
    token = request.headers.get("token")

    if token is None:
        return {'status': -2, 'data': 'JWT token not provided!'}

    try:
        decoded_jwt = jwt.decode(token, "garvita123", algorithms=["HS256"])
        user_id = decoded_jwt["user_id"]
    except jwt.exceptions.InvalidTokenError:
        return {'status': -1, 'data': 'Invalid JWT token!'}

    if user_id != 'image_verification':
        return {'status': -1, 'data': 'Failed authentication'}
    
    data = await request.json()
    base64= data['image']
    platform  = data['os']
    print(platform)
    if platform =='ios':
        image, bgr_image = process_base64_image_ios(base64)
        # return {'status' : 0}
    else:
        image, bgr_image = process_base64_image(base64)

    # faces = detect_faces(bgr_image)
    # num_faces = len(faces)

    image = image/255.0
    image = np.expand_dims(image, axis=0)

    probs = predict.classify_nd(model, image)
    results = dict(zip(['data'], probs))

    # results['data']['num_faces'] = num_faces
    hentai = results['data']['hentai']
    sexy = results['data']['sexy']
    porn = results['data']['porn']
    drawings = results['data']['drawings']
    neutral = results['data']['neutral']

    if neutral + drawings >= 95:
        results['data']['is_nsfw'] = False
    else:
        results['data']['is_nsfw'] = True

    ist_timezone = pytz.timezone('Asia/Kolkata')
    current_time_ist = datetime.now(ist_timezone)
    results['data']['timestamp'] = current_time_ist.strftime('%Y-%m-%d %H:%M:%S %Z')

    print(json.dumps(results, indent=2))

    save_image_with_dict(bgr_image, results, output_dir= "saved_images")

    # if num_faces  == 0:
    #     return { 'status' : 1}
    # elif num_faces > 1 : 
    #     return {'status' : 2}
    # cv2.imwrite('output_image.jpg', bgr_image)


    if results['data']['is_nsfw']:
        return {'status' : 4}
    else:
        return {'status' : 0}
    
