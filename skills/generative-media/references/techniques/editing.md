# Image Editing Techniques

Currently only supported by **Nano Banana 2** (Gemini 3.1 Flash). Other models are generation-only.

## Generation vs Editing: Key Difference

**Generation**: Build from scratch — describe everything.
**Editing**: Modify existing — describe the desired end state + what to preserve.

- Bad: "Turn the red dress into a blue dress" (describes action)
- Good: "The dress should be deep navy blue (#1b2838). Keep everything else unchanged." (describes result)
- Bad: "Remove the person from the background"
- Good: "Empty park bench on a gravel path, soft afternoon light" (describes what should be there)

## Edit Types

### Background Changes
```
"Remove the background and replace with pure white (#ffffff). Keep everything else unchanged."
"Replace the background with a blurred office environment. Maintain the subject's position and scale."
"Make the background a soft gradient from #f5f5f5 to #e0e0e0."
```

### Color Modifications
```
"Change the shirt color from red to navy blue (#1b2838). Maintain all other details."
"Convert to black and white while keeping the roses red."
"Shift the entire color palette to warmer tones."
```

### Object Manipulation
```
"Remove the person on the right side of the image. Fill the area with the surrounding background."
"Add a coffee cup on the table in front of the laptop."
"Replace the text on the sign with 'OPEN' in the same font style."
```

### Style Transfer
```
"Convert this photo to a watercolor painting style while maintaining the original composition and subject placement."
"Make this look like a vintage 1970s photograph with film grain. Keep the framing identical."
"Apply a flat vector illustration style. Preserve the layout and color scheme."
```

### Enhancement
```
"Increase the contrast and make the colors more vibrant. Do not change the composition."
"Add dramatic lighting with rim light from the left."
"Make this image look more professional and polished."
```

## Edit Prompt Best Practices

1. **Be specific about location**: "in the top-right corner", "on the table", "behind the subject"
2. **Reference colors by hex**: "#ff6b35" not "orange-ish"
3. **One change at a time**: Multiple edits in one prompt may conflict. Chain them.
4. **Describe the desired result**: "The car should be blue" > "Change the car"
5. **Explicitly preserve**: "Keep everything else unchanged" or "Maintain identical facial features"
6. **State aspect ratio preservation**: "Do not change the input aspect ratio" when needed

## Identity Preservation

When editing images of people or characters:

- **Lock features explicitly**: "Maintain identical facial features, eye color, hairstyle, and expression"
- **Anchor identity**: Use "this exact person/character" with specific feature callouts
- **Reinforce each turn**: Re-specify preservation details — the model drifts without reinforcement
- **Use granular verbs**: "Change the clothes to..." (targeted) not "Transform" (wholesale change)
- **Avoid vague transforms**: "Convert to pencil sketch with natural graphite lines" preserves structure better than "make it a sketch"

## Chaining Edits

For complex modifications, chain multiple edit calls sequentially:

1. **First pass**: Major structural change (e.g., background removal)
2. **Second pass**: Color/style adjustment on the result
3. **Third pass**: Final polish (lighting, contrast)

Each pass uses the output of the previous as input. This produces better results than cramming everything into a single prompt.

## Handling Drift

If quality or identity drifts after multiple editing turns:
- **Restart from the original** with a more comprehensive prompt
- **Establish a "character anchor"** image for multi-scene work
- **Make small changes per turn** rather than large overhauls
- **Re-describe** critical preservation details in each prompt

## Script Usage

```bash
# Single edit
OPENROUTER_API_KEY="..." uv run --with requests python3 scripts/nano_banana.py edit \
  --prompt "Remove the background and replace with soft gray gradient. Keep everything else unchanged." \
  --input original.png --output-dir ./edits --prefix bg-removed

# Chain edits (run sequentially)
OPENROUTER_API_KEY="..." uv run --with requests python3 scripts/nano_banana.py edit \
  --prompt "Remove background" --input photo.png --output-dir ./edits --prefix step1

OPENROUTER_API_KEY="..." uv run --with requests python3 scripts/nano_banana.py edit \
  --prompt "Add soft shadow beneath the object" --input ./edits/step1-edited.png \
  --output-dir ./edits --prefix step2
```

## Edit Prompt Template

```
[What to change]: [Specific description of the desired modification]
[What to preserve]: [Explicit list of elements that must remain unchanged]
[Style/Mood]: [Any style adjustments, or "maintain current style"]
[Constraints]: [Additional restrictions — aspect ratio, color palette, etc.]
```

**Example:**
```
Change the background to a sunset beach scene with warm golden light.
Preserve the person's exact face, expression, hairstyle, and clothing.
Maintain the current photographic style and color grading.
Keep the person in the same position and scale within the frame.
```
