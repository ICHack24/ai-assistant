import os
import warnings
from openai import OpenAI

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

class Text2Speech():
    def __init__(self):
        api_key = os.environ["OPENAI_API_KEY"]
        self.client = OpenAI(api_key=api_key)

    def speak(self, text):
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="shimmer",
            input=text,
            speed=1.2,
        )

        # Remove file if it already exists
        try:
            os.remove("ai_voice.mp3")
        except FileNotFoundError:
            pass
        response.write_to_file("ai_voice.mp3")

        pygame.mixer.init()
        pygame.mixer.music.load("ai_voice.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

if __name__ == '__main__':
    tts = Text2Speech()
    tts.speak("Hello, I am an AI assistant. How can I help you today?")