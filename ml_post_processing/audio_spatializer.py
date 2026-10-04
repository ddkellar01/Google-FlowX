import numpy as np

class AudioSpatializer:
    """Maps mono/stereo generated audio tracks to 3D spatial Atmos vectors aligned with camera motion."""
    
    def __init__(self, sample_rate: int = 48000):
        self.sample_rate = sample_rate

    def apply_3d_panning(self, pcm_audio: np.ndarray, camera_pan_x: float) -> np.ndarray:
        """Pans stereo audio based on normalized camera coordinates [-1.0 (left) to 1.0 (right)]."""
        # Calculate Interaural Level Difference (ILD)
        left_gain = np.cos((camera_pan_x + 1) * np.pi / 4)
        right_gain = np.sin((camera_pan_x + 1) * np.pi / 4)

        panned_audio = np.zeros((len(pcm_audio), 2), dtype=np.float32)
        panned_audio[:, 0] = pcm_audio * left_gain  # Left Channel
        panned_audio[:, 1] = pcm_audio * right_gain # Right Channel

        return panned_audio
