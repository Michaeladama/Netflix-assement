from google_drive_assessment.auth import create_drive_service

def copy_file(service, file_id, destination_folder_id):
    copied_file = {'parents': [destination_folder_id]}
    service.files().copy(fileId=file_id, body=copied_file).execute()

def copy_folder(service, source_folder_id, destination_folder_id):
    query = f"'{source_folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    
    for item in results.get('files', []):
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            new_folder = service.files().create(body={
                'name': item['name'],
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [destination_folder_id]
            }).execute()
            copy_folder(service, item['id'], new_folder['id'])
        else:
            copy_file(service, item['id'], destination_folder_id)

def copy_source_to_destination(source_folder_id, destination_folder_id):
    service = create_drive_service()
    copy_folder(service, source_folder_id, destination_folder_id)
    print(f"Copied all content from {source_folder_id} to {destination_folder_id}")

if __name__ == "__main__":
    SOURCE_FOLDER_ID = "1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V"
    DESTINATION_FOLDER_ID = "16FugRGct1ZZfDWgH7xtWYYZts6yJtkmt"
    copy_source_to_destination(SOURCE_FOLDER_ID, DESTINATION_FOLDER_ID)
