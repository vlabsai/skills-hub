---
name: find-skills
description: >-
  Descobre e instala skills de agentes do ecossistema skills.sh. Faz busca
  local primeiro, depois em fontes curadas e no ecossistema. Use quando
  precisar encontrar uma skill para uma tarefa especifica.
license: Apache-2.0
compatibility: Requires internet access and skills CLI
allowed-tools: Bash Read WebFetch WebSearch Glob
metadata:
  author: vector-labs
  version: "1.0"
tags: [discovery, tools]
complexity: beginner
---

# Find Skills

Discover skills from installed local skills and the open skills.sh ecosystem. Local-first: check what's already installed before searching externally.

## Workflow

### Step 1: Understand the Need

Identify from the user's request:
1. The domain (e.g., marketing, document processing, frontend, testing)
2. The specific task (e.g., writing copy, creating PDFs, optimizing conversions)
3. Whether this is common enough that a skill likely exists

### Step 2: Check Installed Skills

List what's already available locally:

```bash
npx skills ls -g
```

Also check project-level skills:

```bash
npx skills ls
```

If an installed skill matches, tell the user it's already available and how to use it. Done.

### Step 3: Search Curated Sources

If no local match, consult [references/curated-sources.md](references/curated-sources.md) for trusted repositories organized by domain. Recommend from curated sources first — these have been vetted.

To list skills from a specific source:

```bash
npx skills add <source> -l
```

Example:
```bash
npx skills add anthropics/skills -l
npx skills add coreyhaines31/marketingskills -l
```

### Step 4: Search the Ecosystem

If curated sources don't have a match, search the broader ecosystem:

```bash
npx skills find <query>
```

Tips:
- Use specific keywords: "react testing" > "testing"
- Try alternative terms: "deploy", "deployment", "ci-cd"
- Browse at https://skills.sh/ for category discovery

### Step 5: Present Options

When presenting a skill to the user, include:
1. Skill name and what it does
2. Source repository
3. Install command
4. Link to skills.sh page

Example:
```
Found "seo-audit" from coreyhaines31/marketingskills — audits SEO issues on pages.

Install: npx skills add coreyhaines31/marketingskills --skill seo-audit -g
More info: https://skills.sh/coreyhaines31/marketingskills/seo-audit
```

**Always ask the user before installing.** Never auto-install.

### Step 6: Install (After User Confirms)

```bash
npx skills add <source> --skill <skill-name> -g -y
```

- `-g` installs globally (user-level)
- `-y` skips confirmation (only use after user has already confirmed)
- Use `--skill <name>` to install a specific skill from a multi-skill repo

### When Nothing is Found

1. Acknowledge no skill was found
2. Offer to help directly with general capabilities
3. Suggest creating a custom skill: `npx skills init <name>` (reference the skill-creator skill)
