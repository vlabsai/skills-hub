#!/usr/bin/env python3
"""Shared utilities for generative-media scripts.

Handles: API key resolution, image saving, filename generation, preview gallery.
"""

import base64
import os
import sys
from datetime import datetime
from pathlib import Path

# --- API Key Resolution ---

def get_api_key(provider: str) -> str:
    """Resolve API key for the given provider. Exits on failure."""
    env_map = {
        "openrouter": "OPENROUTER_API_KEY",
        "gemini": "GEMINI_API_KEY",
    }
    env_var = env_map.get(provider)
    if not env_var:
        print(f"ERROR: Unknown provider '{provider}'")
        sys.exit(1)
    key = os.environ.get(env_var)
    if not key:
        print(f"ERROR: {env_var} environment variable is required.")
        sys.exit(1)
    return key


# --- File Handling ---

def generate_filename(prefix: str, index: int, ext: str = "png") -> str:
    """Generate a numbered filename: prefix-01.png"""
    return f"{prefix}-{index:02d}.{ext}"


def save_base64_image(b64_data: str, output_path: Path) -> bool:
    """Decode base64 image data and save to file. Returns True on success."""
    try:
        # Strip data URI prefix if present
        if "," in b64_data:
            b64_data = b64_data.split(",", 1)[1]
        img_bytes = base64.b64decode(b64_data)
        output_path.write_bytes(img_bytes)
        return True
    except Exception as e:
        print(f"  ERROR saving image: {e}")
        return False


def ensure_output_dir(path: str) -> Path:
    """Create output directory if needed, return Path object."""
    out = Path(path)
    out.mkdir(parents=True, exist_ok=True)
    return out


# --- Response Parsing ---

def extract_image_b64(response: dict) -> str | None:
    """Extract base64 image data from OpenRouter chat completion response."""
    try:
        message = response["choices"][0]["message"]

        # Method 1: images array (Nano Banana style)
        images = message.get("images", [])
        if images:
            return images[0]["image_url"]["url"]

        # Method 2: content parts with image_url
        content = message.get("content", "")
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "image_url":
                    return part["image_url"]["url"]

        # Method 3: inline_data in content parts (Gemini native)
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and "inline_data" in part:
                    return part["inline_data"].get("data")

        return None
    except (KeyError, IndexError):
        return None


def extract_text_response(response: dict) -> str | None:
    """Extract text content from response (useful for edit responses that include text)."""
    try:
        message = response["choices"][0]["message"]
        content = message.get("content", "")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            texts = [p.get("text", "") for p in content if isinstance(p, dict) and p.get("type") == "text"]
            return "\n".join(texts) if texts else None
        return None
    except (KeyError, IndexError):
        return None


# --- Preview Gallery ---

def build_preview_html(image_dir: Path, title: str = "Generated Images") -> str:
    """Build an HTML preview gallery for images in a directory."""
    images = sorted(image_dir.glob("*.png"))
    if not images:
        return "<html><body><p>No images found.</p></body></html>"

    cards = []
    for img in images:
        b64 = base64.b64encode(img.read_bytes()).decode()
        cards.append(f"""
        <div class="card" onclick="this.classList.toggle('selected')">
            <img src="data:image/png;base64,{b64}" alt="{img.name}">
            <div class="name">{img.name}</div>
            <div class="size">{img.stat().st_size / 1024:.0f} KB</div>
        </div>""")

    return f"""<!DOCTYPE html>
<html><head>
<title>{title}</title>
<style>
body {{ font-family: system-ui; background: #1a1a1a; color: #fff; padding: 20px; }}
h1 {{ text-align: center; font-weight: 300; }}
.controls {{ text-align: center; margin: 20px 0; }}
.controls button {{ padding: 8px 16px; margin: 0 4px; border: 1px solid #555; background: #333; color: #fff; border-radius: 6px; cursor: pointer; }}
.controls button.active {{ background: #4a9eff; border-color: #4a9eff; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }}
.card {{ border: 2px solid transparent; border-radius: 12px; overflow: hidden; cursor: pointer; transition: all 0.2s; background: #222; }}
.card:hover {{ border-color: #555; }}
.card.selected {{ border-color: #4a9eff; box-shadow: 0 0 20px rgba(74,158,255,0.3); }}
.card img {{ width: 100%; display: block; }}
.name {{ padding: 8px 12px 2px; font-size: 14px; font-weight: 500; }}
.size {{ padding: 2px 12px 8px; font-size: 12px; color: #888; }}
.bg-checker {{ background-image: repeating-conic-gradient(#808080 0% 25%, transparent 0% 50%); background-size: 20px 20px; }}
.bg-white .card img {{ background: #fff; }}
.bg-dark .card img {{ background: #000; }}
</style>
</head><body>
<h1>{title}</h1>
<div class="controls">
    <button onclick="setbg('')" class="active">Default</button>
    <button onclick="setbg('bg-checker')">Checker</button>
    <button onclick="setbg('bg-white')">White</button>
    <button onclick="setbg('bg-dark')">Dark</button>
</div>
<div class="grid" id="grid">{"".join(cards)}</div>
<script>
function setbg(c) {{
    const g = document.getElementById('grid');
    g.className = 'grid ' + c;
    document.querySelectorAll('.controls button').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
}}
</script>
</body></html>"""
