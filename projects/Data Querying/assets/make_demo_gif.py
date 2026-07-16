from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(__file__).resolve().parent / 'demo.gif'
W, H = 800, 420
font = ImageFont.load_default()

steps = [
    'Type question',
    'Generating SQL',
    'Running query',
    'Summarizing results',
    'Answer ready'
]

frames = []
for i, s in enumerate(steps):
    img = Image.new('RGB', (W, H), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    # header
    d.rectangle([20, 20, W-20, 90], outline=(37,99,235), width=3)
    d.text((40, 30), 'GenAI Data Query Demo', fill=(10, 10, 10), font=font)
    # panel
    d.rectangle([40, 120, W-40, H-60], outline=(200,200,200), width=2)
    d.text((60, 140), s, fill=(60,60,60), font=font)
    # footer progress dots
    for j in range(len(steps)):
        x = 60 + j*30
        y = H-40
        fill = (37,99,235) if j <= i else (200,200,200)
        d.ellipse([x, y, x+16, y+16], fill=fill)
    frames.append(img)

frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=700, loop=0)
print('Wrote', OUT)
