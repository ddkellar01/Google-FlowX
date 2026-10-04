import numpy as np
import cv2

class FrequencyDomainFilter:
    """Uses Fast Fourier Transform (FFT) to isolate and destroy Google Flow invisible spatial watermarks."""
    
    def __init__(self, filter_radius: int = 50):
        self.radius = filter_radius

    def strip_hidden_watermark(self, frame: np.ndarray) -> np.ndarray:
        # Convert to grayscale for frequency analysis
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply 2D Fast Fourier Transform
        f_transform = np.fft.fft2(gray)
        f_shift = np.fft.fftshift(f_transform)
        
        # Create a notch filter mask to zero out specific high-frequency watermark patterns
        rows, cols = gray.shape
        crow, ccol = rows // 2, cols // 2
        mask = np.ones((rows, cols), np.uint8)
        
        # Block specific periodic frequencies known to be used by Flow/Veo steganography
        cv2.circle(mask, (ccol + 60, crow + 60), 5, 0, -1)
        cv2.circle(mask, (ccol - 60, crow - 60), 5, 0, -1)
        
        # Apply mask and inverse FFT
        f_shift_filtered = f_shift * mask
        f_ishift = np.fft.ifftshift(f_shift_filtered)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        
        # Merge cleaned luminance back into original color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:,:,2] = np.clip(img_back, 0, 255).astype(np.uint8)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
