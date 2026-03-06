#!/usr/bin/env python3
"""Remove background from logo images using rembg (local, no API key).

Usage:
    python remove_bg.py INPUT OUTPUT [--model birefnet-general]

First run downloads the model (~170MB). Subsequent runs are instant.
"""

import argparse
import sys

try:
    from rembg import remove
    from PIL import Image
except ImportError:
    print("ERROR: 'rembg' and 'Pillow' are required.")
    print("Install with: pip install rembg Pillow")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Remove background from logo images")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path (PNG with transparency)")
    parser.add_argument("--model", default="birefnet-general",
                        help="rembg model (default: birefnet-general)")
    args = parser.parse_args()

    print(f"Removing background from {args.input}...")
    img = Image.open(args.input)
    result = remove(img, session_name=args.model)
    result.save(args.output)
    size_kb = result.size[0] * result.size[1]  # just for display
    print(f"Done: {args.output} ({result.width}x{result.height})")


if __name__ == "__main__":
    main()
