from googleapiclient.discovery import build
from httplib2 import Http
from googleapiclient.http import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials
from common.normalise import normalise
from loguru import logger
import json
import os
import wget

SCOPE = 'https://www.googleapis.com/auth/drive.file'


class GoogleDrive:

    def __init__(self, credentials: str):
        credentials = json.loads(credentials)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, SCOPE)
        self.drive_service = build('drive', 'v3', http=creds.authorize(Http()))

    def upload_pdf_file(self, filepath: str, target_name: str, google_drive_folder: str) -> str:
        file_metadata = {
            'name': target_name,
            'mimeType': 'application/pdf',
            'parents': [google_drive_folder]
        }
        media = MediaFileUpload(filepath,
                                mimetype='application/pdf',
                                resumable=True)
        uploaded_file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        url = f"https://drive.google.com/file/d/{uploaded_file.get('id')}/view"
        return url

    def import_files(self, files: list, google_drive_folder: str):
        for file in files:
            downloaded_filename, downloaded_fileext = os.path.splitext(file['file_url'])
            target_dir = '/tmp'
            target_file = normalise(
                f"HA_{file.get('first_name', 'NA').upper()}_{file.get('last_name', 'NA').capitalize()}_Certif{downloaded_fileext}")
            target_pathfile = f'{target_dir}/{target_file}'
            try:
                logger.info(
                    f"Download {file['file_url']} for {file.get('first_name', 'NA')} {file.get('last_name', 'NA')}")
                wget.download(file['file_url'], target_pathfile)
            except Exception as e:
                logger.error(f"Can't download {file['file_url']}. File skipped.")
                continue

            try:
                logger.info(f"Upload {target_file} to Google Drive")
                self.upload_pdf_file(target_pathfile, target_file, google_drive_folder)
            except Exception as e:
                logger.error(f"Can't Upload {target_file}. File skipped.")
                continue

            os.remove(target_pathfile)
