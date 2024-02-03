import base64
import os
import pdb
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt

class BookingAPI():
    def __init__(self):
        api_key = os.environ["RESOS_API_KEY"]
        encoded_key = base64.b64encode(api_key.encode("utf-8")).decode("utf-8")
        self.auth_headers = {
            'Authorization': f'Basic {encoded_key}',
        }

    # data = {
    #         "date": "2021-09-18",
    #         "time": "21:00",
    #         "people": 4,
    #         "duration": 120,
    #         "guest": {
    #             "name": "Thomas A. Anderson",
    #             "email": "neo@resos.com",
    #             "phone": "+13115552368",
    #             "notificationSms": False,
    #             "notificationEmail": True
    #         },
    #         "status": "request",
    #         "source": "website",
    #         "comment": "This is a comment written by the guest regarding this booking, visible to both the guest and the restaurant",
    #         "note": "This is an internal note regarding this booking only visible to the restaurant",
    #         "noteAuthor": "Morpheus",
    #         "referrer": "https://www.some-website.com",
    #         "languageCode": "en"
    # }

    @retry(wait=wait_random_exponential(multiplier=0.5, max=40), stop=stop_after_attempt(5))
    def create_booking(self, date, time, people, name, email):
        url = "https://api.resos.com/v1/bookings"
        data = {
            "date": date,
            "time": time,
            "people": people,
            "duration": 120,
            "tables": [
                "A3CAfJycSJMHEWHHd"
            ],
            "guest": {
                "name": name,
                "email": email,
                "notificationEmail": True
            },
            "status": "request",
            "languageCode": "en"
        }
        response = requests.post(url, headers=self.auth_headers, json=data)
        
        # List tables
        # Table 1 ID: A3CAfJycSJMHEWHHd
        # url = "https://api.resos.com/v1/tables"
        # response = requests.request("GET", url, headers=self.auth_headers, data={}, files={})

        return response.json()

if __name__ == "__main__":
    api = BookingAPI()
    response = api.create_booking("2024-02-04", "18:00", 2, "Luke Skywalker", "imperialhackathon@gmail.com")
    print(response)