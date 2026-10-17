# /// script
# requires-python = ">=3.12"
# dependencies = ["pillow"]
# ///
"""Build Pepper's animation frames from the hand-drawn source sprites.

uv run scripts/pepper_sprites.py

Sources in assets/pepper/src/ are left untouched. Every frame is written to
assets/pepper/frames/ on one canvas with the paws on the same baseline, so
pepper_harvest.py can swap frames without the dog jumping or resizing.
"""

from pathlib import Path

from PIL import Image

PEPPER = Path(__file__).parents[1] / "assets" / "pepper"
SRC, OUT = PEPPER / "src", PEPPER / "frames"
CANVAS = (86, 68)
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
N8 = N4 + ((1, 1), (1, -1), (-1, 1), (-1, -1))

# walk_a geometry: legs start at LEG_ROW; back and front leg pairs by x range.
LEG_ROW = 52
BACK, FRONT = (0, 31), (32, 66)


def dark(p: tuple[int, ...]) -> bool:
    return p[3] > 0 and max(p[:3]) < 70


def clean(im: Image.Image) -> Image.Image:
    """Drop the light anti-alias fringe outside the black outline and stray specks."""
    im = im.convert("RGBA")
    px, (w, h) = im.load(), im.size

    def at(x: int, y: int) -> tuple[int, ...]:
        return px[x, y] if 0 <= x < w and 0 <= y < h else (0, 0, 0, 0)

    while True:
        kill = []
        for y in range(h):
            for x in range(w):
                p = px[x, y]
                if not p[3] or dark(p) or all(at(x + dx, y + dy)[3] for dx, dy in N4):
                    continue
                neutral = max(p[:3]) - min(p[:3]) < 40
                outline = any(dark(at(x + dx, y + dy)) for dx, dy in N8)
                lonely = sum(1 for dx, dy in N8 if at(x + dx, y + dy)[3]) <= 2
                if (neutral and outline) or lonely:
                    kill.append((x, y))
        if not kill:
            break
        for x, y in kill:
            px[x, y] = (0, 0, 0, 0)

    # Keep only the largest connected shape (drops detached motion marks).
    seen, best = set(), set()
    for y in range(h):
        for x in range(w):
            if px[x, y][3] and (x, y) not in seen:
                comp, stack = set(), [(x, y)]
                while stack:
                    cx, cy = stack.pop()
                    if (cx, cy) in comp or not (0 <= cx < w and 0 <= cy < h) or not px[cx, cy][3]:
                        continue
                    comp.add((cx, cy))
                    stack.extend((cx + dx, cy + dy) for dx, dy in N8)
                seen |= comp
                best = max(best, comp, key=len)
    for y in range(h):
        for x in range(w):
            if (x, y) not in best:
                px[x, y] = (0, 0, 0, 0)
    return im


def legs(base: Image.Image, back: str, front: str) -> Image.Image:
    """Redraw the two leg pairs below LEG_ROW: 'none', 'flip' (other stride) or 'gather'."""
    out, src, (w, h) = base.copy(), base.load(), base.size
    px = out.load()
    for y in range(LEG_ROW, h):
        for x in range(w):
            px[x, y] = (0, 0, 0, 0)
    for (x0, x1), op in ((BACK, back), (FRONT, front)):
        cx = (x0 + x1 - 1) / 2
        for y in range(LEG_ROW, h):
            for x in range(x0, x1):
                sx = {"flip": round(2 * cx - x), "gather": round(cx + (x - cx) / 0.62)}.get(op, x)
                if x0 <= sx < x1 and src[sx, y][3]:
                    px[x, y] = src[sx, y]
    return out


def rotate_part(base: Image.Image, box: tuple[int, int, int, int], pivot: tuple[int, int],
                degrees: float, refill: tuple[int, int, int, int] | None = None) -> Image.Image:
    """Rotate the pixels inside box about pivot, clockwise for positive degrees.

    Pixels inside refill that the turned part no longer covers keep their original
    colour, so the neck stays joined to the body instead of showing a cut.
    """
    part = Image.new("RGBA", base.size)
    part.paste(base.crop(box), box[:2])
    out = base.copy()
    out.paste((0, 0, 0, 0), box)
    out.alpha_composite(part.rotate(-degrees, resample=Image.NEAREST, center=pivot))
    if refill:
        src, px = base.load(), out.load()
        x0, y0, x1, y1 = refill
        for y in range(y0, y1):
            for x in range(x0, x1):
                if not px[x, y][3]:
                    px[x, y] = src[x, y]
    return out


def lower_head(base: Image.Image, degrees: float) -> Image.Image:
    """Bend at the shoulder so the nose points at the grass; legs stay planted."""
    padded = Image.new("RGBA", (base.width + 8, base.height))
    padded.paste(base)
    padded.paste((0, 0, 0, 0), (36, 0, 46, 25))  # the raised neck line of the upright pose
    out = rotate_part(padded, (46, 0, padded.width, LEG_ROW), (46, 42), degrees,
                      refill=(36, 25, 54, LEG_ROW))
    # Close the new back line: outline on top, back fur below, like the rest of the back.
    px, fur = out.load(), padded.getpixel((30, 34))
    for x in range(36, 54):
        top = next((y for y in range(20, LEG_ROW) if px[x, y][3]), None)
        if top is not None and not dark(px[x, top]):
            px[x, top] = (0, 0, 0, 255)
            for y in range(top + 1, min(top + 4, LEG_ROW)):
                px[x, y] = fur
    return out


def place(frame: Image.Image, x: int) -> Image.Image:
    """Paws on the canvas bottom row, left edge at x."""
    canvas = Image.new("RGBA", CANVAS)
    canvas.alpha_composite(frame, (x, CANVAS[1] - frame.height))
    return canvas


def main() -> None:
    walk = clean(Image.open(SRC / "walk_a.png"))
    sit = clean(Image.open(SRC / "sit.png"))
    frames = {
        "walk0": legs(walk, "none", "none"),
        "walk1": legs(walk, "gather", "gather"),
        "walk2": legs(walk, "flip", "flip"),
        "walk3": legs(walk, "gather", "gather"),
        "sniff0": lower_head(walk, 38),
        "sniff1": lower_head(walk, 43),
        "dig0": legs(lower_head(walk, 40), "none", "flip"),
        "dig1": legs(lower_head(walk, 40), "none", "gather"),
        "eat0": lower_head(walk, 30),
        "eat1": lower_head(walk, 22),
    }
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.png"):
        old.unlink()
    for name, im in frames.items():
        place(im, 2).save(OUT / f"{name}.png")
    # Seated finale: tail sways between two positions.
    tail, root = (42, 36, sit.width, sit.height - 4), (44, sit.height - 8)
    seam = (40, 36, 50, sit.height - 4)
    place(rotate_part(sit, tail, root, -7, refill=seam), 12).save(OUT / "sit0.png")
    place(rotate_part(sit, tail, root, 7, refill=seam), 12).save(OUT / "sit1.png")
    print(f"wrote {len(frames) + 2} frames to {OUT}")


if __name__ == "__main__":
    main()
