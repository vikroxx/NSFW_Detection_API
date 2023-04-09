import base64
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

class ImageInput(BaseModel):
    base64: str

class DetectionResult(BaseModel):
    faces_detected: int

def detect_faces(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

@app.post("/detect_faces/", response_model=DetectionResult)
async def detect_faces_endpoint(image_input: ImageInput):
    base64_image = image_input.base64
    image_bytes = base64.b64decode(base64_image)
    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    faces = detect_faces(image)
    result = DetectionResult(faces_detected=len(faces))

    return result

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
