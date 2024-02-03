import json
from llm import LangModel

tools = [
    {
        "type": "function",
        "function": {
            "name": "lunch_notification",
            "description": "Let person X know how long it will take before we will be able to join him for lunch",
            "parameters": {
                "type": "object",
                "properties": {
                    "time_m": {
                        "type": "integer",
                        "description": "The number of minutes that it will take",
                    },
                    "name": {
                        "type": "string",
                        "description": "Name of Person X"
                    }
                },
                "required": ["time_m", "name"]
            }
        }
    }
]

def lunch_notification(time_m:int, name:str):
    print(f"\nHey {name}, we'll be there in {time_m} minutes")

if __name__ == '__main__':
    cache_path = "llm_cache.json"
    assistant = LangModel(read_cache=True, cache_path=cache_path, model_name='gpt-3.5-turbo-0613')
    
    messages = []
    messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
    messages.append({"role": "user", "content": "Notify Paul that we will be in the kitchen ready for lunch in 5 minutes"})
    chat_response = assistant.chat_completion_request(
        messages, tools=tools
    )
    assistant_message = chat_response.choices[0].message
    messages.append(assistant_message)
    print(assistant_message)

    function_name = assistant_message.tool_calls[0].function.name
    function_arguments = assistant_message.tool_calls[0].function.arguments
    if function_name == "lunch_notification":
        lunch_notification(json.loads(function_arguments)["time_m"], json.loads(function_arguments)["name"])

