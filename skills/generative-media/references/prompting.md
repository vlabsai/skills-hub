# Universal Prompting Best Practices

Applies to all image generation models. Model-specific tips in `models/` directory.

## Prompt Anatomy

A strong prompt has 5 layers. Not all are needed every time — match complexity to the task.

```
[Subject] + [Style] + [Composition] + [Lighting/Color] + [Constraints]
```

**Example:**
> A ceramic coffee mug on a wooden table, product photography style, centered composition with shallow depth of field, warm golden hour side lighting, white background, no text, no watermarks

## 1. Subject — What

Be specific. "A dog" → "A golden retriever puppy sitting on grass, looking at camera."

- Name the exact object, person type, animal breed, etc.
- Describe pose, action, expression, and relationship between elements
- Include material/texture when relevant: "brushed aluminum", "hand-knitted wool", "frosted glass"
- Replace vague descriptions with precise ones: "ornate elven plate armor, etched with silver leaf patterns" not "a knight in armor"

## 2. Style — How It Looks

Style descriptors dramatically shift output. Layer them for precision.

**Photography styles:**
- Product photography, editorial photography, street photography
- Portrait, macro, aerial/drone, architectural
- Film grain, Polaroid, 35mm, medium format, tilt-shift
- Studio lighting, natural light, golden hour

**Film stock references** (especially effective for FLUX):
- "Shot on Hasselblad" — high-end commercial photography look
- "Shot on Kodak Portra 400" — warm, natural skin tones with gentle grain
- "Shot on Fuji Velvia 50" — saturated colors, high contrast
- "Shot on Sony A7IV" — clean, sharp, modern digital
- "Polaroid" — vintage, washed-out, square format feel

**Illustration/Art styles:**
- Flat vector illustration, line art, watercolor, oil painting
- Isometric, pixel art, low poly, paper cut-out
- Art nouveau, bauhaus, ukiyo-e, comic book, storybook
- Technical drawing, blueprint, infographic

**Digital/3D styles:**
- 3D render, clay render, wireframe
- Unreal Engine, Cinema 4D, Blender
- Glass morphism, neumorphism

**Abstract keywords:** minimalist, maximalist, geometric, organic, surreal, hyperrealistic, photorealistic

## 3. Composition — Where Things Are

**Camera angles:**
- Eye level — neutral, natural
- Low angle — makes subject powerful, imposing
- High angle / bird's eye — makes subject small, shows layout
- Dutch angle — tilted, creates tension
- Worm's eye view — extreme low angle looking up

**Shot types:**
- Extreme close-up (ECU) — detail of eyes, texture, small object
- Close-up — face, single object fills frame
- Medium shot — waist up, subject in context
- Full shot — entire body or object
- Wide/establishing shot — subject in environment

**Composition rules:**
- Rule of thirds, centered, symmetrical, asymmetrical
- Leading lines guiding eye toward subject
- Frame within a frame (doorway, window, arch)
- Negative space: "generous negative space on the right" (useful for text overlay)
- Shallow depth of field (bokeh), deep focus, layered foreground/midground/background

## 4. Lighting & Color

**Lighting:**
- **Rembrandt lighting** — dramatic triangle on shadowed cheek
- **Butterfly lighting** — front-facing, glamour shadow under nose
- **Rim lighting / backlighting** — halo effect from behind
- **Split lighting** — half face lit, half in shadow
- Golden hour, blue hour, overcast, harsh midday sun
- Volumetric light, god rays, studio softbox
- Chiaroscuro — extreme contrast between light and dark
- High key (bright, minimal shadows) vs low key (dark, dramatic)

**Color:**
- Specify palette: "muted earth tones", "vibrant neon", "monochromatic blue"
- HEX codes for exact colors: "#4a9eff", "#1a2332"
- Mood via color: "warm palette", "cool desaturated tones", "sepia"
- Color schemes: monochromatic, complementary (orange/blue), analogous (blue/teal/green)
- Contrast: "high contrast", "pastel", "washed out"

## 5. Constraints — What to Avoid

**For models that support negative prompts (Stable Diffusion):**
- "no text", "no watermarks", "no borders"
- "no people", "no hands"
- "no gradients", "no drop shadows"

**For FLUX and Nano Banana (no negative prompts):** Rephrase as positives:
- "clean image without text overlays" instead of "no text"
- "sharp focus throughout" instead of "no blur"
- "anatomically correct hands with five fingers" instead of "no extra fingers"
- "well-lit, evenly illuminated scene" instead of "no dark areas"

## Prompt Length

- **Short** (10-30 words): Creative freedom, exploration
- **Medium** (30-80 words): Balanced control. Best for most use cases.
- **Long** (80-150 words): Maximum control. Risk of conflicting instructions.

Rule of thumb: start short, add specificity only where the model needs guidance.

## Iteration Strategy

1. **Start broad** — Short prompt, many variations. Identify what works.
2. **Lock the good** — Keep elements that work, modify what doesn't.
3. **Add specificity** — Layer in composition, lighting, color constraints.
4. **Refine constraints** — Add negative/positive constraints to eliminate artifacts.
5. **Change one variable at a time** — Understand what each element controls.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too vague ("nice image") | Add specific subject, style, composition |
| Contradictory styles ("minimalist and maximalist") | Pick one direction |
| Too many subjects | Focus on one hero element |
| Describing only what you DON'T want | Lead with what you DO want |
| Overloading with adjectives | Use 2-3 key descriptors, not 10 |
| Ignoring aspect ratio context | Match ratio to content (portrait for people, landscape for scenes) |
| Front-loading quality tags ("8K ultra-detailed masterpiece") | Camera/composition terms steer realism more reliably |
| Ignoring lighting | Lighting is the #1 underutilized element that separates amateur from pro results |
| Changing too many variables when iterating | Change one element at a time |

## Aspect Ratio Guide

| Ratio | Use Case |
|-------|----------|
| 1:1 | Icons, avatars, social media posts (Instagram feed), logos |
| 4:5 | Instagram feed (max screen space), portraits, posters |
| 3:4 | Portraits, phone wallpapers, print photography |
| 2:3 | Tall portraits, 4x6" prints, book covers, Pinterest pins |
| 9:16 | Stories, Reels, TikTok, mobile-first vertical content |
| 3:2 | Standard landscape photography, 6x4" prints, DSLR-native |
| 4:3 | Presentations, tablets, compact camera native |
| 16:9 | YouTube thumbnails, hero banners, desktop wallpapers, cinematic |
| 21:9 | Ultra-wide cinematic, website hero banners, panoramic |
