import json
from .booking_api import BookingAPI

def create_booking(api: BookingAPI, f_args:str):
    booking_id = api.create_booking(
        date=json.loads(f_args)["date"],
        time=json.loads(f_args)["time"],
        people=json.loads(f_args)["people"]
    )
    return str(booking_id)