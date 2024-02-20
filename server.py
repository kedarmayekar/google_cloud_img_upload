from flask import Flask, request, jsonify
from google.cloud import storage
from dotenv import load_dotenv
from flask_cors import CORS
import datetime
import os
load_dotenv()

app = Flask(__name__)
CORS(app)

# This is new
GOOGLE_CLOUD_BUCKET_NAME = os.environ['GOOGLE_CLOUD_BUCKET_NAME']
def upload_image(uploaded_image):
    """ Uploads images to google cloud which are uploaded by frontend """
    try:
        # Define your credentials (replace with your own)
        credentials_path = "credentials/credentials.json"
        client = storage.Client.from_service_account_json(credentials_path)

        # Define a unique filename based on timestamp
        filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"

        # Create a blob object
        blob = client.bucket(GOOGLE_CLOUD_BUCKET_NAME).blob(filename)

        # Upload the image
        blob.upload_from_string(
            uploaded_image.read(),
            content_type=uploaded_image.content_type
        )

        print(f"Image uploaded to {GOOGLE_CLOUD_BUCKET_NAME}")
        return True
    except Exception as ae:
        print('func ',ae)
        return False

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        image = request.files['image']
        if upload_image(image):
            return jsonify({'message': 'Image uploaded successfully'}), 200
        else:
            return jsonify({'message': 'Internal Server Error'}), 500

    except Exception as e:
        print('api call ',e)


if __name__ == '__main__':
    app.run(debug=True)