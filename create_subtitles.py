import json
import re
import subprocess
from pathlib import Path

import imageio_ffmpeg

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
SCRIPT_FILE = OUTPUT / "script.json"
AUDIO_FILE = OUTPUT / "spiderman_narration.mp3"
SUBTITLES_FILE = OUTPUT / "subtitles.json"


def get_duration(audio_file):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    result = subprocess.run(
        [ffmpeg, "-i", str(audio_file)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    match = re.search(
        r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)",
        result.stderr,
    )

    if not match:
        raise RuntimeError("Не удалось определить длительность аудио.")

    hours, minutes, seconds = match.groups()

    return (
        int(hours) * 3600
        + int(minutes) * 60
        + float(seconds)
    )


def main():
    if not SCRIPT_FILE.exists():
        raise FileNotFoundError(f"Не найден сценарий: {SCRIPT_FILE}")

    if not AUDIO_FILE.exists():
        raise FileNotFoundError(f"Не найдена озвучка: {AUDIO_FILE}")

    with open(SCRIPT_FILE, "r", encoding="utf-8-sig") as file:
        script = json.load(file)

    scenes = script.get("scenes", [])

    if not scenes:
        raise ValueError("В сценарии нет фраз для субтитров.")

    duration = get_duration(AUDIO_FILE)
    segment_duration = duration / len(scenes)

    subtitles = []

    for index, text in enumerate(scenes):
        start = index * segment_duration
        end = (index + 1) * segment_duration

        subtitles.append({
            "start": round(start, 2),
            "end": round(end, 2),
            "text": text.strip(),
        })

    with open(SUBTITLES_FILE, "w", encoding="utf-8") as file:
        json.dump(subtitles, file, ensure_ascii=False, indent=2)

    print(f"Создано фрагментов: {len(subtitles)}")
    print(f"Длительность озвучки: {duration:.2f} сек.")
    print(f"Субтитры сохранены: {SUBTITLES_FILE}")


if __name__ == "__main__":
    main()