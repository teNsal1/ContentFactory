from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import json
import math
import random

OUT = Path("output/scenes")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 720, 1280
random.seed(42)

def font(size):
    for path in [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def make_scene(index, title, subtitle, color):
    img = Image.new("RGB", (W, H), (7, 12, 24))
    pixels = img.load()

    # Холодный свет в центре композиции
    for y in range(H):
        for x in range(W):
            dx = (x - W * 0.5) / W
            dy = (y - H * 0.43) / H
            glow = max(0, 1 - math.sqrt(dx * dx + dy * dy) * 2)
            pixels[x, y] = (
                int(7 + color[0] * glow * 0.45),
                int(12 + color[1] * glow * 0.45),
                int(24 + color[2] * glow * 0.45),
            )

    draw = ImageDraw.Draw(img)

    # Звёзды и рунические золотые точки
    for _ in range(90):
        x = random.randint(20, W - 20)
        y = random.randint(20, H - 20)
        r = random.choice([1, 1, 2, 3])
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(125, 144, 166))

    # Символическая рамка
    draw.rounded_rectangle(
        (35, 35, W-35, H-35),
        radius=18,
        outline=(173, 135, 65),
        width=3,
    )

    # Большой стилизованный знак в центре
    cx, cy = W // 2, 490
    draw.ellipse((cx-155, cy-155, cx+155, cy+155),
                 outline=(179, 139, 66), width=4)
    draw.ellipse((cx-125, cy-125, cx+125, cy+125),
                 outline=(90, 110, 142), width=2)

    # Символическая маска Локи
    draw.polygon([
        (cx-75, cy-85), (cx-20, cy-45),
        (cx, cy-100), (cx+20, cy-45),
        (cx+75, cy-85), (cx+52, cy+35),
        (cx, cy+100), (cx-52, cy+35)
    ], outline=(220, 185, 105), fill=(18, 29, 47))

    draw.line((cx-48, cy-20, cx-12, cy-5),
              fill=(240, 190, 95), width=5)
    draw.line((cx+12, cy-5, cx+48, cy-20),
              fill=(240, 190, 95), width=5)

    # Заголовок
    title_font = font(48)
    subtitle_font = font(28)

    draw.text((W//2, 800), title, font=title_font,
              fill=(245, 218, 160), anchor="mm",
              stroke_width=1, stroke_fill=(30, 20, 10))

    draw.text((W//2, 875), subtitle, font=subtitle_font,
              fill=(218, 225, 237), anchor="mm")

    draw.text((W//2, 1150), f"NORDIC MYTHS  /  {index:02d}",
              font=font(22), fill=(173, 135, 65), anchor="mm")

    img.save(OUT / f"scene_{index:02d}.png")
    print(f"Создана сцена {index}/6: {title}")

scenes = [
    ("THE TRICKSTER", "A god no one could predict", (35, 65, 110)),
    ("CHAOS", "Friend today. Enemy tomorrow.", (75, 30, 45)),
    ("GOLDEN GIFTS", "A trick changed everything", (95, 65, 25)),
    ("CLEVERNESS", "His mind could save Asgard", (25, 65, 75)),
    ("DANGER", "Sometimes Loki caused the chaos", (90, 25, 30)),
    ("WOULD YOU TRUST HIM?", "The most dangerous god?", (65, 45, 100)),
]

for i, (title, subtitle, color) in enumerate(scenes, 1):
    make_scene(i, title, subtitle, color)

print("\nГотово! Все сцены сохранены в output/scenes/")