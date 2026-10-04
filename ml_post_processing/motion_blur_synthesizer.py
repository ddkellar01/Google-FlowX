import cv2
import numpy as np

class MotionBlurSynthesizer:
    """Applies realistic cinematic shutter-angle motion blur using dense optical flow."""
    
    def __init__(self, shutter_angle: float = 180.0, fps: float = 24.0):
        # Calculate blur exposure time based on cinematic shutter angle
        self.exposure_time = (shutter_angle / 360.0) / fps
        print(f"Initialized Motion Blur Engine. Shutter: {shutter_angle}°, Exposure: {self.exposure_time}s")

    def apply_directional_blur(self, prev_frame: np.ndarray, curr_frame: np.ndarray) -> np.ndarray:
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate pixel velocity vectors
        flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        
        # In a full implementation, this flow field dictates a spatially-varying 
        # convolution kernel to smear moving objects while keeping static backgrounds sharp.
        blurred_frame = cv2.addWeighted(prev_frame, 0.2, curr_frame, 0.8, 0) # Simplified blend
        return blurred_frame
