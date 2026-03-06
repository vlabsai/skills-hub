#!/usr/bin/env python3
"""Generate images via FLUX models (FLUX.2 Pro, FLUX.2 Flex) through OpenRouter.

Usage:
    # Generate single image
    python flux.py generate --prompt "PROMPT" --output-dir DIR [options]

    # Batch variations
    python flux.py batch --prompt "PROMPT" --output-dir DIR --count 5 [options]

Environment:
    OPENROUTER_API_KEY - Required.

Note: FLUX models are generation-only (no image editing support).
"""

import argparse
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' required. Run with: uv run --with requests python3 flux.py ...")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).parent))
from utils import get_api_key, save_base64_image, extract_image_b64, ensure_output_dir, generate_filename

API_URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = {
    "pro": "black-forest-labs/flux.2-pro",
    "flex": "black-forest-labs/flux.2-flex",
}

VALID_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]


def call_api(prompt: str, api_key: str, model_key: str = "pro", aspect_ratio: str = "1:1") -> dict:
    """Call OpenRouter FLUX endpoint."""
    model = MODELS.get(model_key, MODELS["pro"])
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image"],
        "image_config": {
            "aspect_ratio": aspect_ratio,
        },
    }
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=180)
    resp.raise_for_status()
    return resp.json()


def generate_single(prompt: str, api_key: str, output_path: Path,
                     model_key: str = "pro", aspect_ratio: str = "1:1") -> bool:
    """Generate single image. Returns True on success."""
    response = call_api(prompt, api_key, model_key, aspect_ratio)
    b64 = extract_image_b64(response)
    if not b64:
        print(f"  WARNING: No image in response for {output_path.name}")
        return False
    return save_base64_image(b64, output_path)


def cmd_generate(args):
    api_key = get_api_key("openrouter")
    out_dir = ensure_output_dir(args.output_dir)
    output_path = out_dir / f"{args.prefix}.png"

    model_name = MODELS.get(args.model, args.model)
    print(f"Generating with {model_name} | ratio={args.aspect_ratio}")
    print(f"Output: {output_path}")

    if generate_single(args.prompt, api_key, output_path, args.model, args.aspect_ratio):
        size_kb = output_path.stat().st_size / 1024
        print(f"OK ({size_kb:.0f} KB)")
    else:
        print("FAILED")
        sys.exit(1)


def cmd_batch(args):
    api_key = get_api_key("openrouter")
    out_dir = ensure_output_dir(args.output_dir)

    model_name = MODELS.get(args.model, args.model)
    print(f"Generating {args.count} variations with {model_name} | ratio={args.aspect_ratio}")
    print(f"Output: {out_dir}\n")

    success = 0
    for i in range(1, args.count + 1):
        filename = generate_filename(args.prefix, i)
        output_path = out_dir / filename
        print(f"[{i}/{args.count}] {filename}...", end=" ", flush=True)

        try:
            if generate_single(args.prompt, api_key, output_path, args.model, args.aspect_ratio):
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
    parser = argparse.ArgumentParser(description="FLUX image generation via OpenRouter")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common(p):
        p.add_argument("--prompt", required=True, help="Generation prompt")
        p.add_argument("--output-dir", required=True, help="Output directory")
        p.add_argument("--aspect-ratio", default="1:1", choices=VALID_RATIOS)
        p.add_argument("--model", default="pro", choices=["pro", "flex"],
                       help="FLUX variant: pro (high quality) or flex (fast/cheap)")
        p.add_argument("--prefix", default="img", help="Filename prefix")

    gen = sub.add_parser("generate", help="Generate single image")
    add_common(gen)
    gen.set_defaults(func=cmd_generate)

    bat = sub.add_parser("batch", help="Generate multiple variations")
    add_common(bat)
    bat.add_argument("--count", type=int, default=5, help="Number of variations")
    bat.set_defaults(func=cmd_batch)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
