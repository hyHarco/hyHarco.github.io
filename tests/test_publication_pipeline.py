import importlib
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path


class PublicationPipelineTest(unittest.TestCase):
    def test_scholar_scraper_import_does_not_request_network(self):
        sys.modules.pop("scripts.scrape_scholar", None)

        fake_requests = types.SimpleNamespace(
            get=lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("import should not fetch"))
        )
        previous_requests = sys.modules.get("requests")
        sys.modules["requests"] = fake_requests
        try:
            module = importlib.import_module("scripts.scrape_scholar")
        finally:
            if previous_requests is None:
                sys.modules.pop("requests", None)
            else:
                sys.modules["requests"] = previous_requests

        self.assertTrue(callable(module.fetch_publications))

    def test_scholar_html_rows_are_parsed_to_publications(self):
        from scripts.scrape_scholar import parse_publication_rows

        html = """
        <table>
          <tr class="gsc_a_tr">
            <td class="gsc_a_t">
              <a class="gsc_a_at" href="/citations?citation_for_view=abc">Conference Paper</a>
              <div class="gs_gray">A Author, B Author</div>
              <div class="gs_gray">2025 IEEE International Conference on Robotics, 1-6, 2025</div>
            </td>
            <td class="gsc_a_y"><span>2025</span></td>
          </tr>
          <tr class="gsc_a_tr">
            <td class="gsc_a_t">
              <a class="gsc_a_at" href="/citations?citation_for_view=old">Old Paper</a>
              <div class="gs_gray">A Author</div>
              <div class="gs_gray">Old Journal, 2014</div>
            </td>
            <td class="gsc_a_y"><span>2014</span></td>
          </tr>
        </table>
        """

        publications = parse_publication_rows(html, min_year=2015)

        self.assertEqual(
            publications,
            [
                {
                    "title": "Conference Paper",
                    "authors": "A Author, B Author",
                    "year": 2025,
                    "journal": "2025 IEEE International Conference on Robotics, 1-6, 2025",
                    "link": "https://scholar.google.com/citations?citation_for_view=abc",
                    "category": "conference",
                }
            ],
        )

    def test_scholar_parser_keeps_unlinked_title_rows(self):
        from scripts.scrape_scholar import parse_publication_rows

        html = """
        <table>
          <tr class="gsc_a_tr">
            <td class="gsc_a_t">
              <span>Unlinked Journal Paper</span>
              <div class="gs_gray">A Author</div>
              <div class="gs_gray">Robotics Journal, 2025</div>
            </td>
            <td class="gsc_a_y"><span>2025</span></td>
          </tr>
        </table>
        """

        publications = parse_publication_rows(html, min_year=2015)

        self.assertEqual(publications[0]["title"], "Unlinked Journal Paper")
        self.assertEqual(publications[0]["link"], "")

    def test_overrides_match_scholar_title_and_win_over_enrichment(self):
        from scripts.publication_pipeline import merge_publications

        scholar_publications = [
            {
                "title": "A Multi-Task Energy-Aware Impedance Controller",
                "authors": "S Choi, S Ha, W Kim",
                "year": 2024,
                "journal": "IEEE Robotics and Automation Letters, 2024",
                "link": "https://scholar.google.com/citations?view_op=view_citation&citation_for_view=x",
                "category": "journal",
            }
        ]
        overrides = [
            {
                "match_title": "A Multi-Task Energy-Aware Impedance Controller",
                "title": "A Multi-Task Energy-Aware Impedance Controller for Enhanced Safety in Physical Human-Robot Interaction",
                "doi": "10.1109/LRA.2024.1234567",
                "journal": "IEEE Robotics and Automation Letters",
                "link": "https://doi.org/10.1109/LRA.2024.1234567",
                "category": "journal",
            }
        ]

        enriched = merge_publications(
            scholar_publications,
            overrides,
            citation_lookup=lambda source_id: {
                "title": "Wrong title from metadata",
                "authors": ["S. Choi", "S. Ha", "W. Kim"],
                "publisher": "IEEE RA-L",
                "date": "2024-05-01",
                "link": "https://ieeexplore.ieee.org/document/1234567",
            },
        )

        self.assertEqual(
            enriched,
            [
                {
                    "title": "A Multi-Task Energy-Aware Impedance Controller for Enhanced Safety in Physical Human-Robot Interaction",
                    "authors": "S. Choi, S. Ha, W. Kim",
                    "year": 2024,
                    "journal": "IEEE Robotics and Automation Letters",
                    "link": "https://doi.org/10.1109/LRA.2024.1234567",
                    "category": "journal",
                    "doi": "10.1109/LRA.2024.1234567",
                }
            ],
        )

    def test_doi_source_ids_are_normalized_for_manubot(self):
        from scripts.publication_pipeline import source_id_from_publication

        self.assertEqual(
            source_id_from_publication({"id": "DOI:10.1109/LRA.2024.1234567"}),
            "doi:10.1109/LRA.2024.1234567",
        )
        self.assertEqual(
            source_id_from_publication({"doi": "https://doi.org/10.1109/LRA.2024.1234567"}),
            "doi:10.1109/LRA.2024.1234567",
        )

    def test_publications_are_deduplicated_and_sorted_by_year_then_title(self):
        from scripts.publication_pipeline import merge_publications

        scholar_publications = [
            {
                "title": "Beta Paper",
                "authors": "B Author",
                "year": 2024,
                "journal": "Conference on Robotics, 2024",
                "link": "https://example.com/beta",
                "category": "conference",
            },
            {
                "title": "Alpha Paper",
                "authors": "A Author",
                "year": 2025,
                "journal": "Robotics Journal, 2025",
                "link": "https://example.com/alpha",
                "category": "journal",
            },
            {
                "title": " beta   paper ",
                "authors": "B Author",
                "year": 2024,
                "journal": "Conference on Robotics, 2024",
                "link": "https://example.com/duplicate",
                "category": "conference",
            },
        ]

        merged = merge_publications(scholar_publications, overrides=[])

        self.assertEqual([publication["title"] for publication in merged], ["Alpha Paper", "Beta Paper"])

    def test_openalex_work_is_mapped_to_site_publication(self):
        from scripts.fetch_openalex import map_openalex_work_to_publication

        publication = map_openalex_work_to_publication(
            {
                "id": "https://openalex.org/W123",
                "doi": "https://doi.org/10.1109/example.2026.1234567",
                "display_name": "Stable Variable Impedance Control",
                "publication_year": 2026,
                "type": "conference-paper",
                "authorships": [
                    {
                        "raw_author_name": "Seungmin Choi",
                        "author": {"display_name": "Seung-Min Choi"},
                    },
                    {
                        "raw_author_name": "Wansoo Kim",
                        "author": {"display_name": "Wansoo Kim"},
                    },
                ],
                "primary_location": {
                    "landing_page_url": "https://doi.org/10.1109/example.2026.1234567",
                    "raw_source_name": "2026 IEEE/RSJ International Conference on Intelligent Robots and Systems",
                    "source": {"display_name": "IROS", "type": "conference"},
                    "raw_type": "proceedings-article",
                },
            }
        )

        self.assertEqual(
            publication,
            {
                "title": "Stable Variable Impedance Control",
                "authors": "Seungmin Choi, Wansoo Kim",
                "year": 2026,
                "journal": "2026 IEEE/RSJ International Conference on Intelligent Robots and Systems",
                "link": "https://doi.org/10.1109/example.2026.1234567",
                "category": "conference",
                "doi": "10.1109/example.2026.1234567",
            },
        )

    def test_openalex_retraction_work_is_skipped(self):
        from scripts.fetch_openalex import map_openalex_work_to_publication

        publication = map_openalex_work_to_publication(
            {
                "display_name": "Retraction Note: Some Paper",
                "publication_year": 2026,
                "type": "retraction",
                "authorships": [{"author": {"display_name": "A Author"}}],
                "primary_location": {"raw_source_name": "Some Journal"},
            }
        )

        self.assertIsNone(publication)

    def test_openalex_fetch_requires_target_author_affiliation_match(self):
        sys.modules.pop("scripts.fetch_openalex", None)

        response_payload = {
            "meta": {"next_cursor": None},
            "results": [
                {
                    "id": "https://openalex.org/W1",
                    "display_name": "Correct Robotics Paper",
                    "publication_year": 2026,
                    "type": "article",
                    "authorships": [
                        {
                            "author": {"id": "https://openalex.org/A5101430480", "display_name": "Wansoo Kim"},
                            "raw_author_name": "Wansoo Kim",
                            "institutions": [{"id": "https://openalex.org/I4575257"}],
                        }
                    ],
                    "primary_location": {"raw_source_name": "IEEE Robotics and Automation Letters"},
                },
                {
                    "id": "https://openalex.org/W2",
                    "display_name": "Unrelated Biology Paper",
                    "publication_year": 2026,
                    "type": "article",
                    "authorships": [
                        {
                            "author": {"id": "https://openalex.org/A5101430480", "display_name": "Wansoo Kim"},
                            "raw_author_name": "Wansoo Kim",
                            "institutions": [{"id": "https://openalex.org/I31419693"}],
                            "raw_affiliation_strings": ["School of Life Science, Kyungpook National University"],
                        },
                        {
                            "author": {"id": "https://openalex.org/A5026761651", "display_name": "Se-Hyeon Han"},
                            "raw_author_name": "Se-Hyeon Han",
                            "institutions": [{"id": "https://openalex.org/I4575257"}],
                        },
                    ],
                    "primary_location": {"raw_source_name": "Life Sciences"},
                },
            ],
        }

        class FakeResponse:
            status_code = 200

            def json(self):
                return response_payload

        fake_requests = types.SimpleNamespace(get=lambda *args, **kwargs: FakeResponse())
        previous_requests = sys.modules.get("requests")
        sys.modules["requests"] = fake_requests
        try:
            from scripts.fetch_openalex import fetch_publications

            publications = fetch_publications(author_ids=("A5101430480",), institution_ids=("I4575257",))
        finally:
            if previous_requests is None:
                sys.modules.pop("requests", None)
            else:
                sys.modules["requests"] = previous_requests

        self.assertEqual([publication["title"] for publication in publications], ["Correct Robotics Paper"])

    def test_update_publications_writes_merged_dataset(self):
        from scripts.update_publications import update_publications

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "publications.json"
            cache_path = Path(temp_dir) / "cache.json"
            overrides_path = Path(temp_dir) / "missing_overrides.yaml"

            publications = update_publications(
                fetcher=lambda **kwargs: [
                    {
                        "title": "Fetched Paper",
                        "authors": "A Author",
                        "year": 2026,
                        "journal": "Robotics Journal, 2026",
                        "link": "https://example.com/fetched",
                        "category": "journal",
                    }
                ],
                output_path=output_path,
                overrides_path=overrides_path,
                cache_path=cache_path,
                enrich=False,
            )

            self.assertEqual(publications[0]["title"], "Fetched Paper")
            self.assertEqual(json.loads(output_path.read_text(encoding="utf-8"))[0]["title"], "Fetched Paper")
            self.assertFalse(cache_path.exists())

    def test_update_publications_defaults_to_scholar_source(self):
        import scripts.update_publications as module

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "publications.json"
            cache_path = Path(temp_dir) / "cache.json"
            overrides_path = Path(temp_dir) / "missing_overrides.yaml"
            original_fetchers = module.FETCHERS

            def scholar_fetcher(**kwargs):
                return [
                    {
                        "title": "Scholar Default Paper",
                        "authors": "A Author",
                        "year": 2026,
                        "journal": "Robotics Journal, 2026",
                        "link": "https://example.com/scholar",
                        "category": "journal",
                    }
                ]

            def openalex_fetcher(**kwargs):
                raise AssertionError("OpenAlex should not be the default publication source")

            module.FETCHERS = {"openalex": openalex_fetcher, "scholar": scholar_fetcher}
            try:
                publications = module.update_publications(
                    output_path=output_path,
                    overrides_path=overrides_path,
                    cache_path=cache_path,
                    enrich=False,
                )
            finally:
                module.FETCHERS = original_fetchers

            self.assertEqual(publications[0]["title"], "Scholar Default Paper")

    def test_update_publications_merges_fetched_results_with_existing_dataset(self):
        from scripts.update_publications import update_publications

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "publications.json"
            cache_path = Path(temp_dir) / "cache.json"
            overrides_path = Path(temp_dir) / "missing_overrides.yaml"
            existing_publications = [
                {
                    "title": "Existing Paper",
                    "authors": "A Author",
                    "year": 2025,
                    "journal": "Robotics Journal, 2025",
                    "link": "https://example.com/existing",
                    "category": "journal",
                }
            ]
            output_path.write_text(json.dumps(existing_publications, ensure_ascii=False), encoding="utf-8")

            publications = update_publications(
                fetcher=lambda **kwargs: [
                    {
                        "title": "Fetched Paper",
                        "authors": "B Author",
                        "year": 2026,
                        "journal": "Robotics Conference, 2026",
                        "link": "https://example.com/fetched",
                        "category": "conference",
                    }
                ],
                output_path=output_path,
                overrides_path=overrides_path,
                cache_path=cache_path,
                enrich=False,
            )

            self.assertEqual([publication["title"] for publication in publications], ["Fetched Paper", "Existing Paper"])
            self.assertEqual(
                [publication["title"] for publication in json.loads(output_path.read_text(encoding="utf-8"))],
                ["Fetched Paper", "Existing Paper"],
            )

    def test_update_publications_keeps_existing_data_when_fetch_returns_empty_results(self):
        from scripts.update_publications import update_publications

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "publications.json"
            cache_path = Path(temp_dir) / "cache.json"
            overrides_path = Path(temp_dir) / "missing_overrides.yaml"
            existing_publications = [
                {
                    "title": "Existing Paper",
                    "authors": "A Author",
                    "year": 2025,
                    "journal": "Robotics Journal, 2025",
                    "link": "https://example.com/existing",
                    "category": "journal",
                }
            ]
            output_path.write_text(json.dumps(existing_publications, ensure_ascii=False), encoding="utf-8")

            publications = update_publications(
                fetcher=lambda **kwargs: [],
                output_path=output_path,
                overrides_path=overrides_path,
                cache_path=cache_path,
                enrich=False,
            )

            self.assertEqual(publications, existing_publications)
            self.assertEqual(json.loads(output_path.read_text(encoding="utf-8")), existing_publications)

    def test_update_publications_can_require_successful_fetch(self):
        from scripts.update_publications import update_publications

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "publications.json"
            cache_path = Path(temp_dir) / "cache.json"
            overrides_path = Path(temp_dir) / "missing_overrides.yaml"
            existing_publications = [
                {
                    "title": "Existing Paper",
                    "authors": "A Author",
                    "year": 2025,
                    "journal": "Robotics Journal, 2025",
                    "link": "https://example.com/existing",
                    "category": "journal",
                }
            ]
            output_path.write_text(json.dumps(existing_publications, ensure_ascii=False), encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "No publications were fetched"):
                update_publications(
                    fetcher=lambda **kwargs: [],
                    output_path=output_path,
                    overrides_path=overrides_path,
                    cache_path=cache_path,
                    enrich=False,
                    require_fetch_success=True,
                )

            self.assertEqual(json.loads(output_path.read_text(encoding="utf-8")), existing_publications)

    def test_update_publications_fails_empty_initial_dataset(self):
        from scripts.update_publications import update_publications

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "publications.json"
            cache_path = Path(temp_dir) / "cache.json"
            overrides_path = Path(temp_dir) / "missing_overrides.yaml"

            with self.assertRaisesRegex(RuntimeError, "No publications were generated"):
                update_publications(
                    fetcher=lambda **kwargs: [],
                    output_path=output_path,
                    overrides_path=overrides_path,
                    cache_path=cache_path,
                    enrich=False,
                )


if __name__ == "__main__":
    unittest.main()
