#!/usr/bin/env python3
"""Generate or edit images via Nano Banana 2 (Gemini 3.1 Flash Image) through OpenRouter.

Usage:
    # Generate new image
    python nano_banana.py generate --prompt "PROMPT" --output-dir DIR [options]

    # Edit existing image
    python nano_banana.py edit --prompt "INSTRUCTIONS" --input IMAGE --output-dir DIR [options]

    # Generate batch variations
    python nano_banana.py batch --prompt "PROMPT" --output-dir DIR --count 5 [options]

Environment:
    OPENROUTER_API_KEY - Required.
"""

import argparse
import base64
import json
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' required. Run with: uv run --with requests python3 nano_banana.py ...")
    sys.exit(1)

# Import shared utils (same directory)
sys.path.insert(0, str(Path(__file__).parent))
from utils import get_api_key, save_base64_image, extract_image_b64, ensure_output_dir, generate_filename

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-3.1-flash-image-preview"
VALID_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]
VALID_SIZES = ["1K", "2K", "4K"]


def call_api(messages: list, api_key: str, aspect_ratio: str = "1:1", size: str = "1K") -> dict:
    """Call OpenRouter Nano Banana endpoint. Returns raw JSON response."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "modalities": ["image", "text"],
        "image_config": {
            "aspect_ratio": aspect_ratio,
            "image_size": size,
        },
    }
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=180)
    resp.raise_for_status()
    return resp.json()


def generate_single(prompt: str, api_key: str, output_path: Path,
                     aspect_ratio: str = "1:1", size: str = "1K") -> bool:
    """Generate a single image. Returns True on success."""
    messages = [{"role": "user", "content": prompt}]
    response = call_api(messages, api_key, aspect_ratio, size)
    b64 = extract_image_b64(response)
    if not b64:
        print(f"  WARNING: No image in response for {output_path.name}")
        return False
    return save_base64_image(b64, output_path)


def edit_image(prompt: str, input_path: Path, api_key: str, output_path: Path,
               aspect_ratio: str = "1:1", size: str = "1K") -> bool:
    """Edit an existing image with instructions. Returns True on success."""
    if not input_path.exists():
        print(f"ERROR: Input image not found: {input_path}")
        return False

    img_bytes = input_path.read_bytes()
    b64_img = base64.b64encode(img_bytes).decode()
    mime = "image/png" if input_path.suffix.lower() == ".png" else "image/jpeg"

    messages = [{
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {"url": f"data:{mime};base64,{b64_img}"}
            },
            {
                "type": "text",
                "text": prompt
            }
        ]
    }]

    response = call_api(messages, api_key, aspect_ratio, size)
    b64 = extract_image_b64(response)
    if not b64:
        print(f"  WARNING: No image in edit response")
        return False
    return save_base64_image(b64, output_path)


def cmd_generate(args):
    api_key = get_api_key("openrouter")
    out_dir = ensure_output_dir(args.output_dir)
    output_path = out_dir / f"{args.prefix}.png"

    print(f"Generating | ratio={args.aspect_ratio} size={args.size}")
    print(f"Output: {output_path}")

    if generate_single(args.prompt, api_key, output_path, args.aspect_ratio, args.size):
        size_kb = output_path.stat().st_size / 1024
        print(f"OK ({size_kb:.0f} KB)")
    else:
        print("FAILED")
        sys.exit(1)


def cmd_edit(args):
    api_key = get_api_key("openrouter")
    out_dir = ensure_output_dir(args.output_dir)
    input_path = Path(args.input)
    output_path = out_dir / f"{args.prefix}-edited.png"

    print(f"Editing {input_path.name} | ratio={args.aspect_ratio} size={args.size}")
    print(f"Output: {output_path}")

    if edit_image(args.prompt, input_path, api_key, output_path, args.aspect_ratio, args.size):
        size_kb = output_path.stat().st_size / 1024
        print(f"OK ({size_kb:.0f} KB)")
    else:
        print("FAILED")
        sys.exit(1)


def cmd_batch(args):
    api_key = get_api_key("openrouter")
    out_dir = ensure_output_dir(args.output_dir)

    print(f"Generating {args.count} variations | ratio={args.aspect_ratio} size={args.size}")
    print(f"Output: {out_dir}\n")

    success = 0
    for i in range(1, args.count + 1):
        filename = generate_filename(args.prefix, i)
        output_path = out_dir / filename
        print(f"[{i}/{args.count}] {filename}...", end=" ", flush=True)

        try:
            if generate_single(args.prompt, api_key, output_path, args.aspect_ratio, args.size):
                size_kb = output_path.stat().st_size / 1024
                print(f"OK ({size_kb:.0f} KB)")
                success += 1
            else:
                print("FAILED (no image)")
        except requests.exceptions.HTTPError as e:
            print(f"FAILED ({e.response.status_code}: {e.response.text[:200]})")
        except Exception as e:
            print(f"FAILED ({e})")

        if i < args.count:
            time.sleep(1)

    print(f"\nDone: {success}/{args.count} images in {out_dir}")


def main():
    parser = argparse.ArgumentParser(description="Nano Banana 2 (Gemini 3.1 Flash) image generation")
    sub = parser.add_subparsers(dest="command", required=True)

    # Shared args
    def add_common(p):
        p.add_argument("--prompt", required=True, help="Generation prompt or edit instructions")
        p.add_argument("--output-dir", required=True, help="Output directory")
        p.add_argument("--aspect-ratio", default="1:1", choices=VALID_RATIOS)
        p.add_argument("--size", default="1K", choices=VALID_SIZES, help="1K, 2K, or 4K")
        p.add_argument("--prefix", default="img", help="Filename prefix")

    # generate
    gen = sub.add_parser("generate", help="Generate single image")
    add_common(gen)
    gen.set_defaults(func=cmd_generate)

    # edit
    ed = sub.add_parser("edit", help="Edit existing image")
    add_common(ed)
    ed.add_argument("--input", required=True, help="Path to input image")
    ed.set_defaults(func=cmd_edit)

    # batch
    bat = sub.add_parser("batch", help="Generate multiple variations")
    add_common(bat)
    bat.add_argument("--count", type=int, default=5, help="Number of variations")
    bat.set_defaults(func=cmd_batch)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
