---
name: antfarm-ops
description: >-
  Referencia operacional do Antfarm — orquestrador de times de agentes AI sobre
  OpenClaw. Arquitetura Ralph Loop, workflows YAML, dashboard, patches, operacao.
  Assets por topico para consulta sob demanda.
license: Apache-2.0
compatibility: claude-code
allowed-tools: Read Glob Grep WebFetch WebSearch
metadata:
  author: vector-labs
  version: "1.0"
tags: [ai-agents, workflows, multi-agent]
complexity: advanced
featured: true
links:
  - label: Diagrama Interativo de Arquitetura
    url: https://skills.vectorlabs.com.br/antfarm-ops/arquitetura.html
    icon: "🏗️"
---

# Antfarm Operations

Conhecimento operacional do Antfarm — orquestrador de times de agentes AI que roda nativamente sobre o OpenClaw. Para conhecimento da plataforma OpenClaw em si (gateway, agentes, sessions, memory, tools), veja a skill `openclaw-ops`.

## Diagrama Interativo

[Explorar arquitetura visual Antfarm](https://skills.vectorlabs.com.br/antfarm-ops/arquitetura.html) — Visao drill-down com todos os componentes expansiveis: workflow.yml, polling, handoff, dashboard e pontos de integracao com o OpenClaw.

## O que e o Antfarm

CLI TypeScript que orquestra times de agentes AI no OpenClaw. YAML + SQLite + cron, zero infraestrutura extra. O Antfarm **nao e parte do OpenClaw** — e um projeto externo (MIT, por Ryan Carson) que usa o OpenClaw como runtime.

## Assets

| Tarefa / Duvida | Asset |
|------------------|-------|
| Arquitetura, workflows, roles, CLI, dashboard, bugs, patches, operacao | `assets/antfarm.md` |
| URLs da documentacao oficial (repo, site, OpenClaw docs relacionados) | `assets/docs-urls.md` |

## Checklist operacional

```bash
antfarm workflow list              # Workflows instalados
antfarm workflow runs              # Runs ativos
openclaw cron list                 # Crons do Antfarm
antfarm dashboard status           # Dashboard rodando?
```
