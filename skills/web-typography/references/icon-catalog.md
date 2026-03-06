# Icon Catalog

Free icon libraries for web apps. Comparison, selection guide, and implementation patterns.

## Table of Contents

- [Library Comparison](#library-comparison)
- [Detailed Profiles](#detailed-profiles)
- [Icon-Typography Pairing](#icon-typography-pairing)
- [SVG vs Icon Font](#svg-vs-icon-font)
- [Implementation Patterns](#implementation-patterns)

---

## Library Comparison

| Library | Icons | Styles | Tree-Shakable | Framework Support | License |
|---|---|---|---|---|---|
| **Lucide** | 1,600+ | Outline (2px stroke) | Yes | React, Vue, Svelte, Solid, Angular, Preact, Web Components | MIT |
| **Phosphor** | 1,500+ base (9,000+ with weights) | Thin, Light, Regular, Bold, Fill, Duotone | Yes | React, Vue, Svelte, Elm, Flutter | MIT |
| **Tabler** | 6,000+ | Outline (customizable stroke) | Yes | React, Vue, Svelte, Solid, Preact | MIT |
| **Heroicons** | 292 | Outline, Solid, Mini (20px), Micro (16px) | Yes | React, Vue | MIT |
| **Material Symbols** | 2,500+ | Outlined, Rounded, Sharp + variable axes | Partial | React (via MUI) | Apache 2.0 |
| **Remix Icons** | 3,200+ | Outlined, Filled | Yes | React | Apache 2.0 |
| **Bootstrap Icons** | 2,000+ | Outline, Fill | Partial | Framework-agnostic | MIT |
| **Feather** | 287 | Outline only | Yes | React | MIT (**abandoned**) |

---

## Detailed Profiles

### Lucide (Recommended Default)
- Fork of Feather Icons, actively maintained with weekly additions
- Consistent 24x24 grid, 2px stroke
- Excellent tree-shaking: only imported icons enter the bundle
- **Best for**: General-purpose web/app UI
- **Limitation**: Outline only (no filled/duotone)
- `npm install lucide-react`

### Phosphor (Best for Design Systems)
- 6 weights per icon — unmatched weight variation
- Duotone style: background layer at 20% opacity, great for feature illustrations and empty states
- Systematic weight mapping to typography scale
- **Best for**: Design systems needing icon-typography weight coupling
- **Limitation**: Slightly smaller base count than Lucide/Tabler
- `npm install @phosphor-icons/react`

### Tabler (Largest Free Set)
- 6,000+ icons — widest coverage from a single library
- Customizable stroke width and size
- 24x24 grid, 2px default stroke
- **Best for**: Complex admin UIs, SaaS with many distinct features
- **Limitation**: Outline only, quality slightly less consistent than smaller curated sets
- `npm install @tabler/icons-react`

### Heroicons (Tailwind Ecosystem)
- By Tailwind Labs — impeccable quality, small curated set
- 4 size variants: Outline/Solid (24px), Mini (20px), Micro (16px)
- Micro variant is excellent for dense, high-information UIs
- **Best for**: Tailwind CSS projects, small-to-medium apps
- **Limitation**: Only ~292 icons — will hit gaps for niche icons
- `npm install @heroicons/react`

### Material Symbols (Variable Font)
- Only library with variable axes: Fill (0-100), Weight (100-700), Grade (-50 to 200), Optical Size (20-48px)
- Optical size auto-adjusts stroke weight at different sizes
- **Best for**: Material Design / MUI apps
- **Limitation**: Distinctly "Google" aesthetic, large font file (4-6MB full set), loads all icons
- Via Google Fonts CSS or `@mui/icons-material`

### Remix Icons
- Good balance: 3,200+ icons with both outline and fill per icon
- Neutral style works across aesthetics
- **Best for**: General-purpose where you need outline + fill
- **Limitation**: Smaller community, slower update cadence
- `npm install remixicon`

### Others Worth Knowing
- **Iconoir** (~1,600, outline, MIT) — Strong Lucide alternative
- **Radix Icons** (~300, outline) — Small but extremely high quality, for Radix UI
- **css.gg** (~700, pure CSS) — No SVG/font, CSS-only icons

---

## Icon-Typography Pairing

### Matching Stroke Weight to Font Weight

| Typography Weight | Icon Approach |
|---|---|
| Light/Thin (300-) | Thin stroke (1px). Phosphor Thin/Light. |
| Regular (400) | Standard 1.5-2px stroke. Lucide, Heroicons Outline, Tabler default, Phosphor Regular. |
| Medium (500) | Slightly heavier stroke or Phosphor Bold. |
| Semi-Bold/Bold (600-700) | Filled/solid icons. Heroicons Solid, Phosphor Bold/Fill, Remix Fill. |

### Proven Pairings

| Font | Icon Library | Why it works |
|---|---|---|
| Inter 400 | Lucide | Clean geometric sans + geometric 2px stroke outlines |
| Inter 400 | Phosphor Regular | Balanced stroke weight at body sizes |
| Geist | Lucide or Phosphor | Geometric precision matches both libraries |
| System UI / SF Pro | Heroicons | Designed together for Tailwind ecosystem |
| Roboto | Material Symbols | Canonical Material Design pairing, variable weight tuning |
| Poppins / Nunito | Material Symbols Rounded | Rounded terminals match rounded typefaces |

### By Typeface Category

| Typeface Style | Icon Style |
|---|---|
| Sans-serif (Inter, Geist, Helvetica) | Clean geometric strokes: Lucide, Phosphor, Heroicons, Tabler |
| Serif (Merriweather, Lora) | Refined strokes: Phosphor Light, Material Symbols Outlined low-weight |
| Monospace (JetBrains Mono, Fira Code) | Sharp precise: Heroicons Micro, Material Symbols Sharp, tight-stroke Tabler |
| Rounded (Poppins, Nunito) | Rounded terminals: Material Symbols Rounded |
| Display/Decorative | Match personality: Phosphor Duotone (playful), Phosphor Bold (punchy), filled for heavy display |

### Phosphor Weight Mapping (Design Systems)

```
h1 (Bold 700)       → Phosphor Bold or Fill
h2 (Semi-Bold 600)  → Phosphor Bold
h3 (Medium 500)     → Phosphor Regular or Bold
body (Regular 400)   → Phosphor Regular
caption (Light 300)  → Phosphor Light
```

---

## SVG vs Icon Font

**SVG is the recommended default in 2025-2026.** Icon fonts are legacy.

| Approach | Initial Load (few) | Initial Load (many) | Cached | Customization | Accessibility |
|---|---|---|---|---|---|
| Inline SVG | Excellent | Good | N/A (in bundle) | Full (multi-color, animate per path) | Excellent |
| SVG Sprite | Good | Excellent | Excellent | Good (currentColor, size) | Good |
| Icon Font | Poor (full file) | Good (one file) | Excellent | Limited (single color) | Poor |

### When to use what

- **Inline SVG (React/Vue/Svelte components)**: Default for <50 unique icons. No FOUT, tree-shakable, full CSS control.
- **SVG Sprite**: 50+ icons on one page, or server-rendered apps (PHP, Rails).
- **Icon Font**: Only for CMS/legacy systems where SVG tooling is impractical.

---

## Implementation Patterns

### Pattern A: npm + Tree-Shaking (Default for Modern Apps)

```tsx
// Lucide
import { Home, Settings } from 'lucide-react';
<Home size={20} strokeWidth={1.5} />

// Phosphor
import { House, Gear } from '@phosphor-icons/react';
<House size={20} weight="regular" />

// Heroicons
import { HomeIcon } from '@heroicons/react/24/outline';
<HomeIcon className="h-5 w-5" />

// Tabler
import { IconHome } from '@tabler/icons-react';
<IconHome size={20} stroke={1.5} />
```

### Pattern B: SVG Sprite

```html
<!-- Define once -->
<svg style="display:none">
  <symbol id="icon-home" viewBox="0 0 24 24">
    <path d="..." />
  </symbol>
</svg>

<!-- Use anywhere -->
<svg width="24" height="24"><use href="#icon-home" /></svg>

<!-- Or external file (cacheable) -->
<svg width="24" height="24"><use href="/sprite.svg#icon-home" /></svg>
```

### Pattern C: CDN (Prototypes)

```html
<!-- Lucide -->
<script src="https://unpkg.com/lucide@latest"></script>
<script>lucide.createIcons();</script>

<!-- Material Symbols -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
```

### Recommendation by Project Type

| Project Type | Pattern |
|---|---|
| React / Next.js / Vue / Svelte | npm + tree-shaking |
| Server-rendered (Rails, PHP, Django) | SVG sprite or self-hosted icon font |
| Prototype / landing page | CDN |
| WordPress / CMS | CDN or self-hosted icon font |
| Design system / component library | npm, wrapped in your own `<Icon>` component |
