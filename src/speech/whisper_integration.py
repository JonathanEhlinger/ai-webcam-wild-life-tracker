from whisper import Whisper

class WhisperIntegration:
    def __init__(self):
        self.model = Whisper.load_model("base")

    def transcribe_audio(self, audio_file_path):
        result = self.model.transcribe(audio_file_path)
        return result['text']

    def process_voice_command(self, audio_file_path):
        transcription = self.transcribe_audio(audio_file_path)
        # Here you can add logic to process the transcription and execute commands
        return transcription