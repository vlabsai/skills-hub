---
name: vercel-deploy
description: >-
  Faz deploy de projetos na Vercel direto pela CLI autenticada. Suporta
  sites estaticos, Next.js, Node.js e outros frameworks. Resolve
  automaticamente escopo, linking de projeto e modo nao-interativo.
license: Apache-2.0
compatibility: Requires Vercel CLI authenticated
allowed-tools: Bash Read Write Glob
metadata:
  author: vector-labs
  version: "1.0"
tags: [deploy, vercel, hosting]
complexity: beginner
---

# Vercel Deploy

Deploy any project to the user's authenticated Vercel account. Handles the non-interactive CLI
quirks automatically (scope resolution, project creation, project linking).

## Prerequisites

- `vercel` CLI installed (`npm i -g vercel`)
- Authenticated (`vercel login` done previously)

## Quick Deploy

Run the deploy script:

```bash
bash ~/.claude/skills/vercel-deploy/scripts/deploy.sh <source-dir> <project-name> [--preview]
```

- `source-dir`: Directory containing the project (must have `index.html` or `package.json`)
- `project-name`: Vercel project name (lowercase, hyphens, e.g. `my-cool-app`)
- `--preview`: Optional flag to deploy as preview instead of production

The script automatically:
1. Resolves the Vercel org ID from existing config
2. Creates the project if it doesn't exist
3. Writes `.vercel/project.json` to bypass the non-interactive linking bug
4. Deploys to production (or preview)

## Static Sites

For deploying a single HTML file or a folder with `index.html`:

1. Prepare a directory with the files (copy if needed to a temp folder)
2. Ensure there's an `index.html` at the root
3. Run the deploy script

Example:
```bash
mkdir -p /tmp/my-deploy
cp path/to/page.html /tmp/my-deploy/index.html
bash ~/.claude/skills/vercel-deploy/scripts/deploy.sh /tmp/my-deploy my-project-name
```

## Framework Projects (Next.js, Node, etc.)

For projects with `package.json`, deploy directly from the project directory:

```bash
bash ~/.claude/skills/vercel-deploy/scripts/deploy.sh ./my-nextjs-app my-project-name
```

Vercel auto-detects the framework and configures the build.

## Naming

Project names must be lowercase with hyphens. Production URL: `https://<project-name>.vercel.app`.

## Updating Existing Deployments

Re-run the same command with the same project name. The script detects the existing project and deploys over it.

## Troubleshooting

If the script fails on org ID resolution, ensure at least one project exists in the Vercel account.
If no projects exist, create one manually first with `vercel project add <name>`.
