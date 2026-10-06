"""Step 1: split every document in a bid package into numbered passages.

A passage id is "<file>:<line>", e.g. "02-spec-excerpts.md:4". Blank lines are skipped but keep
their numbers, so an id always points at the same line a person sees when they open the file.
"""
from pathlib import Path


def ingest(package_dir):
    passages = {}
    for path in sorted(Path(package_dir).iterdir()):
        if path.suffix not in (".txt", ".md"):
            continue
        for n, line in enumerate(path.read_text().splitlines(), start=1):
            if line.strip():
                passages[f"{path.name}:{n}"] = line.strip()
    return passages


def resolves(passages, cite):
    """A citation is real only if the passage exists and contains the quoted text."""
    text = passages.get(cite.get("id", ""))
    return bool(text) and bool(cite.get("quote")) and norm(cite["quote"]) in norm(text)


def norm(s):
    return " ".join(s.lower().split())
