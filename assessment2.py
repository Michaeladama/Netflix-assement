from google_drive_assessment.auth import create_drive_service

def count_child_objects(service, folder_id):
    total_files, total_folders = 0, 0
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, mimeType)").execute()
    
    files = results.get('files', [])
    for f in files:
        if f['mimeType'] == 'application/vnd.google-apps.folder':
            folder_files, folder_folders = count_child_objects(service, f['id'])
            total_files += folder_files
            total_folders += folder_folders + 1
        else:
            total_files += 1
    return total_files, total_folders

def generate_recursive_report(source_folder_id):
    service = create_drive_service()
    top_level_folders = service.files().list(
        q=f"'{source_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id, name)"
    ).execute().get('files', [])
    
    report = {}
    for folder in top_level_folders:
        files, folders = count_child_objects(service, folder['id'])
        report[folder['name']] = {"files": files, "folders": folders}
    
    print(report)
    return report

if __name__ == "__main__":
    SOURCE_FOLDER_ID = "1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V"
    generate_recursive_report(SOURCE_FOLDER_ID)
