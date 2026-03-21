# Arquitetura OpenClaw

## Camadas

```
┌─ Interfaces: CLI, Web UI (Control UI), macOS app, iOS/Android nodes ─┐
├─ Gateway (WebSocket :18789) ─ Control Plane único ───────────────────┤
│  ├─ Session Router (mensagem → agente correto)                       │
│  ├─ Channel Adapters (WhatsApp/Baileys, Telegram/grammY, Discord...) │
│  ├─ Auth & Device Pairing (Ed25519 challenge-response)               │
│  └─ Event Bus (agent, presence, health, tick a cada 15s)             │
├─ Agent Runtime (PiEmbeddedRunner / Pi Agent Core) ───────────────────┤
│  ├─ Context Assembly: Base PI Core → AGENTS.md → SOUL.md → Skills    │
│  ├─ ReAct Loop: reason → act (tool) → observe → repeat              │
│  ├─ Tool Dispatch (com sandbox opcional Docker)                      │
│  ├─ Compaction (auto-summarização quando contexto enche)             │
│  └─ Memory (SQLite + vector embeddings, hybrid search)               │
├─ Storage ────────────────────────────────────────────────────────────┤
│  ├─ Config: openclaw.json (JSON5, hot-reload)                        │
│  ├─ Sessions: JSONL append-only por agente                           │
│  ├─ Memory: SQLite + embeddings (semantic + BM25)                    │
│  ├─ Workspaces: Git repos por agente                                 │
│  └─ Credentials: 0600 permissions                                    │
└──────────────────────────────────────────────────────────────────────┘
```

## Diretórios (~/.openclaw/)

```
~/.openclaw/
├── openclaw.json              # Config principal (JSON5)
├── agents/<id>/agent/         # Auth por agente
│   ├── auth-profiles.json     # OAuth tokens
│   └── models.json            # Model overrides por agente
├── workspace/                 # Workspace do agente principal (git repo)
│   ├── AGENTS.md / SOUL.md / IDENTITY.md / USER.md / TOOLS.md
│   ├── MEMORY.md / HEARTBEAT.md / BOOTSTRAP.md
│   ├── memory/                # Notas diárias (YYYY-MM-DD.md)
│   └── skills/                # Skills do workspace (maior precedência)
├── workspaces/                # Workspaces de agentes adicionais
├── skills/                    # Skills gerenciadas (2a precedência)
├── memory/<agentId>.sqlite    # Vector embeddings + FTS
├── browser/                   # Perfil Chrome/Playwright
├── credentials/               # Secrets (permissão 0600)
├── cron/jobs.json             # Cron jobs
├── plugins/                   # Extensões npm
├── identity/device.json       # Ed25519 keypair
├── canvas/                    # Canvas/A2UI server data
├── logs/ media/ devices/ delivery-queue/ subagents/
└── exec-approvals.json        # Allowlists de execução
```

## Data flow de uma mensagem

1. **Ingestion** — Adapter do canal (Baileys/grammY/discord.js) recebe evento
2. **Access Control** — Verifica allowlist, DM pairing, grupo
3. **Session Resolution** — Mapeia para session key (`agent:<id>:dm:<channel>:<peer>`)
4. **Context Assembly** — Carrega sessão, monta system prompt, injeta skills relevantes, busca memória
5. **Model Invocation** — Streaming para o LLM provider
6. **Tool Dispatch** — Intercepta tool calls, executa (sandbox se necessário), resultado volta ao contexto
7. **Response Delivery** — Formata para o canal (markdown, chunking, mídia), transmite, persiste sessão

Latência típica: access control ~10ms, disk load ~50ms, prompt assembly ~100ms, first token 200-500ms.

## Componentes-chave

- **Pi Agent Core** (`@mariozechner/pi-agent-core`): runtime do agente, ReAct loop
- **Pi AI** (`@mariozechner/pi-ai`): integrações com LLM providers
- **PiEmbeddedRunner**: execução embedida no gateway
- **Canal únicos por host**: WhatsApp (Baileys) exige single-device, 1 gateway por host
- **Canvas/A2UI**: servidor separado (:18793), agents geram HTML com atributos `a2ui-*`, interação bidirecional

## Docs oficiais
- Arquitetura: https://docs.openclaw.ai/concepts/architecture
- Agent runtime: https://docs.openclaw.ai/concepts/agent
- Agent loop: https://docs.openclaw.ai/concepts/agent-loop
