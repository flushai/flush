import os
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from flushai import ImageGallery
from flushai.loaders.base_loader import BaseLoader

class GoogleDriveLoader(BaseLoader):
    def __init__(self, folder_id, token_path, creds_path):
        self.folder_id = folder_id
        self.token_file = token_path
        self.creds_file = creds_path

    def load(self, num_images):
        service = self._get_drive_service()
        gallery = ImageGallery()

        # Initial parameters for the API call
        page_token = None
        query = f"'{self.folder_id}' in parents and mimeType contains 'image/'"
        fetched_images = 0

        while True:
            results = service.files().list(q=query, pageSize=1000, fields="nextPageToken, files(id, name)", pageToken=page_token).execute()
            items = results.get('files', [])

            if not items:
                print('No more image files found.')
                return gallery

            for item in items:
                if num_images and fetched_images >= num_images:
                    return gallery
                print(f"Downloading {item['name']}...")
                request = service.files().get_media(fileId=item['id'])
                img_data = io.BytesIO()
                downloader = MediaIoBaseDownload(img_data, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                gallery.add_image_from_bytes(img_data.getvalue(), item['name'])
                fetched_images += 1

            # Check if there are more files to fetch
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break

        return gallery

    # Set up the Drive API client
    def _get_drive_service(self):
        creds = None
        token_file = 'token.json'
        creds_file = 'client_secret_135692672093-gnehpv31bbpfhshehfknfj4m53h126nv.apps.googleusercontent.com.json'

        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_file, ['https://www.googleapis.com/auth/drive.readonly'])
                creds = flow.run_local_server(port=0)
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
        
        service = build('drive', 'v3', credentials=creds)
        return service