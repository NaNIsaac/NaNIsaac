# /// script
# requires-python = ">=3.12"
# dependencies = ["pillow"]
# ///
"""Build Pepper's animation frames from the sprite sheet.

uv run scripts/pepper_sprites.py

assets/pepper/src/sheet.png is a 4 x 3 grid drawn at roughly 4.4 screen pixels
per art pixel, with soft edges. Each pose is cut out, brought back to one art
pixel per pixel with a single shared scale and palette, cleaned of edge fringe,
and written to assets/pepper/frames/ on one canvas with the paws on the bottom
row, so pepper_harvest.py can swap frames without the dog jumping or resizing.
"""

from pathlib import Path

from PIL import Image

PEPPER = Path(__file__).parents[1] / "assets" / "pepper"
SRC, OUT = PEPPER / "src", PEPPER / "frames"
CANVAS = (86, 68)
WALK_HEIGHT = 64  # art pixels from ear tip to paw in the walk row
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
N8 = N4 + ((1, 1), (1, -1), (-1, 1), (-1, -1))
NAMES = (("walk0", "walk1", "walk2", "walk3"),
         ("sniff0", "sniff1", "dig0", "dig1"),
         ("eat0", "eat1", "sit0", "sit1"))


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


def bands(profile: list[int], min_len: int = 20) -> list[tuple[int, int]]:
    out, start = [], None
    for i, v in enumerate(profile + [0]):
        if v and start is None:
            start = i
        elif not v and start is not None:
            if i - start > min_len:
                out.append((start, i))
            start = None
    return out


def cut_sheet(sheet: Image.Image) -> list[list[Image.Image]]:
    """Split the sheet into its poses by the empty gaps between them."""
    solid = sheet.getchannel("A").point(lambda v: 255 if v > 128 else 0)
    w, h = solid.size
    data = solid.load()
    rows = bands([sum(1 for x in range(0, w, 2) if data[x, y]) for y in range(h)])
    cols = bands([sum(1 for y in range(0, h, 2) if data[x, y]) for x in range(w)])
    grid = []
    for y0, y1 in rows:
        line = []
        for x0, x1 in cols:
            cell = sheet.crop((x0, y0, x1, y1))
            line.append(cell.crop(cell.getchannel("A").point(lambda v: 255 if v > 128 else 0).getbbox()))
        grid.append(line)
    return grid


def pixelate(cells: list[Image.Image], scale: float) -> list[Image.Image]:
    """Average back to art pixels, then snap alpha and share one 32-colour palette."""
    small = [c.resize((round(c.width * scale), round(c.height * scale)), Image.BOX) for c in cells]
    strip = Image.new("RGB", (sum(im.width for im in small), max(im.height for im in small)))
    x = 0
    for im in small:
        strip.paste(im.convert("RGB"), (x, 0))
        x += im.width
    palette = strip.quantize(32, method=Image.Quantize.MAXCOVERAGE)
    out = []
    for im in small:
        rgb = im.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE).convert("RGBA")
        rgb.putalpha(im.getchannel("A").point(lambda v: 255 if v > 110 else 0))
        out.append(rgb)
    return out


def place(frame: Image.Image, x: int) -> Image.Image:
    """Paws on the canvas bottom row, left edge at x."""
    canvas = Image.new("RGBA", CANVAS)
    canvas.alpha_composite(frame, (x, CANVAS[1] - frame.height))
    return canvas


def tail_x(im: Image.Image) -> int:
    """Left edge of the curled tail (top half), the steadiest point between side poses."""
    top = im.crop((0, 0, im.width, im.height // 2))
    return top.getchannel("A").getbbox()[0]


def main() -> None:
    grid = cut_sheet(Image.open(SRC / "sheet.png").convert("RGBA"))
    scale = WALK_HEIGHT / max(im.height for im in grid[0])
    frames = pixelate([im for line in grid for im in line], scale)
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.png"):
        old.unlink()
    for name, im in zip((n for line in NAMES for n in line), frames):
        im = clean(im)
        side = not name.startswith("sit")
        x = 4 - tail_x(im) if side else (CANVAS[0] - im.width) // 2
        place(im, x).save(OUT / f"{name}.png")
    print(f"wrote {len(frames)} frames to {OUT} (scale {scale:.4f})")


if __name__ == "__main__":
    main()
