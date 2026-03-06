#!/usr/bin/env python3
"""Build an HTML preview gallery from generated images.

Usage:
    python preview_gallery.py --input-dir DIR [--output FILE] [--title TITLE]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import build_preview_html


def main():
    parser = argparse.ArgumentParser(description="Build HTML image preview gallery")
    parser.add_argument("--input-dir", required=True, help="Directory containing generated images")
    parser.add_argument("--output", default=None, help="Output HTML file (default: input-dir/preview.html)")
    parser.add_argument("--title", default="Generated Images", help="Gallery title")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"ERROR: Directory not found: {input_dir}")
        sys.exit(1)

    output_path = Path(args.output) if args.output else input_dir / "preview.html"
    html = build_preview_html(input_dir, args.title)
    output_path.write_text(html)
    print(f"Gallery saved to {output_path}")


if __name__ == "__main__":
    main()
