from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

OUT = Path("output/spiderman_scenes")
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

scenes = [
    ("НОВАЯ ЖИЗНЬ", "Обычный парень. Необычная сила.", (55, 12, 35)),
    ("ЧУВСТВО ОПАСНОСТИ", "Он замечает угрозу раньше других.", (15, 35, 90)),
    ("ПАУТИНА", "Стены больше не преграда.", (70, 15, 25)),
    ("ДВОЙНАЯ ЖИЗНЬ", "Учёба, друзья и ответственность.", (15, 35, 65)),
    ("ТРУДНЫЙ ВЫБОР", "Помочь другим или себе?", (75, 18, 20)),
    ("НАСТОЯЩИЙ ГЕРОЙ", "Сила требует ответственности.", (20, 30, 75)),
]

for i, (title, subtitle, color) in enumerate(scenes, 1):
    make_scene(i, title, subtitle, color)

print("Готово! Сцены сохранены в output/spiderman_scenes/")
