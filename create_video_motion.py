from pathlib import Path
import subprocess
import json
import re
import imageio_ffmpeg

OUT = Path("output")
SCENES = OUT / "scenes"
AUDIO = OUT / "loki_narration.mp3"
VIDEO = OUT / "loki_motion.mp4"

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
images = [SCENES / f"scene_{i:02d}.png" for i in range(1, 7)]

for path in images + [AUDIO]:
    if not path.exists():
        raise FileNotFoundError(f"Не найден файл: {path}")

probe = subprocess.run(
    [ffmpeg, "-i", str(AUDIO)],
    capture_output=True, text=True,
    encoding="utf-8", errors="replace"
)
match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", probe.stderr)
if not match:
    raise RuntimeError("Не удалось определить длительность аудио.")

h, m, s = match.groups()
duration = int(h) * 3600 + int(m) * 60 + float(s)
part = duration / len(images)

cmd = [ffmpeg, "-y"]

for img in images:
    cmd += [
        "-loop", "1", "-framerate", "30",
        "-t", f"{part:.4f}", "-i", str(img)
    ]

audio_index = len(images)
cmd += ["-i", str(AUDIO)]

filters = []
for i in range(len(images)):
    filters.append(
        f"[{i}:v]scale=1440:2560:flags=lanczos,"
        "zoompan="
        f"z='min(1+0.08*on/({part * 30:.2f}),1.08)':"
        "x='iw/2-(iw/zoom/2)':"
        "y='ih/2-(ih/zoom/2)':"
        "d=1:s=720x1280:fps=30,"
        "setsar=1,"
        f"format=yuv420p[v{i}]"
    )

inputs = "".join(f"[v{i}]" for i in range(len(images)))
filters.append(
    f"{inputs}concat=n={len(images)}:v=1:a=0,"
    "format=yuv420p[v]"
)

cmd += [
    "-filter_complex", ";".join(filters),
    "-map", "[v]", "-map", f"{audio_index}:a",
    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
    "-c:a", "aac", "-b:a", "128k",
    "-t", f"{duration:.3f}",
    "-movflags", "+faststart", str(VIDEO)
]

print("Создаём видео с плавным движением камеры...")
subprocess.run(cmd, check=True)
print(f"Готово: {VIDEO}")