import requests
import concurrent.futures
from glob import glob
import time
import base64
from tqdm import tqdm
import os

def jpeg_to_base64(image_filename):
    with open(image_filename, "rb") as img_file:
        # Read the binary image data
        img_data = img_file.read()
        # print(type(img_data))
        # Encode the binary image data to base64
        base64_str = base64.b64encode(img_data).decode("utf-8")

    return base64_str

def send_post_requests_concurrently(url, data_list, headers):
    # Create a function to send a single post request
    def send_post_request(data):
        response = requests.post(url, json={"image" : data}, headers=headers)
        return response.text
    
    # Use concurrent.futures to execute multiple post requests in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the post requests to the executor
        futures = [executor.submit(send_post_request, data) for data in data_list]
        
        # Wait for all the requests to complete and collect the results
        results = [f.result() for f in futures]
        
    # Return the results
    return results


url =  "http://15.207.192.148:8000/liveness"
headers = {
            "Content-Type": "application/json"
        }

data_list = []
for img in tqdm(os.listdir('images')[0:300]): 
    # print('Image : ' , img)
    # print(os.path.join('images' , img))
    base64_encoded_image = jpeg_to_base64(os.path.join('images' , img))
    data_list.append(base64_encoded_image)

# Send the post requests concurrently
t1= time.time()
results = send_post_requests_concurrently(url, data_list, headers)
print((time.time() - t1)*1000)
# Print the results
print(results)
print(len(results))