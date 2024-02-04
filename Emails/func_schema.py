dictionary_form = \
"sender: The name of the sender\n" +\
"subject: The subject of the email\n" +\
"content: the content of the email"

email_tools = [
    {
        "type": "function",
        "function": {
            "name": "emails_check_unread",
            "description": "Inform the user on whether there are emails " +
                           "that they haven't read or that they are " +
                           "unaware of. If there are, it reads them",
            "parameters": {},
            "outputs": {
                "type": "object",
                "properties": {
                    "output": {
                        "type": "list",
                        "description": "The output will be a list of dictionaries " +
                                       f"Each dictionary will be of the form {dictionary_form}." +
                                       "If there were no emails the list will be epty",
                    },
                },
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "emails_read",
            "description": "Read the last emails from the user's inbox",
            "parameters": {
                "type": "object",
                "properties": {
                    "n_emails": {
                        "type": "integer",
                        "description": "The number of last emails to read",
                    },
                },
                "required": []
            },
            "outputs": {
                "type": "object",
                "properties": {
                    "output": {
                        "type": "list",
                        "description": "The output will be a list of dictionaries " +
                                        f"Each dictionary will be of the form {dictionary_form}",
                    },
                },
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "emails_reply",
            "description": "Reply to an email from someone",
            "parameters": {
                "type": "object",
                "properties": {
                    "receiver_name": {
                        "type": "string",
                        "description": "The name of the person who we want to " +
                                       "reply to. The name must match one of " +
                                       "the names from the previously read " +
                                       "emails, otherwise ask for clarification.",
                    },
                    "body": {
                        "type": "string",
                        "description": "This will be the body of the email. " +
                                       "The user will provide a summary of what " +
                                       "they want the email to be about. However " +
                                       "you should use that summary to write a " +
                                       "more elaborated body of text.",
                    },
                },
                "required": ['receiver_name', 'body']
            },
            "outputs": {
                "type": "object",
                "properties": {
                    "output": {
                        "type": "boolean",
                        "description": "Whether the email was successfully sent",
                    },
                },
            }
        }
    },
]

sending = {
        "type": "function",
        "function": {
            "name": "emails_send",
            "description": "Send an email to someone",
            "parameters": {
                "type": "object",
                "properties": {
                    "receiver_email": {
                        "type": "string",
                        "description": "The name of the person who we want to " +
                                       "reply to. The name must match one of " +
                                       "the names from the previously read " +
                                       "emails, otherwise ask for clarification.",
                    },
                    "body": {
                        "type": "string",
                        "description": "This will be the body of the email. " +
                                       "The user will provide a summary of what " +
                                       "they want the email to be about. However " +
                                       "you should use that summary to write a " +
                                       "more elaborated body of text.",
                    },
                },
                "required": []
            },
            "outputs": {
                "type": "object",
                "properties": {
                    "output": {
                        "type": "boolean",
                        "description": "Whether the email was successfully sent",
                    },
                },
            }
        }
    },