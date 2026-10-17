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
        "foot": "#807467",
    },
    "dark": {
        "background": "#0d1117", "text": "#e6edf3", "muted": "#9aa7aa",
        "empty": "#18221e", "grass": ["#18221e", "#133d2a", "#18683c", "#29954d", "#49c16e"],
        "blades": ["#314c3a", "#277e49", "#34a35c", "#54d77c", "#8bea9e"],
        "foot": "#b1a08d",
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
    return format(num, ".4f").rstrip("0").rstrip(".")


def choose_treats(weeks: list[list[dict]]) -> list[tuple[int, int]]:
    """Choose a few real nonzero contribution days spaced across the calendar.

    A sparse profile may have fewer than four treats. Never invent activity.
    """
    candidates = []
    for col, week in enumerate(weeks):
        for row, day in enumerate(week[:7]):
            count = int(day.get("contributionCount", 0))
            if count > 0 and 1 <= row <= 5:
                candidates.append((col, row, count))
    if not candidates:
        return []
    # Four evenly spaced chapters make the story legible in the narrow README.
    results = []
    for lo, hi in [(4, 15), (17, 28), (30, 41), (43, len(weeks))]:
        region = [(c, r, n) for c, r, n in candidates if lo <= c < hi]
        if not region:
            continue
        target = (lo + hi - 1) / 2
        col, row, _ = max(region, key=lambda v: (v[2], -abs(v[0] - target), -abs(v[1] - 3)))
        results.append((col, row))
    return results


def svg_anim_visibility(intervals: list[tuple[float, float]], duration: float) -> str:
    """Discrete opacity switches that repeat and work inside an SVG <img>."""
    if not intervals:
        return ''
    times = {0.0, duration}
    for a, b in intervals:
        times.update((a, b))
    ordered = sorted(times)
    # At an exact boundary, the newest phase wins.
    def state(t):
        return '1' if any(a <= t < b for a, b in intervals) else '0'
    values = ';'.join(state(t) for t in ordered)
    keytimes = ';'.join(fmt(t / duration) for t in ordered)
    return (f'<animate attributeName="opacity" values="{values}" '
            f'keyTimes="{keytimes}" calcMode="discrete" '
            f'dur="{fmt(duration)}s" repeatCount="indefinite"/>')


def bone_shape(x: float, y: float, color: str = '#f3d39c') -> str:
    """Tiny geometric dog treat, deliberately not an emoji/font glyph."""
    return (f'<g transform="translate({fmt(x)} {fmt(y)})" '
            f'fill="{color}" stroke="#7c583b" stroke-width="1">'
            '<path d="M-6 -1 Q-11 -6 -12 -2 Q-13 1 -9 2 Q-13 5 -9 7 Q-6 9 -4 5 '
            'L5 -4 Q9 -7 10 -3 Q12 1 8 2 Q12 5 8 7 Q5 9 2 4 Z"/>'
            '</g>')


def make_svg(weeks: list[list[dict]], *, theme: str, username: str,
             assets_dir: Path, demo: bool = False) -> str:
    """A self-contained, animated SVG: walk / sniff / find / nibble / wag / sit.

    Grass remains readable. Only the few selected contribution days react.
    All sprite PNGs are embedded as data URIs; no external assets or JavaScript.
    """
    if not weeks or not any(weeks):
        raise ValueError('Contribution calendar returned no days; refusing to overwrite output')
    if theme not in PALETTES:
        raise ValueError(f'Unknown palette: {theme}')
    p = PALETTES[theme]
    pitch, tile, left, top = 13, 10, 24, 46
    width = left * 2 + len(weeks) * pitch - (pitch - tile)
    height = top + 7 * pitch + 33
    count = sum(int(d['contributionCount']) for week in weeks for d in week)
    dates = [d['date'] for week in weeks for d in week]
    subtitle = 'DEMO / synthetic contributions' if demo else f'{count:,} contributions · through {max(dates)}'
    treats = choose_treats(weeks)

    # A tiny hand-authored animation timeline. All times below are seconds.
    t = 0.0
    dogx, dogy = -35.0, 73.0
    position = [(0., dogx, dogy)]
    phases: dict[str, list[tuple[float, float]]] = {
        'walk': [], 'sniff': [], 'dig': [], 'munch': [], 'wag': [], 'sit': []
    }
    scenes = []
    t += .4
    position.append((t, dogx, dogy))
    for i, (col, row) in enumerate(treats):
        # The dog approaches from the left. Nose ends just beside the target tile.
        target_x = left + col * pitch - 50
        target_y = max(40, min(82, top + row * pitch - 25))
        travel = 2.35 if i == 0 else 2.8
        phases['walk'].append((t, t + travel))
        t += travel
        position.append((t, target_x, target_y))
        dogx, dogy = target_x, target_y
        intervals = {}
        for action, dt in [('sniff', .75), ('dig', .60), ('munch', .72), ('wag', .42)]:
            intervals[action] = (t, t + dt)
            phases[action].append((t, t + dt))
            t += dt
        position.append((t, dogx, dogy))
        scenes.append({'col': col, 'row': row, 'intervals': intervals,
                       'nose_x': dogx + 50, 'nose_y': dogy + 24})
    if treats:
        phases['sit'].append((t, t + 2.25))
        t += 2.25
    else:
        # On a profile with no contributions: Pepper only walks and sits.
        phases['walk'].append((t, t + 5))
        t += 5
        dogx, dogy = left + (len(weeks) - 3) * pitch, 70
        position.append((t, dogx, dogy))
        phases['sit'].append((t, t + 2.25))
        t += 2.25
    position.append((t, dogx, dogy))
    duration = t + .65  # short hold before looping back to the beginning
    position.append((duration, dogx, dogy))
    if phases['sit']:
        # Keep Pepper seated during the finale; don't leave an orphaned basket.
        phases['sit'][-1] = (phases['sit'][-1][0], duration)
    duration_s = f'{fmt(duration)}s'

    esc = html.escape
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"',
        f' width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"',
        f' aria-label="Pepper the Shiba Inu exploring {esc(username)}\'s GitHub contribution garden">',
        f'<title>Pepper\'s Harvest — {esc(username)}</title>',
        f'<desc>{esc(subtitle)}. Pepper sniffs out {len(treats)} treats among contribution days.</desc>',
        f'<rect width="{width}" height="{height}" rx="12" fill="{p["background"]}"/>',
        f'<text x="{left}" y="24" font-family="Arial,sans-serif" font-size="13" font-weight="bold" fill="{p["text"]}">Pepper\'s Harvest</text>',
        f'<text x="{width-left}" y="23" text-anchor="end" font-family="Arial,sans-serif" font-size="10" fill="{p["muted"]}">{esc(username)}</text>',
        f'<text x="{left}" y="{height-13}" font-family="Arial,sans-serif" font-size="10" fill="{p["muted"]}">{esc(subtitle)}</text>',
        f'<text x="{width-left}" y="{height-13}" text-anchor="end" font-family="Arial,sans-serif" font-size="10" fill="{p["muted"]}">sniff · find · nom!</text>',
        # Background grass is ALWAYS preserved (no moving opacity masks on columns).
    ]
    for col, week in enumerate(weeks):
        x = left + col * pitch
        for row, day in enumerate(week[:7]):
            y = top + row * pitch
            level = LEVELS.get(day.get('contributionLevel', 'NONE'), 0)
            parts.append(f'<rect x="{x}" y="{y}" width="{tile}" height="{tile}" rx="1.5" fill="{p["grass"][level]}"/>')
            if level >= 3:
                parts.append(f'<path d="M{x+5} {y+8} l-2 -3 M{x+5} {y+8} l0 -5 M{x+5} {y+8} l2 -3" stroke="{p["blades"][level]}" stroke-width=".8" fill="none" stroke-linecap="round"/>')

    # At most four selected events; never animate whole columns disappearing.
    for scene in scenes:
        col, row = scene['col'], scene['row']
        x, y = left + col * pitch, top + row * pitch
        a, b = scene['intervals']['dig']
        # The target tile pulses briefly; the underlying contributions are preserved.
        parts.append(f'<rect x="{x-1}" y="{y-1}" width="12" height="12" rx="2" fill="none" stroke="#e8b44b" stroke-width="1.8" opacity="0">'
                     + svg_anim_visibility([(scene['intervals']['sniff'][0], b)], duration) + '</rect>')
        found_start = b - .09
        found_end = scene['intervals']['munch'][1] - .12
        # The bone pops upward from this single day, then disappears when eaten.
        bone_x = x + 7
        bone_y = y - 10
        # During the "nom" phase, the treat moves from its tile to Pepper's
        # mouth. It disappears only as he eats it, rather than vanishing on a timer.
        mouth_dx = scene['nose_x'] - 19 - bone_x
        mouth_dy = scene['nose_y'] + 5 - bone_y
        fly_seconds = max(.2, found_end - found_start)
        parts.append(f'<g opacity="0">{bone_shape(bone_x, bone_y)}'
                     + svg_anim_visibility([(found_start, found_end)], duration)
                     + f'<animateTransform attributeName="transform" type="translate" '
                       f'values="0 3;{fmt(.25*mouth_dx)} {fmt(.2*mouth_dy)};{fmt(mouth_dx)} {fmt(mouth_dy)}" '
                       f'keyTimes="0;.3;1" '
                       f'begin="{fmt(found_start)}s" dur="{fmt(fly_seconds)}s" fill="freeze"/>'
                     + '</g>')
        # Short-lived dust puffs and little paw marks; no permanent visual clutter.
        da, db = scene['intervals']['dig']
        for dx, dy in [(-5, 8), (7, 13), (15, 6)]:
            parts.append(f'<circle cx="{x+dx}" cy="{y+dy}" r="2.4" fill="{p["foot"]}" opacity="0">'
                         + svg_anim_visibility([(da, min(db+.23, duration))], duration) + '</circle>')
        wa, wb = scene['intervals']['wag']
        parts.append(f'<text x="{x+5}" y="{y-18}" font-size="14" text-anchor="middle" opacity="0">✦'
                     + svg_anim_visibility([(wa, wb)], duration) + '</text>')

    # The dog is a single sprite group; all positional changes use SMIL.
    keytimes = ';'.join(fmt(pos[0] / duration) for pos in position)
    xy = ';'.join(f'{fmt(pos[1])} {fmt(pos[2])}' for pos in position)
    parts.append('<g id="pepper">')
    parts.append(f'<animateTransform attributeName="transform" type="translate" '
                 f'values="{xy}" keyTimes="{keytimes}" calcMode="linear" '
                 f'dur="{duration_s}" repeatCount="indefinite"/>')

    sprites = {k: sprite_data(assets_dir / (v+'.png')) for k, v in
               [('walk_a','walk_a'),('walk_b','walk_b'),('sniff','walk_b'),
                ('dig','walk_a'),('munch','idle'),('wag','idle'),('sit','sit')]}
    # First, walk_a / walk_b alternate via two nested frames.
    for name, initial, swing in [('walk_a','1','0;1;0'),('walk_b','0','1;0;1')]:
        parts.append(f'<g opacity="0">{svg_anim_visibility(phases["walk"],duration)}')
        parts.append(f'<image x="0" y="0" width="62" height="57" preserveAspectRatio="xMidYMax meet" href="{sprites[name]}" opacity="{initial}">')
        parts.append(f'<animate attributeName="opacity" values="{swing}" keyTimes="0;.5;1" '
                     f'calcMode="discrete" dur=".44s" repeatCount="indefinite"/>')
        parts.append('</image></g>')
    # Sniff: body dips and nose approaches the tile.
    parts.append(f'<g opacity="0">{svg_anim_visibility(phases["sniff"],duration)}')
    parts.append(f'<image x="0" y="4" width="62" height="57" transform="rotate(9 32 35)" '
                 f'preserveAspectRatio="xMidYMax meet" href="{sprites["sniff"]}"/>')
    parts.append('</g>')
    # Dig: a small pawing motion, distinct from the sniffing pose.
    parts.append(f'<g opacity="0">{svg_anim_visibility(phases["dig"],duration)}')
    parts.append(f'<image x="0" y="2" width="62" height="57" '
                 f'preserveAspectRatio="xMidYMax meet" href="{sprites["dig"]}">'
                 '<animate attributeName="y" values="2;6;2" keyTimes="0;.5;1" '
                 'dur=".3s" repeatCount="indefinite"/></image></g>')
    # Nom: a front-facing smile with tiny jaw bounce, rather than a disappearing column.
    parts.append(f'<g opacity="0">{svg_anim_visibility(phases["munch"],duration)}')
    parts.append(f'<image x="1" y="2" width="60" height="57" '
                 f'preserveAspectRatio="xMidYMax meet" href="{sprites["munch"]}">'
                 '<animate attributeName="y" values="2;5;2" keyTimes="0;.5;1" '
                 'dur=".27s" repeatCount="indefinite"/></image></g>')
    # Wag after discovery, and a seated finale.
    for action, img, px in [('wag',sprites['wag'],'1'), ('sit',sprites['sit'],'1')]:
        parts.append(f'<g opacity="0">{svg_anim_visibility(phases[action],duration)}')
        parts.append(f'<image x="{px}" y="0" width="60" height="57" preserveAspectRatio="xMidYMax meet" href="{img}"/>')
        if action == 'wag':
            parts.append('<path d="M47 26 Q65 14 58 31" stroke="#b58b55" '
                         'stroke-width="3" stroke-linecap="round" fill="none">'
                         '<animate attributeName="d" '
                         'values="M47 26 Q65 14 58 31;M47 26 Q65 27 58 32;M47 26 Q65 14 58 31" '
                         'dur=".25s" repeatCount="indefinite"/></path>')
        parts.append('</g>')
    # A tiny woven picnic basket clipped to Pepper's side. Intentionally subtle.
    parts.append('<g transform="translate(9 23)">'
                 '<path d="M0 0 Q2 -9 12 -8 L15 0" fill="none" stroke="#76502e" stroke-width="2"/>'
                 '<path d="M-1 0 L16 0 L13 12 L2 12 Z" fill="#bf9153" stroke="#64452d" stroke-width="1.1"/>'
                 '<path d="M0 4 L15 4 M1 8 L14 8 M4 0 L5 12 M10 0 L10 12" '
                 'stroke="#8e653f" stroke-width="1" fill="none"/></g>')
    parts.append('</g>')
    parts.append('</svg>')
    svg = '\n'.join(parts) + '\n'
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
