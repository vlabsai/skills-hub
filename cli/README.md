# @vector-labs/skills

CLI to browse and install curated AI skills from [Vector Labs Skills Hub](https://vlabsai.github.io/skills-hub/).

Skills are markdown instructions that teach AI assistants (Claude Code, Cursor, Copilot, Gemini) to perform specific tasks — from generating dashboards to reviewing PRs.

## Quick start

```bash
# List all available skills
npx @vector-labs/skills list

# Install a skill into your project
npx @vector-labs/skills add <skill-name>
```

The CLI auto-detects your AI tool and installs to the right directory:

| Tool | Detected by | Installs to |
|------|------------|-------------|
| Claude Code | `.claude/` | `.claude/skills/` |
| Cursor | `.cursor/` | `.cursor/skills/` |
| GitHub Copilot | `.github/copilot-*` | `.github/skills/` |
| Gemini CLI | `.gemini/` | `.gemini/skills/` |

## Commands

```bash
npx @vector-labs/skills list                      # List available skills
npx @vector-labs/skills add <skill-name>          # Install a skill
npx @vector-labs/skills add <name> --tool cursor  # Install for specific tool
npx @vector-labs/skills info <skill-name>         # Show skill details
npx @vector-labs/skills setup                     # Configure GitHub token (optional)
```

## Options

| Flag | Description |
|------|-------------|
| `--tool <id>` | Target tool: `claude-code`, `cursor`, `copilot`, `gemini` |
| `--dest <path>` | Custom install path (overrides auto-detection) |
| `--branch <name>` | GitHub branch to fetch from (default: `main`) |
| `--source <path>` | Read skills from a local directory instead of GitHub |
| `-y, --yes` | Skip prompts, use defaults |

## Browse the catalog

Visit the [Skills Hub](https://vlabsai.github.io/skills-hub/) to explore skills by category, search, and read documentation before installing.

## License

MIT
