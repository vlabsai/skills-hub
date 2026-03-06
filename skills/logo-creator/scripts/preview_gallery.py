#!/usr/bin/env python3
"""Generate an interactive HTML gallery to compare logo variations.

Usage:
    python preview_gallery.py --input-dir DIR --output FILE [--title "Project Name"]
"""

import argparse
import base64
import sys
from pathlib import Path


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title} - Logo Preview</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0a0a0a; color: #e0e0e0; padding: 2rem; }}
  h1 {{ font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }}
  .subtitle {{ color: #888; margin-bottom: 2rem; font-size: 0.9rem; }}
  .controls {{ display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }}
  .controls button {{ padding: 0.5rem 1rem; border: 1px solid #333; background: #1a1a1a; color: #ccc; border-radius: 6px; cursor: pointer; font-size: 0.85rem; transition: all 0.2s; }}
  .controls button:hover {{ background: #2a2a2a; border-color: #555; }}
  .controls button.active {{ background: #2a4a2a; border-color: #4a8a4a; color: #8f8; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }}
  .card {{ background: #141414; border: 1px solid #222; border-radius: 12px; overflow: hidden; transition: all 0.2s; position: relative; }}
  .card:hover {{ border-color: #444; transform: translateY(-2px); }}
  .card.selected {{ border-color: #4a8a4a; box-shadow: 0 0 20px rgba(74, 138, 74, 0.15); }}
  .card img {{ width: 100%; aspect-ratio: 1; object-fit: contain; padding: 1.5rem; }}
  .card .bg-checker {{ background: repeating-conic-gradient(#1a1a1a 0% 25%, #222 0% 50%) 50%/20px 20px; }}
  .card .bg-white {{ background: #fff; }}
  .card .bg-dark {{ background: #0a0a0a; }}
  .card-footer {{ padding: 0.75rem 1rem; border-top: 1px solid #222; display: flex; justify-content: space-between; align-items: center; }}
  .card-footer .name {{ font-size: 0.85rem; font-weight: 500; }}
  .card-footer .size {{ font-size: 0.75rem; color: #666; }}
  .badge {{ position: absolute; top: 0.75rem; right: 0.75rem; background: #4a8a4a; color: #fff; font-size: 0.7rem; padding: 0.2rem 0.5rem; border-radius: 4px; display: none; }}
  .card.selected .badge {{ display: block; }}
</style>
</head>
<body>
<h1>{title}</h1>
<p class="subtitle">{count} variations | Click to select favorites</p>
<div class="controls">
  <button onclick="setBg('bg-checker')" class="active">Checker</button>
  <button onclick="setBg('bg-white')">White</button>
  <button onclick="setBg('bg-dark')">Dark</button>
</div>
<div class="grid" id="gallery">{cards}</div>
<script>
function setBg(cls) {{
  document.querySelectorAll('.card img').forEach(img => {{
    img.className = cls;
  }});
  document.querySelectorAll('.controls button').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
}}
document.querySelectorAll('.card').forEach(card => {{
  card.addEventListener('click', () => card.classList.toggle('selected'));
}});
</script>
</body>
</html>"""

CARD_TEMPLATE = """
<div class="card">
  <span class="badge">Selected</span>
  <img src="data:image/png;base64,{b64}" class="bg-checker" alt="{name}">
  <div class="card-footer">
    <span class="name">{name}</span>
    <span class="size">{size}</span>
  </div>
</div>"""


def main():
    parser = argparse.ArgumentParser(description="Generate HTML logo preview gallery")
    parser.add_argument("--input-dir", required=True, help="Directory with logo PNGs")
    parser.add_argument("--output", required=True, help="Output HTML file path")
    parser.add_argument("--title", default="Logo Preview", help="Gallery title")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    images = sorted(input_dir.glob("*.png"))

    if not images:
        print(f"No PNG files found in {input_dir}")
        sys.exit(1)

    cards = []
    for img_path in images:
        b64 = base64.b64encode(img_path.read_bytes()).decode()
        size_kb = img_path.stat().st_size / 1024
        size_str = f"{size_kb:.0f} KB" if size_kb < 1024 else f"{size_kb/1024:.1f} MB"
        cards.append(CARD_TEMPLATE.format(b64=b64, name=img_path.name, size=size_str))

    html = HTML_TEMPLATE.format(title=args.title, count=len(images), cards="".join(cards))

    Path(args.output).write_text(html)
    print(f"Gallery created: {args.output} ({len(images)} images)")


if __name__ == "__main__":
    main()
