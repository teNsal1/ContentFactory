from pathlib import Path
import subprocess
import json
import re
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

OUT = Path("output")
VIDEO = OUT / "spiderman_visuals.mp4"
AUDIO = OUT / "spiderman_narration.mp3"
SUBTITLES = OUT / "subtitles.json"
FINAL = OUT / "spiderman_final.mp4"

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

for path in (VIDEO, AUDIO, SUBTITLES):
    if not path.exists():
        raise FileNotFoundError(f"Не найден файл: {path}")

with open(SUBTITLES, "r", encoding="utf-8-sig") as f:
    subtitles = json.load(f)

probe = subprocess.run(
    [ffmpeg, "-i", str(VIDEO)],
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
    raise RuntimeError("Не удалось определить длительность видео.")

h, m, s = match.groups()
duration = int(h) * 3600 + int(m) * 60 + float(s)

W, H = 720, 1280
FPS = 30
FRAMES = int(duration * FPS)
overlay_dir = OUT / "spiderman_subtitle_frames"
overlay_dir.mkdir(exist_ok=True)

font_path = "C:/Windows/Fonts/arialbd.ttf"
font = (
    ImageFont.truetype(font_path, 34)
    if Path(font_path).exists()
    else ImageFont.load_default()
)

print(f"Создаём субтитры: {len(subtitles)} фрагментов...")

for frame_no in range(FRAMES):
    t = frame_no / FPS
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    current = next(
        (
            sub for sub in subtitles
            if sub["start"] <= t < sub["end"]
        ),
        None,
    )

    if current:
        text = current["text"].strip()
        words = text.split()
        lines = []
        line = ""

        for word in words:
            candidate = f"{line} {word}".strip()
            if draw.textbbox((0, 0), candidate, font=font)[2] <= 640:
                line = candidate
            else:
                if line:
                    lines.append(line)
                line = word

        if line:
            lines.append(line)

        line_height = 44
        y = 970 - len(lines) * line_height // 2

        for line in lines:
            box = draw.textbbox(
                (0, 0), line, font=font, stroke_width=2
            )
            x = (W - (box[2] - box[0])) // 2
            draw.text(
                (x, y),
                line,
                font=font,
                fill=(255, 255, 255, 255),
                stroke_width=3,
                stroke_fill=(0, 0, 0, 255),
            )
            y += line_height

    img.save(overlay_dir / f"frame_{frame_no:05d}.png")

print("Накладываем субтитры на видео...")

subprocess.run(
    [
        ffmpeg, "-y",
        "-i", str(VIDEO),
        "-framerate", str(FPS),
        "-i", str(overlay_dir / "frame_%05d.png"),
        "-i", str(AUDIO),
        "-filter_complex",
        "[0:v][1:v]overlay=0:0:format=auto[v]",
        "-map", "[v]",
        "-map", "2:a",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        "-movflags", "+faststart",
        str(FINAL),
    ],
    check=True,
)

print(f"Готово! Итоговый ролик: {FINAL}")
