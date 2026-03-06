#!/usr/bin/env python3
"""Crop whitespace from logo images and optionally enforce a target aspect ratio.

Usage:
    python crop_logo.py INPUT OUTPUT [--ratio 1:1] [--padding 20]
"""

import argparse
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    print("ERROR: 'Pillow' is required. Install with: pip install Pillow")
    sys.exit(1)


def crop_whitespace(img: Image.Image, padding: int = 20) -> Image.Image:
    """Remove whitespace borders, then add uniform padding."""
    # Convert to RGBA to handle transparency
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Get bounding box of non-transparent/non-white content
    bbox = img.getbbox()
    if bbox is None:
        return img

    cropped = img.crop(bbox)

    # Add padding
    new_w = cropped.width + padding * 2
    new_h = cropped.height + padding * 2
    padded = Image.new("RGBA", (new_w, new_h), (255, 255, 255, 0))
    padded.paste(cropped, (padding, padding))
    return padded


def enforce_ratio(img: Image.Image, ratio: str) -> Image.Image:
    """Pad image to match target aspect ratio (centered)."""
    w_ratio, h_ratio = map(int, ratio.split(":"))
    target = w_ratio / h_ratio

    current = img.width / img.height

    if abs(current - target) < 0.01:
        return img

    if current < target:
        # Too tall, widen
        new_w = int(img.height * target)
        new_h = img.height
    else:
        # Too wide, heighten
        new_w = img.width
        new_h = int(img.width / target)

    result = Image.new("RGBA", (new_w, new_h), (255, 255, 255, 0))
    x = (new_w - img.width) // 2
    y = (new_h - img.height) // 2
    result.paste(img, (x, y))
    return result


def main():
    parser = argparse.ArgumentParser(description="Crop whitespace from logo images")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path")
    parser.add_argument("--ratio", default=None, help="Target aspect ratio (e.g. 1:1)")
    parser.add_argument("--padding", type=int, default=20, help="Padding in pixels (default: 20)")
    args = parser.parse_args()

    img = Image.open(args.input)
    img = crop_whitespace(img, args.padding)

    if args.ratio:
        img = enforce_ratio(img, args.ratio)

    img.save(args.output)
    print(f"Cropped: {args.output} ({img.width}x{img.height})")


if __name__ == "__main__":
    main()
