from flask import Flask, request, jsonify
from google.cloud import storage
from dotenv import load_dotenv
from flask_cors import CORS
import json
import requests
from urllib.request import urlopen
import os
load_dotenv()

app = Flask(__name__)
CORS(app)
# # Set the path to the JSON key file for authentication
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials/credentials.json"
#
# # Define your bucket name
# GOOGLE_CLOUD_BUCKET_NAME = os.environ['GOOGLE_CLOUD_BUCKET_NAME']
# # Define your credentials (replace with your own)
# credentials_path = "credentials/credentials.json"
# client = storage.Client.from_service_account_json(credentials_path)
#
# folder_path = 'images'

# This is new
GOOGLE_CLOUD_BUCKET_NAME = os.environ['GOOGLE_CLOUD_BUCKET_NAME']
def upload_image(image_url):
    """ Uploads images to google cloud which are uploaded by frontend """
    try:
        # Define your credentials (replace with your own)
        credentials_path = "credentials/credentials.json"
        client = storage.Client.from_service_account_json(credentials_path)

        # response = requests.get(image_url)
        # file_path = "./images/downloaded_image_1"
        # # Open the URL directly using urllib
        # with urlopen(image_url) as response:
        #     # Read the binary data
        #     image_binary_data = response.read()

        # # Check if the request was successful (status code 200)
        # if response.status_code == 200:
        #         # Now 'response.content' contains the binary content of the image
        #     image_binary_data = response.content

            # You can save the binary data to a file or process it as needed
        # with open(file_path, "wb") as f:
        #     f.write(image_binary_data)
        # else:
        #     print(f"Failed to retrieve image. Status code: {response.status_code}")
        # Create a blob object
        # blob = client.bucket(GOOGLE_CLOUD_BUCKET_NAME).blob(file_path)
        #
        # # Upload the image
        # blob.upload_from_filename(file_path)

        bucket = client.get_bucket(GOOGLE_CLOUD_BUCKET_NAME)
        blob = bucket.blob('downloaded_image_1')
        blob.upload_from_string(image_url, content_type='image/jpeg')

        # def upload_image_to_gcs(bucket_name, image_name, image_data):
        #     client = storage.Client()
        #     bucket = client.bucket(bucket_name)
        #     blob = bucket.blob(image_name)
        #     blob.upload_from_string(image_data, content_type='image/jpeg')
        print(f"Image {image_url} uploaded to {GOOGLE_CLOUD_BUCKET_NAME}")
        return True
    except Exception as ae:
        print('func ',ae)
        return False

@app.route('/upload', methods=['POST'])
def upload():
    try:
        print('request ',request.files)
        print('request data',request.data)
        # if 'image' not in request.files:
        #     return jsonify({'error': 'No image provided'}), 400
        #
        # image = request.files['image']
        # print('type ',type(image), ' image ',image)
        json_data = request.data.decode('utf-8')
        data_dict = json.loads(json_data)
        image_url = data_dict.get('image')
        if upload_image(image_url):
            return jsonify({'message': 'Image uploaded successfully'}), 200
        else:
            return jsonify({'message': 'Internal Server Error'}), 500

    except Exception as e:
        print('api call ',e)
    # Now you can use the 'image_url' variable in your code

    # client = storage.Client()
    # bucket = client.get_bucket(GOOGLE_CLOUD_BUCKET_NAME)
    # blob = bucket.blob(image.filename)
    # blob.upload_from_file(image)
    #
    # # convert request.data bytes data to json format
    # jsonify_data = request.data.decode('utf-8')
    # print(jsonify_data)

    # # Upload the image
    # blob.upload_from_filename(file_path)

    # print(f"Image {file_path} uploaded to {GOOGLE_CLOUD_BUCKET_NAME}")    


if __name__ == '__main__':
    app.run(debug=True)