dictionary_form = \
"name: The name of the event\n" +\
"location: The location of the event\n" +\
"decsription: A description of the event\n" +\
"start: The start time and date of the event in ISO format\n" +\
"end: The end time and date of the event in ISO format"

calendar_tools = [
    {
        "type": "function",
        "function": {
            "name": "calendar_get_upcoming",
            "description": "Get information regarding the " +\
                           "upcoming events in the user's calendar. " +\
                           "Use this when no specific time period is specified.",
            "parameters": {},
            "outputs": {
                "type": "object",
                "properties": {
                    "output": {
                        "type": "list",
                        "description": "The output will be a list of dictionaries " +
                                       f"Each dictionary will be of the form {dictionary_form}." +
                                       "If there are no events the list will be epty",
                    },
                },
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calendar_add_event",
            "description": "Create a new event. Hence this is to " +\
                           " add a new event to the user's calendar",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the event",
                    },
                    "location": {
                        "type": "string",
                        "description": "The location of the event",
                    },
                    "description": {
                        "type": "string",
                        "description": "A brief description of the event",
                    },
                    "start": {
                        "type": "string",
                        "description": "The date and time of the start of the " \
                                       "event in ISO format",
                    },
                    "end": {
                        "type": "string",
                        "description": "The date and time of the start of the " \
                                       "event in ISO format",
                    },
                },
                "required": ['name', 'location', 'description',
                             'start', 'end']
            },
            "outputs": {
                "type": "object",
                "properties": {
                    "output": {
                        "type": "boolean",
                        "description": "Whether the event was successfully created",
                    },
                },
            }
        }
    },
]

period_events = {
        "type": "function",
        "function": {
            "name": "calendar_events_in_time_period",
            "description": "Get information regarding the " +\
                           "events in the user's calendar " +\
                           "within a certain time period",
            "parameters": {
                "type": "object",
                "properties": {
                    "startDateTime": {
                        "type": "string",
                        "description": "The date and time of the start " \
                                       "of the considered period, expressed " \
                                       "in ISO format. If no time is specified " \
                                       "assume the start of day T00:00:01",
                    },
                    "endDateTime": {
                        "type": "string",
                        "description": "The date and time of the end " \
                                       "of the considered period, expressed " \
                                       "in ISO format. If a single day is mentioned by the user, " \
                                       "set this to 'None'",
                    },
                },
                "required": ['startDateTime', 'endDateTime']
            },
            "outputs": {
                "type": "object",
                "properties": {
                    "output": {
                        "type": "list",
                        "description": "The output will be a list of dictionaries " +
                                       f"Each dictionary will be of the form {dictionary_form}." +
                                       "If there are no events the list will be epty",
                    },
                },
            }
        }
    },