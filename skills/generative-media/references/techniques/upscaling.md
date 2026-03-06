# Upscaling & Post-Processing

## Native Upscaling

**Nano Banana** supports native resolution tiers:
- 1K (~1024px) — Default, fastest
- 2K (~2048px) — 2x quality
- 4K (~4096px) — Maximum, slowest

Always generate at 1K first for exploration, then regenerate at 2K/4K for finals (rather than upscaling a 1K image).

**FLUX** outputs at ~1024px max — no native upscaling.

## Post-Processing Pipeline

After generation, common post-processing steps:

### 1. Crop & Resize
Use any image tool to crop whitespace or resize to exact dimensions:
```bash
# Using ImageMagick (if installed)
convert input.png -trim -resize 1200x630 output.png

# Using Python/Pillow
uv run --with Pillow python3 -c "
from PIL import Image
img = Image.open('input.png')
img = img.resize((1200, 630), Image.LANCZOS)
img.save('output.png')
"
```

### 2. Background Removal
For transparent backgrounds, use the logo-creator's rembg script if available:
```bash
uv run --with "rembg>=2.0.57" --with Pillow --with onnxruntime --python 3.10 \
  python3 ~/.claude/skills/logo-creator/scripts/remove_bg.py input.png output-transparent.png
```

### 3. Format Conversion
```bash
# PNG to JPEG (with quality setting)
uv run --with Pillow python3 -c "
from PIL import Image
Image.open('input.png').convert('RGB').save('output.jpg', quality=90)
"

# PNG to WebP (smaller file size for web)
uv run --with Pillow python3 -c "
from PIL import Image
Image.open('input.png').save('output.webp', quality=85)
"
```

### 4. SVG Vectorization
For logos and icons, convert to SVG using logo-creator's vectorizer:
```bash
uv run --with vtracer python3 ~/.claude/skills/logo-creator/scripts/vectorize.py \
  input.png output.svg --detail medium --colormode color
```

## Batch Post-Processing

For multiple images, loop through a directory:
```bash
for img in ./output/*.png; do
  base=$(basename "$img" .png)
  # Your processing command here
done
```
