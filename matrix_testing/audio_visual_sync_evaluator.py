import numpy as np

class AudioVisualSyncEvaluator:
    """QA Agent: Ensures explosive events in video perfectly align with audio peaks."""
    
    def __init__(self, sync_tolerance_frames=2):
        self.tolerance = sync_tolerance_frames

    def evaluate_impact_sync(self, video_luminance_spikes: list, audio_waveform_peaks: list, fps: int = 24) -> bool:
        print("Checking temporal sync between visual events (e.g., explosions) and audio impacts...")
        
        for v_frame in video_luminance_spikes:
            # Find closest audio peak in time
            closest_audio_frame = min(audio_waveform_peaks, key=lambda x: abs(x - v_frame))
            frame_delta = abs(v_frame - closest_audio_frame)
            
            if frame_delta > self.tolerance:
                print(f"FAILED: Visual event at frame {v_frame} desynced from audio peak by {frame_delta} frames.")
                return False
                
        print("PASSED: Audio-visual sync is within tolerance.")
        return True
