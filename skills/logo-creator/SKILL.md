---
name: logo-creator
description: >-
  Gera logos com workflow iterativo de design assistido por IA. Cria
  variacoes, processa finalistas com crop, remocao de fundo e vetorizacao
  para SVG. Entrega assets prontos para producao (PNG recortado, PNG
  transparente, SVG escalavel).
license: Apache-2.0
compatibility: Requires Python, uv, OPENROUTER_API_KEY
allowed-tools: Bash Read Write Glob
metadata:
  author: vector-labs
  version: "1.0"
tags: [design, branding]
complexity: intermediate
---

# Logo Creator

Generate professional logo variations using AI, then process selected finalists into production-ready assets (cropped PNG, transparent PNG, scalable SVG).

## Setup

All scripts use `uv run` with inline dependencies — no manual install needed.

### Environment

```bash
export OPENROUTER_API_KEY="your-openrouter-api-key"
```

## Running Scripts

All script paths below are relative to this skill's directory. Prefix every script invocation as follows:

- **batch_generate.py, crop_logo.py, preview_gallery.py**: `uv run --with requests --with Pillow python3 scripts/SCRIPT.py`
- **remove_bg.py**: `uv run --with "rembg>=2.0.57" --with Pillow --with onnxruntime --python 3.10 python3 scripts/remove_bg.py` (requires Python 3.10 due to numba)
- **vectorize.py**: `uv run --with vtracer python3 scripts/vectorize.py`

## Workflow

### Step 1: Gather Brief

Collect from the user:
- **Brand/project name** and what it does
- **Style direction**: minimalist, geometric, wordmark, lettermark, mascot, abstract, pixel art, 3D, etc.
- **Color preferences**: specific hex codes, palette direction, or "surprise me"
- **Aspect ratio**: 1:1 (default), 16:9, 3:2, etc.
- **Reference images or logos** they like (optional)
- **Must include/exclude**: specific symbols, letters, concepts

Craft a detailed prompt. Good prompts specify: subject, style, colors, composition, and what to avoid. Example:
> "Minimalist geometric logo for a tech consulting firm called 'Vector Labs'. Abstract V shape formed by intersecting lines. Colors: deep navy (#1a2332) and electric blue (#4a9eff) on white background. Clean, professional, no gradients. Flat design suitable for both dark and light backgrounds."

### Step 2: Generate 10 Variations

```bash
PROJECT=.skill-archive/logo-creator/$(date +%Y-%m-%d)-projectname
mkdir -p $PROJECT

OPENROUTER_API_KEY="your-openrouter-api-key" \
uv run --with requests --with Pillow python3 scripts/batch_generate.py \
  --prompt "YOUR DETAILED PROMPT" \
  --output-dir $PROJECT \
  --count 10 \
  --workers 5 \
  --aspect-ratio 1:1 \
  --size 1K \
  --prefix logo
```

### Step 3: Build Preview Gallery

```bash
uv run --with Pillow python3 scripts/preview_gallery.py \
  --input-dir $PROJECT \
  --output $PROJECT/preview.html \
  --title "Project Name"
```

Open `preview.html` in browser. User clicks cards to mark favorites. Gallery supports checker/white/dark background toggle.

Ask the user which logos to **keep**, **iterate on**, or **discard**.

### Step 4: Iterate (if needed)

Generate refined variations with adjusted prompts and version suffixes:

```bash
OPENROUTER_API_KEY="your-openrouter-api-key" \
uv run --with requests --with Pillow python3 scripts/batch_generate.py \
  --prompt "REFINED PROMPT" \
  --output-dir $PROJECT \
  --count 5 \
  --prefix logo-v2
```

Rebuild gallery after each round. Repeat until user approves finalist(s).

### Step 5: Finalize Selected Logos

For each approved logo, run three processing steps:

**Crop whitespace:**
```bash
uv run --with Pillow python3 scripts/crop_logo.py \
  INPUT.png OUTPUT-cropped.png --ratio 1:1 --padding 20
```

**Remove background:**
```bash
uv run --with "rembg>=2.0.57" --with Pillow --with onnxruntime --python 3.10 \
  python3 scripts/remove_bg.py INPUT.png OUTPUT-transparent.png
```

First run downloads ~170MB model. Subsequent runs are instant.

**Vectorize to SVG:**
```bash
uv run --with vtracer python3 scripts/vectorize.py \
  INPUT-transparent.png OUTPUT.svg --detail medium --colormode color
```

Detail presets: `low` (simpler/smaller), `medium` (balanced), `high` (finest detail).

### Step 6: Deliver Final Assets

```
projectname/
  logo-03.png              # Original generation
  logo-03-cropped.png      # Whitespace removed, 1:1
  logo-03-transparent.png  # Background removed
  logo-03.svg              # Scalable vector
```

## Script Reference

| Script | Purpose | Key args |
|--------|---------|----------|
| `batch_generate.py` | Generate variations via OpenRouter | `--prompt`, `--count 10`, `--workers 5`, `--aspect-ratio`, `--size` |
| `crop_logo.py` | Remove whitespace, enforce ratio | `--ratio 1:1`, `--padding 20` |
| `remove_bg.py` | Remove background (local AI) | `--model birefnet-general` |
| `vectorize.py` | PNG to SVG conversion | `--detail low/medium/high`, `--colormode color/binary` |
| `preview_gallery.py` | HTML comparison gallery | `--input-dir`, `--title` |

## Prompt Crafting Tips

- Be specific about style: "flat minimalist" not just "modern"
- Mention negative constraints: "no gradients, no text, no 3D effects"
- Specify background: "on pure white background" or "on transparent background"
- For wordmarks, spell out the exact text: "the word 'ACME' in..."
- Request multiple concepts in one prompt: "Option A: abstract mark. Option B: lettermark"
- Aspect ratio 1:1 works best for icon-style logos; 3:2 or 16:9 for horizontal wordmarks
