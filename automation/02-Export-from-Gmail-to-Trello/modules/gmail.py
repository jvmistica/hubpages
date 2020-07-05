import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from apiclient import errors


def create_service(scopes):
    """
    Creates a Gmail service based on the credentials.json found in the current directory.
    """

    creds = None
    if os.path.exists("modules/token.pickle"):
        with open("modules/token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "modules/credentials.json", scopes)
            creds = flow.run_local_server(port=0)
        with open("modules/token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service


def query_messages(service, user_id, subject):
    """
    Searches the mailbox for a matching subject.
    """

    try:
        query = f"subject: {subject}"
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if "messages" in response:
            messages.extend(response["messages"])
        while "nextPageToken" in response:
            page_token = response["nextPageToken"]
            response = service.users().messages().list(userId=user_id, q=query, \
                                                       pageToken=page_token).execute()
            messages.extend(response["messages"])
        return messages
    except errors.HttpError as error:
        print("An error occurred.", error)


def read_message(service, user_id, msg_id):
    """
    Read the contents of the email.
    """

    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        return message
    except errors.HttpError as error:
        print("An error occurred.", error)
