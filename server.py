from flask import Flask, request, jsonify
from google.cloud import storage
from dotenv import load_dotenv
from flask_cors import CORS
import datetime
import os
import json
from cryptography.fernet import Fernet
import base64
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


# This is new
GOOGLE_CLOUD_BUCKET_NAME = os.environ['GOOGLE_CLOUD_BUCKET_NAME']
ENCRYPTION_KEY = os.environ['ENCRYPTION_KEY']
ENCRYPTED_GCP_DATA = os.environ['ENCRYPTED_GCP_DATA']

def convert_string_to_bytes(string_data):
    bytes_data = string_data.encode('utf-8')
    return bytes_data

cipher_suite = Fernet(convert_string_to_bytes(ENCRYPTION_KEY))

def decrypt_from_base64(base64_encrypted_data):
    # Decode the Base64 data
    encrypted_data = base64.b64decode(base64_encrypted_data.encode('utf-8'))

    # Decrypt the data
    decrypted_data = cipher_suite.decrypt(encrypted_data)

    # Convert bytes to JSON
    json_data = json.loads(decrypted_data.decode('utf-8'))

    return json_data

# Decrypt Base64 data to get back JSON
credentials_dict = decrypt_from_base64(ENCRYPTED_GCP_DATA)

def upload_image(uploaded_image):
    """ Uploads images to google cloud which are uploaded by frontend """
    # Define your credentials (replace with your own)
    client = storage.Client.from_service_account_info(credentials_dict)

    # Define a unique filename based on timestamp
    filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"

    # Create a blob object
    blob = client.bucket(GOOGLE_CLOUD_BUCKET_NAME).blob(filename)

    # Upload the image
    # blob.upload_from_filename(uploaded_image)
     # Upload the image
    blob.upload_from_string(
            uploaded_image.read(),
            content_type=uploaded_image.content_type
        )
    print(f"Image uploaded to {GOOGLE_CLOUD_BUCKET_NAME}")
    return True


@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        image = request.files['image']
        upload_status = upload_image(image)
        # # write uploaded image to images folder
        # file_path=f'./images/{image.filename}'
        # print('file path ',file_path)
        # image.save(file_path)
        # upload_status = upload_image(file_path)
        if upload_status:
            return jsonify({'message': 'Image uploaded successfully'}), 200

    except Exception as e:
        print('api call ',e)
        return jsonify({'message': 'Internal Server Error Upload failure', 'error': f'{e}'}).headers.add('Access-Control-Allow-Origin', '*'), 500

@app.route('/', methods=['GET','POST'])
def hello():
    if request.method == 'POST':
        return jsonify({'message': 'Working route method'}), 200
    return jsonify({'message': 'ok'}), 200

@app.route('/status', methods=['GET'])
def status_check():
    return "status ok"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))