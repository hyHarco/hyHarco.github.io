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
    from fetch_openalex import fetch_publications as fetch_openalex_publications
    from scrape_scholar import DEFAULT_PROFILE_URL, fetch_publications as fetch_scholar_publications
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
    from scripts.fetch_openalex import fetch_publications as fetch_openalex_publications
    from scripts.scrape_scholar import DEFAULT_PROFILE_URL, fetch_publications as fetch_scholar_publications

Fetcher = Callable[..., list[dict]]
FETCHERS = {
    "openalex": fetch_openalex_publications,
    "scholar": fetch_scholar_publications,
}


def update_publications(
    fetcher: Fetcher | None = None,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
    overrides_path: str | Path = DEFAULT_OVERRIDES_PATH,
    cache_path: str | Path = DEFAULT_CACHE_PATH,
    profile_url: str = DEFAULT_PROFILE_URL,
    min_year: int = 2015,
    enrich: bool = True,
    source: str = "scholar",
    require_fetch_success: bool = False,
) -> list[dict]:
    if source not in FETCHERS:
        raise ValueError(f"Unknown publication source: {source}")

    selected_fetcher = fetcher or FETCHERS[source]
    existing_publications = load_json_data(output_path, default=[])

    try:
        fetched_publications = selected_fetcher(profile_url=profile_url, min_year=min_year)
    except Exception as error:
        existing_count = len(existing_publications) if isinstance(existing_publications, list) else 0
        if existing_count:
            if require_fetch_success:
                raise RuntimeError(f"Publication fetch failed: {error}") from error
            print(
                f"[WARN] Publication fetch failed with {error}; keeping existing output with "
                f"{existing_count} publications."
            )
            return existing_publications
        raise

    overrides = load_publication_overrides(overrides_path)
    citation_cache = load_json_data(cache_path, default={})
    citation_lookup = cite_with_manubot if enrich else None
    existing_publication_list = existing_publications if isinstance(existing_publications, list) else []
    raw_publications = fetched_publications + existing_publication_list

    if not fetched_publications and existing_publication_list and require_fetch_success:
        raise RuntimeError(
            "No publications were fetched from the selected source; existing publication data was preserved."
        )

    publications = merge_publications(
        raw_publications,
        overrides,
        citation_lookup=citation_lookup,
        citation_cache=citation_cache,
    )

    if not publications:
        raise RuntimeError(
            "No publications were generated and no existing publication data was available. "
            "Check the publication source fetch or parser before rerunning."
        )

    if not fetched_publications and existing_publication_list:
        print(
            "[WARN] No publications were fetched; keeping existing output with "
            f"{len(existing_publication_list)} publications."
        )

    write_json_data(output_path, publications)
    if citation_cache:
        write_json_data(cache_path, citation_cache)

    return publications


def main() -> int:
    parser = argparse.ArgumentParser(description="Update HARCO publication data.")
    parser.add_argument("--source", choices=sorted(FETCHERS), default="scholar")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--overrides", default=str(DEFAULT_OVERRIDES_PATH))
    parser.add_argument("--cache", default=str(DEFAULT_CACHE_PATH))
    parser.add_argument("--profile-url", default=DEFAULT_PROFILE_URL)
    parser.add_argument("--min-year", type=int, default=2015)
    parser.add_argument("--no-enrich", action="store_true", help="Skip Manubot DOI metadata enrichment.")
    parser.add_argument(
        "--require-fetch-success",
        action="store_true",
        help="Fail instead of silently preserving existing data when the selected source returns nothing.",
    )
    args = parser.parse_args()

    publications = update_publications(
        output_path=args.output,
        overrides_path=args.overrides,
        cache_path=args.cache,
        profile_url=args.profile_url,
        min_year=args.min_year,
        enrich=not args.no_enrich,
        source=args.source,
        require_fetch_success=args.require_fetch_success,
    )

    print(f"Publication data contains {len(publications)} publications at {args.output}")
    if publications:
        print("Latest publications:")
        for publication in publications[:3]:
            print(f"- {publication['year']} {publication['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
