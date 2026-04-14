#!/usr/bin/env python3
"""Build data/spotify_canonical_map.json from data/*.json famousScores + spotifyQuery."""

from __future__ import annotations

import html as html_lib
import json
import os
import re
import subprocess
import time
import urllib.parse
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "spotify_canonical_map.json")

ORDER = [
    "josquin",
    "palestrina",
    "lasso",
    "byrd",
    "monteverdi",
    "pachelbel",
    "vivaldi",
    "bach",
    "handel",
    "haydn",
    "clementi",
    "mozart",
    "beethoven",
    "schumann",
    "chopin",
    "liszt",
    "wagner",
    "brahms",
    "tchaikovsky",
    "faure",
    "debussy",
    "satie",
    "ravel",
    "schoenberg",
    "bartok",
    "stravinsky",
    "shostakovich",
    "glass",
]

TRACK_RE = re.compile(r"open\.spotify\.com/track/([0-9A-Za-z]{22})")
OG_TITLE = re.compile(r'<meta\s+property="og:title"\s+content="([^"]*)"')
MUSIC_ALBUM = re.compile(
    r'<meta\s+name="music:album"\s+content="https://open\.spotify\.com/album/([0-9A-Za-z]{22})"'
)
DESC_ARTIST = re.compile(
    r'Listen to .+? on Spotify\. Song · (.+?) · \d{4}', re.DOTALL
)


def curl(url: str) -> str:
    return subprocess.check_output(
        ["curl", "-sL", "-A", "Mozilla/5.0", url],
        text=True,
        timeout=60,
    )


def brave_track_ids(query: str, limit: int = 12) -> list[str]:
    q = urllib.parse.quote(query)
    url = f"https://search.brave.com/search?q={q}"
    body = curl(url)
    found = TRACK_RE.findall(body)
    out: list[str] = []
    seen: set[str] = set()
    for tid in found:
        if tid in seen:
            continue
        seen.add(tid)
        out.append(tid)
        if len(out) >= limit:
            break
    return out


def parse_track_page(page: str) -> tuple[str, str, str | None]:
    m = OG_TITLE.search(page)
    if not m:
        raise ValueError("missing og:title on track page")
    track_title = html_lib.unescape(m.group(1))
    m2 = DESC_ARTIST.search(page)
    performer = html_lib.unescape(m2.group(1).strip()) if m2 else ""
    m3 = MUSIC_ALBUM.search(page)
    album_id = m3.group(1) if m3 else None
    return track_title, performer, album_id


def parse_album_title(page: str) -> str:
    m = OG_TITLE.search(page)
    if not m:
        raise ValueError("missing og:title on album page")
    raw = html_lib.unescape(m.group(1))
    raw = raw.replace(" | Spotify", "").strip()
    if " - Album by " in raw:
        raw = raw.split(" - Album by ", 1)[0].strip()
    return raw


def resolve_track(spotify_query: str) -> dict[str, Any]:
    queries = [
        spotify_query + " open.spotify.com/track",
        spotify_query + " spotify track",
        spotify_query,
    ]
    last_err: Exception | None = None
    for q in queries:
        time.sleep(0.35)
        ids = brave_track_ids(q)
        for tid in ids:
            try:
                time.sleep(0.22)
                tp = curl(f"https://open.spotify.com/track/{tid}")
                track_title, performer, album_id = parse_track_page(tp)
                album_name = ""
                if album_id:
                    time.sleep(0.22)
                    ap = curl(f"https://open.spotify.com/album/{album_id}")
                    album_name = parse_album_title(ap)
                if not performer:
                    performer = "Unknown Artist"
                if not album_name:
                    album_name = "Unknown Album"
                return {
                    "canonicalPerformer": performer,
                    "canonicalAlbum": album_name,
                    "canonicalTrackTitle": track_title,
                    "canonicalSpotifyTrackId": tid,
                }
            except Exception as e:
                last_err = e
                continue
        last_err = last_err or RuntimeError(f"no ids for query {q!r}")
    raise RuntimeError(f"could not resolve {spotify_query!r}: {last_err}")


def main() -> None:
    result: dict[str, list[dict[str, Any]]] = {}
    for comp in ORDER:
        path = os.path.join(DATA, f"{comp}.json")
        data = json.load(open(path, encoding="utf-8"))
        rows: list[dict[str, Any]] = []
        for fs in data["famousScores"]:
            q = fs["spotifyQuery"]
            print(comp, "->", q[:70], flush=True)
            rows.append(resolve_track(q))
        result[comp] = rows
        with open(OUT + ".partial", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            f.write("\n")

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
