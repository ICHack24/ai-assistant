import os
import pdb
import time
import openai
from openai import OpenAI
import json
import re

class LangModel():
    # Note that this writes to the cache even if read_cache is False. That flag is only used for reading.
    # To avoid any cache connection, just do not pass a cache_path.
    def __init__(self, read_cache=True, cache_path=""):
        self.check_cache = read_cache
        self.cache_path = cache_path
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
                model="gpt-4",
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

if __name__ == '__main__':
    cache_path = "/home/tempuser/SuperCurric/ichack24/ai-assistant/llm_cache.json"
    model = LangModel(read_cache=True, cache_path=cache_path)
    test_prompt = "Hello GPT-4! Do you read me ok?"
    response = model.submit_prompt(test_prompt)
    print(response)