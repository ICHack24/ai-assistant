import os
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
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.continue_recording = True  # Initialize the continue_recording attribute

    def _on_press(self, key):
        if key == keyboard.Key.space:
            self.continue_recording = False  # Use the class attribute
            return False

    def record(self, out_path="test.wav"):
        stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                 rate=RATE, input=True,
                                 frames_per_buffer=CHUNK)
        print("Recording...")

        # Start the listener in a non-blocking way
        listener = keyboard.Listener(on_press=self._on_press)
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
    # recorder = AudioRecorder()
    # recorder.record(WAVE_OUTPUT_FILENAME)
    # options = whisper.DecodingOptions(fp16=False)
    model = whisper.load_model("tiny.en", device="cpu")
    audio_path = "/home/tempuser/SuperCurric/ichack24/ai-assistant/hello.wav"
    # audio_path = "/home/tempuser/Downloads/piano-moment-9835.mp3"
    transcription = model.transcribe(audio_path)["text"]
    print(transcription)

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # audio = whisper.load_audio(audio_path)
    # audio = whisper.pad_or_trim(audio)
    # mel = whisper.log_mel_spectrogram(audio).to(model.device)
    # options = whisper.DecodingOptions(fp16=False)

# model = whisper.load_model("small.en")
# transcription = model.transcribe("hello.wav")["text"]
# print(transcription)
