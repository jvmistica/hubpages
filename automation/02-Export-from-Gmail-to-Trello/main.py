import base64
from modules.gmail import create_service, query_messages, read_message
from modules.trello import create_board, create_list, create_card
from settings import email_address, scopes, subject, minutes_date, items_start, items_end


service = create_service(scopes)
messages = query_messages(service, email_address, subject)

# Go through each email that matches the subject
for message in messages:
    body = read_message(service, email_address, message.get("id"))
    parts = body["payload"]["parts"]
    for part in parts:
        if part["mimeType"] == "text/plain":
            message = part["body"]["data"]
            message = base64.b64decode(message).decode("utf-8")

    # Find the parts of the message from items_start to items_end inclusive
    lines = message.split("\r\n")
    subject_date = next(line.split()[1].replace("'", "") for line in lines if minutes_date in line)
    lines = lines[lines.index(items_start): lines.index(items_end)]

    # Create Trello board and list
    list_id = create_list(create_board(f"{subject} - {subject_date}"), items_start.replace("*", ""))
    for item in lines[1:-1]:
        item = item.strip()
        if item != "":
            create_card(list_id, item[2:])
