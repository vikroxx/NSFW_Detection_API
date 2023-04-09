from api import predict, app
from api.functions import download_image, process_base64_image
from config import PORT
import os
import uvicorn
import numpy as np 

model = predict.load_model('nsfw_detector/nsfw_model.h5')




@app.get("/main")
async def detect_nsfw(url: str):
    return {'status' : 0}
    if not url:
        return {"ERROR": "URL PARAMETER EMPTY"}
    image = await download_image(url)
    if not image:
        return {"ERROR": "IMAGE SIZE TOO LARGE OR INCORRECT URL"}
    results = predict.classify(model, image)
    os.remove(image)
    hentai = results['data']['hentai']
    sexy = results['data']['sexy']
    porn = results['data']['porn']
    drawings = results['data']['drawings']
    neutral = results['data']['neutral']
    if neutral >= 25:
        results['data']['is_nsfw'] = False
        return results
    elif (sexy + porn + hentai) >= 70:
        results['data']['is_nsfw'] = True
        return results
    elif drawings >= 40:
        results['data']['is_nsfw'] = False
        return results
    else:
        results['data']['is_nsfw'] = False
        return results


@app.get("/verify_nsfw")
async def detect_nsfw_route(base64: str):
    # if not url:
    #     return {"ERROR": "URL PARAMETER EMPTY"}
    # image = await download_image(url)
    # if not image:
    #     return {"ERROR": "IMAGE SIZE TOO LARGE OR INCORRECT URL"}
    image = process_base64_image(base64)
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
    return results
    


# if __name__ == "__main__":
#     uvicorn.run("api:app", host="0.0.0.0", port=PORT, log_level="info", reload = True)
