from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

Path("output").mkdir(exist_ok=True)

WIDTH, HEIGHT = 720, 1280
image = Image.new("RGB", (WIDTH, HEIGHT), (15, 20, 35))
draw = ImageDraw.Draw(image)

# Золотая рамка
draw.rounded_rectangle(
    (35, 35, WIDTH - 35, HEIGHT - 35),
    radius=24,
    outline=(190, 150, 75),
    width=3,
)

def get_font(size):
    candidates = [
        r"C:\Windows\Fonts\georgiab.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()

title_font = get_font(64)
subtitle_font = get_font(34)

def centered_text(text, y, font, fill):
    box = draw.textbbox((0, 0), text, font=font)
    x = (WIDTH - (box[2] - box[0])) // 2
    draw.text((x, y), text, font=font, fill=fill)

centered_text("NORDIC MYTHS", 330, subtitle_font, (205, 170, 100))
centered_text("WHY FEARED", 490, title_font, (245, 240, 225))
centered_text("LOKI?", 580, title_font, (225, 175, 80))
centered_text("THE GOD OF MISCHIEF", 720, subtitle_font, (190, 195, 210))

image.save("output/loki_cover.png")
print("Заставка создана: output/loki_cover.png")