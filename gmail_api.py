import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Set up the Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = Path(current_dir).parent

    token_path = parent_dir / "token.json"
    credentials_path = parent_dir / "credentials.json"

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    return creds

def list_most_recent_emails():
    # Authenticate and authorize
    credentials = authenticate()
    service = build('gmail', 'v1', credentials=credentials)

    # Get the user's Gmail account information
    user_info = service.users().getProfile(userId='me').execute()
    user_email = user_info['emailAddress']

    # List the most recent emails
    results = service.users().messages().list(userId=user_email, labelIds=['INBOX'], maxResults=2).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
    else:
        print(f'Most recent emails ({len(messages)}):')
        for message in messages:
            msg = service.users().messages().get(userId=user_email, id=message['id']).execute()
            print(f"\n{msg}\n\n\n")
            for k, v in msg.items():
                if k == "payload":
                    for k2, v2 in v.items():
                        if k2 == "headers":
                            for item_ in v2:
                                print(f"~~ {item_}\n\n")
                            # for k3, v3 in v2.items():
                            #     print("~~ ", k3, "\n", v3, "\n\n")
                            continue
                        print("## ", k2, "\n", v2, "\n\n")
                    continue
                print(k, "\n", v, "\n\n")
            # print(f"Subject: {msg['subject']}, Date: {msg['internalDate']}")
            # print(f"Subject: {msg['payload']['headers'][-3]['value']},\nDate: {msg['payload']['headers'][-5]['value']},\nFrom: {msg['payload']['headers'][-6]['value']}")
            print("\n", msg['snippet'], "\n\n\n")

if __name__ == '__main__':
    list_most_recent_emails()




# import os.path

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

# # If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


# def main():
#     """Shows basic usage of the Gmail API.
#     Lists the user's Gmail labels.
#     """
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists("token5.json"):
#         print("Here")
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "/home/pita/Documents/PersonalProjects/ICHack24/credentials.json", SCOPES
#             )
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())
  
#     try:
#         # Call the Gmail API
#         service = build("gmail", "v1", credentials=creds)
#         results = service.users().labels().list(userId="me").execute()
#         labels = results.get("labels", [])
  
#         if not labels:
#             print("No labels found.")
#             return
#         print("Labels:")
#         for label in labels:
#             print(label["name"])
  
#     except HttpError as error:
#         # TODO(developer) - Handle errors from gmail API.
#         print(f"An error occurred: {error}")


# if __name__ == "__main__":
#     print("before")
#     main()
#     print("after")