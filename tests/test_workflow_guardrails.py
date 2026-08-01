import unittest
from pathlib import Path


class WorkflowGuardrailTest(unittest.TestCase):
    def test_gitlab_sync_requires_explicit_enable_variable(self):
        workflow = Path(".github/workflows/sync_gitlab.yml").read_text(encoding="utf-8")

        self.assertIn("if: ${{ vars.ENABLE_GITLAB_SYNC == 'true' }}", workflow)
        self.assertIn("ENABLE_GITLAB_SYNC", workflow)

    def test_github_publication_update_is_manual_only(self):
        workflow = Path(".github/workflows/update-publications.yml").read_text(encoding="utf-8")

        self.assertIn("workflow_dispatch:", workflow)
        self.assertNotIn("schedule:", workflow)
        self.assertNotIn("push:", workflow)

    def test_gitlab_sync_does_not_persist_github_credentials(self):
        workflow = Path(".github/workflows/sync_gitlab.yml").read_text(encoding="utf-8")

        self.assertIn("persist-credentials: false", workflow)

    def test_network_workflows_have_job_timeouts(self):
        for path in (
            ".github/workflows/sync_gitlab.yml",
            ".github/workflows/update-publications.yml",
            ".github/workflows/update-youtube.yml",
        ):
            with self.subTest(path=path):
                workflow = Path(path).read_text(encoding="utf-8")
                self.assertIn("timeout-minutes:", workflow)


if __name__ == "__main__":
    unittest.main()
