import requests
from glob import glob
import time
import jwt
import os
import base64
import json 
import cv2
from tqdm import tqdm

def jpeg_to_base64(image_filename):
    with open(image_filename, "rb") as img_file:
        # Read the binary image data
        img_data = img_file.read()
        # print(type(img_data))
        # Encode the binary image data to base64
        base64_str = base64.b64encode(img_data).decode("utf-8")

    return base64_str

def write_dict_on_image(image_path, output_path, data_dict, position=(10, 40), font_scale=0.6, color=(0, 255, 0), thickness=2):
    # Read the image using OpenCV
    img = cv2.imread(image_path)

    # Convert the dictionary to a string
    data_str = json.dumps(data_dict, indent=2)

    # Define font and line type
    font = cv2.FONT_HERSHEY_SIMPLEX
    line_type = cv2.LINE_AA

    # Write the string on the image
    y = position[1]
    for line in data_str.split('\n'):
        cv2.putText(img, line, (position[0], y), font, font_scale, color, thickness, line_type)
        y += int(font_scale * 30)

    # Save the modified image
    cv2.imwrite(output_path, img)




def check_nsfw(base64_image):
    # Set the API endpoint URL
    url =  "http://15.207.192.148:8001/detect_faces/"

    headers = {
            "Content-Type": "application/json"
        }
    data = {
        "base64": base64_image,
    }

    # Send the POST request with the image data and headers
    response = requests.post(url, json = data, headers=headers)
    # print(response.status_code)
    return response

# print(os.listdir('images'))
for img in tqdm(os.listdir('teenagers')): 
    print('Image : ' , img)
    # print(os.path.join('images' , img))
    base64_encoded_image = jpeg_to_base64(os.path.join('teenagers' , img))
    t1 =time.time()
    response = check_nsfw(base64_encoded_image)
    print(time.time() -t1)
    if response.status_code == 200:
        # Get the response body as a string
        response_text = response.text
        # print("Response text:", response_text)

        # If the response is in JSON format, you can also parse it as a dictionary
        try:
            response_json = response.json()
            formatted_json = json.dumps(response_json, indent=4)
            write_dict_on_image(os.path.join('teenagers', img), os.path.join('teenager_face_output',img), response_json)

            # print("Response JSON:\n", formatted_json)
        except ValueError:
            print("The response body is not valid JSON.")
    else:
        print(f"Request failed with status code {response.status_code}")

