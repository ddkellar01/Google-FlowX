from google.cloud import texttospeech

class DialogueSynthesizer:
    """Generates lifelike dialogue and extracts timestamps for ML lip-syncing."""
    
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def generate_audio_with_visemes(self, text, voice_name="en-US-Journey-F", speaking_rate=1.0):
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code="en-US", name=voice_name)
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            speaking_rate=speaking_rate
        )
        
        # Enables Timepoint array for NNL lip-sync mesh mapping
        request = texttospeech.SynthesizeSpeechRequest(
            input=synthesis_input, voice=voice, audio_config=audio_config,
            enable_time_pointing=[texttospeech.SynthesizeSpeechRequest.TimepointType.SSML_MARK]
        )
        
        response = self.client.synthesize_speech(request=request)
        return response.audio_content, response.timepoints
