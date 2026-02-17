"""Simple launcher for running PANOPTO locally.

Usage:
    python3 panopto.py
"""

from __future__ import annotations

import argparse
import os
import sys
import types
from pathlib import Path


def _ensure_panopto_package(root: Path) -> None:
    """Prevent `panopto.py` from shadowing the `panopto/` package."""
    package_dir = root / "panopto"
    module = types.ModuleType("panopto")
    module.__path__ = [str(package_dir)]  # type: ignore[attr-defined]
    module.__file__ = str(package_dir / "__init__.py")
    sys.modules["panopto"] = module


def main() -> None:
    root = Path(__file__).resolve().parent
    venv_python = root / ".venv" / "bin" / "python"
    current_executable = Path(sys.executable).absolute()
    target_executable = venv_python.absolute()
    if (
        os.environ.get("PANOPTO_SKIP_REEXEC") != "1"
        and venv_python.exists()
        and current_executable != target_executable
    ):
        os.execve(
            str(venv_python),
            [str(venv_python), str(Path(__file__).resolve()), *sys.argv[1:]],
            {**os.environ, "PANOPTO_SKIP_REEXEC": "1"},
        )

    _ensure_panopto_package(root)

    parser = argparse.ArgumentParser(description="Run PANOPTO local server.")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Bind port (default: 8000)")
    args = parser.parse_args()

    try:
        from frontend.server import run
    except ModuleNotFoundError as exc:
        missing = str(exc).split("'")[1] if "'" in str(exc) else str(exc)
        print(
            f"Missing dependency: {missing}\n"
            "Install dependencies with:\n"
            "  python3 -m pip install -r requirements.txt",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc

    run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
