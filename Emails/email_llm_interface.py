import json
from copy import deepcopy
from .email_api import EmailAPI

def emails_check_unread(api: EmailAPI):
    n_unread = api.check_unread_emails()
    if n_unread == 0:
        return []
    emails_info = api.get_recent_emails(
        n_unread)
    minimal_info = deepcopy(emails_info)
    for email in minimal_info:
        email = {
            "sender": email["sender"],
            "subject": email["subject"],
            "content": email["content"],
        }
    return str(minimal_info)

def emails_read(api: EmailAPI, f_args:str):
    if json.loads(f_args).get("n_emails"):
        emails_info = api.get_recent_emails(
            n_emails=json.loads(f_args)["n_emails"]
        )
    else:
        emails_info = api.get_recent_emails()
    minimal_info = deepcopy(emails_info)
    for email in minimal_info:
        email = {
            "sender": email["sender"],
            "subject": email["subject"],
            "content": email["content"],
        }
    return str(minimal_info)

def emails_reply(api: EmailAPI, f_args:str):
    success = api.reply_to_someone(
        receiver_name=json.loads(f_args)["receiver_name"],
        body=json.loads(f_args)["body"],
    )
    return str(success)
    
    