from gtts import gTTS
import os

class TextToSpeech:
    def __init__(self, language='en'):
        self.language = language

    def speak(self, text):
        tts = gTTS(text=text, lang=self.language, slow=False)
        audio_file = 'temp_audio.mp3'
        tts.save(audio_file)
        os.system(f"start {audio_file}")  # For Windows, use 'open' for macOS and 'xdg-open' for Linux

    def speak_alert(self, alert_message):
        self.speak(alert_message)