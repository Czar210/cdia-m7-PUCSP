"""Entry point for the datagen package.

This file works when executed as a module (`python -m datagen`) or as a script
(`python datagen/main.py`) by resolving imports dynamically.
"""
import importlib
import sys
from pathlib import Path


def _get_ensure_data():
    try:
        mod = importlib.import_module("datagen.ensure_data")
        return mod.ensure_data
    except Exception:
        # If running as a script (python Hug/main.py), ensure parent folder
        # (repo root) is on sys.path so `import Hug...` works.
        parent = Path(__file__).resolve().parent.parent
        if str(parent) not in sys.path:
            sys.path.insert(0, str(parent))
        mod = importlib.import_module("datagen.ensure_data")
        return mod.ensure_data


def main():
    ensure_data = _get_ensure_data()
    result = ensure_data()
    files = result.get("files", [])
    if result.get("generated"):
        print(f"Generated {len(files)} file(s):")
        for f in files:
            print(f"  - {f}")
    else:
        print(f"Data already present ({len(files)} file(s)).")


if __name__ == "__main__":
    main()
