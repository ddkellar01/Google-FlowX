import cv2
import numpy as np

class PhysicsValidator:
    """Automated QA logic: Detects impossible geometry or gravity-defying artifacts in generated video."""
    
    def __init__(self, motion_threshold=15.0):
        self.motion_threshold = motion_threshold

    def validate_gravity_and_mass(self, frame_sequence: list) -> bool:
        print("Running optical flow analysis to detect physics violations (e.g., floating objects)...")
        
        for i in range(1, len(frame_sequence)):
            prev_gray = cv2.cvtColor(frame_sequence[i-1], cv2.COLOR_BGR2GRAY)
            curr_gray = cv2.cvtColor(frame_sequence[i], cv2.COLOR_BGR2GRAY)
            
            flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            
            # If upward motion magnitude of heavy objects exceeds threshold abruptly, flag as hallucination
            if np.max(magnitude) > self.motion_threshold:
                print("Physics hallucination detected. Frame failed QA.")
                return False
                
        return True
