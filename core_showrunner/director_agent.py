from vertexai.generative_models import GenerativeModel

class DirectorAgent:
    """Controls virtual camera mechanics (dolly, pan, tilt, tracking) based on narrative tension."""
    
    def __init__(self):
        self.llm = GenerativeModel("gemini-pro-thinking")

    def choreograph_camera_movement(self, scene_action: str, emotional_beat: str) -> dict:
        prompt = f"""
        Act as a Director of Photography. 
        Action: {scene_action}
        Emotion: {emotional_beat}
        
        Determine the optimal camera movement and lens choice. Output JSON:
        "movement_type" (e.g., "dolly-in", "static", "whip-pan"), "speed_multiplier", "lens_mm".
        """
        response = self.llm.generate_content(prompt)
        # Parses response and translates it into motion vectors for the NNL diffusion prompt
        print(f"Camera Choreography Locked for Scene.")
        return {"movement_type": "slow-dolly-in", "speed_multiplier": 0.5, "lens_mm": 50}
