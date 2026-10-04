from vertexai.generative_models import GenerativeModel
import json

class SubtextGenerator:
    """Extracts emotional subtext from dialogue to drive micro-expressions in the NNL rendering."""
    
    def __init__(self):
        self.model = GenerativeModel("gemini-1.5-pro")

    def infer_emotional_state(self, character_name: str, dialogue_line: str, scene_context: str) -> dict:
        prompt = f"""
        Analyze the following dialogue line for emotional subtext to guide a video rendering AI.
        Context: {scene_context}
        Character: {character_name}
        Dialogue: "{dialogue_line}"
        
        Output JSON with keys: "primary_emotion", "intensity_1_to_10", "facial_micro_expression", "eye_movement".
        """
        response = self.model.generate_content(prompt)
        return json.loads(response.text.strip('```json').strip('```'))
