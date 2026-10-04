from vertexai.generative_models import GenerativeModel

class PromptOptimizer:
    """Translates high-level script context into dense, token-optimized diffusion prompts."""
    
    def __init__(self):
        self.llm = GenerativeModel("gemini-1.5-pro")

    def translate_to_diffusion_tokens(self, scene_narrative, previous_state):
        system_instruction = (
            "Convert the narrative into comma-separated, high-weight diffusion prompt tokens for video generation. "
            "Enforce strict adherence to previous character state, specify camera lens (e.g., 35mm anamorphic), "
            "lighting, and film stock."
        )
        payload = f"System: {system_instruction}\nContext: {previous_state}\nScene: {scene_narrative}"
        response = self.llm.generate_content(payload)
        return response.text.strip()
