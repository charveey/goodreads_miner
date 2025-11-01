# tasks.py
import subprocess
import sys
import re
from pathlib import Path
import argparse
import shutil

# ========================
# CONFIG
# ========================
CHANGELOG_FILE = Path("CHANGELOG.md")
DIST_DIR = Path("dist")

# ========================
# HELPER FUNCTIONS
# ========================
def run(cmd, dry_run=False):
    """Run shell command"""
    print(f"$ {cmd}")
    if not dry_run:
        subprocess.run(cmd, shell=True, check=True)

# ========================
# TASKS
# ========================
def clean_build(dry_run=False):
    """Remove the dist/ directory to ensure a fresh build"""
    if DIST_DIR.exists():
        print(f"Cleaning build directory: {DIST_DIR}")
        if not dry_run:
            shutil.rmtree(DIST_DIR)
    else:
        print(f"No build directory to clean: {DIST_DIR}")

def release(level=None, exact_version=None, dry_run=False):
    """
    Automate release process with uv, git-cliff, and PyPI upload.

    Args:
        level (str, optional): "patch", "minor", or "major" for semantic version bump.
        exact_version (str, optional): Exact version to set, e.g. "0.3.1".
        dry_run (bool): If True, simulate the release without making changes.
    """
    if not level and not exact_version:
        sys.exit("Either --level or --exact-version must be provided")

    # ----------------------
    # 1. Determine new version
    # ----------------------
    cmd_uv = "uv version"
    if exact_version:
        cmd_uv += f" {exact_version}"
    elif level:
        cmd_uv += f" --bump {level}"
    if dry_run:
        cmd_uv += " --dry-run"

    print(f"$ {cmd_uv}")
    result = subprocess.run(cmd_uv, shell=True, capture_output=True, text=True, check=True)
    stdout = result.stdout.strip()
    print(stdout)

    # Extract only the new version number
    match = re.search(r"=>\s*([^\s]+)", stdout)
    if match:
        new_version = match.group(1)
    else:
        # If dry-run or exact version without bump, fallback to last word
        new_version = stdout.split()[-1]
    print(f"New version: {new_version}")

    # ----------------------
    # 2. Generate changelog
    # ----------------------
    run(f"git cliff -o {CHANGELOG_FILE} --tag v{new_version}", dry_run=dry_run)

    # ----------------------
    # 3. Commit version bump and changelog
    # ----------------------
    run("git add pyproject.toml CHANGELOG.md uv.lock", dry_run=dry_run)
    run(f'git commit -m "chore(release): v{new_version}"', dry_run=dry_run)

    # ----------------------
    # 4. Tag release
    # ----------------------
    run(f"git tag v{new_version}", dry_run=dry_run)

    # 4b. Push tag to origin
    run(f"git push origin v{new_version}", dry_run=dry_run)


    # ----------------------
    # 5. Clean dist directory
    # ----------------------
    clean_build(dry_run=dry_run)

    # ----------------------
    # 6. Build package
    # ----------------------
    run("uv build", dry_run=dry_run)

    # ----------------------
    # 7. Upload to PyPI
    # ----------------------
    run("twine check dist/*", dry_run=dry_run)
    run("twine upload dist/*", dry_run=dry_run)

    print(f"Release v{new_version} completed ✅" if not dry_run else "[DRY-RUN] Release simulated ✅")

def test():
    """Run tests with pytest"""
    run("pytest tests --color=yes")

# ========================
# CLI
# ========================
def main():

    parser = argparse.ArgumentParser(description="Tasks for Goodreads Miner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ------------------------
    # release subcommand
    # ------------------------
    parser_release = subparsers.add_parser("release", help="Run release process")

    # Either bump level OR exact version must be provided
    parser_release.add_argument(
        "--level",
        choices=["patch", "minor", "major"],
        help="Version bump level (ignored if --exact-version is provided)"
    )
    parser_release.add_argument(
        "--exact-version",
        help="Set exact version (overrides --level)"
    )
    parser_release.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the release without making changes"
    )

    # ------------------------
    # test subcommand
    # ------------------------
    subparsers.add_parser("test", help="Run tests")

    args = parser.parse_args()

    if args.command == "release":
        release(
            level=getattr(args, "level", None),
            exact_version=getattr(args, "exact_version", None),
            dry_run=getattr(args, "dry_run", False)
        )
    elif args.command == "test":
        test()


if __name__ == "__main__":
    main()
