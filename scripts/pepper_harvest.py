#!/usr/bin/env python3
"""Create an animated GitHub contribution garden for Pepper, the Shiba Inu.

Uses only Python's standard library.  Production data comes from GitHub GraphQL;
--demo is explicitly synthetic and intended only for local previews.
"""
from __future__ import annotations

import argparse
import base64
from datetime import date, timedelta
import html
import json
import os
from pathlib import Path
import random
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

API_URL = "https://api.github.com/graphql"
LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2,
          "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
PALETTES = {
    "light": {
        "background": "#f6f7f5", "text": "#252c29", "muted": "#66736b",
        "empty": "#e8eeea", "grass": ["#e8eeea", "#b9ddb3", "#85c781", "#4b9e5b", "#276d43"],
        "blades": ["#a8bcaa", "#6da974", "#3b8550", "#286d3e", "#174d32"],
        "foot": "#6b5d50", "soil": "#8a6a4a", "pit": "#4a3626", "clod": "#9b7450", "ring": "#d9a441", "shadow": "#1d2a22",
    },
    "dark": {
        "background": "#0d1117", "text": "#e6edf3", "muted": "#9aa7aa",
        "empty": "#18221e", "grass": ["#18221e", "#133d2a", "#18683c", "#29954d", "#49c16e"],
        "blades": ["#314c3a", "#277e49", "#34a35c", "#54d77c", "#8bea9e"],
        "foot": "#c9b8a2", "soil": "#6f5640", "pit": "#2a1f16", "clod": "#c49a6c", "ring": "#e8b44b", "shadow": "#000000",
    },
}
QUERY = """query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
  }
}"""


def fetch_contributions(username: str, token: str) -> list[list[dict]]:
    if not token:
        raise ValueError("GITHUB_TOKEN is required. Refusing to publish invented data.")
    payload = json.dumps({"query": QUERY, "variables": {"login": username}}).encode()
    req = urllib.request.Request(API_URL, data=payload,
        headers={"Authorization": f"Bearer {token}", "User-Agent": "pepper-harvest/1.0",
                 "Content-Type": "application/json", "Accept": "application/vnd.github+json"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.load(response)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"GitHub contribution request failed: {exc}") from exc
    if result.get("errors"):
        raise RuntimeError("GitHub GraphQL errors: " + json.dumps(result["errors"]))
    user = result.get("data", {}).get("user")
    if not user:
        raise RuntimeError(f"GitHub user not found or not readable: {username}")
    weeks = user["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [w["contributionDays"] for w in weeks]


def demo_contributions() -> list[list[dict]]:
    """Synthetic sample for visual testing. Never use it in deployed READMEs."""
    random.seed(37)
    start = date.today() - timedelta(days=364)
    start -= timedelta(days=(start.weekday() + 1) % 7)
    weeks = []
    for week in range(53):
        days = []
        for day in range(7):
            day_date = start + timedelta(days=week * 7 + day)
            level = 0 if random.random() < .29 else random.choices([1, 2, 3, 4], [4, 4, 3, 1])[0]
            days.append({"date": day_date.isoformat(), "contributionCount": level * 2,
                         "contributionLevel": list(LEVELS)[level]})
        weeks.append(days)
    return weeks


def sprite_data(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def fmt(num: float) -> str:
    return format(num, ".3f").rstrip("0").rstrip(".")


# Grid and sprite geometry. Frames come from scripts/pepper_sprites.py and share
# one canvas with the paws on its bottom row.
PITCH, TILE, LEFT, TOP = 13, 10, 24, 46
FRAME_W, FRAME_H, SCALE = 86, 68, 0.8
MOUTH = (66, 58)       # open mouth in eat0; it closes on the treat's tile
PAW_X = 58             # front paws, between the two strides
SPEED = 62.0           # px/s; four walk frames per stride keep the paws from sliding
STEP = 0.12            # seconds per walk frame
FRAMES = ("walk0", "walk1", "walk2", "walk3", "sniff0", "sniff1",
          "dig0", "dig1", "eat0", "eat1", "sit0", "sit1")
POSES = {  # action: (frames, seconds per frame)
    "sniff": (("sniff0", "sniff1"), 0.25),
    "dig": (("dig0", "dig1"), 0.14),
    "eat": (("eat0", "eat1"), 0.2),
    "sit": (("sit0", "sit1"), 0.18),
    "stand": (("walk0",), 1.0),
}
PRINT_LIFE = 1.5


def choose_treats(weeks: list[list[dict]]) -> list[tuple[int, int]]:
    """Pick up to three real nonzero days, one per third of the calendar.

    A sparse profile gets fewer treats. Activity is never invented.
    """
    n = len(weeks)
    candidates = [(col, row, int(day.get("contributionCount", 0)))
                  for col, week in enumerate(weeks) for row, day in enumerate(week[:7])
                  if int(day.get("contributionCount", 0)) > 0 and 1 <= row <= 5]
    results = []
    for lo, hi in [(5, n // 3), (n // 3, 2 * n // 3), (2 * n // 3, n - 6)]:
        region = [c for c in candidates if lo <= c[0] < hi]
        if region:
            mid = (lo + hi - 1) / 2
            col, row, _ = max(region, key=lambda c: (c[2], -abs(c[0] - mid), -abs(c[1] - 3)))
            results.append((col, row))
    return results


def key(t: float, duration: float) -> str:
    return format(t / duration, ".6f").rstrip("0").rstrip(".") or "0"


def svg_anim_visibility(intervals: list[tuple[float, float]], duration: float) -> str:
    """Discrete opacity switches that repeat and work inside an SVG <img>."""
    if not intervals:
        return ""
    times = {0.0, duration}
    for a, b in intervals:
        times.update((a, b))
    steps: dict[str, str] = {}  # keyTime -> value; the later state wins at a shared key
    for t in sorted(times):
        steps[key(t, duration)] = "1" if any(a <= t < b for a, b in intervals) else "0"
    values, keytimes = ";".join(steps.values()), ";".join(steps)
    return (f'<animate attributeName="opacity" values="{values}" keyTimes="{keytimes}" '
            f'calcMode="discrete" dur="{fmt(duration)}s" repeatCount="indefinite"/>')


def fade(t0: float, t1: float, t2: float, peak: float, duration: float) -> str:
    """Opacity 0 until t0, rises to peak at t1, back to 0 at t2."""
    keys = [0.0, t0, t1, t2, duration]
    vals = [0, 0, peak, 0, 0]
    pairs = [(k, v) for i, (k, v) in enumerate(zip(keys, vals)) if i == 0 or k > keys[i - 1]]
    return (f'<animate attributeName="opacity" values="{";".join(fmt(v) for _, v in pairs)}" '
            f'keyTimes="{";".join(key(k, duration) for k, _ in pairs)}" '
            f'dur="{fmt(duration)}s" repeatCount="indefinite"/>')


def ramp(points: list[tuple[float, float]], duration: float) -> str:
    """Opacity through (time, value) points, linear in between, 0 outside."""
    pts = [(0.0, 0.0)] + sorted((min(max(t, 0.001), duration - 0.001), v) for t, v in points) + [(duration, 0.0)]
    keep = [pts[0]] + [b for a, b in zip(pts, pts[1:]) if b[0] > a[0]]
    return (f'<animate attributeName="opacity" values="{";".join(fmt(v) for _, v in keep)}" '
            f'keyTimes="{";".join(key(t, duration) for t, _ in keep)}" '
            f'dur="{fmt(duration)}s" repeatCount="indefinite"/>')


def bone_shape(x: float, y: float) -> str:
    """Tiny geometric dog treat, deliberately not an emoji or font glyph."""
    return (f'<g transform="translate({fmt(x)} {fmt(y)}) scale(.6)" fill="#f3d39c" '
            'stroke="#7c583b" stroke-width="1.4">'
            '<path d="M-6 -1 Q-11 -6 -12 -2 Q-13 1 -9 2 Q-13 5 -9 7 Q-6 9 -4 5 '
            'L5 -4 Q9 -7 10 -3 Q12 1 8 2 Q12 5 8 7 Q5 9 2 4 Z"/></g>')


def paw_print(x: float, y: float, color: str) -> str:
    """A pad and three toes, a few pixels across."""
    return (f'<g fill="{color}"><rect x="{fmt(x - 2)}" y="{fmt(y - 1.4)}" width="4" height="2.8" rx="1.1"/>'
            f'<rect x="{fmt(x - 3.2)}" y="{fmt(y - 3.6)}" width="1.6" height="1.6" rx=".4"/>'
            f'<rect x="{fmt(x - .8)}" y="{fmt(y - 4.4)}" width="1.6" height="1.6" rx=".4"/>'
            f'<rect x="{fmt(x + 1.6)}" y="{fmt(y - 3.6)}" width="1.6" height="1.6" rx=".4"/></g>')


class Timeline:
    """Pepper's position and pose over one loop. All times are seconds."""

    def __init__(self, x: float, y: float) -> None:
        self.t, self.x, self.y = 0.0, x, y
        self.keys = [(0.0, x, y)]
        self.shown = {name: [] for name in FRAMES}
        self.contacts: list[tuple[float, float, float, int]] = []
        self.step = 0

    def walk(self, x: float, y: float) -> None:
        dist = ((x - self.x) ** 2 + (y - self.y) ** 2) ** .5
        n = max(4, round(dist / SPEED / STEP))
        dt = dist / SPEED / n if dist else STEP
        for i in range(n):
            t = self.t + i * dt
            frame = self.step % 4
            self.shown[f"walk{frame}"].append((t, t + dt))
            if frame in (0, 2):  # a paw lands on frames 0 and 2
                f = i / n
                self.contacts.append((t, self.x + (x - self.x) * f, self.y + (y - self.y) * f, frame // 2))
            self.step += 1
        self.t += n * dt
        self.x, self.y = x, y
        self.keys.append((self.t, x, y))

    def pose(self, action: str, seconds: float) -> tuple[float, float]:
        frames, every = POSES[action]
        start, i = self.t, 0
        while self.t < start + seconds - 1e-9:
            end = min(self.t + every, start + seconds)
            self.shown[frames[i % len(frames)]].append((self.t, end))
            self.t, i = end, i + 1
        self.keys.append((self.t, self.x, self.y))
        return start, self.t


def make_svg(weeks: list[list[dict]], *, theme: str, username: str,
             assets_dir: Path, demo: bool = False) -> str:
    """A self-contained animated SVG: walk, sniff, dig, eat, then sit and wag.

    The grass stays readable; only the chosen contribution days react.
    Frames are embedded PNG data URIs, animated with SMIL (no scripts).
    """
    if not weeks or not any(weeks):
        raise ValueError("Contribution calendar returned no days; refusing to overwrite output")
    if theme not in PALETTES:
        raise ValueError(f"Unknown palette: {theme}")
    p = PALETTES[theme]
    width = LEFT * 2 + len(weeks) * PITCH - (PITCH - TILE)
    height = TOP + 7 * PITCH + 33
    count = sum(int(d["contributionCount"]) for week in weeks for d in week)
    dates = [d["date"] for week in weeks for d in week]
    subtitle = "DEMO / synthetic contributions" if demo else f"{count:,} contributions · through {max(dates)}"
    treats = choose_treats(weeks)
    dog_h = FRAME_H * SCALE

    def stand_at(col: int, row: int) -> tuple[float, float]:
        """Group origin that puts the eating mouth on the centre of a tile."""
        cx, cy = LEFT + col * PITCH + TILE / 2, TOP + row * PITCH + TILE / 2
        return cx - MOUTH[0] * SCALE, cy - MOUTH[1] * SCALE

    def lane(row: float) -> float:
        """Group y that puts the paws on a given grid row (rows may be fractional)."""
        return TOP + row * PITCH + TILE - dog_h + 2

    tl = Timeline(-FRAME_W * SCALE - 8, lane(3))
    tl.pose("stand", 0.2)
    scenes = []
    for i, (col, row) in enumerate(treats):
        gx, gy = stand_at(col, row)
        # Wander through another row on the way so the route is not a straight line.
        tl.walk((tl.x + gx) / 2, lane(5.2 if i % 2 == 0 else 0.6))
        tl.walk(gx, gy)
        sniff = tl.pose("sniff", 1.0)
        dig = tl.pose("dig", 1.2)
        eat = tl.pose("eat", 1.2)
        tl.pose("stand", 0.25)
        scenes.append({"col": col, "row": row, "sniff": sniff, "dig": dig, "eat": eat})
    tl.walk(min(width - FRAME_W * SCALE - 6, tl.x + 70), lane(3))
    sit = tl.pose("sit", 3.4)
    duration = tl.t + 0.4
    tl.keys.append((duration, tl.x, tl.y))
    tl.shown["sit0"].append((sit[1], duration))

    esc = html.escape
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg"',
        f' width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"',
        f' aria-label="Pepper the Shiba Inu exploring {esc(username)}\'s GitHub contribution garden">',
        f"<title>Pepper's Harvest — {esc(username)}</title>",
        f"<desc>{esc(subtitle)}. Pepper sniffs out {len(treats)} treats among contribution days.</desc>",
        f'<rect width="{width}" height="{height}" rx="12" fill="{p["background"]}"/>',
        f'<text x="{LEFT}" y="24" font-family="Arial,sans-serif" font-size="13" font-weight="bold" fill="{p["text"]}">Pepper\'s Harvest</text>',
        f'<text x="{width - LEFT}" y="23" text-anchor="end" font-family="Arial,sans-serif" font-size="10" fill="{p["muted"]}">{esc(username)}</text>',
        f'<text x="{LEFT}" y="{height - 13}" font-family="Arial,sans-serif" font-size="10" fill="{p["muted"]}">{esc(subtitle)}</text>',
    ]
    for col, week in enumerate(weeks):
        x = LEFT + col * PITCH
        for row, day in enumerate(week[:7]):
            y = TOP + row * PITCH
            level = LEVELS.get(day.get("contributionLevel", "NONE"), 0)
            parts.append(f'<rect x="{x}" y="{y}" width="{TILE}" height="{TILE}" rx="1.5" fill="{p["grass"][level]}"/>')
            if level >= 3:
                parts.append(f'<path d="M{x + 5} {y + 8} l-2 -3 M{x + 5} {y + 8} l0 -5 M{x + 5} {y + 8} l2 -3" '
                             f'stroke="{p["blades"][level]}" stroke-width=".8" fill="none" stroke-linecap="round"/>')

    # Only the chosen tiles react. Pepper digs a hole, dirt flies back past his
    # paws and piles up beside it; after he eats, the hole fills and grass sprouts.
    flying = []  # dirt clods, drawn over Pepper so they are not hidden by his body
    for s in scenes:
        x, y = LEFT + s["col"] * PITCH, TOP + s["row"] * PITCH
        (s0, _), (d0, d1), (e0, e1) = s["sniff"], s["dig"], s["eat"]
        parts.append(f'<rect class="event" x="{x - 1}" y="{y - 1}" width="{TILE + 2}" height="{TILE + 2}" rx="2" '
                     f'fill="none" stroke="{p["ring"]}" stroke-width="1.4" opacity="0">'
                     + svg_anim_visibility([(s0, d1)], duration) + "</rect>")
        parts.append(f'<rect x="{x}" y="{y}" width="{TILE}" height="{TILE}" rx="1.5" fill="{p["soil"]}" opacity="0">'
                     + ramp([(d0, 0), (d0 + .4, 1), (e1 + 3.2, 1), (e1 + 4.6, 0)], duration) + "</rect>")
        parts.append(f'<rect x="{x + 2}" y="{y + 3}" width="{TILE - 4}" height="{TILE - 5}" rx="1.5" fill="{p["pit"]}" opacity="0">'
                     + ramp([(d0 + .3, 0), (d1, 1), (e1 + 2.2, 1), (e1 + 3.2, 0)], duration) + "</rect>")
        for i, (mx, my, mw, mh) in enumerate([(-4, 6, 4, 3), (-3, 4, 2, 2), (-6, 8, 3, 2)]):
            parts.append(f'<rect x="{x + mx}" y="{y + my}" width="{mw}" height="{mh}" rx=".8" fill="{p["soil"]}" opacity="0">'
                         + ramp([(d0 + .3 + i * .25, 0), (d0 + .5 + i * .25, 1), (e1 + 2.4, 1), (e1 + 3.4, 0)], duration) + "</rect>")
        # Clods land ahead of the nose and behind the front paws, where the grass shows them.
        clods = [(9, -8), (-12, 9), (14, -3), (-18, 11), (6, -12), (-8, 12), (17, -9), (-15, 7), (11, -14)]
        for i, (dx, dy) in enumerate(clods):
            t = d0 + 0.05 + i * 0.12
            flying.append(f'<rect x="{x + 3}" y="{y + 3}" width="3.4" height="3.4" rx=".8" fill="{p["clod"]}" opacity="0">'
                         + fade(t, t + 0.04, t + 0.55, 1, duration)
                         + f'<animateTransform attributeName="transform" type="translate" '
                           f'values="0 0;0 0;{dx / 2} {dy - 12};{dx} {dy};{dx} {dy}" '
                           f'keyTimes="0;{key(t, duration)};{key(t + .25, duration)};{key(t + .5, duration)};1" '
                           f'dur="{fmt(duration)}s" repeatCount="indefinite"/></rect>')
        sprout = (f'<path d="M{x + 5} {y + 8} l0 -3 M{x + 5} {y + 6} l-2 -2 M{x + 5} {y + 6} l2 -1.5" '
                  f'stroke="{p["blades"][2]}" stroke-width="1.1" stroke-linecap="round" fill="none" opacity="0">')
        parts.append(sprout + ramp([(e1 + 2.6, 0), (e1 + 3.2, 1), (e1 + 4.2, 1), (e1 + 4.8, 0)], duration) + "</path>")
        # The treat pops out of the hole and is gone on the first bite, right where it lay.
        bx, by = x + TILE / 2, y + TILE / 2
        rise, gone = d1 - 0.35, e0 + 0.3
        parts.append(f'<g opacity="0">{bone_shape(bx, by)}'
                     + svg_anim_visibility([(rise, gone)], duration)
                     + '<animateTransform attributeName="transform" type="translate" '
                       f'values="0 3;0 3;0 -2;0 -2;0 0" '
                       f'keyTimes="0;{key(rise, duration)};{key(rise + .25, duration)};{key(e0, duration)};1" '
                       f'dur="{fmt(duration)}s" repeatCount="indefinite"/></g>')

    # Paw prints where the front paws land; each fades after PRINT_LIFE seconds.
    feet = dog_h - 1
    for t, gx, gy, side in tl.contacts:
        px, py = gx + PAW_X * SCALE + (3 if side else -3), gy + feet + (1.5 if side else -0.5)
        parts.append(f'<g opacity="0">{paw_print(px, py, p["foot"])}'
                     + fade(t, t + 0.08, min(t + PRINT_LIFE, duration - 0.01), 0.75, duration) + "</g>")

    keytimes = ";".join(key(t, duration) for t, _, _ in tl.keys)
    xy = ";".join(f"{fmt(x)} {fmt(y)}" for _, x, y in tl.keys)
    parts.append('<g id="pepper">')
    parts.append(f'<animateTransform attributeName="transform" type="translate" values="{xy}" '
                 f'keyTimes="{keytimes}" calcMode="linear" dur="{fmt(duration)}s" repeatCount="indefinite"/>')
    parts.append(f'<ellipse cx="{fmt(32 * SCALE)}" cy="{fmt(feet)}" rx="{fmt(28 * SCALE)}" ry="2.6" '
                 f'fill="{p["shadow"]}" opacity=".22"/>')
    for name in FRAMES:
        parts.append(f'<image width="{fmt(FRAME_W * SCALE)}" height="{fmt(dog_h)}" '
                     f'style="image-rendering:pixelated" href="{sprite_data(assets_dir / "frames" / (name + ".png"))}" opacity="0">'
                     + svg_anim_visibility(tl.shown[name], duration) + "</image>")
    parts.append("</g>")
    parts.extend(flying)
    parts.append("</svg>")
    svg = "\n".join(parts) + "\n"
    ET.fromstring(svg)
    return svg


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Pepper's Harvest SVGs for a GitHub profile")
    parser.add_argument("--username", default="NaNIsaac")
    parser.add_argument("--output-dir", default="assets/pepper")
    parser.add_argument("--demo", action="store_true", help="synthetic data for local preview only")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    assets = root / "assets" / "pepper"
    output_dir = Path(args.output_dir).resolve()
    weeks = demo_contributions() if args.demo else fetch_contributions(args.username, os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or "")
    # Render both to memory first so an API/malformed XML problem cannot write half an update.
    rendered = {theme: make_svg(weeks, theme=theme, username=args.username, assets_dir=assets, demo=args.demo) for theme in PALETTES}
    output_dir.mkdir(parents=True, exist_ok=True)
    for theme, svg in rendered.items():
        path = output_dir / f"pepper-harvest-{theme}.svg"
        path.write_text(svg, encoding="utf-8")
        print(f"Generated {path} ({len(svg):,} bytes)")


if __name__ == "__main__":
    main()
