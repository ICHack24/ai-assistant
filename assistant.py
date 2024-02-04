from datetime import date
from typing import Union
import warnings
from booking.booking_api import BookingAPI

from llm import LangModel
from speech2text import Speech2Text
from Emails.email_api import EmailAPI
from Emails.func_schema import email_tools
from Emails.email_llm_interface import *
from Calendar.calendar_api import CalendarAgent
from Calendar.func_schema import calendar_tools
from Calendar.cal_llm_interface import *
from booking.booking_func_schema import booking_tools
from booking.booking_llm_interface import *

from openai.types.chat import ChatCompletion, ChatCompletionMessage

from text2speech import Text2Speech

warnings.filterwarnings("ignore", category=UserWarning)

tools = email_tools + calendar_tools + booking_tools

class Assistant():
    def __init__(self,
                 cache_path="llm_cache.json",
                 assistant_name='Aida',
                 llm_model='gpt-4',
                 typing=False):
        self.typing = typing
        self.speech2text = Speech2Text()
        self.text2speech = Text2Speech()
        self.assistant_name = assistant_name
        self.lang_model = LangModel(
            read_cache=True, cache_path=cache_path, model_name=llm_model)
        self.tools = tools
        self.tool_choice = None

        self.emailAPI = EmailAPI()
        self.calendarAPI = CalendarAgent()
        self.bookingAPI = BookingAPI()
        self._initialise_assistant()

    def _initialise_assistant(self):
        curr_date = date.today()
        initial_prompt = \
            f"The date is {curr_date} and you are an AI assistant named {self.assistant_name}. Your" +\
            "purpose is to help the user in its daily chores. More "+\
            "specifically you are able to read and write emails. You are " +\
            "also aware of the calendar events of the user and are able to " +\
            "read, delete and add events to the calendar. Finally, you are " +\
            "able to book restaurants. All this while being a very " +\
            "knowledgeable AI, able to answer any question from the user, " +\
            "but your answers are very concise and to the point."
        self.lang_model.system_prompt(initial_prompt)
        func_instructions = \
            "Don't make assumptions about what values to plug into functions. " +\
            "Ask for clarification if a user request is ambiguous."
        self.lang_model.system_prompt(func_instructions)
        input()
        introduction = \
        f"Good afternoon, I am {self.assistant_name}, your " +\
        "AI assistant. How may I help you?"
        self.lang_model.assistant_prompt(introduction)
        self.speak(introduction)

    def speak(self, 
              response: Union[str, ChatCompletionMessage]):
        mode = "text" if self.typing else "speech"
        if isinstance(response, str):
            r_text = response
        else:
            r_text = response.content
        print(f"\n{self.assistant_name}:\n{r_text}\n")
        if mode == "speech":
            self.text2speech.speak(r_text)
            
    def listen(self, mode="speech") -> ChatCompletion:
        mode = "text" if self.typing else "speech"
        self.tool_choice = None
        if mode == "text":
            user_input = input("You: ")
        if mode == "speech":
            user_input = self.speech2text.hear_command()
        print("The AI is processing your request")
        return self._prompt_model(user_input)
    
    def _prompt_model(self, user_input: str) -> ChatCompletion:
        output = self.lang_model.chat(
            prompt=user_input,
            tools=self.tools,
            tool_choice=self.tool_choice
        )
        self._process_output(output)
        return output

    def _process_output(self, output: ChatCompletion):
        response = output.choices[0].message
        if response.tool_calls == None:
            self.speak(response)
        else:
            self._process_function_call(response)

    def _process_function_call(self,
                               response: ChatCompletionMessage):
        # print(f"\n\nFunc Response:\n{response}\n\n")
        function_info = response.tool_calls[0].function
        f_id = response.tool_calls[0].id
        f_name = function_info.name
        f_args = function_info.arguments
        f_entity = f_name.split("_")[0]
        
        if f_entity == "emails":
            user_prompt = self._process_email_funcs(
                f_id, f_name, f_args
            )
        elif f_entity == "calendar":
            user_prompt = self._process_calendar_funcs(
                f_id, f_name, f_args
            )
        elif f_entity == "booking":
            user_prompt = self._process_booking_funcs(
                f_id, f_name, f_args
            )
        if user_prompt is not None:
            self.tool_choice = 'none'
            self._prompt_model(user_prompt)

    def _process_email_funcs(self,
                             f_id: int,
                             f_name: str,
                             f_args: str):
        if f_name == "emails_read":
            f_results = emails_read(self.emailAPI, f_args)
            # print(f"\n\nTool input:\n{f_results}\n\n")
            self.lang_model.tool_prompt(
                f_id, f_name, f_results
            )
            user_prompt = \
                "Reply to my previous request and summarise " +\
                "the information of the emails you " +\
                "just read in a single sentence per email, " +\
                "specifying the sender's name"
            

        if f_name == "emails_check_unread":
            f_results = emails_check_unread(self.emailAPI)
            # print(f"\n\nTool input:\n{f_results}\n\n")
            self.lang_model.tool_prompt(
                f_id, f_name, f_results
            )
            user_prompt = \
                "Reply to my previous request with the " +\
                "information you have acquired. If there " +\
                "were no emails let me know, otherwise " +\
                "summarise in a single sentence per email " +\
                "the contents of the emails you just " +\
                "read, specifying the sender's name"

        if f_name == "emails_reply":
            f_results = emails_reply(self.emailAPI, f_args)
            # print(f"\n\nTool input:\n{f_results}\n\n")
            self.lang_model.tool_prompt(
                f_id, f_name, f_results
            )
            user_prompt = \
                "Reply to my previous request by letting " +\
                "me know if you sent the email successfully."
            
        if f_name == "emails_send":
            f_results = emails_send(self.emailAPI, f_args)
            # print(f"\n\nTool input:\n{f_results}\n\n")
            self.lang_model.tool_prompt(
                f_id, f_name, f_results
            )
            user_prompt = \
                "Reply to my previous request by letting " +\
                "me know if you sent the email successfully."
            
        return user_prompt

    def _process_calendar_funcs(self,
                                f_id: int,
                                f_name: str,
                                f_args: str):
        if f_name == "calendar_get_upcoming":
            f_results = calendar_upcoming(self.calendarAPI)
            # print(f"\n\nTool input:\n{f_results}\n\n")
            self.lang_model.tool_prompt(
                f_id, f_name, f_results
            )
            user_prompt = \
                "Reply to my previous request and summarise, " +\
                "in a list format and in a single sentence " +\
                "per event, all the events information " +\
                "you have just collected. If there are no " +\
                "events, tell me so."

        if f_name == "calendar_events_in_time_period":
            f_results = events_over_period(
                self.calendarAPI, f_args)
            # print(f"\n\nTool input:\n{f_results}\n\n")
            self.lang_model.tool_prompt(
                f_id, f_name, f_results
            )
            user_prompt = \
                "Reply to my previous request and summarise, " +\
                "in a list format and in a single sentence " +\
                "per event, all the events information " +\
                "you have just collected. If there are no " +\
                "events, tell me so."

        if f_name == "calendar_add_event":
            f_results = create_event(
                self.calendarAPI, f_args)
            # print(f"\n\nTool input:\n{f_results}\n\n")
            self.lang_model.tool_prompt(
                f_id, f_name, f_results
            )
            user_prompt = \
                "Reply to my previous request by letting " +\
                "me know if you created the event successfully."
            
        return user_prompt

    # Example user request: Can you please help me book a table for 2 at my favourite restaurant for 7pm next Saturday?
    def _process_booking_funcs(self,
                                f_id: int,
                                f_name: str,
                                f_args: str):
        if f_name == "booking_create_booking":
            f_results = create_booking(self.bookingAPI, f_args)
            # print(f"\n\nTool input:\n{f_results}\n\n")
            self.lang_model.tool_prompt(
                f_id, f_name, f_results
            )
            
            user_prompt = \
                "Reply to my previous request by letting " +\
                "me know that you submitted the booking request. " +\
                "Be positive but concise. Mention the name of " +\
                "the restaurant. Ignore anything about whether " +\
                "the booking was confirmed or not. Additionally add " +\
                "this reservation as a new event in my calendar."
            self.tool_choice={
                "type": "function",
                "function": {
                    "name": "calendar_add_event"
                }}
            self._prompt_model(user_prompt)
        return None

    def converse(self):
        # print('You are now speaking to the AI assistant')
        while True:
            output = assistant.listen()
            # command = self.speech2text.hear_command()
            # print('You:')
            # print(command)
            # print('The assistant is thinking...')
            # response = self.lang_model.submit_prompt(command, silent=True)
            # print('Assistant:')
            # print(response)

if __name__ == '__main__':
    # assistant = Assistant(llm_model="gpt-3.5-turbo-0125")
    assistant = Assistant(llm_model="gpt-4", typing=False)
    assistant.converse()