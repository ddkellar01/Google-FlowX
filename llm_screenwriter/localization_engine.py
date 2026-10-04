from google.cloud import translate_v2 as translate
from llm_screenwriter.dialogue_synth import DialogueSynthesizer

class LocalizationEngine:
    """Translates the final movie script and re-generates lip-synced audio for global distribution."""
    
    def __init__(self):
        self.translate_client = translate.Client()
        self.audio_synth = DialogueSynthesizer()

    def create_foreign_dub(self, dialogue_text: str, target_language: str = 'es'):
        print(f"Translating dialogue to {target_language}...")
        
        # Translate Text
        translation = self.translate_client.translate(dialogue_text, target_language=target_language)
        translated_text = translation['translatedText']
        
        # Generate new localized audio and viseme timepoints
        audio_content, timepoints = self.audio_synth.generate_audio_with_visemes(
            text=translated_text, 
            voice_name=f"{target_language}-Standard-A"
        )
        
        return audio_content, timepoints, translated_text
