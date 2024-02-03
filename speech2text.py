import os
import pyaudio
import wave
from pynput import keyboard
import whisper

# Set the environment variable
os.environ["PYTHONHTTPSVERIFY"] = "0"

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "hello.wav"

class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.continue_recording = True  # Initialize the continue_recording attribute

    def on_press(self, key):
        if key == keyboard.Key.space:
            self.continue_recording = False  # Use the class attribute
            return False

    def record(self, out_path="test.wav"):
        stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                 rate=RATE, input=True,
                                 frames_per_buffer=CHUNK)
        print("Recording...")

        # Start the listener in a non-blocking way
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

        while self.continue_recording:  # Use the class attribute
            data = stream.read(CHUNK)
            self.frames.append(data)

        listener.join()  # Wait for listener to finish

        print("Finished recording.")
        stream.stop_stream()
        stream.close()

        # Save the recorded data
        wf = wave.open(out_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

if __name__ == "__main__":
    recorder = AudioRecorder()
    recorder.record(WAVE_OUTPUT_FILENAME)
    model = whisper.load_model("small.en")
    transcription = model.transcribe(WAVE_OUTPUT_FILENAME)["text"]
    print(transcription)

# model = whisper.load_model("small.en")
# transcription = model.transcribe("hello.wav")["text"]
# print(transcription)
