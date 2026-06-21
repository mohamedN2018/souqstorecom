"""
Fully-offline placeholder image generation.

Generates gradient JPEGs locally with Pillow (built-in default font — no external
font files, no network). Images are written into MEDIA_ROOT and served by the
gateway at /media/. This keeps the whole stack self-contained.
"""
from __future__ import annotations

import os
import random

from PIL import Image, ImageDraw, ImageFont

# A palette of pleasant base colors keyed loosely to product themes.
BASE_COLORS = [
    (37, 99, 235), (22, 163, 74), (219, 39, 119), (147, 51, 234),
    (220, 38, 38), (8, 145, 178), (234, 88, 12), (79, 70, 229),
    (5, 150, 105), (202, 138, 4), (190, 24, 93), (2, 132, 199),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _gradient(width, height, top, bottom):
    base = Image.new("RGB", (width, height), top)
    draw = ImageDraw.Draw(base)
    for y in range(height):
        draw.line([(0, y), (width, y)], fill=_lerp(top, bottom, y / height))
    return base


def make_image(path: str, label: str, seed: int, size=(600, 600)) -> None:
    rnd = random.Random(seed)
    top = rnd.choice(BASE_COLORS)
    bottom = _lerp(top, (15, 23, 42), 0.65)  # fade toward slate
    img = _gradient(size[0], size[1], top, bottom)
    draw = ImageDraw.Draw(img)

    # decorative translucent circles
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for _ in range(4):
        r = rnd.randint(60, 200)
        cx, cy = rnd.randint(0, size[0]), rnd.randint(0, size[1])
        odraw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 18))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 34)
    except OSError:
        font = ImageFont.load_default()

    text = (label or "SouqStore")[:22]
    tb = draw.textbbox((0, 0), text, font=font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    draw.text(
        ((size[0] - tw) / 2, (size[1] - th) / 2),
        text, fill=(255, 255, 255), font=font,
    )

    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "JPEG", quality=82)


def generate_pool(media_root: str, subdir: str, labels, per_label: int = 6):
    """
    Generate `per_label` images for each label under media_root/subdir/.
    Returns a dict: label -> [relative urls]. Skips files that already exist.
    """
    out: dict[str, list[str]] = {}
    for li, label in enumerate(labels):
        urls = []
        for n in range(per_label):
            rel = f"{subdir}/{li:02d}_{n}.jpg"
            full = os.path.join(media_root, rel)
            if not os.path.exists(full):
                make_image(full, label, seed=li * 1000 + n)
            urls.append(f"/media/{rel}")
        out[label] = urls
    return out
