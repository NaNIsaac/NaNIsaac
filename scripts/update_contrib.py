"""Rewrite the upstream-PR block of README.md from the stats snapshot.

The stats collector (NaNIsaac/stats) decides what counts as upstream: a pull request in a
repository outside the owner's account and organizations. This script only lists the newest
entries of its `pulls.elsewhere`, so the README, the homepage and the stats page agree.

    python scripts/update_contrib.py
"""

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

STATS = os.environ.get("STATS_URL", "https://nanisaac.github.io/stats/data/latest.json")
LIMIT = 8
README = Path(__file__).parents[1] / "README.md"


def upstream() -> list[dict]:
    with urllib.request.urlopen(STATS, timeout=60) as r:
        return json.load(r)["pulls"]["elsewhere"]


def line(pr: dict) -> str | None:
    if pr["state"] not in ("merged", "open"):
        return None
    return f"- `{pr['repo']}` [{pr['title']}]({pr['url']}) <sub>{pr['state']}</sub>"


def main() -> int:
    try:
        pulls = upstream()
    except (OSError, KeyError, ValueError) as e:
        # Yesterday's list stays in place; the next scheduled run tries again.
        print(f"stats snapshot not readable ({e}); README left as is", file=sys.stderr)
        return 0
    lines = [text for pr in pulls if (text := line(pr))][:LIMIT]
    lines.sort(key=lambda text: text.endswith("<sub>open</sub>"))  # merged first
    block = "\n".join(lines) or "- none yet"
    text = README.read_text(encoding="utf-8")
    new = re.sub(
        r"(<!-- contrib:start -->).*?(<!-- contrib:end -->)",
        lambda m: f"{m[1]}\n{block}\n{m[2]}",
        text,
        flags=re.DOTALL,
    )
    README.write_text(new, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
