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


def make_svg(weeks: list[list[dict]], *, theme: str, username: str,
             assets_dir: Path, demo: bool = False) -> str:
    if not weeks or not any(weeks):
        raise ValueError("Contribution calendar returned no days; refusing to overwrite output")
    p = PALETTES[theme]
    gap = 3
    tile = 10
    pitch = tile + gap
    left = 24
    top = 45
    num_weeks = len(weeks)
    width = left * 2 + num_weeks * pitch - gap
    height = top + 7 * pitch + 28
    duration = "21s"
    count = sum(int(day["contributionCount"]) for week in weeks for day in week)
    valid_dates = [d["date"] for w in weeks for d in w]
    date_end = max(valid_dates)
    subtitle = "DEMO / synthetic contributions" if demo else f"{count:,} contributions · through {date_end}"
    dog_width, dog_height = 54, 53
    dog_top = top + 7 * pitch / 2 - dog_height / 2
    x_start = left - 37
    x_finish = left + (num_weeks - 1) * pitch - 17

    esc = html.escape
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"',
        f'     width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"',
        f'     aria-label="Pepper the Shiba Inu harvesting {esc(username)}\'s GitHub contributions">',
        f'<title>Pepper\'s Harvest — {esc(username)}</title>',
        f'<desc>Animated black-and-tan Shiba Inu walking across a GitHub contribution garden. {esc(subtitle)}.</desc>',
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="12" fill="{p["background"]}"/>',
        f'<text x="{left}" y="23" font-family="Arial,sans-serif" font-size="13" font-weight="bold" fill="{p["text"]}">Pepper\'s Harvest</text>',
        f'<text x="{width-left}" y="22" text-anchor="end" font-family="Arial,sans-serif" font-size="10" fill="{p["muted"]}">{esc(username)}</text>',
    ]

    # Draw a complete empty field first. Grass is a separate per-week overlay, so
    # mowing does not erase or distort the underlying GitHub grid.
    for col, week in enumerate(weeks):
        x = left + col * pitch
        for row, day in enumerate(week):
            y = top + row * pitch
            parts.append(f'<rect x="{x}" y="{y}" width="{tile}" height="{tile}" rx="1.5" fill="{p["empty"]}"/>')

    # 53 independent column animations, not 371 separate animated elements.
    for col, week in enumerate(weeks):
        x = left + col * pitch
        visit = 0.09 + 0.705 * ((col + .25) / num_weeks)
        gone = visit + 0.014
        parts.append('<g>')
        for row, day in enumerate(week):
            if row > 6:
                continue
            level = LEVELS.get(day["contributionLevel"], 0)
            y = top + row * pitch
            parts.append(f'<rect x="{x}" y="{y}" width="{tile}" height="{tile}" rx="1.5" fill="{p["grass"][level]}"/>')
            if level >= 2:
                blade = p["blades"][level]
                # Small grass blades: recognizable at README size, without visual clutter.
                parts.append(f'<path d="M{x+5} {y+8} l-2 -3 M{x+5} {y+8} l0 -5 M{x+5} {y+8} l2 -3" stroke="{blade}" stroke-width=".8" fill="none" stroke-linecap="round"/>')
        parts.append(f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;{fmt(visit)};{fmt(gone)};.92;1" dur="{duration}" repeatCount="indefinite"/>')
        parts.append('</g>')

    # Sprite pixels come from the approved black-and-tan Shiba Inu concept art.
    walk_a = sprite_data(assets_dir / "walk_a.png")
    walk_b = sprite_data(assets_dir / "walk_b.png")
    sit = sprite_data(assets_dir / "sit.png")
    parts += [
        f'<g opacity="0" transform="translate({x_start} {fmt(dog_top)})">',
        f'<animateTransform attributeName="transform" type="translate" values="{x_start} {fmt(dog_top)};{x_start} {fmt(dog_top)};{x_finish} {fmt(dog_top)};{x_finish} {fmt(dog_top)};{x_start} {fmt(dog_top)}" keyTimes="0;.08;.8;.86;1" dur="{duration}" repeatCount="indefinite"/>',
        f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.08;.79;.83;1" dur="{duration}" repeatCount="indefinite"/>',
        f'<image x="0" y="0" width="{dog_width}" height="{dog_height}" preserveAspectRatio="xMidYMax meet" href="{walk_a}">',
        '<animate attributeName="opacity" values="1;0;1" keyTimes="0;.5;1" calcMode="discrete" dur=".4s" repeatCount="indefinite"/></image>',
        f'<image x="0" y="0" width="{dog_width}" height="{dog_height}" preserveAspectRatio="xMidYMax meet" href="{walk_b}">',
        '<animate attributeName="opacity" values="0;1;0" keyTimes="0;.5;1" calcMode="discrete" dur=".4s" repeatCount="indefinite"/></image>',
        '</g>',
        f'<image x="{x_finish}" y="{fmt(dog_top)}" width="{dog_width}" height="{dog_height}" preserveAspectRatio="xMidYMax meet" href="{sit}" opacity="1">',
        f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.82;.87;.95;1" dur="{duration}" repeatCount="indefinite"/></image>',
        f'<text x="{left}" y="{height-14}" font-family="Arial,sans-serif" font-size="10" fill="{p["muted"]}">{esc(subtitle)}</text>',
        f'<text x="{width-left}" y="{height-14}" text-anchor="end" font-family="Arial,sans-serif" font-size="10" fill="{p["muted"]}">Harvest repeats every 21 seconds</text>',
        '</svg>',
    ]
    result = '\n'.join(parts) + '\n'
    ET.fromstring(result)  # Fail before touching the output if XML is invalid.
    return result


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
