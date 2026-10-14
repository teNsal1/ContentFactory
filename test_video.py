import subprocess
import imageio_ffmpeg
from pathlib import Path

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
Path("output").mkdir(exist_ok=True)

command = [
    ffmpeg,
    "-y",
    "-f", "lavfi",
    "-i", "color=c=0x18212f:s=720x1280:r=30",
    "-i", "output/test_voice.mp3",
    "-map", "0:v:0",
    "-map", "1:a:0",
    "-c:v", "libx264",
    "-tune", "stillimage",
    "-c:a", "aac",
    "-b:a", "128k",
    "-shortest",
    "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    "output/test_video_with_voice.mp4",
]

subprocess.run(command, check=True)
print("Готово! Видео с озвучкой: output/test_video_with_voice.mp4")