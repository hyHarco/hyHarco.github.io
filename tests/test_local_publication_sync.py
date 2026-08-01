import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import local_publication_sync
from scripts.local_publication_sync import build_update_command, venv_python_path


class LocalPublicationSyncTest(unittest.TestCase):
    def test_update_command_uses_scholar_and_requires_fetch_success(self):
        command = build_update_command(
            "python",
            no_enrich=True,
            output_path=Path("tmp/publications.json"),
            cache_path=Path("tmp/cache.json"),
        )

        self.assertEqual(
            command,
            [
                "python",
                "scripts/update_publications.py",
                "--source",
                "scholar",
                "--require-fetch-success",
                "--output",
                "tmp/publications.json",
                "--cache",
                "tmp/cache.json",
                "--no-enrich",
            ],
        )

    def test_check_mode_uses_temporary_files_without_git_guards(self):
        commands = []

        def record_command(command, repo_root, check=True):
            commands.append(command)

        with (
            patch.object(local_publication_sync, "ensure_clean_worktree") as ensure_clean_worktree,
            patch.object(local_publication_sync, "ensure_branch") as ensure_branch,
            patch.object(local_publication_sync, "ensure_virtualenv", return_value="python"),
            patch.object(local_publication_sync, "run", side_effect=record_command),
            patch("builtins.print"),
        ):
            local_publication_sync.check_publications(no_enrich=True)

        ensure_clean_worktree.assert_not_called()
        ensure_branch.assert_not_called()
        self.assertEqual(len(commands), 1)

        command = commands[0]
        self.assertIn("--output", command)
        self.assertIn("--cache", command)
        self.assertIn("--no-enrich", command)
        self.assertEqual(Path(command[command.index("--output") + 1]).name, "publications.json")
        self.assertEqual(Path(command[command.index("--cache") + 1]).name, "publication_metadata_cache.json")

    def test_venv_python_path_is_cross_platform(self):
        venv_dir = Path("venv")

        self.assertEqual(venv_python_path(venv_dir, os_name="nt"), venv_dir / "Scripts" / "python.exe")
        self.assertEqual(venv_python_path(venv_dir, os_name="posix"), venv_dir / "bin" / "python")


if __name__ == "__main__":
    unittest.main()
