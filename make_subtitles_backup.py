from faster_whisper import WhisperModel
from pathlib import Path
import json

audio_path = "output/loki_narration.mp3"
output_path = "output/subtitles.json"

Path("output").mkdir(exist_ok=True)

print("Загружаем модель распознавания...")
model = WhisperModel("tiny", device="cpu", compute_type="int8")

print("Распознаём английскую речь...")
segments, info = model.transcribe(audio_path, language="en")

subtitles = []

for segment in segments:
    subtitles.append({
        "start": round(segment.start, 2),
        "end": round(segment.end, 2),
        "text": segment.text.strip(),
    })

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(subtitles, file, ensure_ascii=False, indent=2)

print(f"\nГотово! Субтитры сохранены: {output_path}")
print(f"Количество фрагментов: {len(subtitles)}")
print(json.dumps(subtitles, ensure_ascii=False, indent=2))