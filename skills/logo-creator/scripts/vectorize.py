#!/usr/bin/env python3
"""Convert raster logo (PNG) to scalable SVG using vtracer.

Usage:
    python vectorize.py INPUT OUTPUT [--colormode color] [--detail medium]

Detail presets:
    low    - Fewer paths, smaller file, simpler shapes
    medium - Balanced (default)
    high   - More paths, larger file, finer detail
"""

import argparse
import sys

try:
    import vtracer
except ImportError:
    print("ERROR: 'vtracer' is required. Install with: pip install vtracer")
    sys.exit(1)

PRESETS = {
    "low": {
        "filter_speckle": 8,
        "color_precision": 4,
        "layer_difference": 32,
        "corner_threshold": 90,
        "length_threshold": 6.0,
        "splice_threshold": 60,
        "path_precision": 3,
    },
    "medium": {
        "filter_speckle": 4,
        "color_precision": 6,
        "layer_difference": 16,
        "corner_threshold": 60,
        "length_threshold": 4.0,
        "splice_threshold": 45,
        "path_precision": 5,
    },
    "high": {
        "filter_speckle": 2,
        "color_precision": 8,
        "layer_difference": 8,
        "corner_threshold": 30,
        "length_threshold": 2.0,
        "splice_threshold": 30,
        "path_precision": 8,
    },
}


def main():
    parser = argparse.ArgumentParser(description="Convert raster logo to SVG")
    parser.add_argument("input", help="Input PNG path")
    parser.add_argument("output", help="Output SVG path")
    parser.add_argument("--colormode", default="color", choices=["color", "binary"],
                        help="Color mode (default: color)")
    parser.add_argument("--detail", default="medium", choices=["low", "medium", "high"],
                        help="Detail level (default: medium)")
    args = parser.parse_args()

    params = PRESETS[args.detail]

    print(f"Vectorizing {args.input} (detail={args.detail}, colormode={args.colormode})...")

    vtracer.convert_image_to_svg_py(
        args.input,
        args.output,
        colormode=args.colormode,
        filter_speckle=params["filter_speckle"],
        color_precision=params["color_precision"],
        layer_difference=params["layer_difference"],
        corner_threshold=params["corner_threshold"],
        length_threshold=params["length_threshold"],
        splice_threshold=params["splice_threshold"],
        path_precision=params["path_precision"],
    )

    from pathlib import Path
    size_kb = Path(args.output).stat().st_size / 1024
    print(f"Done: {args.output} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
