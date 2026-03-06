# Agent Templates for Deep Research

Structured prompts for spawning research agents via the Task tool. All agents use `subagent_type="general-purpose"` unless noted otherwise.

**IMPORTANT**: These templates are reference documentation. Do NOT read this file into the main orchestrator context. Instead, inline the relevant template directly into each agent's prompt when spawning agents in Step 3.

## Web Researcher

For gathering external facts, data, and current information on a specific angle.

```
RESEARCH TASK: [Specific angle/question]

CONTEXT: [1-2 sentences on broader research topic and why this angle matters]

OUTPUT_DIR: [path to research-data directory]
OUTPUT_FILE: [OUTPUT_DIR]/agent-[angle-slug].md

INSTRUCTIONS:
1. Run 3-5 WebSearch queries exploring this angle from different keywords
2. For the 2-3 most promising results, use WebFetch to extract detailed content
3. Focus on: specific data points, statistics, dates, named entities, quotes
4. Write your FULL findings to OUTPUT_FILE using the Write tool (structure below)
5. Return ONLY a concise summary to the orchestrator (see RETURN FORMAT)

FINDINGS FILE STRUCTURE (write to OUTPUT_FILE):
## Findings
- **Claim**: [factual statement] | **Source**: [title](URL) | **Confidence**: high/medium/low
[repeat for each finding]

## Key Data Points
- [specific numbers, dates, statistics — always with source]

## Contradictions or Gaps
- [anything conflicting or missing]

## Sources Used
- [N] Author/Org (Year). "Title". URL
[list all sources consulted, even if not all yielded findings]

RETURN FORMAT (to orchestrator — keep this SHORT):
**File**: [OUTPUT_FILE path]
**Top findings**: 1) [finding] 2) [finding] 3) [finding]
**Confidence**: high/medium/low
```

## Local Analyst

For analyzing project files, meeting notes, or internal documentation. Use `subagent_type="Explore"`.

```
ANALYSIS TASK: [What to look for in the codebase/docs]

CONTEXT: [Broader research topic and what internal context would help]

OUTPUT_DIR: [path to research-data directory]
OUTPUT_FILE: [OUTPUT_DIR]/agent-[angle-slug].md

INSTRUCTIONS:
1. Search project files relevant to [topic] using Glob and Grep
2. Read the most relevant files
3. Extract facts, decisions, context, and data points
4. Write your FULL findings to OUTPUT_FILE using the Write tool (structure below)
5. Return ONLY a concise summary to the orchestrator (see RETURN FORMAT)

FINDINGS FILE STRUCTURE (write to OUTPUT_FILE):
## Findings from Project Context
- **Finding**: [what was found] | **Source**: [file path:line] | **Relevance**: high/medium/low
[repeat]

## Key Context
- [decisions, constraints, or background that informs the research]

## Gaps
- [what internal docs don't cover that external research should address]

RETURN FORMAT (to orchestrator — keep this SHORT):
**File**: [OUTPUT_FILE path]
**Top findings**: 1) [finding] 2) [finding] 3) [finding]
**Confidence**: high/medium/low
```

## Deep Diver

For multi-step investigation of a single source, topic, or complex question that requires following leads.

```
INVESTIGATION TASK: [Specific topic requiring deep exploration]

CONTEXT: [Why this needs depth beyond a simple search]

OUTPUT_DIR: [path to research-data directory]
OUTPUT_FILE: [OUTPUT_DIR]/agent-[angle-slug].md

INSTRUCTIONS:
1. Start with 2-3 broad WebSearch queries
2. Follow the most promising leads with WebFetch for full content
3. If a source references other important sources, search for those too
4. Build a chain of evidence on this topic
5. Aim for 5-10 high-quality sources on this specific angle
6. Write your FULL findings to OUTPUT_FILE using the Write tool (structure below)
7. Return ONLY a concise summary to the orchestrator (see RETURN FORMAT)

FINDINGS FILE STRUCTURE (write to OUTPUT_FILE):
## Investigation Summary
[2-3 paragraph narrative of what was found and how findings connect]

## Evidence Chain
- **Claim**: [statement] | **Source**: [title](URL) | **Confidence**: high/medium/low
[repeat — ordered by strength of evidence]

## Key Data Points
- [specific numbers, dates, statistics with sources]

## Open Questions
- [what remains unanswered after investigation]

## Sources Used
- [N] Author/Org (Year). "Title". URL

RETURN FORMAT (to orchestrator — keep this SHORT):
**File**: [OUTPUT_FILE path]
**Top findings**: 1) [finding] 2) [finding] 3) [finding]
**Confidence**: high/medium/low
```

## Usage Notes

- Always provide **CONTEXT** so agents understand how their angle fits the whole
- Keep agent prompts focused — one angle per agent, not the full research question
- For **Focused** research (3 agents): 2 web-researchers + 1 deep-diver
- For **Broad** research (5-7 agents): 3-4 web-researchers + 1-2 deep-divers + 1 local-analyst (if project context relevant)
- Launch ALL agents in a single message for parallel execution
- **Every agent MUST write full findings to a file and return only a summary** — this is critical for context management
- The orchestrator should create `[output-dir]/` before launching agents (e.g., `mkdir -p` via Bash)
