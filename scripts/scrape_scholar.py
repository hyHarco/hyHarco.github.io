"""Fetch and parse publications from the HARCO Google Scholar profile."""

from __future__ import annotations

import argparse
import time
from html.parser import HTMLParser
from typing import Any

try:
    from publication_pipeline import categorize_publication, write_json_data
except ImportError:
    from scripts.publication_pipeline import categorize_publication, write_json_data

DEFAULT_PROFILE_URL = "https://scholar.google.com/citations?user=o7u_E8wAAAAJ&cstart={}&pagesize=100"
SCHOLAR_ORIGIN = "https://scholar.google.com"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/58.0.3029.110 Safari/537.3"
    )
}


def _class_names(attrs: list[tuple[str, str | None]]) -> set[str]:
    for key, value in attrs:
        if key == "class" and value:
            return set(value.split())
    return set()


def _attr(attrs: list[tuple[str, str | None]], name: str) -> str:
    for key, value in attrs:
        if key == name and value:
            return value
    return ""


class ScholarPublicationParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[dict[str, Any]] = []
        self._row: dict[str, Any] | None = None
        self._capture: str | None = None
        self._capture_tag: str | None = None
        self._buffer: list[str] = []
        self._title_cell_tag: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = _class_names(attrs)

        if tag == "tr" and "gsc_a_tr" in classes:
            self._row = {"title": "", "link": "", "gray": [], "year": ""}
            return

        if self._row is None or self._capture is not None:
            return

        if "gsc_a_t" in classes:
            self._title_cell_tag = tag
            return

        if "gsc_a_at" in classes:
            self._row["link"] = _attr(attrs, "href")
            self._start_capture("title", tag)
        elif self._title_cell_tag and tag == "span" and not self._row.get("title"):
            self._start_capture("title", tag)
        elif "gs_gray" in classes:
            self._start_capture("gray", tag)
        elif "gsc_a_y" in classes:
            self._start_capture("year", tag)

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._capture and tag == self._capture_tag:
            text = " ".join("".join(self._buffer).split())
            if self._capture == "gray":
                self._row["gray"].append(text)
            else:
                self._row[self._capture] = text
            self._capture = None
            self._capture_tag = None
            self._buffer = []
            return

        if tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None
            self._title_cell_tag = None
            return

        if self._title_cell_tag and tag == self._title_cell_tag:
            self._title_cell_tag = None

    def _start_capture(self, capture: str, tag: str) -> None:
        self._capture = capture
        self._capture_tag = tag
        self._buffer = []


def _absolute_scholar_url(href: str) -> str:
    if not href:
        return ""
    if href.startswith("http"):
        return href
    return f"{SCHOLAR_ORIGIN}{href}"


def parse_publication_rows(html: str, min_year: int = 2015) -> list[dict[str, Any]]:
    parser = ScholarPublicationParser()
    parser.feed(html)

    publications = []
    for row in parser.rows:
        title = row.get("title", "")
        gray_texts = row.get("gray", [])
        authors = gray_texts[0] if len(gray_texts) > 0 else ""
        journal = gray_texts[1] if len(gray_texts) > 1 else ""
        year_text = row.get("year", "")

        try:
            year = int(year_text)
        except (TypeError, ValueError):
            continue

        if year < min_year or not title or not authors or not journal:
            continue

        publications.append(
            {
                "title": title,
                "authors": authors,
                "year": year,
                "journal": journal,
                "link": _absolute_scholar_url(row.get("link", "")),
                "category": categorize_publication(journal),
            }
        )

    return publications


def fetch_publications(
    profile_url: str = DEFAULT_PROFILE_URL,
    min_year: int = 2015,
    page_size: int = 100,
    max_invalid_pages: int = 5,
) -> list[dict[str, Any]]:
    try:
        import requests
    except ImportError as error:
        raise RuntimeError("Install requests to fetch Google Scholar publications.") from error

    publications: list[dict[str, Any]] = []
    start = 0
    invalid_pages = 0

    while True:
        paginated_url = profile_url.format(start)
        response = requests.get(paginated_url, headers=HEADERS, timeout=30)

        if response.status_code == 429:
            print("Rate limit exceeded. Waiting for 60 seconds...")
            time.sleep(60)
            continue

        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            break

        page_publications = parse_publication_rows(response.text, min_year=min_year)
        if not page_publications:
            invalid_pages += 1
            print(f"No valid publications found on page {start // page_size + 1}.")
            if invalid_pages >= max_invalid_pages:
                print("Max invalid pages threshold reached. Stopping further requests.")
                break
        else:
            invalid_pages = 0
            publications.extend(page_publications)
            print(f"Added {len(page_publications)} publications from page {start // page_size + 1}.")

        start += page_size

    return sorted(publications, key=lambda publication: (-publication["year"], publication["title"].casefold()))


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrape HARCO publications from Google Scholar.")
    parser.add_argument("--output", default="publication/publications.json")
    parser.add_argument("--min-year", type=int, default=2015)
    parser.add_argument("--profile-url", default=DEFAULT_PROFILE_URL)
    args = parser.parse_args()

    publications = fetch_publications(profile_url=args.profile_url, min_year=args.min_year)
    write_json_data(args.output, publications)
    print(f"Data saved to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
