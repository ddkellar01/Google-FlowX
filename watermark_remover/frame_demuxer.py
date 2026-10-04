import ffmpeg
import numpy as np
from watermark_remover.alpha_unblender import AlphaUnblender

class FrameDemuxer:
    """Demuxes video containers into raw RGB streams, unblends watermarks, and remuxes audio."""
    
    def __init__(self, unblender: AlphaUnblender):
        self.unblender = unblender

    def process_video_stream(self, input_path: str, output_path: str, width: int = 1920, height: int = 1080):
        # Read video frames to stdout buffer
        out, _ = (
            ffmpeg.input(input_path)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run(capture_stdout=True, capture_stderr=True)
        )
        
        video_bytes = np.frombuffer(out, np.uint8)
        frames = video_bytes.reshape([-1, height, width, 3])
        processed_frames = []

        print(f"Demuxing {len(frames)} frames for watermark removal...")
        for frame in frames:
            cleaned = self.unblender.unblend_frame(frame)
            processed_frames.append(cleaned)

        cleaned_bytes = np.stack(processed_frames, axis=0).tobytes()

        # Remux video stream with original audio track preserved
        video_stream = ffmpeg.input('pipe:', format='rawvideo', pix_fmt='rgb24', s=f'{width}x{height}', r=24)
        audio_stream = ffmpeg.input(input_path).audio
        
        process = (
            ffmpeg.output(video_stream, audio_stream, output_path, vcodec='libx264', acodec='copy')
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )
        process.communicate(input=cleaned_bytes)
        print(f"Successfully remuxed watermarked-cleaned stream to {output_path}")
