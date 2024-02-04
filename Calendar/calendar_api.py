import datetime
import os.path
from pathlib import Path
from typing import List
from tenacity import retry, wait_random_exponential, stop_after_attempt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']

class CalendarAgent():
    def authenticate(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        current_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = Path(current_dir).parent.parent

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

    def __init__(self):
        self.creds = self.authenticate()
        self.service = build("calendar", "v3", credentials=self.creds)

    def _create_event_dictionary(self, event_data) -> dict:
        name = event_data.get("summary", "unknown")
        location = event_data.get("location", "unknown")
        desc = event_data.get("description", "unknown")
        start = event_data.get("start", "unknown")
        if start != 'unknown':
            start = start["dateTime"]
        end = event_data.get("end", "unknown")
        if end != 'unknown':
            end = end["dateTime"]
        
        return {
            "name": name,
            "location": location,
            "description": desc,
            "start": start,
            "end": end,
        }

    @retry(wait=wait_random_exponential(multiplier=0.5, max=40), stop=stop_after_attempt(5))
    def get_upcoming_events(self) -> List[dict]:
         # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        # Prints the start and name of the next 10 events
        events_data = []
        for event in events:
            info = self._create_event_dictionary(event)
            events_data.append(info)
        return events_data
    
    def get_events_in_time_period(self,
                                  period_start,
                                  period_end) -> List[dict]:
        if period_end == period_start:
            print("It is None")
            period_end = period_start.split("T")[0]
            period_end = period_end + 'T23:59:59'
        events_result = (
            self.service.events()
            .list(
                calendarId='primary',
                timeMin=period_start,
                timeMax=period_end, 
                timeZone="Europe/London"
            ).execute())
        events = events_result.get("items", [])

        # Prints the start and name of the next 10 events
        events_data = []
        for event in events:
            info = self._create_event_dictionary(event)
            events_data.append(info)
        return events_data


    @retry(wait=wait_random_exponential(multiplier=0.5, max=40), stop=stop_after_attempt(5))
    def create_event(self, name, location, description, start_time, end_time):
        event = {
            "summary": name,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_time,
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "Europe/London",
            },
        }

        event = self.service.events().insert(calendarId="primary", body=event).execute()
        return True

if __name__ == "__main__":
    calendar_agent = CalendarAgent()
    events = calendar_agent.get_upcoming_events()
    for event in events:
        for k, v in event.items():
            print(f"{k}: {v}")
        print("\n\n")
    # print(events)
    # event = calendar_agent.create_event(
    #     "Test Event",
    #     "London",
    #     "This is a test event",
    #     "2024-02-04T18:00:00",
    #     "2024-02-04T18:30:00",
    #     "Europe/London",
    # )
    # print(f"Event created: {event.get('htmlLink')}")