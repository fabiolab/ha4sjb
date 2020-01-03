from googleapiclient.discovery import build
from httplib2 import Http
from googleapiclient.http import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = 'https://www.googleapis.com/auth/drive.file'
FOLDER_ID = '1z7RQWiFVzQV8nX-xuy3nbkTovuZq-9I3'
CREDENTIALS_FILE = "credentials.json"


class GoogleDrive:

    def __init__(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
        self.drive_service = build('drive', 'v3', http=creds.authorize(Http()))

    def upload_pdf_file(self, filepath: str, target_name: str) -> str:
        file_metadata = {
            'name': target_name,
            'mimeType': 'application/pdf',
            'parents': [FOLDER_ID]
        }
        media = MediaFileUpload(filepath,
                                mimetype='application/pdf',
                                resumable=True)
        uploaded_file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        url = f"https://drive.google.com/file/d/{uploaded_file.get('id')}/view"
        return url
