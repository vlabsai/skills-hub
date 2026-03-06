---
name: web-typography
description: >-
  Sistema de decisao tipografica em 7 passos: tipo de app, tom da marca,
  combo de fontes, biblioteca de icones, escala tipografica, loading e
  implementacao. Inclui 14 combinacoes pre-curadas por cenario e regras de
  pareamento fonte-icone.
license: Apache-2.0
compatibility: claude-code
allowed-tools: Read Write Edit Glob
metadata:
  author: vector-labs
  version: "1.0"
tags: [design, typography, fonts]
complexity: beginner
---

# Web Typography

Select fonts, type pairings, and icon libraries for web apps through a structured decision workflow.

## Decision Workflow

### Step 1: Identify app type

Ask or infer from context:

| App Type | Typography Priority |
|---|---|
| SaaS / Dashboard | Data density, numeric clarity, readability at small sizes |
| Marketing / Landing | Visual impact, personality, clear heading/body hierarchy |
| Documentation | Long-form readability, code block integration |
| E-commerce | Scannability, trust, premium feel for campaigns |
| Portfolio / Creative | Personality, visual distinction, memorable type |
| Corporate / Enterprise | Professionalism, trust, accessibility |

### Step 2: Determine brand tone

- **Neutral/Professional** → Inter, Geist, Source Sans 3
- **Friendly/Modern** → DM Sans, Plus Jakarta Sans, Manrope
- **Premium/Editorial** → Serif headings (Playfair Display, Instrument Serif) + sans body
- **Technical/Developer** → Geist, Space Grotesk, JetBrains Mono for code
- **Playful/Creative** → Cabinet Grotesk, Syne, Epilogue

### Step 3: Pick from quick-start combos

| App Type | Heading | Body | Icons | When to use |
|---|---|---|---|---|
| SaaS (safe default) | Inter 600 | Inter 400 | Lucide | Proven, neutral, works everywhere |
| SaaS (modern) | Geist 600 | Geist 400 | Lucide | Next.js ecosystem, web-native feel |
| SaaS (friendly) | Plus Jakarta Sans | DM Sans | Phosphor | Startup, product-led growth |
| Marketing | Playfair Display | Inter | Lucide | Premium, authoritative |
| Marketing (bold) | Bebas Neue | Open Sans | Remix | High-impact hero sections |
| Docs | Inter 600 | Inter 400 + Fira Code | Lucide | Industry standard (Tailwind, Vercel) |
| E-commerce | Playfair Display | Montserrat | Phosphor | Luxury/fashion/lifestyle |
| Portfolio | Syne | Satoshi | Phosphor | Tech-creative studios |
| Corporate | Source Sans 3 | Source Sans 3 | Lucide | Mature, trustworthy, wide language support |

For deeper exploration of all available fonts and pairings, read [references/font-catalog.md](references/font-catalog.md).

### Step 4: Select icon library

| Need | Library | Why |
|---|---|---|
| General purpose (default) | **Lucide** (1,600+ icons) | Best balance: count, consistency, tree-shaking, community |
| Weight variation / design system | **Phosphor** (1,500+ base, 6 weights) | Map icon weight to typography weight systematically |
| Maximum coverage | **Tabler** (6,000+ icons) | Largest free MIT set, good for complex admin UIs |
| Tailwind ecosystem | **Heroicons** (292 icons, 4 styles) | Small but impeccable, by Tailwind Labs |

Match icon stroke to font weight: Regular (400) text pairs with 1.5-2px stroke icons (Lucide default, Phosphor Regular). Bold (600-700) text pairs with filled/solid icons.

For full comparison of all libraries, read [references/icon-catalog.md](references/icon-catalog.md).

### Step 5: Implement type scale

Use Major Third (1.250) as default ratio. Adjust for app type:

| Ratio | Name | Best for |
|---|---|---|
| 1.125 | Major Second | Dense dashboards, admin panels |
| 1.200 | Minor Third | Compact apps, data-rich interfaces |
| **1.250** | **Major Third** | **Most web apps (recommended default)** |
| 1.333 | Perfect Fourth | Marketing sites, editorial |

#### CSS custom properties with fluid sizing

```css
:root {
  --fs-xs:   clamp(0.64rem, 0.6rem + 0.15vw, 0.7rem);
  --fs-sm:   clamp(0.8rem, 0.77rem + 0.15vw, 0.875rem);
  --fs-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --fs-lg:   clamp(1.125rem, 1rem + 0.5vw, 1.25rem);
  --fs-xl:   clamp(1.35rem, 1.15rem + 0.85vw, 1.563rem);
  --fs-2xl:  clamp(1.6rem, 1.3rem + 1.2vw, 1.953rem);
  --fs-3xl:  clamp(1.95rem, 1.5rem + 1.75vw, 2.441rem);
  --fs-4xl:  clamp(2.4rem, 1.75rem + 2.5vw, 3.052rem);

  --lh-tight:  1.1;   /* h1, h2 */
  --lh-snug:   1.25;  /* h3, h4 */
  --lh-normal: 1.5;   /* body */
  --lh-relaxed: 1.65; /* small text, captions */

  --ls-tight: -0.025em;  /* headings */
  --ls-wide:   0.025em;  /* all-caps, small labels */
}
```

### Step 6: Font loading

1. **WOFF2 only** — 97%+ support, best compression
2. **Self-host or Fontsource** — `npm install @fontsource-variable/inter`
3. **`font-display: swap`** for body, **`optional`** for display headings
4. **Preload 1-2 critical files** — `<link rel="preload" href="/fonts/inter-variable.woff2" as="font" type="font/woff2" crossorigin>`
5. **Variable fonts** over multiple static files
6. **Subset** to Latin + Latin Extended-A for 90%+ size reduction

```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-variable.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
}
```

Fallback stack: `'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;`

### Step 7: Icon implementation

Default pattern — npm with tree-shaking:

```tsx
// npm install lucide-react
import { Home, Settings, User } from 'lucide-react';

<Home size={20} strokeWidth={1.5} />
```

For prototypes/landing pages, CDN is fine:
```html
<script src="https://unpkg.com/lucide@latest"></script>
<script>lucide.createIcons();</script>
```

## References

- **[references/font-catalog.md](references/font-catalog.md)** — Full inventory of 40+ free fonts by category, curated pairings by app type with rationale, trending fonts 2025-2026. Read when exploring options beyond the quick-start combos.
- **[references/icon-catalog.md](references/icon-catalog.md)** — Detailed comparison of 8 icon libraries (counts, styles, formats, pros/cons), icon-typography weight matching rules, SVG vs icon font analysis, implementation patterns by project type. Read when selecting or comparing icon libraries.
