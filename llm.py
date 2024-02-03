import os
import pdb
import time
import openai
from openai import OpenAI
import json
import re

from tenacity import retry, wait_random_exponential, stop_after_attempt

class LangModel():
    # Note that this writes to the cache even if read_cache is False. That flag is only used for reading.
    # To avoid any cache connection, just do not pass a cache_path.
    def __init__(self,
                 read_cache=True,
                 cache_path="",
                 model_name='gpt-4'):
        self.check_cache = read_cache
        self.cache_path = cache_path
        self.model_name = model_name
        if cache_path:
            self.cache = json.load(open(cache_path, "r"))
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def submit_prompt(self, prompt, temperature=0.0, silent=False):
        if self.cache_path and self.check_cache and prompt in self.cache.keys():
            if not silent:
                print(f'Using response found in cache for prompt: "{prompt}"')
            completion = self.cache[prompt]
            if not silent:
                print(f'Returning response: "{completion}"')
            return completion
        else:
            if not silent:
                print(f'Submitting prompt to GPT: "{prompt}"')
            max_len = 5000
            if len(prompt) > max_len:
                raise Exception(f"Prompt too long (length: {len(prompt)}). Max length is {max_len}.")

            response = self.client.with_options(max_retries=5).chat.completions.create(
                messages=[{"content": prompt, "role": "user"}],
                model=self.model_name,
                temperature=temperature,
                max_tokens=2000,
            )

            completion = response.choices[0].message.content
            if self.cache_path:
                self.cache[prompt] = completion
                json.dump(self.cache, open(self.cache_path, "w"), indent=4)
            if not silent:
                print(f'Returning response: "{completion}"')
            return completion
        
    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def chat_completion_request(self, messages, tools=None, tool_choice=None):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,
            )
            return response
        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return e


if __name__ == '__main__':
    cache_path = "/home/tempuser/SuperCurric/ichack24/ai-assistant/llm_cache.json"
    model = LangModel(read_cache=True, cache_path=cache_path)
    test_prompt = "Hello GPT-4! Do you read me ok?"
    response = model.submit_prompt(test_prompt)
    print(response)