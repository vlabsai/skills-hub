# Synthesis Templates for Deep Research

Prompt templates for the synthesis and patch agents. These are read by sub-agents or inlined into sub-agent prompts — never loaded into the orchestrator's main context.

## Synthesis Agent

Spawn with `subagent_type="general-purpose"`.

```
SYNTHESIS TASK: Compile research findings into a final report.

RESEARCH BRIEF:
[Original research question/brief — paste the input context here]

AGENT SUMMARIES:
[Paste the 3-5 line summaries returned by each agent]

OUTPUT DIRECTORY: [output-dir]
  — Read all agent-*.md files in this directory for full findings

REPORT PATH: [final-report-path]
REPORT TEMPLATE PATH: [path-to-skill]/templates/report_template.md

INSTRUCTIONS:
1. Read the report template from REPORT TEMPLATE PATH
2. Read ALL agent-*.md files from the output directory
3. Merge findings — deduplicate, group by theme
4. Cross-reference — identify claims supported by multiple agents (triangulation)
5. Resolve contradictions — note them explicitly in the report
6. Generate insights — patterns, implications, second-order effects
7. If critical gaps found, note them in the Limitations section
8. Write the final report to REPORT PATH following the template structure

WRITING STANDARDS:
- Prose-first (bullets only for distinct lists)
- Every factual claim cited inline: "Market reached $2.4B [1]"
- Distinguish facts (from sources) from synthesis (your analysis)
- No vague attributions ("studies show...") — always specific: "According to [1]..."
- Admit gaps: "No sources found for X" rather than fabricating
- Citation format: [N] inline, full bibliography at end
- Bibliography format: [N] Author/Org (Year). "Title". URL (Retrieved: YYYY-MM-DD)

RETURN FORMAT (to orchestrator):
**Report written to**: [path]
**Key numbers**: [3-5 most important statistics/data points from the report]
**Overall confidence**: high/medium/low
**Gaps noted**: [any critical gaps that may need follow-up]
```

## Patch Agent (Late Findings)

Spawn with `subagent_type="general-purpose"`. Use when agents complete after synthesis or when follow-up agents return new data.

```
PATCH TASK: Update an existing research report with new findings.

LATE AGENT OUTPUT: [output-dir]/agent-[late-slug].md
EXISTING REPORT: [final-report-path]

INSTRUCTIONS:
1. Read the late agent's output file
2. Read the existing report
3. Identify high-value additions (new data points, stronger evidence, resolved gaps)
4. Edit the report to integrate additions — update relevant sections and bibliography
5. Do NOT rewrite existing content unless the new findings contradict it

RETURN FORMAT:
**Additions**: [1-2 line summary of what was added]
**Sections modified**: [list of section names touched]
```
