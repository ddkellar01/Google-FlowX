class LoRAInjector:
    """Dynamically loads Low-Rank Adaptation (LoRA) weights into the Veo/Diffusion models for actor consistency."""
    
    def __init__(self, base_model="google-veo-x"):
        self.base_model = base_model
        self.active_loras = {}

    def inject_weights(self, character_name: str, lora_weight_file: str, weight_alpha: float = 0.85):
        print(f"Injecting {character_name} LoRA ({lora_weight_file}) into {self.base_model} at alpha {weight_alpha}")
        self.active_loras[character_name] = {"path": lora_weight_file, "alpha": weight_alpha}

    def get_generation_kwargs(self) -> dict:
        """Returns the dictionary of active LoRAs to pass into the rendering API."""
        return {"adapter_weights": self.active_loras}
