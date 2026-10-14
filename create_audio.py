import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
SCRIPT_FILE = OUTPUT / "script.json"
AUDIO_FILE = OUTPUT / "spiderman_narration.mp3"


def main():
    if not SCRIPT_FILE.exists():
        raise FileNotFoundError(
            f"Не найден сценарий: {SCRIPT_FILE}"
        )

    with open(SCRIPT_FILE, "r", encoding="utf-8-sig") as file:
        script = json.load(file)

    text = " ".join(script["scenes"]).strip()
    voice = script.get("voice", "ru-RU-SvetlanaNeural")

    if not text:
        raise ValueError("Сценарий пустой.")

    command = [
        sys.executable,
        "-m",
        "edge_tts",
        "--voice",
        voice,
        "--rate=-5%",
        "--text",
        text,
        "--write-media",
        str(AUDIO_FILE),
    ]

    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        print(result.stderr)
        raise SystemExit(result.returncode)

    if not AUDIO_FILE.exists() or AUDIO_FILE.stat().st_size == 0:
        raise SystemExit("Аудиофайл не создан или пуст.")

    print(f"Озвучка создана: {AUDIO_FILE}")
    print(f"Размер: {AUDIO_FILE.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()