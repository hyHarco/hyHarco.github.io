"""Merge fetched publications with manual overrides and citation metadata."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any, Callable

DEFAULT_OUTPUT_PATH = Path("publication/publications.json")
DEFAULT_OVERRIDES_PATH = Path("_data/publication_overrides.yaml")
DEFAULT_CACHE_PATH = Path("_data/publication_metadata_cache.json")

CONTROL_FIELDS = {"match_title", "source", "id", "add"}
CONFERENCE_KEYWORDS = (
    "conference",
    "proceedings",
    "symposium",
    "workshop",
    "icra",
    "iros",
    "iccas",
    "humanoids",
    "icorr",
    "biorob",
    "ur,",
)

CitationLookup = Callable[[str], dict[str, Any]]


def normalize_title(title: Any) -> str:
    """Return a stable key for matching fetched titles to overrides."""
    return re.sub(r"\s+", " ", str(title or "").strip()).casefold()


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def parse_year(value: Any) -> int:
    if isinstance(value, int):
        return value

    match = re.search(r"\b(19|20)\d{2}\b", str(value or ""))
    return int(match.group(0)) if match else 0


def categorize_publication(venue: Any) -> str:
    venue_text = clean_text(venue).casefold()
    if any(keyword in venue_text for keyword in CONFERENCE_KEYWORDS):
        return "conference"
    return "journal"


def source_id_from_publication(publication: dict[str, Any]) -> str:
    source_id = clean_text(publication.get("id") or publication.get("source"))
    doi = clean_text(publication.get("doi"))

    if source_id:
        source_prefix = source_id.split(":", 1)[0].casefold()
        if source_prefix in {"doi", "url", "pmid", "pmcid", "arxiv"} and ":" in source_id:
            source_value = source_id.split(":", 1)[1]
            return f"{source_prefix}:{source_value}"
        if "doi.org/" in source_id:
            doi = source_id.split("doi.org/", 1)[1]
        else:
            return source_id

    if doi:
        doi = re.sub(r"^doi:\s*", "", doi, flags=re.IGNORECASE)
        doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)
        return f"doi:{doi}"

    return ""


def _citation_to_publication_fields(citation: dict[str, Any]) -> dict[str, Any]:
    fields: dict[str, Any] = {}

    title = clean_text(citation.get("title"))
    if title:
        fields["title"] = title

    authors = citation.get("authors")
    if isinstance(authors, list):
        author_text = ", ".join(clean_text(author) for author in authors if clean_text(author))
    else:
        author_text = clean_text(authors)
    if author_text:
        fields["authors"] = author_text

    publisher = clean_text(citation.get("publisher") or citation.get("journal"))
    if publisher:
        fields["journal"] = publisher

    year = parse_year(citation.get("date") or citation.get("year"))
    if year:
        fields["year"] = year

    link = clean_text(citation.get("link"))
    if link:
        fields["link"] = link

    return fields


def _public_fields(data: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in data.items() if key not in CONTROL_FIELDS and value not in (None, "")}


def _normalize_publication(publication: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(publication)
    normalized["title"] = clean_text(normalized.get("title"))
    normalized["authors"] = clean_text(normalized.get("authors"))
    normalized["year"] = parse_year(normalized.get("year"))
    normalized["journal"] = clean_text(normalized.get("journal"))
    normalized["link"] = clean_text(normalized.get("link"))
    normalized["category"] = clean_text(normalized.get("category")) or categorize_publication(normalized.get("journal"))
    return normalized


def _overrides_by_title(overrides: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_title = {}
    for override in overrides:
        key = normalize_title(override.get("match_title") or override.get("title"))
        if key:
            by_title[key] = override
    return by_title


def _lookup_citation(
    source_id: str,
    citation_lookup: CitationLookup | None,
    citation_cache: dict[str, Any],
) -> dict[str, Any]:
    if not source_id or citation_lookup is None:
        return {}

    if source_id in citation_cache:
        return citation_cache[source_id]

    try:
        citation = citation_lookup(source_id)
    except Exception as error:
        print(f"[WARN] Citation enrichment skipped for {source_id}: {error}")
        return {}

    citation_cache[source_id] = citation
    return citation


def merge_publications(
    publications: list[dict[str, Any]],
    overrides: list[dict[str, Any]],
    citation_lookup: CitationLookup | None = None,
    citation_cache: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return final site publications from fetched rows plus optional overrides."""
    cache = citation_cache if citation_cache is not None else {}
    overrides_by_title = _overrides_by_title(overrides)
    seen: set[str] = set()
    merged: list[dict[str, Any]] = []

    for raw_publication in publications:
        key = normalize_title(raw_publication.get("title"))
        if not key or key in seen:
            continue

        seen.add(key)
        base = _normalize_publication(raw_publication)
        override = overrides_by_title.get(key, {})
        lookup_base = {**base, **override}
        source_id = source_id_from_publication(lookup_base)
        citation_fields = _citation_to_publication_fields(_lookup_citation(source_id, citation_lookup, cache))

        final_publication = {
            **_public_fields(base),
            **citation_fields,
            **_public_fields(override),
        }

        if source_id.startswith("doi:") and not final_publication.get("doi"):
            final_publication["doi"] = source_id.removeprefix("doi:")

        final_publication = _normalize_publication(final_publication)
        if final_publication["title"] and final_publication["year"]:
            merged.append(final_publication)

    for override in overrides:
        if not override.get("add"):
            continue
        key = normalize_title(override.get("match_title") or override.get("title"))
        if not key or key in seen:
            continue
        seen.add(key)
        final_publication = _normalize_publication(_public_fields(override))
        if final_publication["title"] and final_publication["year"]:
            merged.append(final_publication)

    return sorted(merged, key=lambda publication: (-publication["year"], normalize_title(publication["title"])))


def cite_with_manubot(source_id: str) -> dict[str, Any]:
    result = subprocess.run(
        ["manubot", "cite", source_id, "--log-level=ERROR"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    citation = payload[0] if payload else {}

    authors = []
    for author in citation.get("author", []):
        given = clean_text(author.get("given"))
        family = clean_text(author.get("family"))
        authors.append(clean_text(f"{given} {family}"))

    date_parts = citation.get("issued", {}).get("date-parts", [[]])[0]
    date = "-".join(str(part) for part in date_parts) if date_parts else ""

    return {
        "title": citation.get("title", ""),
        "authors": authors,
        "publisher": citation.get("container-title") or citation.get("publisher") or citation.get("collection-title") or "",
        "date": date,
        "link": citation.get("URL", ""),
    }


def load_json_data(path: str | Path, default: Any) -> Any:
    data_path = Path(path)
    if not data_path.exists():
        return default
    return json.loads(data_path.read_text(encoding="utf-8"))


def write_json_data(path: str | Path, data: Any) -> None:
    data_path = Path(path)
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(json.dumps(data, ensure_ascii=False, indent=4) + "\n", encoding="utf-8")


def load_publication_overrides(path: str | Path = DEFAULT_OVERRIDES_PATH) -> list[dict[str, Any]]:
    overrides_path = Path(path)
    if not overrides_path.exists():
        return []

    try:
        import yaml
    except ImportError as error:
        raise RuntimeError("Install pyyaml to read publication overrides.") from error

    data = yaml.safe_load(overrides_path.read_text(encoding="utf-8")) or []
    if not isinstance(data, list):
        raise ValueError(f"{overrides_path} must contain a YAML list.")

    for entry in data:
        if not isinstance(entry, dict):
            raise ValueError(f"Every entry in {overrides_path} must be a mapping.")

    return data
