import subprocess
import imageio_ffmpeg
from pathlib import Path

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
Path("output").mkdir(exist_ok=True)

command = [
    ffmpeg,
    "-y",
    "-loop", "1",
    "-framerate", "30",
    "-i", "output/loki_cover.png",
    "-i", "output/test_voice.mp3",
    "-vf", "scale=720:1280,format=yuv420p",
    "-c:v", "libx264",
    "-tune", "stillimage",
    "-c:a", "aac",
    "-b:a", "128k",
    "-shortest",
    "-movflags", "+faststart",
    "output/loki_short.mp4",
]

subprocess.run(command, check=True)
print("Готово! Shorts создан: output/loki_short.mp4")