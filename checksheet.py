import os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Set up the API credentials and build the service
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Path to your service account file

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

# Function to get sheet IDs from txt files with specific patterns in their filenames
def get_sheet_ids_from_txt_files():
    sheet_ids = []
    # Get the current directory where the script is located
    current_directory = os.path.dirname(os.path.realpath(__file__))
    
    # List all files in the current directory
    for filename in os.listdir(current_directory):
        if filename.endswith('.txt'):  # Only consider .txt files
            # Check if the file name matches the expected pattern
            if 'sheet_id' in filename:
                file_path = os.path.join(current_directory, filename)
                
                # Read the file and retrieve the sheet_id
                with open(file_path, 'r') as file:
                    sheet_id = file.read().strip()  # Get content and remove extra spaces/newlines
                    sheet_ids.append(sheet_id)  # Add sheet_id to the list
    
    return sheet_ids

# Function to check if a file exists by its file ID
def check_file_existence(file_id):
    try:
        file = drive_service.files().get(fileId=file_id).execute()
        print(f"File {file_id} exists: {file['name']}")
    except Exception as e:
        print(f"File {file_id} does not exist or has been deleted. Error: {e}")

# Function to list all Google Sheets files in the user's Drive
def list_all_google_sheets():
    try:
        results = drive_service.files().list(
            q="mimeType='application/vnd.google-apps.spreadsheet'",
            fields="nextPageToken, files(id, name)"
        ).execute()
        
        items = results.get('files', [])
        
        if not items:
            print("No Google Sheets found in your Google Drive.")
        else:
            print("\nAll Google Sheets in your Google Drive:")
            for item in items:
                print(f"Sheet Name: {item['name']}, Sheet ID: {item['id']}")
    
    except Exception as e:
        print(f"Error retrieving Google Sheets from Google Drive: {e}")

# Get sheet IDs from txt files in the current directory
sheet_ids = get_sheet_ids_from_txt_files()

# Check if files exist for each sheet_id from .txt files
print("\nChecking files from the .txt files:")
for sheet_id in sheet_ids:
    check_file_existence(sheet_id)

# List all Google Sheets in the user's Google Drive account
list_all_google_sheets()
