---
name: excalidraw-diagram
description: >-
  Gera diagramas visuais a partir de descricoes em texto: flowcharts, mind
  maps, hierarquias, timelines, matrizes e mapas de relacionamento. Exporta
  como arquivos Excalidraw compativeis com Obsidian.
license: Apache-2.0
compatibility: claude-code
allowed-tools: Read Write Glob Grep
metadata:
  author: vector-labs
  version: "1.0"
tags: [diagrams, documentation]
complexity: beginner
featured: true
---

# Excalidraw Diagram Generator

Generate visual diagrams from text content as Obsidian-compatible `.excalidraw.md` files with embedded Excalidraw JSON.

## When to Use This Skill

Activate when:
- User asks to create a diagram, chart, flowchart, or visual
- User mentions "diagrama", "fluxo", "mapa mental", "excalidraw", "timeline", "hierarquia"
- User wants to visualize a process, architecture, relationships, or structure
- User asks to diagram something from existing documentation

## Workflow

1. **Analyze content** — Identify concepts, relationships, hierarchies, and flow
2. **Select diagram type** — Choose from 8 types based on content structure
3. **Generate JSON** — Build valid Excalidraw element array
4. **Write file** — Save as `.excalidraw.md` in Obsidian format

## Diagram Types

| Type | When to Use | Key Elements |
|------|-------------|-------------|
| **Flowchart** | Sequential processes, workflows | Rectangles + arrows, left-to-right or top-to-bottom |
| **Mind Map** | Concept expansion, brainstorming | Central node + radiating branches |
| **Hierarchy** | Org charts, taxonomies, tree structures | Parent-child rectangles, top-down |
| **Relationship** | Entity interactions, system dependencies | Nodes + bidirectional connectors |
| **Comparison** | Multi-option analysis, pros/cons | Side-by-side columns or grouped boxes |
| **Timeline** | Chronological events, roadmaps | Horizontal line + milestone markers |
| **Matrix** | 2D classification, quadrants | Grid layout with labeled axes |
| **Freeform** | Unstructured layouts, mixed visuals | Free positioning, mixed elements |

## Output Format

### File Structure (Obsidian `.excalidraw.md`)

```markdown
---

excalidraw-plugin: parsed
tags: [excalidraw]

---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'


# Excalidraw Data

## Text Elements
%%
## Drawing
```json
{EXCALIDRAW_JSON}
```
%%
```

### JSON Root Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin",
  "elements": [],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## Design Rules

### Color Palette

| Role | Color | Hex |
|------|-------|-----|
| Titles / primary stroke | Deep blue | `#1e40af` |
| Secondary elements / accent stroke | Bright blue | `#3b82f6` |
| Body text / neutral stroke | Gray | `#374151` |
| Emphasis / highlights | Gold | `#f59e0b` |
| Primary fill (light) | Light blue | `#dbeafe` |
| Secondary fill (light) | Light gold | `#fef3c7` |
| Neutral fill | Light gray | `#f3f4f6` |
| Success / positive | Green | `#059669` |
| Success fill | Light green | `#d1fae5` |
| Warning / attention | Orange | `#d97706` |
| Error / negative | Red | `#dc2626` |
| Error fill | Light red | `#fee2e2` |
| Default stroke (connectors) | Dark gray | `#1e1e1e` |
| Background | White | `#ffffff` |

### Typography

- **Font family**: `1` (Excalifont — hand-drawn style)
- **Title**: `fontSize: 28`, `strokeColor: "#1e40af"`
- **Subtitle / section header**: `fontSize: 20`, `strokeColor: "#3b82f6"`
- **Body text**: `fontSize: 16`, `strokeColor: "#374151"`
- **Small labels**: `fontSize: 14`, `strokeColor: "#374151"`
- **Line height**: `1.25` for all text
- **textAlign**: `"center"` for bound text, `"left"` for standalone
- **No emojis** in diagram elements

### Canvas

- Target area: **0–1200 x 0–800 pixels**
- Leave **40px margin** from edges
- Minimum **20px gap** between elements

## Element Reference

### Common Properties (all elements)

```json
{
  "id": "unique-string",
  "type": "rectangle",
  "x": 0,
  "y": 0,
  "width": 200,
  "height": 100,
  "angle": 0,
  "strokeColor": "#1e40af",
  "backgroundColor": "#dbeafe",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "index": "a0",
  "roundness": { "type": 3 },
  "seed": 1001,
  "version": 1,
  "versionNonce": 500100,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false
}
```

### Shapes

**Rectangle** — Main container for content boxes, process steps, cards.
```json
{
  "type": "rectangle",
  "roundness": { "type": 3 },
  "boundElements": [
    { "type": "text", "id": "text-id" }
  ]
}
```

**Ellipse** — Used for start/end nodes, emphasis circles.
```json
{
  "type": "ellipse",
  "roundness": { "type": 2 }
}
```

**Diamond** — Decision points, conditional branches.
```json
{
  "type": "diamond",
  "roundness": { "type": 2 }
}
```

### Text

**Standalone text** (titles, labels):
```json
{
  "type": "text",
  "text": "Title Text",
  "rawText": "Title Text",
  "originalText": "Title Text",
  "fontSize": 28,
  "fontFamily": 1,
  "textAlign": "left",
  "verticalAlign": "top",
  "containerId": null,
  "autoResize": true,
  "lineHeight": 1.25
}
```

**Bound text** (text inside a shape):
```json
{
  "type": "text",
  "text": "Step 1",
  "rawText": "Step 1",
  "originalText": "Step 1",
  "fontSize": 16,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "parent-shape-id",
  "autoResize": true,
  "lineHeight": 1.25
}
```

**Binding rules:**
1. Set text `containerId` to the shape's `id`
2. Add `{ "type": "text", "id": "text-id" }` to the shape's `boundElements` array
3. Position text x/y inside the shape bounds (Obsidian auto-centers, but provide reasonable coords)
4. Text `width` and `height` should fit within the container

### Arrows and Lines

**Arrow** (directional connector):
```json
{
  "type": "arrow",
  "points": [[0, 0], [150, 0]],
  "lastCommittedPoint": [150, 0],
  "startBinding": {
    "elementId": "source-shape-id",
    "focus": 0,
    "gap": 1,
    "fixedPoint": null
  },
  "endBinding": {
    "elementId": "target-shape-id",
    "focus": 0,
    "gap": 1,
    "fixedPoint": null
  },
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "elbowed": false
}
```

**Line** (non-directional connector):
```json
{
  "type": "line",
  "points": [[0, 0], [100, 0]],
  "lastCommittedPoint": [100, 0],
  "startBinding": null,
  "endBinding": null,
  "startArrowhead": null,
  "endArrowhead": null
}
```

**Binding rules for arrows:**
1. First point MUST be `[0, 0]`
2. Arrow `x`, `y` = position of the start point in canvas coordinates
3. Set `startBinding.elementId` and `endBinding.elementId` to connect shapes
4. Add `{ "type": "arrow", "id": "arrow-id" }` to both shapes' `boundElements`
5. `focus`: `-1` to `1` — position along the target edge (0 = center)
6. `gap`: distance from shape edge (use `1`)

### Index Values

Each element needs a unique `index` string for ordering. Use alphabetical indexing:
- `"a0"`, `"a1"`, `"a2"`, ... `"a9"`, `"aA"`, `"aB"`, ...

### Seed and Version

- `seed`: Use incrementing integers starting from `1000` (e.g., `1000`, `1001`, `1002`)
- `version`: Always `1` for new diagrams
- `versionNonce`: Use `seed * 100` for simplicity

## Layout Patterns

### Flowchart (left-to-right)
```
[Step 1] ---> [Step 2] ---> [Step 3]
                |
                v
            <Decision>
              /    \
         [Yes]    [No]
```
- Rectangles: `width: 180, height: 80`
- Horizontal gap: `80px` (arrow space)
- Vertical gap: `60px` for branches
- Diamonds for decisions: `width: 140, height: 100`

### Mind Map (radial)
```
           [Branch 1]
              |
[Branch 4] - [CENTER] - [Branch 2]
              |
           [Branch 3]
```
- Center node: `width: 200, height: 80`, deep blue stroke + fill
- Branch nodes: `width: 160, height: 60`, bright blue stroke
- Leaf nodes: `width: 140, height: 50`, gray stroke
- Radial spacing: `200-250px` from center

### Hierarchy (top-down tree)
```
         [Root]
        /      \
   [Child 1]  [Child 2]
    /    \
[Leaf] [Leaf]
```
- Vertical level gap: `100px`
- Horizontal sibling gap: `40px`
- Center children under parents

### Timeline (horizontal)
```
  |        |         |        |
[E1]     [E2]      [E3]     [E4]
  |        |         |        |
  2024     2025      2026     2027
```
- Horizontal line: full width at y=400
- Event markers: rectangles above/below the line (alternating)
- Date labels below each marker
- Spacing: `250px` between events

### Comparison (columns)
```
  [Option A]    [Option B]    [Option C]
  ┌────────┐   ┌────────┐   ┌────────┐
  │ Point 1│   │ Point 1│   │ Point 1│
  │ Point 2│   │ Point 2│   │ Point 2│
  │ Point 3│   │ Point 3│   │ Point 3│
  └────────┘   └────────┘   └────────┘
```
- Column width: `300px`
- Column gap: `40px`
- Header rectangles: accent color
- Content rectangles: neutral fill

### Matrix (2x2 quadrant)
```
        High
    ┌────┬────┐
    │ Q1 │ Q2 │
    ├────┼────┤
    │ Q3 │ Q4 │
    └────┴────┘
  Low          High
```
- Quadrant size: `400x300` each
- Axis labels as standalone text
- Items positioned within quadrants

## File Naming and Location

### Default location
```
3-resources/diagrams/[topic]-[type].excalidraw.md
```

### Project-specific
```
1-projects/[project-name]/[topic]-[type].excalidraw.md
```

### Naming convention
- Lowercase, hyphen-separated
- Pattern: `[descriptive-topic]-[diagram-type].excalidraw.md`
- Examples:
  - `user-onboarding-flowchart.excalidraw.md`
  - `product-architecture-hierarchy.excalidraw.md`
  - `q1-roadmap-timeline.excalidraw.md`
  - `pricing-models-comparison.excalidraw.md`

## Quality Checklist

Before saving, verify:
- [ ] All element IDs are unique strings
- [ ] All text elements have `text`, `rawText`, and `originalText` fields
- [ ] Bound text has `containerId` set and container has matching `boundElements`
- [ ] Arrow first point is `[0, 0]`
- [ ] Arrow bindings reference valid element IDs
- [ ] Shapes with bound arrows list them in `boundElements`
- [ ] Elements fit within 1200x800 canvas
- [ ] Font family is `1` for all text
- [ ] Colors use the defined palette
- [ ] Index values are unique and sequential
- [ ] File has correct Obsidian frontmatter and wrapper
- [ ] JSON is valid and properly escaped

## Post-Generation Message

After saving the file, tell the user:
1. File path where the diagram was saved
2. Diagram type that was used
3. Number of elements generated
4. Instruction: "Open in Obsidian and switch to Excalidraw view to see the diagram"
