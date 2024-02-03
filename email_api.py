import os
from pathlib import Path

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Set up the Gmail API scopes

class EmailAPI():

    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
              'https://www.googleapis.com/auth/gmail.send']

    def __init__(self) -> None:
        self.creds = self._authenticate()
        self.service = build('gmail', 'v1', credentials=self.creds)

        # Get the user's Gmail account information
        user_info = self.service.users().getProfile(userId='me').execute()
        self.user_email = user_info['emailAddress']

    def _authenticate(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        current_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = Path(current_dir).parent

        token_path = parent_dir / "token.json"
        credentials_path = parent_dir / "credentials.json"

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(
                token_path, self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, "w") as token:
                token.write(creds.to_json())
        return creds
    
    def _create_email_dictionary(self, msg_data):
        # messageId = msg_data["id"]
        threadId = msg_data['threadId']
        header_info = msg_data['payload']['headers']
        messageId = [h['value'] for h in header_info
                     if h['name'].lower() == "message-id"][0]
        subject = [h['value'] for h in header_info
                   if h['name'].lower() == "subject"][0]
        date = [h['value'] for h in header_info
                if h['name'].lower() == "date"][0]
        sender_details = [h['value'] for h in header_info
                          if h['name'].lower() == "from"][0]
        # subject = header_info[-3]['value']
        # date = header_info[-5]['value']
        # sender_details = header_info[-6]['value']
        # print(sender_details)
        sender_details = sender_details.split("<")
        sender_name = sender_details[0][:-1]
        sender_email = sender_details[1][:-1]
        content = msg_data['snippet']
        return {
            "messageId": messageId,
            "threadId": threadId,
            "sender": sender_name,
            "sender_email": sender_email,
            "date": date,
            "subject": subject,
            "content": content,
        }
    
    def get_recent_emails(self, n_emails: int=15):
        # List the most recent emails
        results = self.service.users().messages().list(userId=self.user_email, labelIds=['INBOX'], maxResults=n_emails).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')
            return []
        else:
            print(f'Most recent emails ({len(messages)}):')
            emails_info = []
            for message in messages:
                msg = self.service.users().messages().get(userId=self.user_email, id=message['id']).execute()
                info = self._create_email_dictionary(msg)
                emails_info.append(info)
        return emails_info
    
    def _create_message(self, receiver, subject, body):
        message = MIMEMultipart()
        message['to'] = receiver
        message['subject'] = subject
        msg = MIMEText(body)
        message.attach(msg)
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        return {'raw': raw_message}

    def send_email(self, to, subject, body):
        try:
            message = self._create_message(to, subject, body)
            sent_message = self.service.users().messages().send(
                userId=self.user_email, body=message).execute()
            print(f"Message sent: {sent_message['id']}")
        except Exception as error:
            print(f"An error occurred: {error}")

    def reply_email(self, message_info: dict, body: str):
        message = MIMEMultipart()
        receiver = message_info["sender_email"]
        message_id = message_info["messageId"]
        thread_id = message_info["threadId"]
        message['In-Reply-To'] = message_id
        message['References'] = message_id
        message['to'] = receiver
        message['subject'] = "Re: " + message_info["subject"]
        msg = MIMEText(body)
        message.attach(msg)
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        reply =  {
            'raw': raw_message,
            'threadId': thread_id
        }

        try:
            sent_message = self.service.users().messages().send(
                userId=self.user_email, body=reply).execute()
            print(f"Message sent: {sent_message['id']}")
        except Exception as error:
            print(f"An error occurred: {error}")


if __name__ == '__main__':
    email_api = EmailAPI()
    info = email_api.get_recent_emails(15)
    for email in info:
        print(f"{email}\n\n")

    subject = 'testing sending'
    email_content = "Hey there I am a friendly bot"
    to = "ivankapelyukh@gmail.com"
    # email_api.send_email(to, subject, email_content)

    email_api.reply_email(info[-2], email_content)



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