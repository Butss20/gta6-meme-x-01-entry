#!/usr/bin/env python3
"""Build meme.png for the gta6-meme-x-01 bounty.

Joke: MY AI AGENT WON A BOUNTY / AND BOUGHT ME GTA 6 — the make.fun ghost
itself is the hero of the scene, floating over a Vice City synthwave sunset
and proudly holding up a GTA VI game box. The ghost is the real press-kit
mark (assets/mark-1024.png) with its magenta disc removed, so the ghost,
its sparkle eyes and its magenta star coin are the genuine article, worked
into the scene instead of pasted on as a sticker.

Everything is drawn with PIL + numpy, seeded, no network. Deterministic:
two runs write byte-identical files.
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

MAGENTA = (196, 28, 131)
DARK = (22, 10, 36)
SUN_YELLOW = (255, 215, 106)


def extract_ghost(mark_path):
    """Return the make.fun ghost alone, cropped, from the press-kit mark.

    The mark is a white ghost (dark outline, sparkle eyes, magenta star
    coin) on a magenta disc. Drop every magenta-family pixel and every
    low-alpha pixel, keep only pixels within 445 px of the disc centre
    (that excludes the disc's dark outer ring), then paint the coin's
    magenta middle back in underneath the surviving white star.
    """
    im = Image.open(mark_path).convert("RGBA")
    px = np.array(im).astype(np.int16)
    r, g, b, a = px[..., 0], px[..., 1], px[..., 2], px[..., 3]
    magenta = (r > 140) & (g < 110) & (b > 70) & (b < 210) & (r > b)
    keep = (a >= 200) & (~magenta)
    # Keep only the pixels connected to the ghost's body: the disc's dark
    # outer ring is a separate component (a gap of dropped magenta sits
    # between it and the ghost), so growing a seed inside the body drops
    # the ring. The white star on the coin is separate too, so keep
    # everything inside the coin's circle as well.
    seed = np.zeros((1024, 1024), dtype=bool)
    seed[590:610, 502:522] = True
    grown = seed & keep
    for _ in range(1200):
        up = np.zeros_like(grown); up[1:, :] = grown[:-1, :]
        dn = np.zeros_like(grown); dn[:-1, :] = grown[1:, :]
        lf = np.zeros_like(grown); lf[:, 1:] = grown[:, :-1]
        rt = np.zeros_like(grown); rt[:, :-1] = grown[:, 1:]
        nxt = grown | ((up | dn | lf | rt) & keep)
        if (nxt == grown).all():
            break
        grown = nxt
    yy, xx = np.mgrid[0:1024, 0:1024]
    in_coin = (xx - 793) ** 2 + (yy - 441) ** 2 <= 100 ** 2
    keep = grown | (keep & in_coin)
    out = np.zeros((1024, 1024, 4), dtype=np.uint8)
    out[..., 0] = np.where(keep, px[..., 0], 0).astype(np.uint8)
    out[..., 1] = np.where(keep, px[..., 1], 0).astype(np.uint8)
    out[..., 2] = np.where(keep, px[..., 2], 0).astype(np.uint8)
    out[..., 3] = np.where(keep, px[..., 3], 0).astype(np.uint8)
    ghost = Image.fromarray(out, "RGBA")
    coin = Image.new("RGBA", ghost.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(coin)
    d.ellipse([793 - 96, 441 - 96, 793 + 96, 441 + 96],
              fill=MAGENTA + (255,))
    ghost = Image.alpha_composite(coin, ghost)
    return ghost.crop(ghost.getchannel("A").getbbox())


def sky_gradient():
    """Vice City sunset: deep purple -> magenta -> orange, top to bottom."""
    stops = [(0.0, (22, 11, 46)), (0.45, (75, 17, 101)),
             (0.72, (196, 28, 131)), (1.0, (255, 122, 47))]
    ys = np.linspace(0, 1, H)
    cols = np.zeros((H, 3), dtype=np.uint8)
    for i in range(len(stops) - 1):
        y0, c0 = stops[i]
        y1, c1 = stops[i + 1]
        m = (ys >= y0) & (ys <= y1)
        t = ((ys[m] - y0) / (y1 - y0))[:, None]
        cols[m] = (np.array(c0) * (1 - t) + np.array(c1) * t).astype(np.uint8)
    return Image.fromarray(np.repeat(cols[:, None, :], W, axis=1), "RGB")


def retro_sun(base):
    """Pale sun with horizontal slats, low on the horizon."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy, r = 512, 360, 125
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SUN_YELLOW + (255,))
    y = cy + 10
    gap = 4
    while y < cy + r:
        d.rectangle([cx - r, y, cx + r, y + gap], fill=(0, 0, 0, 0))
        y += gap + 14
        gap += 5
    base.alpha_composite(layer)


def skyline(base, rng):
    """Dark building silhouettes with a few lit windows, base at y=720."""
    d = ImageDraw.Draw(base)
    x = -10
    while x < W + 10:
        bw = rng.randint(50, 110)
        bh = rng.randint(55, 175)
        d.rectangle([x, 720 - bh, x + bw, 720], fill=(28, 11, 51, 255))
        for _ in range(rng.randint(2, 7)):
            wx = rng.randint(x + 8, x + bw - 12)
            wy = rng.randint(720 - bh + 10, 700)
            d.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 215, 106, 255))
        x += bw + rng.randint(4, 18)


def palm(base, x0, lean, flip):
    """One palm-tree silhouette: curved trunk + six fronds."""
    d = ImageDraw.Draw(base)
    pts = []
    for t in np.linspace(0, 1, 20):
        pts.append((x0 + lean * t * t * 130, 730 - t * 300))
    d.line(pts, fill=DARK + (255,), width=14, joint="curve")
    tx, ty = pts[-1]
    for k in range(6):
        ang = math.radians(-160 + k * 32) if not flip else math.radians(-20 - k * 32)
        fr = []
        for t in np.linspace(0, 1, 12):
            fx = tx + math.cos(ang) * t * 130 + (0 if not flip else 0)
            fy = ty + math.sin(ang) * t * 130 + t * t * 90
            fr.append((fx, fy))
        d.line(fr, fill=DARK + (255,), width=9, joint="curve")


def neon_grid(base):
    """Synthwave floor: dark ground with a magenta perspective grid."""
    d = ImageDraw.Draw(base)
    d.rectangle([0, 720, W, H], fill=(18, 8, 31, 255))
    for i, y in enumerate([730, 748, 775, 812, 860, 922, 1000]):
        d.line([0, y, W, y], fill=(92, 26, 92, 255), width=2 + i // 3)
    for x in [-300, -80, 200, 380, 512, 644, 824, 1104, 1324]:
        d.line([512 + (x - 512) * 0.25, 720, x, H],
               fill=(92, 26, 92, 255), width=2)


def game_box():
    """A GTA VI game case, drawn on its own layer and tilted -8 degrees."""
    bw, bh = 260, 310
    layer = Image.new("RGBA", (bw + 60, bh + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0 = 30, 30
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=18,
                        fill=(15, 24, 48, 255), outline=(255, 45, 149, 255),
                        width=7)
    d.rounded_rectangle([x0 + 14, y0 + 14, x0 + bw - 14, y0 + bh - 14],
                        radius=12, outline=(255, 45, 149, 255), width=2)
    f_big = ImageFont.truetype(BOLD, 62)
    f_small = ImageFont.truetype(BOLD, 26)
    d.text((x0 + bw / 2, y0 + 105), "GTA VI", font=f_big,
           fill=(255, 255, 255, 255), anchor="mm",
           stroke_width=3, stroke_fill=(0, 0, 0, 255))
    d.text((x0 + bw / 2, y0 + 160), "VICE CITY", font=f_small,
           fill=(255, 215, 106, 255), anchor="mm")
    d.text((x0 + bw / 2, y0 + 245), "★", font=ImageFont.truetype(BOLD, 56),
           fill=MAGENTA + (255,), anchor="mm")
    return layer.rotate(-8, resample=Image.BICUBIC, expand=True)


def caption(draw, text, y, size):
    """One huge white caption line with a black outline, centred."""
    font = ImageFont.truetype(BOLD, size)
    while font.getlength(text) > 940 and size > 30:
        size -= 2
        font = ImageFont.truetype(BOLD, size)
    draw.text((W / 2, y), text, font=font, fill=(255, 255, 255, 255),
              anchor="ma", stroke_width=max(4, size // 12),
              stroke_fill=(0, 0, 0, 255))


def main():
    rng = random.Random(20261119)
    img = sky_gradient().convert("RGBA")
    retro_sun(img)
    skyline(img, rng)
    neon_grid(img)
    palm(img, 60, 1, flip=False)
    palm(img, 964, -1, flip=True)

    ghost = extract_ghost(os.path.join(HERE, "assets", "mark-1024.png"))
    ghost = ghost.resize((int(ghost.width * 460 / ghost.height), 460),
                         Image.LANCZOS)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([512 - 190, 838, 512 + 190, 878], fill=(0, 0, 0, 160))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14)))
    img.alpha_composite(ghost, (512 - ghost.width // 2, 370))

    box = game_box()
    img.alpha_composite(box, (512 - box.width // 2 + 40, 565))

    d = ImageDraw.Draw(img)
    caption(d, "MY AI AGENT WON A BOUNTY", 34, 62)
    caption(d, "AND BOUGHT ME GTA 6", 928, 60)

    out = os.path.join(HERE, "meme.png")
    img.convert("RGB").save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
