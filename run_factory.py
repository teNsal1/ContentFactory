from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

STEPS = [
    ("Создание сценария", "create_script.py"),
    ("Создание сцен", "create_spiderman_scenes.py"),
    ("Создание озвучки", "create_audio.py"),
    ("Создание видео из сцен", "create_spiderman_video.py"),
    ("Создание субтитров из сценария", "create_subtitles.py"),
    ("Наложение русских субтитров", "add_spiderman_subtitles.py"),
]


def main():
    print("=" * 50)
    print("CONTENT FACTORY — SPIDER-MAN")
    print("=" * 50)

    for number, (title, filename) in enumerate(STEPS, 1):
        script = ROOT / filename

        if not script.exists():
            raise FileNotFoundError(
                f"Не найден файл: {filename}"
            )

        print(f"\n[{number}/{len(STEPS)}] {title}")
        print("-" * 50)

        subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            check=True,
        )

    final_video = ROOT / "output" / "spiderman_final.mp4"

    if not final_video.exists():
        raise FileNotFoundError(
            f"Итоговое видео не найдено: {final_video}"
        )

    print("\n" + "=" * 50)
    print("ГОТОВО! Видео создано.")
    print(f"Видео: {final_video}")
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        print(
            f"\nОШИБКА: этап завершился с кодом "
            f"{error.returncode}."
        )
        sys.exit(error.returncode)
    except Exception as error:
        print(f"\nОШИБКА: {error}")
        sys.exit(1)