# Nano Banana 2 (Gemini 3.1 Flash Image)

Model ID: `google/gemini-3.1-flash-image-preview` via OpenRouter.

Note: There are two Nano Banana variants:
- **Nano Banana** (`gemini-2.5-flash-image`) — legacy, good for drafts
- **Nano Banana 2** (`gemini-3.1-flash-image-preview`) — higher fidelity, our default

This skill uses Nano Banana 2 unless noted otherwise.

## Strengths

- **Image editing**: Only model here that accepts an input image + text instructions
- **Text rendering**: Best at placing readable text within images
- **Resolution**: Supports 1K, 2K, and 4K output
- **Versatility**: Handles photo, illustration, diagram, and mixed-media well
- **Conversational prompts**: Responds well to natural language (not just keywords)
- **Instruction following**: Excellent at following specific layout/composition requests
- **Multi-image input**: Supports up to 14 reference images for composition
- **Search grounding**: Can integrate real-time data via Google Search (Gemini 3.1 Flash)

## Weaknesses

- **Consistency across batches**: Faces, characters, and styles may vary between images
- **Hands/fingers**: Can still produce anatomical errors (common across all models)
- **Speed**: 20-40s normal, can spike to 180s+ during peak load
- **Occasional refusals**: May refuse prompts it considers unsafe
- **503 errors**: Preview model gets lower priority — ~45% failure rate at peak hours. Retry on 503.
- **Character drift**: Features may drift after multiple editing turns

## Known Quirks

- **SynthID watermark**: All generated images include invisible SynthID watermarks. Cannot be disabled.
- **"Remove watermark" blocked**: Requesting watermark removal in edit prompts triggers a `MALFORMED_FUNCTION_CALL` error — intentional safety mechanism.
- **Prompt rewriting**: The model has built-in prompt enhancement. Leave it on — disabling reduces quality.
- **Aspect ratio enforcement**: Sometimes defaults to 1:1 despite prompt. Always set `aspect_ratio` explicitly in `image_config` rather than relying on prompt text.
- **Size parameter**: Must use uppercase "K" (1K, 2K, 4K). Lowercase rejected.
- **Rate limits**: ~10-50 RPM, 100+ RPD on preview tier. No free tier.

## Prompting Tips

### Natural Language Works Best

Unlike FLUX (keyword-driven), Nano Banana excels with conversational, narrative prompts:

**Good:**
> Create a cozy coffee shop interior. The scene should feel warm and inviting, with wooden furniture, hanging plants, and soft ambient lighting coming through large windows. A few books are scattered on a table. Style: editorial photography, shallow depth of field.

**Less effective (too keyword-y):**
> coffee shop, cozy, warm lighting, wooden furniture, plants, editorial photography, bokeh

### Include Purpose Context

Adding context about the intended use significantly improves results:

> "Create a logo for a high-end, minimalist skincare brand" >> "create a logo"

The model uses context to set tone, polish level, and appropriate style.

### Be Explicit About What You Want

Nano Banana follows instructions literally. Be precise:

- "Place the logo in the top-left corner" (not "add a logo")
- "Use exactly these colors: #1a2332 and #4a9eff" (not "blue tones")
- "The text should read 'HELLO WORLD' in sans-serif bold" (not "add some text")

### Semantic Negatives

Rather than listing exclusions, describe what you want positively:
- Say "a clean, well-lit studio" instead of "no clutter, no dark areas"
- Say "sharp focus throughout" instead of "no blur"

### Image Editing Prompts

When editing, describe the change with preservation instructions:

**Good:** "Remove the background and replace it with a soft gradient from #f5f5f5 to #e0e0e0. Keep everything else unchanged."
**Good:** "Change the color of the car from red to dark blue (#1a3366). Maintain identical composition and lighting."
**Bad:** "Make it look better" (too vague)

For identity preservation across edits:
- "Maintain identical facial features, eye color, hairstyle, and expression"
- Use "this exact person/character" to anchor identity
- Re-specify preservation details each turn — the model drifts without reinforcement

### Handling Character Consistency

- Restart with detailed character descriptions if features drift
- Use "this exact [character]" with specific feature callouts
- For multi-scene work, establish a "character anchor" image first
- Make small changes per turn rather than large overhauls

### Size Selection

| Size | Actual Resolution | Use Case | Cost |
|------|------------------|----------|------|
| 1K | ~1024px | Drafts, exploration, web thumbnails | Lowest |
| 2K | ~2048px | Social media, blog images, presentations | Medium |
| 4K | ~4096px | Print, hero images, high-DPI displays | Highest |

Start with 1K for exploration, regenerate at 2K/4K for finals (don't upscale 1K images).

### Optimal Prompt Template

```
[Purpose/Context]: Create a [type of image] for [use case]
[Subject]: [Detailed description with specific attributes]
[Setting/Environment]: [Detailed scene description]
[Style/Aesthetic]: [Art style, photography style, or rendering approach]
[Technical]: [Camera angle, lens, lighting setup]
[Mood/Atmosphere]: [Emotional tone, color palette]
```

## Script Usage

```bash
# Generate single image
OPENROUTER_API_KEY="..." uv run --with requests python3 scripts/nano_banana.py generate \
  --prompt "Your prompt" --output-dir ./output --size 2K --aspect-ratio 16:9

# Edit existing image
OPENROUTER_API_KEY="..." uv run --with requests python3 scripts/nano_banana.py edit \
  --prompt "Remove background" --input photo.png --output-dir ./output

# Batch variations
OPENROUTER_API_KEY="..." uv run --with requests python3 scripts/nano_banana.py batch \
  --prompt "Your prompt" --output-dir ./output --count 8 --prefix hero
```

## API Parameters

```json
{
  "model": "google/gemini-3.1-flash-image-preview",
  "messages": [{"role": "user", "content": "prompt"}],
  "modalities": ["image", "text"],
  "image_config": {
    "aspect_ratio": "1:1",
    "image_size": "1K"
  }
}
```

Valid aspect ratios: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
Valid sizes: 1K, 2K, 4K
