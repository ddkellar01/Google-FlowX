import cv2
import numpy as np

class ColorGradingMatcher:
    """Ensures Scene 4B perfectly matches the color palette of Scene 4A, preventing jarring visual cuts."""
    
    def __init__(self):
        pass

    def match_histograms(self, source_frame: np.ndarray, target_reference_frame: np.ndarray) -> np.ndarray:
        matched_frame = np.zeros_like(source_frame)
        
        # Match colors channel by channel (B, G, R)
        for i in range(3):
            src_hist, bins = np.histogram(source_frame[:,:,i].flatten(), 256, [0,256])
            ref_hist, _ = np.histogram(target_reference_frame[:,:,i].flatten(), 256, [0,256])
            
            src_cdf = src_hist.cumsum()
            ref_cdf = ref_hist.cumsum()
            
            # Normalize CDFs
            src_cdf_normalized = src_cdf * float(src_cdf.max()) / src_cdf.max()
            ref_cdf_normalized = ref_cdf * float(ref_cdf.max()) / ref_cdf.max()
            
            # Create lookup table
            lookup_table = np.interp(src_cdf_normalized, ref_cdf_normalized, bins[:-1])
            matched_frame[:,:,i] = cv2.LUT(source_frame[:,:,i], lookup_table.astype(np.uint8))
            
        return matched_frame
