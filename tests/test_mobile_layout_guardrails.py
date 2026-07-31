import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_repo_file(path):
    return (ROOT / path).read_text(encoding="utf-8")


class MobileLayoutGuardrailsTest(unittest.TestCase):
    def assert_has_mobile_single_column_rule(self, css, selector, max_width="640px"):
        pattern = (
            rf"@media\s*\(max-width:\s*{re.escape(max_width)}\)\s*{{"
            rf"[\s\S]*?{re.escape(selector)}\s*{{"
            rf"[\s\S]*?grid-template-columns:\s*1fr\s*;"
        )
        self.assertRegex(css, pattern)

    def test_content_sections_use_border_box_width_on_small_viewports(self):
        section_css = read_repo_file("css/section.scss")

        self.assertRegex(
            section_css,
            r"\.section\s*{[\s\S]*?box-sizing:\s*border-box\s*;",
        )
        self.assertRegex(
            section_css,
            r"\.section\s*{[\s\S]*?width:\s*100%\s*;",
        )

    def test_event_style_grids_stack_and_allow_children_to_shrink(self):
        for path in ("css/project_grid.css", "css/event_grid.css"):
            css = read_repo_file(path)

            with self.subTest(path=path):
                self.assertRegex(css, r"\.event_container\s*>\s*\*\s*{[\s\S]*?min-width:\s*0\s*;")
                self.assertRegex(css, r"\.event_container\s+\.items\s*{[\s\S]*?overflow-wrap:\s*anywhere\s*;")
                self.assert_has_mobile_single_column_rule(css, ".event_container")

    def test_organizer_grid_stacks_and_allows_children_to_shrink(self):
        css = read_repo_file("css/organizer_grid.css")

        self.assertRegex(css, r"\.organizer_container\s*>\s*\*\s*{[\s\S]*?min-width:\s*0\s*;")
        self.assertRegex(css, r"\.organizer_container\s*{[\s\S]*?overflow-wrap:\s*anywhere\s*;")
        self.assert_has_mobile_single_column_rule(css, ".organizer_container")

    def test_homepage_mobile_lists_collapse_to_single_column(self):
        homepage = read_repo_file("index.md")

        self.assertRegex(homepage, r"\.home_news_list\s+a\s*>\s*\*\s*{[\s\S]*?min-width:\s*0\s*;")
        self.assertRegex(homepage, r"\.home_news_list\s+\.home_news_title\s*{[\s\S]*?overflow-wrap:\s*anywhere\s*;")
        self.assert_has_mobile_single_column_rule(homepage, ".home_news_list a", max_width="520px")
        self.assert_has_mobile_single_column_rule(homepage, ".home_youtube_grid", max_width="520px")

    def test_footer_explore_links_stack_on_narrow_screens(self):
        footer_css = read_repo_file("css/footer.scss")

        self.assertRegex(footer_css, r"\.footer_col\s*{[\s\S]*?min-width:\s*0\s*;")
        self.assertRegex(
            footer_css,
            r"@media\s*\(max-width:\s*500px\)\s*{[\s\S]*?\.footer_explore_grid\s*{"
            r"[\s\S]*?grid-template-columns:\s*1fr\s*;",
        )
        self.assertRegex(
            footer_css,
            r"@media\s*\(max-width:\s*500px\)\s*{[\s\S]*?\.footer_explore_grid\s*{[\s\S]*?li\s*{"
            r"[\s\S]*?white-space:\s*normal\s*;",
        )

    def test_header_navigation_wraps_instead_of_widening_the_viewport(self):
        subnav_css = read_repo_file("css/subnav.css")
        research_subnav_css = read_repo_file("css/subnav_research.css")

        self.assertRegex(subnav_css, r"\.navbar\s*{[\s\S]*?flex-wrap:\s*wrap\s*;")
        self.assertRegex(subnav_css, r"\.navbar\s*{[\s\S]*?min-width:\s*0\s*;")
        self.assertRegex(
            subnav_css,
            r"@media\s*\(max-width:\s*600px\)\s*{[\s\S]*?\.navbar\s*{[\s\S]*?flex-direction:\s*column\s*;",
        )
        self.assertRegex(
            subnav_css,
            r"@media\s*\(max-width:\s*600px\)\s*{[\s\S]*?\.subnav-content\s*{[\s\S]*?min-width:\s*0\s*;",
        )
        self.assertRegex(
            research_subnav_css,
            r"@media\s*\(max-width:\s*600px\)\s*{[\s\S]*?\.subnav-research-content\s*{"
            r"[\s\S]*?min-width:\s*0\s*;",
        )

    def test_header_has_accessible_mobile_menu_toggle(self):
        header = read_repo_file("_includes/header.html")

        self.assertIn('data-mobile-menu-open="false"', header)
        self.assertRegex(header, r'<button\s+[^>]*class="mobile_menu_toggle"')
        self.assertRegex(header, r'class="mobile_menu_toggle"[\s\S]*?aria-controls="site-navigation"')
        self.assertRegex(header, r'class="mobile_menu_toggle"[\s\S]*?aria-expanded="false"')
        self.assertRegex(header, r'<nav\s+class="navbar"\s+id="site-navigation"\s+aria-label="Primary navigation"')
        self.assertIn("setMobileMenuOpen", header)
        self.assertIn("data-mobile-menu-open", header)

    def test_mobile_navigation_is_hidden_until_the_hamburger_opens_it(self):
        header_css = read_repo_file("css/header.scss")
        subnav_css = read_repo_file("css/subnav.css")

        self.assertRegex(header_css, r"\.mobile_menu_toggle\s*{[\s\S]*?display:\s*none\s*;")
        self.assertRegex(
            header_css,
            r"@media\s*\(max-width:\s*600px\)\s*{[\s\S]*?\.mobile_menu_toggle\s*{"
            r"[\s\S]*?display:\s*inline-flex\s*;",
        )
        self.assertRegex(
            subnav_css,
            r"@media\s*\(max-width:\s*600px\)\s*{[\s\S]*?\.navbar\s*{"
            r"[\s\S]*?display:\s*none\s*;",
        )
        self.assertRegex(
            subnav_css,
            r"@media\s*\(max-width:\s*600px\)\s*{[\s\S]*?header\[data-mobile-menu-open=\"true\"\]\s+\.navbar\s*{"
            r"[\s\S]*?display:\s*flex\s*;",
        )

    def test_mobile_submenus_open_from_button_state(self):
        header = read_repo_file("_includes/header.html")
        subnav_css = read_repo_file("css/subnav.css")
        research_subnav_css = read_repo_file("css/subnav_research.css")

        self.assertIn('aria-controls="research-subnav"', header)
        self.assertIn('aria-controls="publications-subnav"', header)
        self.assertIn('aria-controls="team-subnav"', header)
        self.assertIn('aria-controls="news-subnav"', header)
        self.assertIn("setSubnavOpen", header)
        self.assertIn("data-subnav-open", header)
        self.assertRegex(
            subnav_css,
            r"\.subnav\[data-subnav-open=\"true\"\]\s+\.subnav-content\s*{[\s\S]*?display:\s*block\s*;",
        )
        self.assertRegex(
            research_subnav_css,
            r"\.subnav-research\[data-subnav-open=\"true\"\]\s+\.subnav-research-content\s*{"
            r"[\s\S]*?display:\s*block\s*;",
        )

    def test_mobile_menu_script_handles_link_clicks_defensively(self):
        header = read_repo_file("_includes/header.html")

        self.assertNotIn("function redirectToResearch", header)
        self.assertIn("event.target instanceof Element", header)
        self.assertNotRegex(header, r"const\s+link\s*=\s*event\.target\.closest\(\"a\"\)")

    def test_subnav_state_is_only_toggled_on_mobile(self):
        header = read_repo_file("_includes/header.html")

        self.assertRegex(
            header,
            r"if\s*\(!mobileQuery\.matches\)\s*{[\s\S]*?if\s*\(target\)\s*window\.location\.href\s*=\s*target;"
            r"[\s\S]*?return;",
        )

    def test_two_column_blocks_allow_children_to_shrink_before_stacking(self):
        two_col_css = read_repo_file("css/two-col.scss")

        self.assertRegex(two_col_css, r"\.two_col\s*{[\s\S]*?grid-template-columns:\s*repeat\(2,\s*minmax\(0,\s*1fr\)\)\s*;")
        self.assertRegex(two_col_css, r"\.two_col\s*{[\s\S]*?>\s*\*\s*{[\s\S]*?min-width:\s*0\s*;")
        self.assertRegex(two_col_css, r"\.two_col\s*{[\s\S]*?>\s*\*\s*{[\s\S]*?overflow-wrap:\s*anywhere\s*;")


if __name__ == "__main__":
    unittest.main()
