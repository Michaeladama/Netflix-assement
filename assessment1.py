from google_drive_assessment.auth import create_drive_service


def generate_count_report(service, folder_id, output_path='count_report.txt'):
    """Generates a text report of file and folder counts in the specified folder."""
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])

    folder_count = sum(1 for item in items if item['mimeType'] == 'application/vnd.google-apps.folder')
    file_count = len(items) - folder_count

    with open(output_path, 'w') as file:
        file.write(f"Folder ID: {folder_id}\n")
        file.write(f"Total Files: {file_count}\n")
        file.write(f"Total Folders: {folder_count}\n\n")
        file.write("Contents:\n")
        for item in items:
            file.write(f"- {item['name']} ({'Folder' if item['mimeType'] == 'application/vnd.google-apps.folder' else 'File'})\n")

    print(f"Count report generated at {output_path}")

def main():
    service = create_drive_service()
    folder_id = '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V'  

  
    generate_count_report(service, folder_id)

if __name__ == "__main__":
    main()
