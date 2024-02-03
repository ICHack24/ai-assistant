from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Set up the Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(
        "/home/pita/Documents/PersonalProjects/ICHack24/credentials.json", SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials

def list_most_recent_emails():
    # Authenticate and authorize
    credentials = authenticate()
    service = build('gmail', 'v1', credentials=credentials)

    # Get the user's Gmail account information
    user_info = service.users().getProfile(userId='me').execute()
    user_email = user_info['emailAddress']

    # List the most recent emails
    results = service.users().messages().list(userId=user_email, labelIds=['INBOX'], maxResults=5).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
    else:
        print('Most recent emails:')
        for message in messages:
            msg = service.users().messages().get(userId=user_email, id=message['id']).execute()
            print(f"\n{msg}\n")
            print(f"Subject: {msg['subject']}, Date: {msg['internalDate']}")

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
#     if os.path.exists("token.json"):
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