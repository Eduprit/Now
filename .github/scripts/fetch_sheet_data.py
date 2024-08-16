import os
import json
import traceback
from google.oauth2 import service_account
from googleapiclient.discovery import build

try:
    # Setup the Sheets API
    creds_json = os.environ['GOOGLE_SHEETS_CREDENTIALS']
    creds_dict = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(creds_dict)
    service = build('sheets', 'v4', credentials=creds)

    # The ID and range of your spreadsheet
    SPREADSHEET_ID = '1EEIcQPmBOzSU-wXebN9i8SweDOrbAAfhr7Kd0cpYf3w'  # Replace this with your actual spreadsheet ID
    RANGE_NAME = 'Sheet1!A1:B50'  # Adjust if your sheet name or range is different

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    # Process the data and update your site files
    data = {}
    for row in values[1:]:  # Skip the header row
        if len(row) > 1:
            data[row[0]] = row[1]

    # Ensure the _data directory exists
    os.makedirs('_data', exist_ok=True)

    # Write to a JSON file
    with open('_data/site_content.json', 'w') as f:
        json.dump(data, f, indent=2)

    print("Data fetched and saved successfully!")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    print("Traceback:")
    print(traceback.format_exc())
    raise  # This will cause the script to exit with a non-zero status, indicating an error
