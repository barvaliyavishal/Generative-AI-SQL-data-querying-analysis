"""Small CLI to inspect repository notebooks and data directories."""
import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def list_files(folder_name: str):
    folder = ROOT / folder_name
    if not folder.exists():
        print(f"{folder_name!r} not found in project root ({ROOT}).")
        return
    files = sorted(folder.glob("**/*"))
    if not files:
        print(f"No files found in {folder_name}.")
        return
    for f in files:
        if f.is_file():
            print(str(f.relative_to(ROOT)))


def main():
    parser = argparse.ArgumentParser(description="Resources project helper CLI")
    parser.add_argument("--list-notebooks", action="store_true", help="List notebooks in notebooks/ and at repo root")
    parser.add_argument("--list-data", action="store_true", help="List files in data/ and root-level datasets")
    args = parser.parse_args()

    if args.list_notebooks:
        # Check notebooks dir and also any .ipynb at root
        list_files("notebooks")
        # list root notebooks
        for nb in sorted(ROOT.glob("*.ipynb")):
            print(nb.name)

    if args.list_data:
        list_files("data")
        for f in sorted(ROOT.glob("*.csv")):
            print(f.name)

    if not (args.list_notebooks or args.list_data):
        parser.print_help()


if __name__ == "__main__":
    main()
