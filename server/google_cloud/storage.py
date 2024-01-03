import json
from google.cloud import storage

storage_client = storage.Client(project='dialogue-362312')
bucket_name = "dialogue-362312.appspot.com"


def save_to_storage(result, file_guid):
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(file_guid + '.json')

    with blob.open("w") as f:
        json.dump(result, f)
