import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


def create_service():
    """
    Creates a Google Sheets service based on the credentials.json found in the current directory.
    """

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = None
    if os.path.exists("gsheets/token.pickle"):
        with open("gsheets/token.pickle", "rb") as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "gsheets/credentials.json", scopes)
            creds = flow.run_local_server(port=0)
    
        with open("gsheets/token.pickle", "wb") as token:
            pickle.dump(creds, token)
    
    service = build("sheets", "v4", credentials=creds)
    return service


def read_spreadsheet(service, sheet_id, cell_range):
    """
    Reads the contents of the given spreadsheet.
    """

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=cell_range).execute()
    values = result.get("values")
    return values


def update_spreadsheet(service, sheet_id, cell_range, values):
    """
    Updates the value of the cells.
    """

    body = values
    result = service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=cell_range,
        valueInputOption="RAW",
        body=body
        ).execute()
    print("{0} cells updated.".format(result.get("updatedCells")))


def append_spreadsheet(service, sheet_id, cell_range, values):
    """
    Appends the values at the end of the spreadsheet.
    """

    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=cell_range,
        valueInputOption="RAW",
        body=values
        ).execute()
    print("{0} cells appended.".format(result.keys()))
