import base64
from gmail import gmail
from gsheets import gsheets


################################################################
# Extract CSV attachment from an email and save it locally.    #
################################################################

user_id = "<user_id>@gmail.com"
gmail_service = gmail.create_service()
messages = gmail.query_messages(gmail_service, user_id, "<subject>")

for message in messages:
    msg = gmail.read_message(gmail_service, user_id, message.get("id"))
    subject = next(header["value"] for header in msg["payload"]["headers"] if header["name"] == "Subject")
    parts = msg["payload"]["parts"]
    message_id = msg["id"]
    for part in parts:
        attachment_id = part["body"].get("attachmentId")
        if attachment_id:
            attachment = gmail_service.users().messages().attachments().get(userId=user_id,
                                                                      messageId=message_id,
                                                                      id=attachment_id
                                                                      ).execute()
            data = attachment["data"]
            file_data = base64.urlsafe_b64decode(data.encode("UTF-8"))
            path = part["filename"]
            with open(path, "wb") as f:
                f.write(file_data)


################################################################
# Read, update, and append values to Google Sheets.            #
################################################################

spreadsheet = "<spreadsheet_id>"
service = gsheets.create_service()

# Read values from the spreadsheet
rows = gsheets.read_spreadsheet(service, spreadsheet, "<tab_name>!A:D")
for row in rows:
    print(*row)

# Update spreadsheet
values = {"values": [["This cell is updated.", "This one too."]]}
gsheets.update_spreadsheet(service, spreadsheet, "<tab_name>!A8", values)

# Append to spreadsheet
values = {"values": [["This goes at the end.", "This one too."]]}
gsheets.append_spreadsheet(service, spreadsheet, "<tab_name>", values)


################################################################
# Extact CSV contents from the email attachment                #
# and append them to Google Sheets.                            #
################################################################

for message in messages:
    msg = gmail.read_message(gmail_service, user_id, message.get("id"))
    subject = next(header["value"] for header in msg["payload"]["headers"] if header["name"] == "Subject")
    parts = msg["payload"]["parts"]
    message_id = msg["id"]
    for part in parts:
        attachment_id = part["body"].get("attachmentId")
        if attachment_id:
            attachment = gmail_service.users().messages().attachments().get(userId=user_id,
                                                                      messageId=message_id,
                                                                      id=attachment_id
                                                                      ).execute()
            data = attachment["data"]
            file_data = base64.urlsafe_b64decode(data.encode("UTF-8"))
            file_data = [data.split(",") for data in file_data.decode().split("\r\n")]
            values = {"values": file_data}
            gsheets.append_spreadsheet(service, spreadsheet, "<tab_name>", values)
