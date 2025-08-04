import yaml
from google.cloud import storage
import os

# Load GCP config from environment variable or config file
def get_gcp_config():
    if os.getenv('GCP_BUCKET_NAME'):
        return {'bucket_name': os.getenv('GCP_BUCKET_NAME')}
    else:
        with open('config/gcp_config.yml', 'r') as file:
            return yaml.safe_load(file)

gcp_storage = get_gcp_config()

def get_gcs_file_as_text(file_name):
    client = storage.Client()
    bucket = client.bucket(gcp_storage['bucket_name'])
    blob = bucket.blob(file_name)
    return blob.download_as_text()

def upload_to_gcs_file(file_name, content):
    client = storage.Client()
    bucket = client.bucket(gcp_storage['bucket_name'])
    blob = bucket.blob(file_name)
    blob.upload_from_string(content)
    print(f"Successfully uploaded to {file_name}")
