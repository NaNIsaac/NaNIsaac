"""Rewrite the upstream-PR block of README.md from the GitHub search API."""

import json
import os
import re
import urllib.request
from pathlib import Path

USER = "NaNIsaac"
SKIP = {"M1zz/TheFirstCommit", "center4upt/XFEL_data"}  # not real contributions
LIMIT = 8
README = Path(__file__).parents[1] / "README.md"


def search() -> list[dict]:
    q = f"author:{USER}+type:pr+-user:{USER}"
    req = urllib.request.Request(
        f"https://api.github.com/search/issues?q={q}&sort=created&per_page=50",
        headers={"Accept": "application/vnd.github+json"},
    )
    if token := os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as r:
        return json.load(r)["items"]


def line(pr: dict) -> str | None:
    repo = pr["repository_url"].removeprefix("https://api.github.com/repos/")
    if repo in SKIP:
        return None
    if pr["pull_request"].get("merged_at"):
        state = "merged"
    elif pr["state"] == "open":
        state = "open"
    else:
        return None
    return f"- [{repo}](https://github.com/{repo}) · [{pr['title']}]({pr['html_url']}) · {state}"


def main() -> None:
    lines = [l for pr in search() if (l := line(pr))][:LIMIT]
    block = "\n".join(lines) or "- none yet"
    text = README.read_text(encoding="utf-8")
    new = re.sub(
        r"(<!-- contrib:start -->).*?(<!-- contrib:end -->)",
        lambda m: f"{m[1]}\n{block}\n{m[2]}",
        text,
        flags=re.S,
    )
    README.write_text(new, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
