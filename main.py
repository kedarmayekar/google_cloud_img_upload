from google.cloud import storage
from dotenv import load_dotenv
import os
load_dotenv()

# Define your bucket name
GOOGLE_CLOUD_BUCKET_NAME = os.environ['GOOGLE_CLOUD_BUCKET_NAME']
def upload_image():
    """ Uploads images to google cloud which are stored in images folder in current working directory """
    # Define your credentials (replace with your own)
    credentials_path = "credentials/credentials.json"
    client = storage.Client.from_service_account_json(credentials_path)

    folder_path = 'images'
    filenames = os.listdir(folder_path)

    for filename in filenames:
        file_path = f"./{folder_path}/{filename}"

        # Create a blob object
        blob = client.bucket(GOOGLE_CLOUD_BUCKET_NAME).blob(file_path)

        # Upload the image
        blob.upload_from_filename(file_path)

        print(f"Image {file_path} uploaded to {GOOGLE_CLOUD_BUCKET_NAME}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    upload_image()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
