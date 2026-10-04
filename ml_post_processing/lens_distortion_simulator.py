import numpy as np
import cv2

class LensDistortionSimulator:
    """Simulates cinematic imperfections: anamorphic barrel distortion and chromatic aberration."""
    
    def __init__(self, k1: float = -0.02, k2: float = 0.0):
        # Negative k1 produces barrel distortion (typical of wide cinematic lenses)
        self.k1 = k1
        self.k2 = k2

    def apply_anamorphic_characteristics(self, frame: np.ndarray) -> np.ndarray:
        h, w = frame.shape[:2]
        
        # 1. Simulate Barrel Distortion
        camera_matrix = np.array([[w, 0, w/2], [0, w, h/2], [0, 0, 1]], dtype=np.float32)
        dist_coeffs = np.array([self.k1, self.k2, 0, 0], dtype=np.float32)
        distorted_frame = cv2.undistort(frame, camera_matrix, dist_coeffs)
        
        # 2. Simulate Chromatic Aberration (Shift Red and Blue channels slightly)
        b, g, r = cv2.split(distorted_frame)
        rows, cols = b.shape
        
        M_red = np.float32([[1, 0, 2], [0, 1, 0]]) # Shift red right
        M_blue = np.float32([[1, 0, -2], [0, 1, 0]]) # Shift blue left
        
        r_shifted = cv2.warpAffine(r, M_red, (cols, rows))
        b_shifted = cv2.warpAffine(b, M_blue, (cols, rows))
        
        return cv2.merge((b_shifted, g, r_shifted))
