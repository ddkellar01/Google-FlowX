import vertexai
from vertexai.generative_models import GenerativeModel
import json

class MasterScriptGenerator:
    """Uses Gemini Pro Thinking to architect the 120-minute narrative arc."""
    
    def __init__(self, project_id, location="us-central1"):
        vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel("gemini-pro-thinking")

    def generate_movie_arc(self, concept_prompt, duration_minutes=120):
        prompt = (
            f"Act as a master showrunner. Generate a {duration_minutes}-minute movie script JSON breakdown "
            f"based on this concept: {concept_prompt}. Divide the narrative into exact 10-second micro-scenes "
            f"with character states, camera angles, and dialogue markers."
        )
        response = self.model.generate_content(prompt)
        return json.loads(response.text)
