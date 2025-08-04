import yaml
from google.cloud import storage

with open('config/gcp_config.yml', 'r') as file:
    gcp_storage = yaml.safe_load(file)

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
