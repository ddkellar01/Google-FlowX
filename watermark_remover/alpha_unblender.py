import numpy as np
import cv2

class AlphaUnblender:
    """Mathematical inverse-blend engine to remove static/dynamic Google Flow & Veo watermarks.
    
    Formula: $I_{\text{clean}} = \frac{I_{\text{watermarked}} - \alpha \cdot W}{1 - \alpha}$
    """
    
    def __init__(self, watermark_template_path: str, alpha_map_path: str):
        self.watermark = cv2.imread(watermark_template_path, cv2.IMREAD_COLOR).astype(np.float32) / 255.0
        self.alpha = cv2.imread(alpha_map_path, cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0
        self.alpha = np.expand_dims(self.alpha, axis=-1)  # Broadcast across RGB channels

    def unblend_frame(self, frame_tensor: np.ndarray) -> np.ndarray:
        """Applies reverse alpha channel blending on a single frame array [H, W, C]."""
        normalized_frame = frame_tensor.astype(np.float32) / 255.0
        
        # Prevent division by zero where alpha approaches 1.0
        safe_alpha = np.clip(self.alpha, 0.0, 0.99)
        
        clean_frame = (normalized_frame - (safe_alpha * self.watermark)) / (1.0 - safe_alpha)
        clean_frame = np.clip(clean_frame * 255.0, 0, 255).astype(np.uint8)
        
        return clean_frame
