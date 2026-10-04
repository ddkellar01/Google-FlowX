import cv2
import numpy as np

class SpatialMaskGenerator:
    """Dynamically generates tracking masks for moving or shifting watermarks across frames."""
    
    def __init__(self, template_path: str):
        self.template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        self.sift = cv2.SIFT_create()
        self.kp1, self.des1 = self.sift.detectAndCompute(self.template, None)

    def locate_and_mask(self, target_frame: np.ndarray) -> np.ndarray:
        gray_frame = cv2.cvtColor(target_frame, cv2.COLOR_BGR2GRAY)
        kp2, des2 = self.sift.detectAndCompute(gray_frame, None)
        
        # Feature matching
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(self.des1, des2, k=2)
        
        good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]
        
        # Generate localized mask
        mask = np.zeros(target_frame.shape[:2], dtype=np.uint8)
        if len(good_matches) > 10:
            src_pts = np.float32([self.kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            matrix, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            h, w = self.template.shape
            pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, matrix)
            cv2.fillPoly(mask, [np.int32(dst)], 255)
            
        return mask
