import os
import pdb
import sys
import pyaudio
import wave
from pynput import keyboard
import whisper
import ssl

# Set the environment variable
os.environ["PYTHONHTTPSVERIFY"] = "0"

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "hello.wav"

class Speech2Text:
    def __init__(self, temp_voice_path="temp_voice.wav"):
        self.audio = pyaudio.PyAudio()
        os.system('clear') # PyAudio outputs a lot
        self.recording = False
        self.model = whisper.load_model("tiny.en", device="cpu")
        self.temp_voice_path = temp_voice_path

    def _on_press(self, key):
        if key == keyboard.Key.space:
            self.recording = not self.recording

    def record(self, out_path):
        print('Press space to unmute')

        # Start the listener in a non-blocking way
        listener = keyboard.Listener(on_press=self._on_press)
        listener.start()

        while not self.recording:
            pass

        # Print backspace to undo the space press
        sys.stdout.write('\b')
        stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                 rate=RATE, input=True,
                                 frames_per_buffer=CHUNK)
        frames = []
        print('The AI is listening (press space to stop)')

        while self.recording:
            data = stream.read(CHUNK)
            frames.append(data)

        # Print backspace to undo the space press
        sys.stdout.write('\b')
        print('The AI has finished listening')

        listener.stop()
        stream.stop_stream()
        stream.close()

        # Save the recorded data
        # First delete the file if it already exists
        try:
            os.remove(out_path)
        except FileNotFoundError:
            pass
        wf = wave.open(out_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def transcribe(self, voice_path):
        transcription = self.model.transcribe(voice_path)["text"]
        return transcription

    def hear_command(self):
        self.record(self.temp_voice_path)
        transcription = self.transcribe(self.temp_voice_path).strip()
        return transcription

if __name__ == "__main__":
    speech2text = Speech2Text()
    command = speech2text.hear_command()
    print('Heard command:')
    print(command)