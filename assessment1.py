from google_drive_assessment.auth import create_drive_service

SOURCE_FOLDER_ID = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'

def count_files_and_folders(folder_id):
    service = create_drive_service()
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])
    
    total_files = sum(1 for item in items if item['mimeType'] != 'application/vnd.google-apps.folder')
    total_folders = sum(1 for item in items if item['mimeType'] == 'application/vnd.google-apps.folder')
    
    print(f"Total files: {total_files}")
    print(f"Total folders: {total_folders}")

if __name__ == '__main__':
    count_files_and_folders(SOURCE_FOLDER_ID)
