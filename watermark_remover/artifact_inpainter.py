import tensorflow as tf
import numpy as np

class ArtifactInpainter:
    """Uses a lightweight diffusion model to cleanly fill in any residual edge artifacts left by the AlphaUnblender."""
    
    def __init__(self, inpaint_model_dir="gs://flowx-models/inpainter-v1"):
        self.model = tf.saved_model.load(inpaint_model_dir)
        print("Loaded ML Artifact Inpainter.")

    def inpaint_watermark_region(self, cleaned_frame: np.ndarray, mask: np.ndarray) -> np.ndarray:
        # Convert to tensor [B, H, W, C]
        frame_tensor = tf.convert_to_tensor(cleaned_frame, dtype=tf.float32) / 255.0
        mask_tensor = tf.convert_to_tensor(mask, dtype=tf.float32)
        
        # Inpaint the masked area based on surrounding contextual pixels
        inpainted_tensor = self.model(frame_tensor, mask_tensor)
        
        return (inpainted_tensor.numpy() * 255.0).astype(np.uint8)
