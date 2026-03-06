#!/usr/bin/env python3
"""Generate logo variations via OpenRouter (Nano Banana 2 / Gemini 3.1 Flash Image Preview).

Usage:
    python batch_generate.py --prompt "PROMPT" --output-dir DIR [--count 10] [--workers 5] [--aspect-ratio 1:1] [--size 1K] [--prefix logo]

Environment:
    OPENROUTER_API_KEY - Required. OpenRouter API key.
"""

import argparse
import base64
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' is required. Install with: pip install requests")
    sys.exit(1)

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-3.1-flash-image-preview"
VALID_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]
VALID_SIZES = ["1K", "2K", "4K"]


def generate_image(prompt: str, api_key: str, aspect_ratio: str = "1:1", size: str = "1K") -> dict:
    """Call OpenRouter to generate a single image. Returns parsed JSON response."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"],
        "image_config": {
            "aspect_ratio": aspect_ratio,
            "image_size": size,
        },
    }
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()


def extract_and_save(response: dict, output_path: Path) -> bool:
    """Extract base64 image from response and save as PNG. Returns True on success."""
    try:
        message = response["choices"][0]["message"]
        images = message.get("images", [])
        if not images:
            # Some models embed image in content parts
            content = message.get("content", "")
            if isinstance(content, list):
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "image_url":
                        images.append(part)
            if not images:
                print(f"  WARNING: No image in response for {output_path.name}")
                return False

        data_url = images[0]["image_url"]["url"]
        # Strip data URI prefix: "data:image/png;base64,..."
        if "," in data_url:
            b64_data = data_url.split(",", 1)[1]
        else:
            b64_data = data_url

        img_bytes = base64.b64decode(b64_data)
        output_path.write_bytes(img_bytes)
        return True
    except (KeyError, IndexError) as e:
        print(f"  ERROR parsing response: {e}")
        return False


def generate_one(index: int, total: int, prompt: str, api_key: str, output_path: Path, aspect_ratio: str, size: str) -> tuple[int, str, bool]:
    """Generate a single image. Returns (index, filename, success)."""
    filename = output_path.name
    try:
        response = generate_image(prompt, api_key, aspect_ratio, size)
        if extract_and_save(response, output_path):
            size_kb = output_path.stat().st_size / 1024
            print(f"  [{index}/{total}] {filename} OK ({size_kb:.0f} KB)", flush=True)
            return (index, filename, True)
        else:
            print(f"  [{index}/{total}] {filename} FAILED (no image in response)", flush=True)
            return (index, filename, False)
    except requests.exceptions.HTTPError as e:
        print(f"  [{index}/{total}] {filename} FAILED ({e.response.status_code}: {e.response.text[:200]})", flush=True)
        return (index, filename, False)
    except Exception as e:
        print(f"  [{index}/{total}] {filename} FAILED ({e})", flush=True)
        return (index, filename, False)


def main():
    parser = argparse.ArgumentParser(description="Batch-generate logo variations via OpenRouter")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--output-dir", required=True, help="Directory to save generated images")
    parser.add_argument("--count", type=int, default=10, help="Number of variations (default: 10)")
    parser.add_argument("--workers", type=int, default=5, help="Parallel workers (default: 5, use 1 for sequential)")
    parser.add_argument("--aspect-ratio", default="1:1", choices=VALID_RATIOS, help="Aspect ratio")
    parser.add_argument("--size", default="1K", choices=VALID_SIZES, help="Image size")
    parser.add_argument("--prefix", default="logo", help="Filename prefix (default: logo)")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY environment variable is required.")
        sys.exit(1)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    workers = min(args.workers, args.count)
    print(f"Generating {args.count} variations | workers={workers} | ratio={args.aspect_ratio} size={args.size}")
    print(f"Output: {out_dir}\n")

    success = 0
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {}
        for i in range(1, args.count + 1):
            filename = f"{args.prefix}-{i:02d}.png"
            output_path = out_dir / filename
            future = pool.submit(generate_one, i, args.count, args.prompt, api_key, output_path, args.aspect_ratio, args.size)
            futures[future] = i

        for future in as_completed(futures):
            _, _, ok = future.result()
            if ok:
                success += 1

    elapsed = time.time() - start_time
    print(f"\nDone: {success}/{args.count} images generated in {out_dir} ({elapsed:.1f}s)")


if __name__ == "__main__":
    main()
