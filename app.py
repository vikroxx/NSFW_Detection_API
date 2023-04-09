# from api import predict, app
# from api.functions import download_image, process_base64_image
from functions import download_image, process_base64_image, detect_faces
import json
from config import PORT
import os
import uvicorn
import numpy as np 
from fastapi import FastAPI, Request
from nsfw_detector import predict

app = FastAPI()

model = predict.load_model('nsfw_detector/nsfw_model.h5')

@app.post("/liveness")
async def detect_nsfw_route(request: Request):
    
    # if not url:
    #     return {"ERROR": "URL PARAMETER EMPTY"}
    # image = await download_image(url)
    # if not image:
    #     return {"ERROR": "IMAGE SIZE TOO LARGE OR INCORRECT URL"}
    data = await request.json()
    base64= data['image']
    image = process_base64_image(base64)

    faces = detect_faces(image)
    num_faces = len(faces)
    image = image/255.0
    image = np.expand_dims(image, axis=0)

    probs = predict.classify_nd(model, image)
    results = dict(zip(['data'], probs))
    hentai = results['data']['hentai']
    sexy = results['data']['sexy']
    porn = results['data']['porn']
    drawings = results['data']['drawings']
    neutral = results['data']['neutral']

    if neutral >= 90:
        results['data']['is_nsfw'] = False
    else:
        results['data']['is_nsfw'] = True
    results['data']['num_faces'] = num_faces

    print(json.dumps(results, indent=2))
    return {'status' : 0}
    


# if __name__ == "__main__":
#     uvicorn.run("api:app", host="0.0.0.0", port=PORT, log_level="info", reload = True)
