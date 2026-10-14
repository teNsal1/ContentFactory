from pathlib import Path
import subprocess
import re
import imageio_ffmpeg

OUT = Path("output")
SCENES = OUT / "scenes"
AUDIO = OUT / "spiderman_narration.mp3"
VIDEO = OUT / "spiderman_visuals.mp4"

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

if not AUDIO.exists():
    raise FileNotFoundError(f"Не найдена озвучка: {AUDIO}")

images = [SCENES / f"scene_{i:02d}.png" for i in range(1, 7)]
for image in images:
    if not image.exists():
        raise FileNotFoundError(f"Не найдена сцена: {image}")

probe = subprocess.run(
    [ffmpeg, "-i", str(AUDIO)],
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
)

match = re.search(
    r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)",
    probe.stderr,
)
if not match:
    raise RuntimeError("Не удалось определить длительность озвучки.")

h, m, s = match.groups()
duration = int(h) * 3600 + int(m) * 60 + float(s)
scene_duration = duration / len(images)

command = [ffmpeg, "-y"]
for image in images:
    command += [
        "-loop", "1",
        "-framerate", "30",
        "-t", f"{scene_duration:.4f}",
        "-i", str(image),
    ]

audio_index = len(images)
command += ["-i", str(AUDIO)]

filters = "".join(
    f"[{i}:v]" for i in range(len(images))
)
filters += (
    f"concat=n={len(images)}:v=1:a=0,"
    "scale=720:1280,fps=30,format=yuv420p[v]"
)

command += [
    "-filter_complex", filters,
    "-map", "[v]",
    "-map", f"{audio_index}:a",
    "-c:v", "libx264",
    "-preset", "ultrafast",
    "-crf", "23",
    "-c:a", "aac",
    "-b:a", "128k",
    "-t", f"{duration:.3f}",
    "-movflags", "+faststart",
    str(VIDEO),
]

print(f"Собираем видео длительностью {duration:.1f} сек...")
subprocess.run(command, check=True)
print(f"Готово! Видео: {VIDEO}")
