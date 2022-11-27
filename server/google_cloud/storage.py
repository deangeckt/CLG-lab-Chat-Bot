import json
from google.cloud import storage

storage_client = storage.Client()
bucket_name = "dialogue-362312.appspot.com"


def save_to_storage(result):
    bucket = storage_client.bucket(bucket_name)

    file_name = result.get('guid')
    blob = bucket.blob(file_name + '.json')

    with blob.open("w") as f:
        json.dump(result, f)


if __name__ == '__main__':
    save_to_storage(result={'test': 'test2', 'guid': 'guid_test.json'})
