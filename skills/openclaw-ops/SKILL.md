---
name: openclaw-ops
description: >-
  Referencia operacional completa do OpenClaw — arquitetura, gateway, agentes,
  skills, channels, sessions, memoria, tools, config, seguranca, Antfarm e OAuth.
  Assets por topico para consulta sob demanda. Use para operar qualquer setup OpenClaw.
license: Apache-2.0
compatibility: claude-code
allowed-tools: Read Glob Grep WebFetch WebSearch
metadata:
  author: vector-labs
  version: "1.0"
tags: [devops, infrastructure, ai-agents]
complexity: advanced
featured: true
---

# OpenClaw Operations

Conhecimento operacional generico do OpenClaw. Nada especifico de instancia — serve para operar qualquer setup. Assets organizados por topico, leia o relevante para a tarefa.

## Arquitetura (resumo)

Gateway WebSocket (:18789) = control plane unico (Node.js 22+). Recebe mensagens de Channels (40+), roteia para Agentes isolados via ReAct loop (reason → act → observe), usando Tools (~25 built-in) e Skills (SKILL.md runbooks). Estado em Sessions (JSONL), Memory (SQLite + vector embeddings), Git (workspace). Config: `~/.openclaw/openclaw.json` (JSON5).

## Assets

| Tarefa / Duvida | Asset |
|------------------|-------|
| Camadas, componentes, data flow, diretorios | `assets/architecture.md` |
| Gateway: lifecycle, protocol, bind, auth, discovery | `assets/gateway.md` |
| Agentes: criacao, isolamento, routing, workspace files (soul-based) | `assets/agents.md` |
| Skills: SKILL.md format, precedencia, ClawHub, metadata, gating | `assets/skills-system.md` |
| Channels: setup, politicas DM/grupo, pairing, media | `assets/channels.md` |
| Sessions, compaction, memoria, embeddings, persistencia | `assets/sessions-memory.md` |
| Tools, permissoes, profiles, policy precedence, sandbox, exec | `assets/tools-permissions.md` |
| openclaw.json: estrutura, keys, secrets, env, $include, hot-reload | `assets/config.md` |
| Seguranca: modelo de confianca, audit, sandbox, incident response | `assets/security.md` |
| CLI: todos os comandos com subcomandos | `assets/cli.md` |
| Antfarm: multi-agent workflows, YAML, dashboard, patches, operacao | `assets/antfarm.md` |
| OAuth: lifecycle, auto-refresh, re-autenticacao manual, bugs | `assets/oauth.md` |
| URLs da documentacao oficial para web_fetch | `assets/docs-urls.md` |

## Checklist operacional

```bash
openclaw gateway health
openclaw --version
openclaw channels status
openclaw skills list --eligible
openclaw doctor
```
