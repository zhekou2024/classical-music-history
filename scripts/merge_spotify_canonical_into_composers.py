#!/usr/bin/env python3
"""Merge data/spotify_canonical_map.json into each data/{composer}.json famousScores entry."""

from __future__ import annotations

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
MAP_PATH = os.path.join(DATA, "spotify_canonical_map.json")


def main() -> None:
    with open(MAP_PATH, encoding="utf-8") as f:
        m: dict[str, list[dict]] = json.load(f)

    for composer_id, entries in m.items():
        path = os.path.join(DATA, f"{composer_id}.json")
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        scores = data["famousScores"]
        if len(scores) != len(entries):
            raise SystemExit(f"{composer_id}: famousScores {len(scores)} != map {len(entries)}")
        for i, score in enumerate(scores):
            rec = entries[i]
            tid = rec["canonicalSpotifyTrackId"].strip()
            if len(tid) != 22:
                raise SystemExit(f"{composer_id}[{i}]: bad track id {tid!r}")
            score["canonicalPerformer"] = rec["canonicalPerformer"]
            score["canonicalAlbum"] = rec["canonicalAlbum"]
            score["canonicalTrackTitle"] = rec["canonicalTrackTitle"]
            score["canonicalSpotifyTrackId"] = tid
            score["canonicalSpotifyUrl"] = f"https://open.spotify.com/track/{tid}"
            score.pop("spotifyQuery", None)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("merged", composer_id)


if __name__ == "__main__":
    main()
