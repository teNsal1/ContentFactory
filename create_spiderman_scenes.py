from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

OUT = Path("output/scenes")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 720, 1280
random.seed(17)

def get_font(size):
    for path in [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def make_scene(index, title, subtitle, color):
    if "космос" in script["topic"].casefold():
        img = Image.new("RGB", (W, H), (3, 7, 28))
        draw = ImageDraw.Draw(img, "RGBA")

        # Звёздное небо
        for _ in range(220):
            x = random.randint(0, W - 1)
            y = random.randint(0, 900)
            r = random.choice([1, 1, 2, 3])
            draw.ellipse(
                (x - r, y - r, x + r, y + r),
                fill=(220, 235, 255, random.randint(100, 255))
            )

        # Большая планета
        planet_x = random.randint(260, 460)
        planet_y = random.randint(390, 650)
        planet_r = random.randint(120, 185)

        planet_colors = [
            (75, 125, 220, 255),
            (190, 100, 75, 255),
            (125, 90, 190, 255),
            (60, 170, 175, 255),
            (210, 155, 90, 255),
            (100, 145, 190, 255),
        ]

        planet_color = planet_colors[(index - 1) % len(planet_colors)]

        draw.ellipse(
            (
                planet_x - planet_r,
                planet_y - planet_r,
                planet_x + planet_r,
                planet_y + planet_r,
            ),
            fill=planet_color,
            outline=(210, 230, 255, 230),
            width=4,
        )

        # Кольцо планеты
        draw.ellipse(
            (
                planet_x - planet_r - 55,
                planet_y - 45,
                planet_x + planet_r + 55,
                planet_y + 45,
            ),
            outline=(220, 220, 255, 190),
            width=8,
        )

        # Заголовок и подпись
        title_font = get_font(38)
        subtitle_font = get_font(25)

        draw.rounded_rectangle(
            (30, 900, W - 30, 1120),
            radius=24,
            fill=(0, 0, 15, 210),
            outline=(100, 170, 255, 230),
            width=3,
        )

        def centered(text, y, font, fill):
            box = draw.textbbox((0, 0), text, font=font)
            x = (W - (box[2] - box[0])) // 2
            draw.text((x, y), text, font=font, fill=fill)

        centered(title, 930, title_font, (255, 255, 255, 255))
        centered(subtitle, 1000, subtitle_font, (190, 220, 255, 255))
        centered(
            f"КОСМОС  /  {index:02d}",
            1160,
            get_font(21),
            (120, 190, 255, 255),
        )

        img.save(OUT / f"scene_{index:02d}.png")
        print(f"Создана космическая сцена {index}/6: {title}")
        return
    img = Image.new("RGB", (W, H), (5, 8, 20))
    pixels = img.load()

    for y in range(H):
        for x in range(W):
            glow = max(0, 1 - math.sqrt(
                ((x - W * 0.5) / W) ** 2 +
                ((y - H * 0.43) / H) ** 2
            ) * 2)
            pixels[x, y] = (
                min(255, int(5 + color[0] * glow)),
                min(255, int(8 + color[1] * glow)),
                min(255, int(20 + color[2] * glow)),
            )

    draw = ImageDraw.Draw(img, "RGBA")

    # Nighttime city skyline
    for i in range(18):
        bx = i * 43 - 5
        bw = random.randint(25, 42)
        bh = random.randint(130, 380)
        top = 850 - bh
        draw.rectangle((bx, top, bx + bw, 900),
                       fill=(9, 16, 34, 245))
        for wy in range(top + 15, 875, 25):
            for wx in range(bx + 7, bx + bw - 5, 12):
                if random.random() < 0.35:
                    draw.rectangle((wx, wy, wx + 4, wy + 8),
                                   fill=(255, 190, 90, 170))

    # Spider-web lines in the upper part
    cx, cy = 360, 360
    for angle in range(0, 360, 30):
        a = math.radians(angle)
        ex = cx + math.cos(a) * 330
        ey = cy + math.sin(a) * 330
        draw.line((cx, cy, ex, ey),
                  fill=(190, 205, 230, 85), width=2)

    for radius in (70, 130, 195, 265, 330):
        points = []
        for angle in range(0, 361, 5):
            a = math.radians(angle)
            points.append((cx + math.cos(a) * radius,
                           cy + math.sin(a) * radius * 0.9))
        draw.line(points, fill=(190, 205, 230, 65), width=2)

    # Original stylized hero silhouette, not an existing movie frame
    hx, hy = 360, 600
    draw.ellipse((hx - 100, hy - 150, hx + 100, hy + 65),
                 fill=(160, 25, 42, 255),
                 outline=(245, 70, 75, 255), width=5)
    draw.polygon([
        (hx - 65, hy - 45), (hx - 155, hy + 5),
        (hx - 195, hy + 130), (hx - 135, hy + 150),
        (hx - 75, hy + 65), (hx - 40, hy + 180),
        (hx + 55, hy + 180), (hx + 75, hy + 65),
        (hx + 140, hy + 150), (hx + 195, hy + 125),
        (hx + 145, hy + 5), (hx + 65, hy - 45)
    ], fill=(20, 55, 125, 255),
       outline=(80, 145, 240, 255))

    # Mask eyes
    draw.polygon([
        (hx - 75, hy - 65), (hx - 20, hy - 45),
        (hx - 48, hy - 5), (hx - 80, hy - 20)
    ], fill=(245, 245, 255, 255))
    draw.polygon([
        (hx + 20, hy - 45), (hx + 75, hy - 65),
        (hx + 80, hy - 20), (hx + 48, hy - 5)
    ], fill=(245, 245, 255, 255))

    # Headline and subtitle
    title_font = get_font(38)
    subtitle_font = get_font(25)
    draw.rounded_rectangle((35, 930, W - 35, 1110),
                           radius=24, fill=(0, 0, 0, 175),
                           outline=(235, 55, 65, 220), width=3)

    def centered(text, y, font, fill):
        box = draw.textbbox((0, 0), text, font=font)
        x = (W - (box[2] - box[0])) // 2
        draw.text((x, y), text, font=font, fill=fill)

    centered(title, 955, title_font, (255, 255, 255, 255))
    centered(subtitle, 1025, subtitle_font, (210, 220, 240, 255))
    centered(f"ЧЕЛОВЕК-ПАУК  /  {index:02d}", 1170,
             get_font(21), (245, 90, 100, 255))

    img = img.filter(ImageFilter.GaussianBlur(0.25))
    img.save(OUT / f"scene_{index:02d}.png")
    print(f"Создана сцена {index}/6: {title}")

import json

SCRIPT_FILE = Path("output/script.json")

with open(SCRIPT_FILE, "r", encoding="utf-8-sig") as file:
    script = json.load(file)

titles = script["scene_titles"]
captions = script["scene_captions"]

colors = [
    (55, 12, 35),
    (15, 35, 90),
    (70, 15, 25),
    (15, 35, 65),
    (75, 18, 20),
    (20, 30, 75),
]

if not (len(titles) == len(captions) == len(colors) == 6):
    raise ValueError("В script.json должно быть ровно 6 заголовков и подписей.")

for i, (title, caption, color) in enumerate(
    zip(titles, captions, colors), 1
):
    make_scene(i, title, caption, color)

print("Готово! Сцены сохранены в output/spiderman_scenes/")