from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap

OUT = Path(__file__).resolve().parent / 'demo.gif'
W, H = 900, 480
try:
    # try to use a truetype font for better rendering if available
    font = ImageFont.truetype("arial.ttf", 16)
    header_font = ImageFont.truetype("arial.ttf", 20)
except Exception:
    font = ImageFont.load_default()
    header_font = font

slides = [
    {
        "title": "Type question",
        "content": "Which customers spent the most in March?"
    },
    {
        "title": "Generating SQL",
        "content": (
            "SELECT c.name, SUM(s.amount) AS total_spent\n"
            "FROM customer c JOIN sales s ON c.customer_id = s.customer_id\n"
            "WHERE sale_date BETWEEN '2023-03-01' AND '2023-03-31'\n"
            "GROUP BY c.customer_id, c.name ORDER BY total_spent DESC"
        )
    },
    {
        "title": "Running query",
        "content": "Results:\nAsha Sharma — 1225.0\nRahul Verma — 300.0"
    },
    {
        "title": "Summarizing results",
        "content": "Asha Sharma spent the most in March (total $1,225)."
    },
    {
        "title": "Answer ready",
        "content": "Asha Sharma — $1,225"
    }
]

def draw_multiline_text(draw, text, xy, font, max_width, fill=(60,60,60)):
    lines = []
    # use a conservative wrap width for readability
    wrap_width = 70
    for paragraph in text.split('\n'):
        wrapped = textwrap.wrap(paragraph, width=wrap_width)
        if not wrapped:
            lines.append('')
        else:
            lines.extend(wrapped)
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        # measure text height using textbbox for compatibility
        bbox = draw.textbbox((0, 0), line, font=font)
        line_h = bbox[3] - bbox[1]
        y += line_h + 6

frames = []
for i, s in enumerate(slides):
    img = Image.new('RGB', (W, H), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    # header
    d.rectangle([20, 20, W-20, 100], outline=(37,99,235), width=3)
    d.text((40, 34), 'GenAI Data Query Demo', fill=(10, 10, 10), font=header_font)
    # title box
    d.rectangle([40, 120, W-40, H-60], outline=(200,200,200), width=2)
    d.text((60, 130), s['title'], fill=(20,20,20), font=header_font)
    # main content
    draw_multiline_text(d, s['content'], (60, 170), font, max_width=W-160)
    # footer progress dots
    for j in range(len(slides)):
        x = 60 + j*36
        y = H-40
        fill = (37,99,235) if j <= i else (200,200,200)
        d.ellipse([x, y, x+20, y+20], fill=fill)
    frames.append(img)

frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=900, loop=0)
print('Wrote', OUT)
