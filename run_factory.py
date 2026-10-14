from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

STEPS = [
    ("Создание сценария", "create_script.py"),
    ("Генерация озвучки", "create_audio.py"),
    ("Создание сцен", "create_scenes.py"),
    ("Распознавание речи и субтитры", "make_subtitles.py"),
    ("Сборка видео", "create_video.py"),
    ("Наложение субтитров", "add_subtitles.py"),
]

def main():
    print("=" * 50)
    print("CONTENT FACTORY — запуск производства")
    print("=" * 50)

    for number, (title, filename) in enumerate(STEPS, 1):
        script = ROOT / filename

        if not script.exists():
            raise FileNotFoundError(
                f"Не найден скрипт: {filename}"
            )

        print(f"\n[{number}/{len(STEPS)}] {title}")
        print("-" * 50)

        subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            check=True,
        )

    final_video = ROOT / "output" / "loki_final.mp4"

    if not final_video.exists():
        raise FileNotFoundError(
            "Процесс завершился, но итоговое видео не найдено."
        )

    print("\n" + "=" * 50)
    print("ГОТОВО! Все этапы выполнены.")
    print(f"Видео: {final_video}")
    print("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        print(f"\nОШИБКА: этап завершился с кодом {error.returncode}.")
        print("Исправим ошибку, не удаляя рабочие файлы.")
        sys.exit(error.returncode)
    except Exception as error:
        print(f"\nОШИБКА: {error}")
        sys.exit(1)