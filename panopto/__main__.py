"""CLI entrypoint for launching the PANOPTO local server."""

from __future__ import annotations

import argparse

from frontend.server import run


def main() -> None:
    parser = argparse.ArgumentParser(description="Run PANOPTO local server.")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Bind port (default: 8000)")
    args = parser.parse_args()
    run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
