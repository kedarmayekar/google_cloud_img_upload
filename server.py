from flask import Flask, request, jsonify
from google.cloud import storage
from dotenv import load_dotenv
from flask_cors import CORS
import datetime
import os
import asyncio
load_dotenv()

app = Flask(__name__)
CORS(app)

# This is new
GOOGLE_CLOUD_BUCKET_NAME = os.environ['GOOGLE_CLOUD_BUCKET_NAME']
credentials_dict= {
            "type": os.environ['GCP_type'],
            "project_id": os.environ['GCP_project_id'],
            "private_key_id": os.environ['GCP_private_key_id'],
            "private_key": os.environ['GCP_private_key'],
            "client_email": os.environ['GCP_client_email'],
            "client_id": os.environ['GCP_client_id'],
            "auth_uri": os.environ['GCP_auth_uri'],
            "token_uri": os.environ['GCP_token_uri'],
            "auth_provider_x509_cert_url": os.environ['GCP_auth_provider_x509_cert_url'],
            "client_x509_cert_url": os.environ['GCP_client_x509_cert_url'],
            "universe_domain": os.environ['GCP_universe_domain']
            }


async def upload_image(uploaded_image):
    """ Uploads images to google cloud which are uploaded by frontend """
    # Define your credentials (replace with your own)
    client = storage.Client.from_service_account_info(credentials_dict)

    filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    blob = client.bucket(GOOGLE_CLOUD_BUCKET_NAME).blob(filename)
    
    # Use async upload method
    await asyncio.get_event_loop().run_in_executor(None, blob.upload_from_string, uploaded_image.read(), uploaded_image.content_type)

    print(f"Image uploaded to {GOOGLE_CLOUD_BUCKET_NAME}")
    return True

@app.route('/upload', methods=['POST'])
async def upload():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        image = request.files['image']
        upload_status = await upload_image(image)
        if upload_status:
            return jsonify({'message': 'Image uploaded successfully'}), 200

    except Exception as e:
        print('api call ', e)
        return jsonify({'message': 'Internal Server Error Upload failure', 'error': f'{e}'}), 500
    

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