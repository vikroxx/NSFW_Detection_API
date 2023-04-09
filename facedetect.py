import base64
import cv2
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from mtcnn.mtcnn import MTCNN

app = FastAPI()

class ImageInput(BaseModel):
    base64: str

class DetectionResult(BaseModel):
    faces_detected: int

def detect_faces(image):
    detector = MTCNN()
    faces = detector.detect_faces(image)
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


