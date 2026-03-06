# FLUX Models (Black Forest Labs)

Available via OpenRouter:
- `black-forest-labs/flux.2-pro` — High quality, production-grade
- `black-forest-labs/flux.2-flex` — Fast and economical

Other variants (not on OpenRouter): FLUX.2 Dev (open-weight, local), FLUX.2 Max (flagship), FLUX.2 Klein (lightweight).

## Strengths

- **Artistic/illustration styles**: Exceptional at stylized, creative outputs
- **Prompt adherence**: Very faithful to detailed visual descriptions
- **Speed**: Fast generation, especially Flex variant
- **Photorealism**: FLUX.2 Pro produces highly realistic photos
- **Consistency**: More consistent aesthetic across batch generations
- **HEX color matching**: Supports exact color specification (e.g., "The vase is color #02eb3c")
- **Text rendering**: FLUX.2 Flex is actually strong at typography (better than Pro)

## Weaknesses

- **No image editing**: Generation only — cannot modify existing images
- **No negative prompts**: Fundamental difference from Stable Diffusion. Rephrase negatives as positives.
- **Resolution**: Max 4MP, dimensions must be multiples of 16
- **Limited control via OpenRouter**: Fewer parameters exposed than BFL's direct API

## FLUX.2 Pro vs FLUX.2 Flex

| Aspect | Pro | Flex |
|--------|-----|------|
| Quality | Production-grade, highest fidelity | Good, adjustable via steps |
| Speed | 3-8s | 2-5s |
| Cost | ~$0.05/img | ~$0.02/img |
| Text rendering | Moderate | Best among FLUX variants |
| Best for | Final outputs, hero shots, faces/hands | Exploration, typography, branded content |

**Recommended workflow:** Prototype with Flex → Finalize with Pro for maximum quality.

## Prompting Tips

### No Negative Prompts

This is the single most important difference from Stable Diffusion. FLUX does not support negative prompts. Instead, rephrase as positives:

| Don't say | Say instead |
|-----------|------------|
| "no blur" | "sharp focus throughout" |
| "no extra fingers" | "anatomically correct hands with five fingers" |
| "no watermark" | "clean image without text overlays" |
| "no dark areas" | "well-lit, evenly illuminated scene" |

### Natural Language + Keywords

FLUX responds well to descriptive, structured prompts. Front-load the most important elements:

**Good:**
> Golden retriever puppy sitting in autumn leaves, warm sunlight, shallow depth of field, 35mm film photography, soft bokeh background, eye-level shot

**Also good (more natural):**
> A golden retriever puppy sits in a pile of autumn leaves, bathed in warm sunlight. Shot on 35mm film with shallow depth of field and soft bokeh.

### Prompt Structure for FLUX

```
[Subject description], [style keywords], [lighting], [composition], [technical specs]
```

### HEX Color Control

FLUX supports exact color specification — critical for branded content:

- Object color: "The vase is color #02eb3c"
- Gradients: "starting with color #02eb3c and finishing with color #edfa3c"
- Background: "on a background of color #1a2332"

### Text Rendering

FLUX.2 Flex is strong at typography. For best results:
- Use quotation marks: `The text 'OPEN' appears in red neon letters`
- Specify placement relative to other elements
- Describe font style: "elegant serif," "bold industrial lettering"
- Include color and sizing information

### Photography/Film Stock References

For photorealistic results, reference specific equipment:
- Modern: "shot on Sony A7IV, clean sharp, high dynamic range"
- Vintage: "shot on Kodak Portra 400, natural grain, warm skin tones"
- Commercial: "shot on Hasselblad, medium format, tack sharp"
- Cinematic: "shot on Arri Alexa, cinematic color grade, 2.39:1"
- Specific lens: "Canon 5D Mark IV, 85mm f/1.4, shallow depth of field"

### Examples

Product shot:
> Minimalist ceramic vase with dried eucalyptus branches, product photography, studio lighting, white background, centered composition, soft shadows

Illustration:
> Mountain village at sunset, Studio Ghibli style, hand-painted watercolor, warm color palette, panoramic view, detailed architecture

Portrait:
> Young woman reading in a library, Vermeer lighting, oil painting style, warm golden tones, medium close-up, bokeh lights in background

Branded content:
> Sleek smartphone on a desk, the screen shows color #4a9eff, minimalist product photography, soft side lighting, the text 'LAUNCH' in bold sans-serif below

### Tips Summary

- Front-load the most important elements (FLUX pays more attention to the beginning)
- Use commas to separate concepts cleanly
- Reference specific art styles, photographers, or artistic movements
- Specify camera settings for photorealism
- Use HEX codes for exact brand colors
- Use FLUX.2 Flex when text rendering matters

## Script Usage

```bash
# Generate with Pro
OPENROUTER_API_KEY="..." uv run --with requests python3 scripts/flux.py generate \
  --prompt "Your prompt" --output-dir ./output --model pro --aspect-ratio 16:9

# Fast exploration with Flex
OPENROUTER_API_KEY="..." uv run --with requests python3 scripts/flux.py batch \
  --prompt "Your prompt" --output-dir ./output --model flex --count 8

# Production batch with Pro
OPENROUTER_API_KEY="..." uv run --with requests python3 scripts/flux.py batch \
  --prompt "Your prompt" --output-dir ./output --model pro --count 4 --prefix final
```
