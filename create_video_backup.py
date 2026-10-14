from pathlib import Path
import subprocess
import json
import re
import imageio_ffmpeg

OUT = Path("output")
SCENES = OUT / "scenes"
AUDIO = OUT / "loki_narration.mp3"
VIDEO = OUT / "loki_visuals.mp4"

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

if not AUDIO.exists():
    raise FileNotFoundError(f"Не найден аудиофайл: {AUDIO}")

images = [SCENES / f"scene_{i:02d}.png" for i in range(1, 7)]

for image in images:
    if not image.exists():
        raise FileNotFoundError(f"Не найдена сцена: {image}")

# Получаем длительность озвучки
result = subprocess.run(
    [ffmpeg, "-i", str(AUDIO)],
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
)

match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", result.stderr)

if not match:
    raise RuntimeError("Не удалось определить длительность озвучки.")

hours, minutes, seconds = match.groups()
duration = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
scene_duration = duration / len(images)

print(f"Длительность озвучки: {duration:.2f} сек.")
print(f"Время на каждую сцену: {scene_duration:.2f} сек.")

command = [ffmpeg, "-y"]

# Каждое изображение превращаем в видеопоток
for image in images:
    command += [
        "-loop", "1",
        "-framerate", "30",
        "-t", f"{scene_duration:.4f}",
        "-i", str(image),
    ]

audio_index = len(images)
command += ["-i", str(AUDIO)]

# Склеиваем сцены, затем добавляем озвучку
filters = "".join(
    f"[{i}:v]"
    for i in range(len(images))
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

print("\nСобираем видео. Это может занять некоторое время...\n")
subprocess.run(command, check=True)

print(f"\nГОТОВО! Видео сохранено: {VIDEO}")