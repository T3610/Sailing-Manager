from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sqlite3
from datetime import datetime

from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'Keys.json'
credentials = None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1urL-VkFTOkZqX6S7ipQ-_IooGbmDZP-pYR94Ugo6xYQ'

service = build('sheets', 'v4', credentials=credentials)


conn = sqlite3.connect('DSC.db')
c = conn.cursor()
data = list(c.execute("select * FROM Racers"))
data[0] = list(data[0])
print(data)
time = str(datetime.now())
print(time)
data[0].append(time)

print(data)
# Call the Sheets API
sheet = service.spreadsheets()

Request = sheet.values().append(spreadsheetId = SAMPLE_SPREADSHEET_ID,range = "Sheet1!A1",
                                valueInputOption = "RAW", body ={"values":data}).execute()