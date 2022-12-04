from googleapiclient.http import MediaFileUpload
from .Google import Create_Service
import sys
import os

sys.path.insert(0, os.getcwd() + '/Drive/')

Client_Secret = 'Drive/client_secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPE = ['https://www.googleapis.com/auth/drive']

service = Create_Service(Client_Secret, API_NAME, API_VERSION, SCOPE)


def upload_files(file, parentID):
    file_metadata = {
        'name': file,
        'parents': [parentID]
    }
    media = MediaFileUpload('uploads/{0}'.format(file), mimetype='application/zip')
    temp = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return temp['id']


def create_folder(folders: list, parentID):
    for folder in folders:
        file_metadata = {
            'name': folder,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parentID]
        }
    sub_folder = service.files().create(body=file_metadata).execute()
    return sub_folder['id']


def create_parent_folder(parentName):
    file_metadata = {
        'name': parentName,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    root_folder = service.files().create(body=file_metadata).execute()
    return root_folder['id']

# parrent_id = '1hDSrXbTMiHYvDDDWd9RiSIH1DIMXY5hB'
# dir = ['vishnu']
#
# folder_id = create_folder(dir,parrent_id)
# print(folder_id)

# download_link = upload_files("111.zip", "1uEdloVc_v0cP55k5Hp8XbYCA_j-ZwrRK")
# print("https://drive.google.com/uc?export=download&id={0}".format(download_link))
def delete_file(id):
    service.files().delete(fileId=id, ).execute()
