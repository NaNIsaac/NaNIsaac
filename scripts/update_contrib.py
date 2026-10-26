"""Rewrite the pull-request blocks of README.md from the GitHub search API.

Two blocks: the newest pull requests in the NaNIsaac Research organization, and pull requests
merged by third-party projects. The second block, heading included, is written only when such a
merge exists, so the profile never presents the owner's own organization as upstream work.
"""

import json
import os
import re
import urllib.request
from pathlib import Path

USER = "NaNIsaac"
ORG = "NaNIsaac-Research"
# Not contributions to the owner's field: a first-commit exercise, a branch-only PR, a prompt gallery.
SKIP = {"M1zz/TheFirstCommit", "center4upt/XFEL_data", "Q07K/prompt-gallery"}
LIMIT = 8
README = Path(__file__).parents[1] / "README.md"


def search(query: str) -> list[dict]:
    req = urllib.request.Request(
        f"https://api.github.com/search/issues?q={query}&sort=created&per_page=100",
        headers={"Accept": "application/vnd.github+json"},
    )
    if token := os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as r:
        return json.load(r)["items"]


def state(pr: dict) -> str | None:
    if pr["pull_request"].get("merged_at"):
        return "merged"
    return "open" if pr["state"] == "open" else None


def repo(pr: dict) -> str:
    return pr["repository_url"].removeprefix("https://api.github.com/repos/")


def line(pr: dict) -> str:
    return f"- `{repo(pr)}` [{pr['title']}]({pr['html_url']}) <sub>{state(pr)}</sub>"


def research_block(prs: list[dict]) -> str:
    shown = [pr for pr in prs if state(pr)][:LIMIT]
    # Merged first, newest first within each.
    shown.sort(key=lambda pr: state(pr) == "open")
    lines = "\n".join(map(line, shown)) or "- none yet"
    return f"### Research organization\n\n{lines}"


def upstream_block(prs: list[dict]) -> str:
    merged = [pr for pr in prs if state(pr) == "merged" and repo(pr) not in SKIP]
    merged = merged[:LIMIT]
    if not merged:
        return ""
    return "### Upstream\n\n" + "\n".join(map(line, merged))


def fill(text: str, name: str, block: str) -> str:
    return re.sub(
        rf"(<!-- {name}:start -->).*?(<!-- {name}:end -->)",
        lambda m: f"{m[1]}\n{block}\n{m[2]}" if block else f"{m[1]}\n{m[2]}",
        text,
        flags=re.DOTALL,
    )


def main() -> None:
    research = search(f"author:{USER}+type:pr+org:{ORG}")
    # A separate query, so a busy organization cannot push outside work out of the results.
    outside = search(f"author:{USER}+type:pr+-user:{USER}+-org:{ORG}")
    text = README.read_text(encoding="utf-8")
    text = fill(text, "research", research_block(research))
    text = fill(text, "upstream", upstream_block(outside))
    README.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
