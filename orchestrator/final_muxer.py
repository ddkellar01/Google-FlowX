import subprocess
import os

class FinalMuxer:
    """Stitches thousands of 10-second micro-scenes into the final 120-minute feature film."""
    
    def __init__(self, output_filename="final_movie_render.mp4"):
        self.output = output_filename

    def concatenate_all_chunks(self, chunk_directory: str):
        print("Generating FFmpeg concatenation list...")
        
        # Ensure clips are sorted chronologically
        clips = sorted([f for f in os.listdir(chunk_directory) if f.endswith('.mp4')])
        list_file_path = os.path.join(chunk_directory, "concat_list.txt")
        
        with open(list_file_path, "w") as f:
            for clip in clips:
                f.write(f"file '{clip}'\n")

        print(f"Muxing {len(clips)} scenes into {self.output}...")
        
        # Fast stream copy without re-encoding
        cmd = [
            "ffmpeg", "-f", "concat", "-safe", "0", 
            "-i", list_file_path, "-c", "copy", self.output
        ]
        
        subprocess.run(cmd, check=True)
        print(f"SUCCESS: Feature-length cinematic export complete -> {self.output}")
