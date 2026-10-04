from vertexai.generative_models import GenerativeModel

class FoleyPromptGenerator:
    """Translates visual actions into dense audio prompts for sound effect generation (AudioLM)."""
    
    def __init__(self):
        self.model = GenerativeModel("gemini-1.5-flash")

    def generate_sfx_prompts(self, action_description: str, terrain: str) -> list:
        prompt = f"""
        Extract specific sound effects required for this action. Format as comma-separated audio prompts.
        Action: {action_description}
        Terrain/Environment: {terrain}
        
        Example Output: "Heavy leather boots crunching on dry gravel", "Distant metallic scrape, echoing"
        """
        response = self.model.generate_content(prompt)
        prompts = [p.strip() for p in response.text.split(',')]
        print(f"Generated {len(prompts)} distinct Foley layers.")
        return prompts
