---
name: presentation
description: >-
  Cria apresentacoes HTML navegaveis em 16:9 e documentos visuais em scroll
  vertical usando o design system da Vector Labs. Use para pitch decks,
  propostas, workshops, one-pagers e relatorios visuais.
license: Apache-2.0
compatibility: claude-code
allowed-tools: Read Write Edit Glob Bash
metadata:
  author: vector-labs
  version: "1.0"
tags: [slides, design]
complexity: intermediate
featured: true
---

# Presentation Skill

Create and edit HTML presentations (slide decks) and visual documents using the Vector Labs design system.

## Two Modes

| | Slide Deck | Visual Document |
|---|---|---|
| **Layout** | Horizontal, 16:9, one slide at a time | Vertical, scrollable, reading width |
| **Navigation** | Keyboard/touch/buttons | Natural scroll |
| **Output** | Engine folder + slide files | Single self-contained HTML |
| **Use cases** | Pitch decks, propostas, workshops | One-pagers, relatórios, briefs, guias |
| **Engine** | Copies `3-resources/presentations/engine/` | No engine needed |

## Key References (read on demand)

- **Slide catalog** (14 types, full HTML/CSS): `3-resources/presentations/slide-catalog.md`
- **Design system** (colors, typography, spacing, animations): `3-resources/presentations/design-system.md`
- **Engine** (copy for new decks): `3-resources/presentations/engine/`
- **Palette catalog**: `references/palettes.md` (bundled)
- **Document sections** (base patterns for visual docs): `references/document-sections.md` (bundled)
- **README**: `3-resources/presentations/README.md`

## Initial Flow (both modes)

1. Read the document/project the user points to (or their description)
2. Ask using AskUserQuestion:
   - **Formato**: Slide deck ou documento visual?
   - **Objetivo**: Qual o objetivo? (pitch, proposta, update, relatório, brief...)
   - **Público**: Quem vai ver?
   - **Tom**: Formal, casual, técnico?
3. Read `references/palettes.md`, ask user to choose palette or create custom
4. Proceed to the appropriate workflow below

---

## Slide Deck

### Slide Types (quick reference)

1. **Cover** — Title + subtitle + date (dark)
2. **Statement** — Single powerful message
3. **Problem** — Two-column reality vs consequences
4. **Market/Comparison** — 2-4 option cards
5. **TAM/Data Viz** — Market sizing, left text + right visual
6. **Roadmap/Flow** — Data flows, architecture, features
7. **Pricing/Proposal** — Two paths with highlighted option
8. **Closing** — Logo, next steps, CTA
9. **Section Divider** — Section number + title
10. **Team** — Grid of members
11. **Quote/Testimonial** — Blockquote with attribution
12. **Single Stat Hero** — One massive number
13. **Timeline** — Milestones with dots and dates
14. **Thank You/Contact** — Generic closing

For full HTML/CSS of each type, read `3-resources/presentations/slide-catalog.md`.

### New Deck

1. Suggest slide composition (which types, what order, brief content outline per slide)
2. Confirm with user. Iterate until approved.
3. Read `3-resources/presentations/slide-catalog.md` for HTML/CSS templates
4. Read `3-resources/presentations/design-system.md` for tokens
5. Copy `3-resources/presentations/engine/` to target directory
6. Edit `parts/head.html`: set deck title, add stylesheet `<link>` tags
7. Generate each slide as `slides/NN-name.html`:
   - Single `<div class="slide" data-theme="dark|light">` per file
   - **Every `<div>` must have a matching `</div>`** — `build.sh` validates this and will refuse to build if tags are unbalanced (unclosed divs cause slides to nest inside each other, breaking navigation)
   - Use `.anim-in` + `.d1`..`.d8` for animation stagger
   - Use `.slide-label`, `.slide-title`, `.slide-inner` structure
   - Lucide icons inline SVG when needed
8. If non-default palette: create `styles/theme.css` with CSS overrides, add `<link>` to `parts/head.html`
9. If architecture diagrams: add anime.js CDN + `architecture.js` + hooks in `parts/foot.html`
10. Run `./build.sh` to assemble `index.html`

#### Slide HTML pattern

```html
<div class="slide" data-theme="dark">
  <div class="slide-inner">
    <span class="slide-label anim-in d1">LABEL</span>
    <h1 class="slide-title anim-in d2">Title</h1>
    <div class="anim-in d3"><!-- content --></div>
  </div>
</div>
```

### Edit Existing Deck

1. List the `slides/` directory to see current slides
2. Read existing slide files
3. Ask what to change: add slide, edit content, remove, reorder, change palette
4. Confirm before writing
5. After changes: run `./build.sh` to reassemble `index.html`

---

## Visual Document

### New Document

1. Read `references/document-sections.md` for base HTML structure and section patterns
2. Suggest document structure (which sections, content outline)
3. Confirm with user. Iterate until approved.
4. Generate single self-contained HTML file:
   - Google Fonts CDN for typography
   - Inline `<style>` with design system tokens + palette
   - `.doc` container, width controlled by `--doc-width` variable
   - Compose from base sections (hero, stats, cards, text, callout, table, divider)
   - Invent new section patterns as needed, following design tokens from `references/document-sections.md`
5. Dark or light variant based on content and user preference

### Edit Existing Document

1. Read the existing HTML file
2. Ask what to change: add section, edit content, change palette, restructure
3. Confirm before writing

---

## Shared Guidelines

- **Typography**: Fraunces (titles, 800), Plus Jakarta Sans (body), JetBrains Mono (labels/data)
- **Labels**: JetBrains Mono 11px, uppercase, letter-spacing 0.15em, accent color
- **Icons**: Lucide inline SVG, stroke-width 2, 16-24px
- **Palette**: Always ask and apply from catalog or custom. Read `references/palettes.md`.
- **Confirm before generating**: Always present plan to user before writing files
