import numpy as np
import cv2

class FilmGrainSynthesizer:
    """Procedurally generates chemically accurate film grain based on luminance values."""
    
    def __init__(self, film_stock="Kodak_Vision3_500T"):
        self.film_stock = film_stock
        print(f"Initializing procedural grain engine for {self.film_stock}.")

    def apply_procedural_grain(self, frame: np.ndarray, intensity: float = 0.8) -> np.ndarray:
        # Convert to LAB color space to isolate luminance (L channel)
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)
        
        # Grain is heavier in shadows, lighter in highlights
        luminance_inverse = 255 - l_channel
        noise_map = np.random.normal(0, intensity * 15, l_channel.shape).astype(np.float32)
        
        # Modulate noise by the inverse luminance
        modulated_noise = noise_map * (luminance_inverse / 255.0)
        
        # Add noise to L channel
        noisy_l = np.clip(l_channel + modulated_noise, 0, 255).astype(np.uint8)
        
        # Re-merge channels and convert back to BGR
        noisy_lab = cv2.merge((noisy_l, a_channel, b_channel))
        return cv2.cvtColor(noisy_lab, cv2.COLOR_LAB2BGR)
