import unittest
from pathlib import Path
from functools import lru_cache
from html.parser import HTMLParser
import re
import subprocess
import tempfile
from struct import unpack


ROOT = Path(__file__).resolve().parents[1]
MAX_OPTIMIZED_IMAGE_BYTES = 6 * 1024 * 1024
MAX_JPEG_IMAGE_BYTES = 2 * 1024 * 1024
MAX_REFERENCED_RASTER_IMAGE_BYTES = 2_500_000
MAX_REFERENCED_ANIMATED_IMAGE_BYTES = 5 * 1024 * 1024
MAX_OPTIMIZED_IMAGE_DIMENSION = 2400
IMAGE_REFERENCE_RE = re.compile(r"/?(images/[^\s\"')]+?\.(?:gif|jpe?g|png))", re.IGNORECASE)
TEXT_ASSET_EXTENSIONS = {".css", ".html", ".js", ".json", ".md", ".scss", ".yaml", ".yml"}
SKIPPED_SCAN_ROOTS = {".git", ".jekyll-cache", "_site", "_site_check", "venv"}


class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stylesheets = []
        self.scripts = []

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)

        if tag == "script" and attributes.get("src"):
            self.scripts.append(attributes["src"])
            return

        if tag != "link":
            return

        rel = attributes.get("rel", "")
        rel_values = rel if isinstance(rel, list) else str(rel).split()
        if "stylesheet" in rel_values and attributes.get("href"):
            self.stylesheets.append(attributes["href"])


class VisibleTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.text_parts.append(text)

    @property
    def text(self):
        return " ".join(self.text_parts)


class MainVisibleTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_main = False
        self.skip_depth = 0
        self.text_parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.in_main = True
            return

        if self.in_main and tag in {"script", "style"}:
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False
            return

        if self.in_main and tag in {"script", "style"} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data):
        if not self.in_main or self.skip_depth:
            return

        text = data.strip()
        if text:
            self.text_parts.append(text)

    @property
    def text(self):
        return " ".join(self.text_parts)


def read_repo_file(path):
    return (ROOT / path).read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def built_site_files():
    with tempfile.TemporaryDirectory() as destination:
        result = subprocess.run(
            ["bundle", "exec", "jekyll", "build", "--destination", destination],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)

        destination_path = Path(destination)
        return {
            path.relative_to(destination_path): path.read_text(encoding="utf-8")
            for path in destination_path.rglob("*.html")
        }


def stylesheet_links(html):
    parser = AssetParser()
    parser.feed(html)
    return parser.stylesheets


def script_links(html):
    parser = AssetParser()
    parser.feed(html)
    return parser.scripts


def visible_text(html):
    parser = VisibleTextParser()
    parser.feed(html)
    return parser.text


def main_visible_text(html):
    parser = MainVisibleTextParser()
    parser.feed(html)
    return parser.text


def is_redirect_page(html):
    return "<title>Redirecting&hellip;</title>" in html and 'http-equiv="refresh"' in html


def image_format(path):
    data = (ROOT / path).read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8"):
        return "jpg"
    if data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        return "gif"
    raise AssertionError(f"Unsupported image format for {path}")


def image_size(path):
    data = (ROOT / path).read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return unpack(">II", data[16:24])

    if data.startswith(b"\xff\xd8"):
        index = 2
        while index < len(data):
            while index < len(data) and data[index] == 0xFF:
                index += 1
            marker = data[index]
            index += 1
            if marker in (0xD8, 0xD9):
                continue
            length = unpack(">H", data[index:index + 2])[0]
            if 0xC0 <= marker <= 0xC3:
                height, width = unpack(">HH", data[index + 3:index + 7])
                return width, height
            index += length

    raise AssertionError(f"Unsupported image format for {path}")


def referenced_image_paths():
    image_paths = set()

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_ASSET_EXTENSIONS:
            continue
        relative_path = path.relative_to(ROOT)
        if relative_path.parts[0] in SKIPPED_SCAN_ROOTS:
            continue
        if relative_path.name in {"CONVENTIONS.md", "README.md"}:
            continue

        contents = path.read_text(encoding="utf-8")
        for match in IMAGE_REFERENCE_RE.finditer(contents):
            image_paths.add(Path(match.group(1)))

    return sorted(image_paths)


class SiteHardeningTest(unittest.TestCase):
    def test_jekyll_excludes_development_and_source_files_from_public_output(self):
        config = read_repo_file("_config.yaml")

        self.assertIn("exclude:", config)
        for path in (
            ".github",
            "scripts",
            "tests",
            "docs",
            "venv",
            "assets/source",
            "_site_check",
            "README.md",
            "CONVENTIONS.md",
            "Gemfile",
            "Gemfile.lock",
        ):
            with self.subTest(path=path):
                self.assertIn(f"  - {path}", config)

    def test_start_script_skips_dependency_install_when_bundle_is_ready(self):
        script = read_repo_file("scripts/start.sh")

        self.assertTrue(script.startswith("#!/usr/bin/env sh\n"))
        self.assertIn("set -e", script)
        self.assertIn("bundle check", script)
        self.assertIn("bundle install", script)
        self.assertLess(script.index("bundle check"), script.index("bundle install"))

    def test_homepage_prioritizes_only_the_first_hero_slide_image(self):
        homepage = read_repo_file("index.md")

        self.assertIn('src="/images/main_img/1.png" alt="HARCO Lab" fetchpriority="high" decoding="async"', homepage)
        for image in ("2.jpg", "3.png", "4.jpg"):
            with self.subTest(image=image):
                self.assertIn(
                    f'src="/images/main_img/{image}" alt="HARCO Lab" loading="lazy" decoding="async"',
                    homepage,
                )

    def test_shared_image_includes_use_async_decoding_for_lazy_images(self):
        for path in (
            "_includes/card.html",
            "_includes/card-info.html",
            "_includes/card-info_2.html",
            "_includes/event.html",
            "_includes/figure.html",
            "_includes/gallery.html",
            "_includes/memberpicture.html",
            "_includes/portrait.html",
            "_includes/portrait-spc.html",
            "_includes/project_grid.html",
        ):
            with self.subTest(path=path):
                include = read_repo_file(path)
                self.assertIn('loading="lazy"', include)
                self.assertIn('decoding="async"', include)

    def test_publication_page_avoids_html_injection_from_publication_json(self):
        page = read_repo_file("publication/index.md")

        self.assertNotIn("innerHTML", page)
        self.assertIn("textContent", page)
        self.assertIn("rel = 'noopener'", page)

    def test_project_pages_with_date_ranges_render_body_content_as_visible_text(self):
        html = built_site_files()[Path("2024/04/01/project_forestry_work.html")]
        text = main_visible_text(html)

        self.assertIn("Goal of This Project", text)
        self.assertIn("Development of intelligent forestry machinery", text)
        self.assertIn("Participating Researchers", text)

    def test_post_pages_render_visible_main_content(self):
        short_pages = []

        for path, html in built_site_files().items():
            if not re.match(r"20[0-9][0-9]/[0-9]{2}/[0-9]{2}/.+\.html$", path.as_posix()):
                continue
            if is_redirect_page(html):
                continue

            text = main_visible_text(html)
            if len(text) < 80:
                short_pages.append(f"{path}: {text[:120]}")

        self.assertEqual(short_pages, [])

    def test_optimized_large_images_stay_within_web_sized_bounds(self):
        for path in (
            "images/equipment/equipments_1.png",
            "images/equipment/equipments_2.png",
            "images/equipment/equipments_3.png",
            "images/equipment/equipments_4.png",
            "images/members/jeongmok_kim.jpg",
            "images/members/sooin_choi.jpg",
            "images/news/230511_presentation_on_kspe_shindc/dongcheol_pr1.jpg",
            "images/news/230511_presentation_on_kspe_shindc/dongcheol_pr2.jpg",
            "images/news/240627_ur2024/ur_2024_present_2.jpg",
            "images/news/250429_eurecat/eurecat_1.jpg",
            "images/news/250429_eurecat/eurecat_2.jpg",
            "images/news/260605_icra2026/icra2026_donggyu_1.jpg",
            "images/news/260605_icra2026/icra2026_donggyu_2.jpg",
            "images/news/260605_icra2026/icra2026_kaili_1.jpg",
            "images/news/260605_icra2026/icra2026_kaili_2.jpg",
            "images/news/260605_icra2026/icra2026_main.jpg",
            "images/news/260703_icros/gitae.jpg",
            "images/news/260703_icros/jaegyun.jpg",
            "images/news/260703_icros/jingwang.jpg",
            "images/news/260703_icros/sooin.jpg",
        ):
            with self.subTest(path=path):
                file_path = ROOT / path
                width, height = image_size(path)

                message = f"{path} is too large for a web image"
                self.assertLessEqual(file_path.stat().st_size, MAX_OPTIMIZED_IMAGE_BYTES, message)
                self.assertLessEqual(max(width, height), MAX_OPTIMIZED_IMAGE_DIMENSION)

    def test_png_extensions_do_not_point_to_jpeg_content(self):
        for path in (ROOT / "images").rglob("*.png"):
            relative_path = path.relative_to(ROOT)
            with self.subTest(path=str(relative_path)):
                self.assertEqual(image_format(relative_path), "png")

    def test_jpeg_images_stay_within_web_sized_file_bounds(self):
        for path in (ROOT / "images").rglob("*"):
            if path.suffix.lower() not in {".jpg", ".jpeg"}:
                continue

            relative_path = path.relative_to(ROOT)
            with self.subTest(path=str(relative_path)):
                self.assertLessEqual(path.stat().st_size, MAX_JPEG_IMAGE_BYTES)

    def test_referenced_raster_images_stay_within_web_sized_file_bounds(self):
        for relative_path in referenced_image_paths():
            if relative_path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                continue

            path = ROOT / relative_path
            if not path.exists():
                continue

            with self.subTest(path=str(relative_path)):
                self.assertLessEqual(path.stat().st_size, MAX_REFERENCED_RASTER_IMAGE_BYTES)

    def test_referenced_animated_images_stay_within_web_sized_file_bounds(self):
        for relative_path in referenced_image_paths():
            if relative_path.suffix.lower() != ".gif":
                continue

            path = ROOT / relative_path
            if not path.exists():
                continue

            with self.subTest(path=str(relative_path)):
                self.assertLessEqual(path.stat().st_size, MAX_REFERENCED_ANIMATED_IMAGE_BYTES)

    def test_image_asset_paths_use_lowercase_names_without_spaces(self):
        for path in (ROOT / "images").rglob("*"):
            relative_path = path.relative_to(ROOT).as_posix()
            with self.subTest(path=relative_path):
                self.assertEqual(relative_path, relative_path.lower())
                self.assertNotIn(" ", relative_path)

    def test_referenced_image_paths_use_lowercase_names_without_spaces(self):
        for relative_path in referenced_image_paths():
            image_path = relative_path.as_posix()
            with self.subTest(path=image_path):
                self.assertEqual(image_path, image_path.lower())
                self.assertNotIn(" ", image_path)

    def test_referenced_image_assets_exist(self):
        for relative_path in referenced_image_paths():
            referenced_path = ROOT / relative_path
            with self.subTest(image=str(relative_path)):
                self.assertTrue(referenced_path.exists())

    def test_readme_documents_current_verification_and_asset_rules(self):
        readme = read_repo_file("README.md")

        for command in (
            "python3 -m unittest discover tests",
            "git diff --check",
            "bundle exec jekyll build --destination _site_check",
        ):
            with self.subTest(command=command):
                self.assertIn(command, readme)

        self.assertIn("2400px", readme)
        self.assertIn("2 MB", readme)
        self.assertIn("Do not publish development files", readme)

    def test_homepage_uses_a_bundled_core_stylesheet_budget(self):
        stylesheets = stylesheet_links(built_site_files()[Path("index.html")])

        local_component_styles = [
            href
            for href in stylesheets
            if href.startswith("/css/") and href != "/css/all.css"
        ]

        self.assertLessEqual(len(stylesheets), 8)
        self.assertEqual(local_component_styles, [])

    def test_pages_use_one_local_stylesheet_bundle(self):
        unexpected_links = []

        for path, html in built_site_files().items():
            for href in stylesheet_links(html):
                if href.startswith("/css/") and href != "/css/all.css":
                    unexpected_links.append(f"{path}: {href}")

        self.assertEqual(unexpected_links, [])

    def test_third_party_cdn_assets_pin_exact_versions(self):
        floating_major_version = re.compile(r"@[0-9]+(?:/|$)")
        external_assets = set()

        for html in built_site_files().values():
            external_assets.update(
                href
                for href in stylesheet_links(html) + script_links(html)
                if href.startswith("https://")
            )

        unpinned_assets = sorted(
            href for href in external_assets if floating_major_version.search(href)
        )

        self.assertEqual(unpinned_assets, [])

    def test_pages_load_local_javascript_in_dependency_order(self):
        expected_site_scripts = [
            "/js/true-hide.js",
            "/js/mobile-menu.js",
            "/js/anchors.js",
            "/js/search.js",
            "/js/tooltips.js",
        ]
        mismatches = []

        for path, html in built_site_files().items():
            local_scripts = [
                src for src in script_links(html) if src.startswith("/js/")
            ]
            if not local_scripts:
                continue

            expected_local_scripts = expected_site_scripts
            if path == Path("index.html"):
                expected_local_scripts = expected_site_scripts + [
                    "/js/home-youtube.js",
                    "/js/home-hero.js",
                ]

            if local_scripts != expected_local_scripts:
                mismatches.append(f"{path}: {local_scripts}")

        if mismatches:
            shown = "\n".join(mismatches[:5])
            self.fail(
                "Unexpected local script order:\n"
                f"{shown}\n"
                f"... and {len(mismatches) - min(len(mismatches), 5)} more"
            )

    def test_mobile_menu_logic_is_loaded_from_cacheable_javascript(self):
        repeated_inline_scripts = []

        for path, html in built_site_files().items():
            for inline_script in re.findall(r"<script>(.*?)</script>", html, re.DOTALL):
                if "setMobileMenuOpen" in inline_script:
                    repeated_inline_scripts.append(str(path))

        if repeated_inline_scripts:
            shown = ", ".join(repeated_inline_scripts[:5])
            self.fail(
                "Mobile menu logic is repeated inline in built HTML: "
                f"{shown}"
            )

    def test_unused_github_topic_fetcher_is_not_loaded_site_wide(self):
        has_repo_topic_rows = any(
            "data-repo=" in html for html in built_site_files().values()
        )
        loaded_fetch_tag_scripts = [
            str(path)
            for path, html in built_site_files().items()
            if "/js/fetch-tags.js" in script_links(html)
        ]

        if not has_repo_topic_rows:
            if loaded_fetch_tag_scripts:
                shown = ", ".join(loaded_fetch_tag_scripts[:5])
                self.fail(f"Unused fetch-tags.js is loaded by: {shown}")

    def test_disabled_snow_effect_is_not_published(self):
        with tempfile.TemporaryDirectory() as destination:
            result = subprocess.run(
                ["bundle", "exec", "jekyll", "build", "--destination", destination],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            homepage = (Path(destination) / "index.html").read_text(encoding="utf-8")
            site_css = (Path(destination) / "css" / "all.css").read_text(encoding="utf-8")

        self.assertNotIn("makeSnowflakes", homepage)
        self.assertNotIn(".snowflake", site_css)

    def test_homepage_uses_cacheable_page_assets(self):
        with tempfile.TemporaryDirectory() as destination:
            result = subprocess.run(
                ["bundle", "exec", "jekyll", "build", "--destination", destination],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            homepage = (Path(destination) / "index.html").read_text(encoding="utf-8")
            site_css = (Path(destination) / "css" / "all.css").read_text(encoding="utf-8")

        inline_styles = re.findall(r"<style>(.*?)</style>", homepage, re.DOTALL)
        inline_scripts = re.findall(r"<script>(.*?)</script>", homepage, re.DOTALL)

        self.assertFalse(
            any(".home_hero" in style for style in inline_styles),
            "homepage CSS should be bundled into css/all.css",
        )
        self.assertFalse(
            any("new Swiper" in script or "home_youtube_card" in script for script in inline_scripts),
            "homepage JavaScript should be loaded from cacheable files",
        )
        self.assertIn(".home_hero", site_css)

        scripts = script_links(homepage)
        self.assertIn("/js/home-youtube.js", scripts)
        self.assertIn("/js/home-hero.js", scripts)
        self.assertLess(
            scripts.index("https://cdn.jsdelivr.net/npm/swiper@10.3.1/swiper-bundle.min.js"),
            scripts.index("/js/home-hero.js"),
        )


if __name__ == "__main__":
    unittest.main()
