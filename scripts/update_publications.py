"""Build the final publication JSON used by the website."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable

try:
    from publication_pipeline import (
        DEFAULT_CACHE_PATH,
        DEFAULT_OUTPUT_PATH,
        DEFAULT_OVERRIDES_PATH,
        cite_with_manubot,
        load_json_data,
        load_publication_overrides,
        merge_publications,
        write_json_data,
    )
    from scrape_scholar import DEFAULT_PROFILE_URL, fetch_publications
except ImportError:
    from scripts.publication_pipeline import (
        DEFAULT_CACHE_PATH,
        DEFAULT_OUTPUT_PATH,
        DEFAULT_OVERRIDES_PATH,
        cite_with_manubot,
        load_json_data,
        load_publication_overrides,
        merge_publications,
        write_json_data,
    )
    from scripts.scrape_scholar import DEFAULT_PROFILE_URL, fetch_publications

Fetcher = Callable[..., list[dict]]


def update_publications(
    fetcher: Fetcher = fetch_publications,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
    overrides_path: str | Path = DEFAULT_OVERRIDES_PATH,
    cache_path: str | Path = DEFAULT_CACHE_PATH,
    profile_url: str = DEFAULT_PROFILE_URL,
    min_year: int = 2015,
    enrich: bool = True,
) -> list[dict]:
    raw_publications = fetcher(profile_url=profile_url, min_year=min_year)
    overrides = load_publication_overrides(overrides_path)
    citation_cache = load_json_data(cache_path, default={})
    citation_lookup = cite_with_manubot if enrich else None

    publications = merge_publications(
        raw_publications,
        overrides,
        citation_lookup=citation_lookup,
        citation_cache=citation_cache,
    )

    write_json_data(output_path, publications)
    if citation_cache:
        write_json_data(cache_path, citation_cache)

    return publications


def main() -> int:
    parser = argparse.ArgumentParser(description="Update HARCO publication data.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--overrides", default=str(DEFAULT_OVERRIDES_PATH))
    parser.add_argument("--cache", default=str(DEFAULT_CACHE_PATH))
    parser.add_argument("--profile-url", default=DEFAULT_PROFILE_URL)
    parser.add_argument("--min-year", type=int, default=2015)
    parser.add_argument("--no-enrich", action="store_true", help="Skip Manubot DOI metadata enrichment.")
    args = parser.parse_args()

    publications = update_publications(
        output_path=args.output,
        overrides_path=args.overrides,
        cache_path=args.cache,
        profile_url=args.profile_url,
        min_year=args.min_year,
        enrich=not args.no_enrich,
    )

    print(f"Saved {len(publications)} publications to {args.output}")
    if publications:
        print("Latest publications:")
        for publication in publications[:3]:
            print(f"- {publication['year']} {publication['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
