import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']
folder_id = '1tha-65POJz9SPfRWkaLTY7g0K2txy0Ec'


def upload(result):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('google_drive/token.json'):
        creds = Credentials.from_authorized_user_file('google_drive/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('google_drive/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('google_drive/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        with open("google_drive/result.json", "w") as outfile:
            json.dump(result, outfile)

        service = build('drive', 'v3', credentials=creds)
        file_name = result.get('guid')
        file_metadata = {
            'name': f'{file_name}.json',
            'parents': [folder_id]
        }
        media = MediaFileUpload("google_drive/result.json", mimetype='application/json', resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        print(F'File with ID: "{file.get("id")}" has added to the folder with 'F'ID "{folder_id}".')

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred in google drive: {error}')


if __name__ == '__main__':
    upload(result={'test': 'test2', 'guid': 'guid_test'})
