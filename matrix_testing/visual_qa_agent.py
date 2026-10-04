import vertexai
from vertexai.generative_models import GenerativeModel, Part
import json

class VisualQAAgent:
    """Multimodal evaluation agent leveraging Gemini Pro Vision to score render fidelity."""
    
    def __init__(self, project_id: str):
        vertexai.init(project=project_id)
        self.model = GenerativeModel("gemini-1.5-pro")

    def evaluate_test_render(self, image_bytes: bytes, target_prompt: str) -> dict:
        image_part = Part.from_data(data=image_bytes, mime_type="image/jpeg")
        
        eval_prompt = f"""
        Analyze this rendered frame against the target script prompt: "{target_prompt}".
        Evaluate on a scale of 0-100 for:
        1. Prompt Adherence
        2. Anatomical/Physical Consistency (check for flickering artifacts or morphed limbs)
        3. Lighting and Temporal Stability

        Return ONLY a JSON object with keys: "adherence_score", "physics_score", "stability_score", "passed" (bool).
        """
        
        response = self.model.generate_content([image_part, eval_prompt])
        return json.loads(response.text.strip('```json').strip('```'))
