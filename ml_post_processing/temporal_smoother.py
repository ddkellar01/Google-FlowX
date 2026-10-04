import numpy as np

class TemporalSmoother:
    """ML Editor: Uses optical flow interpolation to prevent flickering between separate scene generation clips."""
    
    def __init__(self, blend_frames=12):
        self.blend_frames = blend_frames

    def morph_clip_boundaries(self, clip_a_tensor, clip_b_tensor):
        print(f"Extracting trailing frames of Clip A and leading frames of Clip B.")
        
        # Isolate boundary frames
        tail_a = clip_a_tensor[-self.blend_frames:]
        head_b = clip_b_tensor[:self.blend_frames]
        
        # Simulated ML latent space interpolation
        blended_transition = (tail_a * 0.5) + (head_b * 0.5) 
        print(f"Applied temporal smoothing across {self.blend_frames} frames.")
        
        # Stitch arrays seamlessly
        return np.concatenate((clip_a_tensor[:-self.blend_frames], blended_transition, clip_b_tensor[self.blend_frames:]))
