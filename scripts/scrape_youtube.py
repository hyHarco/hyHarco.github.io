#!/usr/bin/env python3
"""Fetch latest videos from the HARCO Lab YouTube channel RSS feed and write to _data/youtube.json."""

import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

CHANNEL_ID = "UCsosxxmWD4mQdyjWRXQsuyA"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "_data" / "youtube.json"
LIMIT = 8

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


def fetch_feed(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8")


def parse_entries(xml_text: str):
    root = ET.fromstring(xml_text)
    entries = []
    for entry in root.findall("atom:entry", NS):
        video_id = entry.findtext("yt:videoId", default="", namespaces=NS)
        title = entry.findtext("atom:title", default="", namespaces=NS)
        published = entry.findtext("atom:published", default="", namespaces=NS)
        thumb_el = entry.find("media:group/media:thumbnail", NS)
        thumb_url = thumb_el.attrib.get("url") if thumb_el is not None else ""
        if not video_id:
            continue
        entries.append({
            "id": video_id,
            "title": title.strip(),
            "published": published,
            "date": published.split("T")[0] if published else "",
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "thumbnail": thumb_url or f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
        })
    return entries


def main():
    print(f"Fetching {FEED_URL}")
    xml_text = fetch_feed(FEED_URL)
    entries = parse_entries(xml_text)
    entries.sort(key=lambda e: e["published"], reverse=True)
    entries = entries[:LIMIT]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(entries)} videos to {OUTPUT_PATH}")


if __name__ == "__main__":
    sys.exit(main() or 0)
