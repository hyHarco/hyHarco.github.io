"""Fetch publications from OpenAlex, the API-backed Scholar replacement."""

from __future__ import annotations

import html
import os
import re
from typing import Any

try:
    from publication_pipeline import categorize_publication, clean_text
except ImportError:
    from scripts.publication_pipeline import categorize_publication, clean_text

OPENALEX_WORKS_URL = "https://api.openalex.org/works"
DEFAULT_AUTHOR_IDS = ("A5101430480",)
DEFAULT_INSTITUTION_IDS = ("I4575257",)
DEFAULT_WORK_TYPES = ("article", "conference-paper")
DEFAULT_AFFILIATION_KEYWORDS = (
    "harco",
    "hanyang",
    "erica",
    "robotics",
    "mechatronics",
    "human-robot",
    "human robot",
)
SELECT_FIELDS = (
    "id",
    "doi",
    "display_name",
    "publication_year",
    "type",
    "is_retracted",
    "authorships",
    "primary_location",
)
SKIPPED_WORK_TYPES = {"retraction", "paratext"}


def _split_csv(value: str | None) -> list[str]:
    return [item.strip() for item in str(value or "").split(",") if item.strip()]


def _openalex_id(value: str) -> str:
    return clean_text(value).rstrip("/").rsplit("/", 1)[-1]


def _strip_markup(value: Any) -> str:
    return clean_text(re.sub(r"<[^>]+>", "", html.unescape(str(value or ""))))


def _doi_value(value: Any) -> str:
    doi = clean_text(value)
    doi = re.sub(r"^doi:\s*", "", doi, flags=re.IGNORECASE)
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)
    return doi


def _work_link(work: dict[str, Any], location: dict[str, Any], doi: str) -> str:
    landing_page_url = clean_text(location.get("landing_page_url"))
    if landing_page_url:
        return landing_page_url
    if doi:
        return f"https://doi.org/{doi}"
    return clean_text(work.get("id"))


def _work_venue(work: dict[str, Any], location: dict[str, Any]) -> str:
    source = location.get("source") if isinstance(location.get("source"), dict) else {}
    return (
        clean_text(location.get("raw_source_name"))
        or clean_text(source.get("display_name"))
        or clean_text(location.get("raw_type"))
        or clean_text(work.get("type"))
    )


def _work_category(work: dict[str, Any], location: dict[str, Any], venue: str) -> str:
    source = location.get("source") if isinstance(location.get("source"), dict) else {}
    work_type = clean_text(work.get("type")).casefold()
    source_type = clean_text(source.get("type")).casefold()
    raw_type = clean_text(location.get("raw_type")).casefold()

    if work_type == "conference-paper" or source_type == "conference" or "proceedings" in raw_type:
        return "conference"
    return categorize_publication(venue)


def _work_authors(work: dict[str, Any]) -> str:
    authors = []
    for authorship in work.get("authorships", []):
        if not isinstance(authorship, dict):
            continue
        author = authorship.get("author") if isinstance(authorship.get("author"), dict) else {}
        name = clean_text(authorship.get("raw_author_name")) or clean_text(author.get("display_name"))
        if name:
            authors.append(name)
    return ", ".join(authors)


def _authorship_institution_ids(authorship: dict[str, Any]) -> set[str]:
    institution_ids = set()
    for institution in authorship.get("institutions", []):
        if isinstance(institution, dict):
            institution_id = clean_text(institution.get("id"))
            if institution_id:
                institution_ids.add(_openalex_id(institution_id))
    return institution_ids


def _authorship_affiliation_text(authorship: dict[str, Any]) -> str:
    values = []
    for field in ("raw_affiliation_strings", "affiliations"):
        for item in authorship.get(field, []):
            if isinstance(item, dict):
                values.append(clean_text(item.get("raw_affiliation_string")))
            else:
                values.append(clean_text(item))
    return " ".join(value for value in values if value).casefold()


def work_matches_selected_author(
    work: dict[str, Any],
    author_ids: list[str] | tuple[str, ...],
    institution_ids: list[str] | tuple[str, ...],
    affiliation_keywords: list[str] | tuple[str, ...] = DEFAULT_AFFILIATION_KEYWORDS,
) -> bool:
    selected_author_ids = {_openalex_id(author_id) for author_id in author_ids}
    selected_institution_ids = {_openalex_id(institution_id) for institution_id in institution_ids}
    selected_keywords = tuple(keyword.casefold() for keyword in affiliation_keywords if keyword)

    for authorship in work.get("authorships", []):
        if not isinstance(authorship, dict):
            continue
        author = authorship.get("author") if isinstance(authorship.get("author"), dict) else {}
        author_id = _openalex_id(clean_text(author.get("id")))
        if author_id not in selected_author_ids:
            continue

        if not selected_institution_ids:
            return True

        if _authorship_institution_ids(authorship) & selected_institution_ids:
            return True

        affiliation_text = _authorship_affiliation_text(authorship)
        if affiliation_text and any(keyword in affiliation_text for keyword in selected_keywords):
            return True

    return False


def map_openalex_work_to_publication(work: dict[str, Any]) -> dict[str, Any] | None:
    work_type = clean_text(work.get("type")).casefold()
    title = _strip_markup(work.get("display_name"))
    year = int(work.get("publication_year") or 0)

    if work.get("is_retracted") or work_type in SKIPPED_WORK_TYPES or title.casefold().startswith("retraction"):
        return None

    location = work.get("primary_location") if isinstance(work.get("primary_location"), dict) else {}
    authors = _work_authors(work)
    venue = _work_venue(work, location)

    if not title or not year or not authors or not venue:
        return None

    doi = _doi_value(work.get("doi"))
    publication = {
        "title": title,
        "authors": authors,
        "year": year,
        "journal": venue,
        "link": _work_link(work, location, doi),
        "category": _work_category(work, location, venue),
    }
    if doi:
        publication["doi"] = doi
    return publication


def fetch_publications(
    profile_url: str | None = None,
    min_year: int = 2015,
    author_ids: list[str] | tuple[str, ...] | None = None,
    institution_ids: list[str] | tuple[str, ...] | None = None,
    affiliation_keywords: list[str] | tuple[str, ...] = DEFAULT_AFFILIATION_KEYWORDS,
    page_size: int = 100,
    api_url: str = OPENALEX_WORKS_URL,
) -> list[dict[str, Any]]:
    try:
        import requests
    except ImportError as error:
        raise RuntimeError("Install requests to fetch OpenAlex publications.") from error

    selected_author_ids = tuple(author_ids or _split_csv(os.getenv("OPENALEX_AUTHOR_IDS")) or DEFAULT_AUTHOR_IDS)
    selected_institution_ids = tuple(
        institution_ids if institution_ids is not None else _split_csv(os.getenv("OPENALEX_INSTITUTION_IDS")) or DEFAULT_INSTITUTION_IDS
    )

    filters = [
        f"authorships.author.id:{'|'.join(_openalex_id(author_id) for author_id in selected_author_ids)}",
        f"publication_year:>{min_year - 1}",
        f"type:{'|'.join(DEFAULT_WORK_TYPES)}",
    ]
    if selected_institution_ids:
        filters.append(
            "authorships.institutions.id:"
            + "|".join(_openalex_id(institution_id) for institution_id in selected_institution_ids)
        )

    params = {
        "filter": ",".join(filters),
        "sort": "publication_year:desc",
        "per_page": page_size,
        "cursor": "*",
        "select": ",".join(SELECT_FIELDS),
    }

    api_key = clean_text(os.getenv("OPENALEX_API_KEY"))
    mailto = clean_text(os.getenv("OPENALEX_MAILTO"))
    if api_key:
        params["api_key"] = api_key
    if mailto:
        params["mailto"] = mailto

    publications: list[dict[str, Any]] = []
    seen: set[str] = set()

    while True:
        response = requests.get(api_url, params=params, timeout=30)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to retrieve OpenAlex works. Status code: {response.status_code}")

        payload = response.json()
        for work in payload.get("results", []):
            if not work_matches_selected_author(work, selected_author_ids, selected_institution_ids, affiliation_keywords):
                continue
            publication = map_openalex_work_to_publication(work)
            if not publication:
                continue
            key = publication["title"].casefold()
            if key in seen:
                continue
            seen.add(key)
            publications.append(publication)

        next_cursor = payload.get("meta", {}).get("next_cursor")
        if not next_cursor:
            break
        params["cursor"] = next_cursor

    return sorted(publications, key=lambda publication: (-publication["year"], publication["title"].casefold()))
