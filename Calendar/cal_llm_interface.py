import json
from copy import deepcopy
from .calendar_api import CalendarAgent

def calendar_upcoming(api: CalendarAgent):
    events_info = api.get_upcoming_events()
    return str(events_info)

def events_over_period(api: CalendarAgent, f_args):
    events_info = api.get_events_in_time_period(
        period_start=json.loads(f_args)["startDateTime"],
        period_end=json.loads(f_args)["startDateTime"],
    )
    return str(events_info)

def create_event(api: CalendarAgent, f_args):
    success = api.create_event(
        name=json.loads(f_args)["name"],
        location=json.loads(f_args)["location"],
        description=json.loads(f_args)["description"],
        start_time=json.loads(f_args)["start"],
        end_time=json.loads(f_args)["end"],
    )
    return str(success)

