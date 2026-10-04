import pynvml
import time

class GPUMemoryManager:
    """Dynamically scales chunk sizes to prevent VRAM Out-of-Memory (OOM) errors during 4K/8K renders."""
    
    def __init__(self):
        pynvml.nvmlInit()
        self.handle = pynvml.nvmlDeviceGetHandleByIndex(0)

    def optimize_batch_size(self, base_batch_size: int, safe_vram_margin_mb: int = 2048) -> int:
        info = pynvml.nvmlDeviceGetMemoryInfo(self.handle)
        free_vram_mb = info.free / (1024 ** 2)
        
        print(f"Node VRAM Check: {free_vram_mb:.0f} MB Free.")
        
        if free_vram_mb < safe_vram_margin_mb:
            reduced_batch = max(1, base_batch_size // 2)
            print(f"Warning: Low VRAM. Throttling batch size down to {reduced_batch}.")
            return reduced_batch
            
        return base_batch_size
