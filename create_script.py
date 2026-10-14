import json
from pathlib import Path

output = Path("output")
output.mkdir(exist_ok=True)

script = {
    "title": "Почему Человек-паук — необычный герой?",
    "topic": "Человек-паук и цена ответственности",
    "language": "ru",
    "voice": "ru-RU-DmitryNeural",
    "scenes": [
        "Питер Паркер получил невероятные способности, но его жизнь не стала легче.",
        "Он мог взбираться по стенам, чувствовать опасность и выпускать паутину.",
        "Но самое сложное было вовсе не в борьбе с преступниками.",
        "Питер постоянно выбирал между личной жизнью и помощью другим.",
        "Он знал: если у тебя есть сила, важно то, как ты её используешь.",
        "Именно поэтому Человек-паук — герой не только из-за своих способностей."
    ]
}

with open(output / "script.json", "w", encoding="utf-8") as f:
    json.dump(script, f, ensure_ascii=False, indent=2)

print("Русский сценарий создан!")
print(f"Тема: {script['topic']}")
print(f"Количество сцен: {len(script['scenes'])}")