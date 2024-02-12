from google.cloud import storage

def upload_image():
    # Define your credentials (replace with your own)
    credentials_path = "credentials/credentials.json"
    client = storage.Client.from_service_account_json(credentials_path)
    # Define your bucket name
    bucket_name = "gc-photos-storage-dev"

    # Define the file path of the image you want to upload
    file_path = "./images/a-beautiful-women-with-green-floral-dress-with-on.jpg"

    # Create a blob object
    blob = client.bucket(bucket_name).blob(file_path)

    # Upload the image
    blob.upload_from_filename(file_path)

    print(f"Image {file_path} uploaded to {bucket_name}")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    upload_image()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
