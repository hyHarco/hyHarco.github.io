"""Cross-platform local publication sync for Google Scholar updates."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

GENERATED_FILES = (
    "publication/publications.json",
    "_data/publication_metadata_cache.json",
)
COMMIT_SUBJECT = "Update publication data from local Scholar sync"
COMMIT_BODY = "Refresh generated publication data from the local Google Scholar update pipeline."


def venv_python_path(venv_dir: Path, os_name: str = os.name) -> Path:
    if os_name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def build_update_command(
    python_executable: str,
    no_enrich: bool = False,
    output_path: Path | None = None,
    cache_path: Path | None = None,
) -> list[str]:
    command = [
        python_executable,
        "scripts/update_publications.py",
        "--source",
        "scholar",
        "--require-fetch-success",
    ]
    if output_path is not None:
        command.extend(["--output", str(output_path)])
    if cache_path is not None:
        command.extend(["--cache", str(cache_path)])
    if no_enrich:
        command.append("--no-enrich")
    return command


def run(command: list[str], repo_root: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("+ " + " ".join(command))
    return subprocess.run(command, cwd=repo_root, check=check, text=True)


def capture(command: list[str], repo_root: Path) -> str:
    result = subprocess.run(command, cwd=repo_root, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def ensure_clean_worktree(repo_root: Path) -> None:
    status = capture(["git", "status", "--porcelain"], repo_root)
    if status:
        raise RuntimeError("Working tree has pending changes. Commit, stash, or discard them before local sync.")


def ensure_branch(repo_root: Path, branch: str) -> None:
    current_branch = capture(["git", "branch", "--show-current"], repo_root)
    if current_branch != branch:
        raise RuntimeError(f"Local publication sync must run on {branch}; current branch is {current_branch}.")


def ensure_virtualenv(repo_root: Path) -> str:
    venv_dir = repo_root / "venv"
    python_path = venv_python_path(venv_dir)
    if not python_path.exists():
        run([sys.executable, "-m", "venv", str(venv_dir)], repo_root)

    dependencies = ["requests", "pyyaml", "manubot"]
    run([str(python_path), "-m", "pip", "install", "-q", "--disable-pip-version-check", *dependencies], repo_root)
    return str(python_path)


def has_staged_generated_changes(repo_root: Path) -> bool:
    result = run(["git", "diff", "--cached", "--quiet", "--", *GENERATED_FILES], repo_root, check=False)
    return result.returncode != 0


def check_publications(no_enrich: bool) -> int:
    repo_root = Path(__file__).resolve().parents[1]
    python_path = ensure_virtualenv(repo_root)

    with tempfile.TemporaryDirectory(prefix="harco-publication-check-") as temp_dir:
        temp_path = Path(temp_dir)
        output_path = temp_path / "publications.json"
        cache_path = temp_path / "publication_metadata_cache.json"
        run(
            build_update_command(
                python_path,
                no_enrich=no_enrich,
                output_path=output_path,
                cache_path=cache_path,
            ),
            repo_root,
        )

    print("Publication check completed without changing repository files.")
    return 0


def sync_publications(branch: str, remote: str, no_enrich: bool, no_pull: bool, no_push: bool) -> int:
    repo_root = Path(__file__).resolve().parents[1]
    ensure_clean_worktree(repo_root)
    ensure_branch(repo_root, branch)

    if not no_pull:
        run(["git", "pull", "--ff-only", remote, branch], repo_root)

    python_path = ensure_virtualenv(repo_root)
    run(build_update_command(python_path, no_enrich=no_enrich), repo_root)
    run(["git", "add", "--", *GENERATED_FILES], repo_root)

    if not has_staged_generated_changes(repo_root):
        print("No publication changes to commit.")
        return 0

    run(["git", "commit", "-m", COMMIT_SUBJECT, "-m", COMMIT_BODY], repo_root)

    if not no_push:
        run(["git", "push", remote, branch], repo_root)

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Update HARCO publications locally from Google Scholar.")
    parser.add_argument("--branch", default="main", help="Branch to update and push.")
    parser.add_argument("--remote", default="origin", help="Git remote to pull from and push to.")
    parser.add_argument("--no-enrich", action="store_true", help="Skip Manubot DOI enrichment.")
    parser.add_argument("--no-pull", action="store_true", help="Skip the initial git pull.")
    parser.add_argument("--no-push", action="store_true", help="Commit locally without pushing.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fetch publications into temporary files without checking git state or changing repository files.",
    )
    args = parser.parse_args()

    try:
        if args.check:
            return check_publications(no_enrich=args.no_enrich)

        return sync_publications(
            branch=args.branch,
            remote=args.remote,
            no_enrich=args.no_enrich,
            no_pull=args.no_pull,
            no_push=args.no_push,
        )
    except Exception as error:
        print(f"Publication sync failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
