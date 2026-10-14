import json
import subprocess
from pathlib import Path

OUTPUT = Path("output")
SCRIPT_FILE = OUTPUT / "script.json"
AUDIO_FILE = OUTPUT / "spiderman_narration.mp3"

with open(SCRIPT_FILE, "r", encoding="utf-8-sig") as f:
    script = json.load(f)

text = " ".join(script["scenes"])
voice = script.get("voice", "ru-RU-DmitryNeural")

result = subprocess.run(
    [
        "edge-tts",
        "--voice", voice,
        "--rate=-5%",
        "--text", text,
        "--write-media", str(AUDIO_FILE),
    ],
    capture_output=True,
    text=True,
    encoding="utf-8-sig",
    errors="replace",
)

if result.returncode != 0:
    print(result.stderr)
    raise SystemExit(result.returncode)

if not AUDIO_FILE.exists() or AUDIO_FILE.stat().st_size == 0:
    raise SystemExit("Audio file was not created or is empty.")

print(f"Audio created: {AUDIO_FILE}")
print(f"Size: {AUDIO_FILE.stat().st_size // 1024} KB")

