from speech2text import Speech2Text
from llm import LangModel
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

class Assistant():
    def __init__(self, cache_path="llm_cache.json"):
        self.speech2text = Speech2Text()
        self.lang_model = LangModel(read_cache=True, cache_path=cache_path)

    def converse(self):
        print('You are now speaking to the AI assistant')
        while True:
            command = self.speech2text.hear_command()
            print('You:')
            print(command)
            print('The assistant is thinking...')
            response = self.lang_model.submit_prompt(command, silent=True)
            print('Assistant:')
            print(response)

if __name__ == '__main__':
    assistant = Assistant()
    assistant.converse()