import json
from google.cloud import storage

storage_client = storage.Client()
bucket_name = "dialogue-362312.appspot.com"


def upload(result):
    bucket = storage_client.bucket(bucket_name)

    file_name = result.get('guid')
    blob = bucket.blob(file_name)

    with blob.open("w") as f:
        json.dump(result, f)


if __name__ == '__main__':
    upload(result={'test': 'test2', 'guid': 'guid_test.json'})
