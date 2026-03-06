---
name: generative-media
description: >-
  Gera e edita imagens usando modelos de IA via OpenRouter (FLUX.2 Pro,
  FLUX.2 Flex, Nano Banana 2). Suporta geracao texto-para-imagem, edicao,
  variacoes em lote e pos-processamento. Use para criar ilustracoes, arte e
  graficos para redes sociais.
license: Apache-2.0
compatibility: Requires Python, uv, OPENROUTER_API_KEY
allowed-tools: Bash Read Write Glob
metadata:
  author: vector-labs
  version: "1.0"
tags: [images, ai, media]
complexity: intermediate
---

# Generative Media

Generate and edit images using AI models via OpenRouter. Supports multiple models with shared prompting knowledge and dedicated per-model scripts.

## Setup

All scripts use `uv run` with inline deps — no install needed.

```bash
export OPENROUTER_API_KEY="your-key-here"
```

All script paths below are relative to this skill's directory. Run as:
```bash
uv run --with requests python3 scripts/SCRIPT.py COMMAND [args]
```

## Model Selection

| Need | Model | Why |
|------|-------|-----|
| Edit existing image | Nano Banana | Only model with editing |
| Text in image | Nano Banana | Best text rendering |
| 2K/4K resolution | Nano Banana | Only model with size tiers |
| Artistic/illustration | FLUX.2 Pro | Strongest creative styles |
| Fast cheap exploration | FLUX.2 Flex | $0.02/img, 2-5s |
| Default / general | Nano Banana | Most versatile |

Full comparison: [references/models/index.md](references/models/index.md)

## Workflow

### 1. Understand the Request

Clarify with the user:
- **What**: Subject, scene, or concept
- **Style**: Photo, illustration, painting, flat vector, etc.
- **Where it goes**: Social media, hero banner, print, icon (determines aspect ratio + resolution)
- **Edit or new**: Generating from scratch or modifying an existing image?
- **Reference**: Any images or styles they like?

### 2. Choose Model

Use the model selection table above. When unsure, default to Nano Banana.

### 3. Craft the Prompt

Build the prompt using this structure:
```
[Subject] + [Style] + [Composition] + [Lighting/Color] + [Constraints]
```

Key differences by model:
- **Nano Banana 2**: Natural language, conversational prompts. "Create a cozy scene with..."
- **FLUX**: Keyword-driven, comma-separated descriptors. "cozy cafe, warm lighting, 35mm film..."

Full prompting guide: [references/prompting.md](references/prompting.md)

**Quick prompt examples:**

Product shot:
> Minimalist ceramic vase with dried eucalyptus, product photography, soft studio lighting, white background, centered, no text

Social media graphic:
> Abstract geometric pattern with navy (#1a2332) and coral (#ff6b6b) shapes, modern minimalist style, 1:1 square composition, clean edges

Hero banner:
> Aerial view of a winding mountain road through autumn forest, golden hour lighting, cinematic wide shot, warm color palette, 16:9

### 4. Generate

**Single image:**
```bash
OPENROUTER_API_KEY="..." uv run --with requests python3 scripts/nano_banana.py generate \
  --prompt "YOUR PROMPT" --output-dir ./output --aspect-ratio 16:9 --size 2K --prefix hero
```

**Batch variations (for exploration):**
```bash
OPENROUTER_API_KEY="..." uv run --with requests python3 scripts/nano_banana.py batch \
  --prompt "YOUR PROMPT" --output-dir ./output --count 6 --prefix explore
```

**Edit existing image:**
```bash
OPENROUTER_API_KEY="..." uv run --with requests python3 scripts/nano_banana.py edit \
  --prompt "EDIT INSTRUCTIONS" --input source.png --output-dir ./output --prefix edited
```

**FLUX generation:**
```bash
OPENROUTER_API_KEY="..." uv run --with requests python3 scripts/flux.py batch \
  --prompt "YOUR PROMPT" --output-dir ./output --model pro --count 4
```

### 5. Review & Iterate

Build a preview gallery to compare results:
```bash
uv run --with Pillow python3 scripts/preview_gallery.py \
  --input-dir ./output --title "Project Name"
```

Open `preview.html` in browser. Ask user which to keep, iterate, or discard.

**Iteration tips:**
- Keep what works, describe what to change
- Add constraints to remove unwanted elements: "no text, no watermarks"
- Try a different model if current one struggles with the style
- Use `--prefix v2` for iteration rounds

### 6. Post-Processing (if needed)

For post-processing (background removal, format conversion, SVG vectorization): [references/techniques/upscaling.md](references/techniques/upscaling.md)

## Script Reference

| Script | Purpose | Key Commands |
|--------|---------|-------------|
| `nano_banana.py` | Gemini 3.1 Flash generation + editing | `generate`, `edit`, `batch` |
| `flux.py` | FLUX.2 Pro/Flex generation | `generate`, `batch` |
| `preview_gallery.py` | HTML comparison gallery | `--input-dir`, `--title` |
| `utils.py` | Shared utilities | (imported by other scripts) |

## Model-Specific Guides

- [Nano Banana details](references/models/nano-banana.md) — Prompting tips, editing, resolution tiers
- [FLUX details](references/models/flux.md) — Pro vs Flex, keyword-driven prompting
- [Editing techniques](references/techniques/editing.md) — Background removal, color changes, style transfer
