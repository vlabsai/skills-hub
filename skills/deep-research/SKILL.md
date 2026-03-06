---
name: deep-research
description: >-
  Pipeline de pesquisa profunda com multiplos agentes em paralelo. Gera
  relatorios em markdown com citacoes e protocolo anti-alucinacao. Use para
  analises comparativas, investigacoes de mercado e pesquisas abrangentes.
license: Apache-2.0
compatibility: Requires internet access
allowed-tools: Bash Read Edit Write WebFetch WebSearch Agent Glob Grep
metadata:
  author: vector-labs
  version: "1.0"
tags: [research, analysis]
complexity: advanced
featured: true
---

# Deep Research

Agent-orchestrated research pipeline. Takes input text, decomposes into parallel agent tasks, synthesizes results into a citation-backed report.

**Context budget**: Orchestrator stays lean. Agents write to files, return summaries. Synthesis is delegated to a sub-agent. NEVER read agent output files or reference files into orchestrator context — pass paths to sub-agents. NEVER use `run_in_background` — it causes TaskOutput to return full agent logs. If context approaches limit before synthesis, the research is lost.

## Workflow

### 1. Analyze Input

Classify the input:
- **Question**: Direct research question → extract core topic + angles
- **Brief**: Context document with research directive → extract what to investigate
- **Seed context**: Background text that needs expansion → identify knowledge gaps

Determine complexity (drives agent count):
- **Focused** (3 agents): Single topic, clear boundaries
- **Broad** (4-5 agents): Multi-faceted topic, comparison, or trend analysis

### 2. Decompose into Agent Tasks

Break research into 3-5 **independent** investigation angles. Each angle becomes a Task agent.

**Decomposition heuristics:**
- One angle per distinct sub-question or perspective
- Separate factual retrieval from opinion/analysis sources
- Include at least one critical/contrarian angle
- If project context is relevant, dedicate one agent to local analysis

**Agent types** (see [agent-templates](./reference/agent-templates.md) for full prompts):

| Type | Tools | Use when |
|------|-------|----------|
| `web-researcher` | WebSearch, WebFetch | External facts, data, current info |
| `local-analyst` | Grep, Read, Glob | Project files, meeting notes, internal docs |
| `deep-diver` | WebSearch, WebFetch | Single source/topic requiring multi-step investigation |

### 3. Deploy Agents (Parallel)

**CRITICAL: Launch ALL agents in a single message with multiple Task tool calls.**

**CRITICAL: Do NOT use `run_in_background: true`.** Launch all agents as parallel Task calls in a single message. They execute concurrently, and each returns ONLY the agent's final message (the 3-5 line summary). Background agents write full conversation logs to output files — reading those with TaskOutput will overflow orchestrator context.

**Context management**: Do NOT read reference files into orchestrator context. Instead, inline the relevant template from [agent-templates](./reference/agent-templates.md) directly into each agent's prompt.

**Output directory**: Before launching agents, create an output directory:
`[report-directory]/research-data/`

Each agent prompt MUST include these instructions:
1. Write full findings to a file: `[output-dir]/agent-[angle-slug].md` using the Write tool
2. Return ONLY a 3-5 line summary to the orchestrator containing:
   - File path where findings were written
   - Top 3 key findings (one line each)
   - Overall confidence level (high/medium/low)

```
[Single message — all parallel]
Task(subagent_type="general-purpose", description="Research angle A", prompt=<template with OUTPUT_DIR + file-write instructions>)
Task(subagent_type="general-purpose", description="Research angle B", prompt=<template with OUTPUT_DIR + file-write instructions>)
Task(subagent_type="general-purpose", description="Research angle C", prompt=<template with OUTPUT_DIR + file-write instructions>)
Task(subagent_type="Explore", description="Local context analysis", prompt=<template with OUTPUT_DIR + file-write instructions>)
...
```

Each agent returns ONLY a concise summary (NOT full findings) — see return format in [agent-templates](./reference/agent-templates.md). Full findings are written to the agent's output file.

### 4. Synthesize & Write Report (Delegated)

**CRITICAL: Do NOT synthesize in main context.** Delegate to a synthesis sub-agent.

**Output location**: `[relevant-project-or-area-folder]/research-[topic-slug]-[YYYY-MM-DD].md`
If no clear project context, ask the user where to save.

Spawn a single `general-purpose` synthesis agent using the prompt from [synthesis-templates](./reference/synthesis-templates.md#synthesis-agent). Fill in:
- **RESEARCH BRIEF**: the original input context
- **AGENT SUMMARIES**: the 3-5 line summaries returned by each agent
- **OUTPUT DIRECTORY**: path to `research-data/`
- **REPORT PATH**: final report location
- **REPORT TEMPLATE PATH**: `~/.claude/skills/deep-research/templates/report_template.md`

The orchestrator receives only a summary — the full report is written to disk by the sub-agent.

### 4b. Handle Late Agents

If agents complete after synthesis, spawn a patch agent using the prompt from [synthesis-templates](./reference/synthesis-templates.md#patch-agent-late-findings). Fill in the late agent's output file path and the existing report path.

### 5. Validate

Run validation after writing:
```bash
python ~/.claude/skills/deep-research/scripts/validate_report.py --report [path]
```

Optionally verify citations:
```bash
python ~/.claude/skills/deep-research/scripts/verify_citations.py --report [path]
```

If validation fails: fix and re-validate (max 2 attempts).

## Anti-Hallucination Protocol

- **Source grounding**: Every factual claim cites a specific source [N]
- **No fabricated citations**: If unsure a source says X, do NOT cite it
- **Label inference**: "This suggests..." not "Research shows..."
- **Admit uncertainty**: "No sources found" over invented references

## Error Handling

- <5 sources after exhaustive search → note limitation, proceed with extra verification
- Agent returns empty/low-quality → spawn replacement with refined query
- 2 validation failures → stop, report issues, ask user

## Scripts

- `scripts/validate_report.py` — Report quality validation
- `scripts/verify_citations.py` — Citation verification (DOI + URL checks)
- `scripts/source_evaluator.py` — Source credibility scoring (0-100)
- `scripts/citation_manager.py` — Citation tracking utilities

## References (for sub-agents, not orchestrator)

- [Agent Templates](./reference/agent-templates.md) — Structured prompts for research agents. Pass to sub-agents or inline into their prompts.
- [Synthesis Templates](./reference/synthesis-templates.md) — Prompts for synthesis and patch agents.
- [Report Template](./templates/report_template.md) — Report output structure. Synthesis agent reads this from disk.
