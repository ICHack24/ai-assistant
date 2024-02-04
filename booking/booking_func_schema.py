booking_tools = [
    {
        "type": "function",
        "function": {
            "name": "booking_create_booking",
            "description": "Books a table at my favourite restaurant",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "The date to book the table for. Example format: 2021-09-18",
                    },
                    "time": {
                        "type": "string",
                        "description": "The time to book the table for. Example format: 21:00",
                    },
                    "people": {
                        "type": "integer",
                        "description": "The number of people for the booking. If unclear, ask for clarification.",
                    },
                },
            "required": ["date", "time", "people"]
            },
            "outputs": {
                "type": "object",
                "properties": {
                    "output": {
                        "type": "string",
                        "description": "A booking ID. You can ignore this."
                    },
                }
            }
        }
    }
]