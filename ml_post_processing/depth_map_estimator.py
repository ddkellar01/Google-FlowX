import torch
import cv2
import numpy as np

class DepthMapEstimator:
    """Generates 3D depth maps from 2D renders for cinematic parallax adjustments and atmospheric haze depth."""
    
    def __init__(self, model_type="DPT_Large"):
        print(f"Loading MiDaS {model_type} for monocular depth estimation...")
        self.midas = torch.hub.load("intel-isl/MiDaS", model_type)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.midas.to(self.device)
        self.midas.eval()

    def estimate_depth(self, frame: np.ndarray) -> np.ndarray:
        # Transform frame to PyTorch tensor
        img_tensor = torch.from_numpy(frame).permute(2, 0, 1).unsqueeze(0).float().to(self.device)
        
        with torch.no_grad():
            prediction = self.midas(img_tensor)
            
            # Interpolate back to original resolution
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=frame.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()
            
        depth_map = prediction.cpu().numpy()
        return cv2.normalize(depth_map, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
