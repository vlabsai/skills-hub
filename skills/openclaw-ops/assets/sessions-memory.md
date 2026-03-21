# Sessions & Memory

## Sessions

### Session keys (encode security boundaries)
- `agent:<id>:main` — sessão principal (full access)
- `agent:<id>:dm:<channel>:<peer>` — DM (sandboxed por padrão)
- `agent:<id>:group:<channel>:<group>` — Grupo (sandboxed por padrão)

### Storage
JSONL append-only em `~/.openclaw/agents/<id>/sessions/<key>.jsonl`.
Cada linha = um turno (user msg, agent thought, tool call, tool result, response).

### CLI
```bash
openclaw sessions                  # Listar
openclaw sessions --agent <id>     # Por agente
openclaw sessions --all-agents     # Todos
openclaw sessions --active 60      # Ativas nos últimos N min
openclaw sessions cleanup          # Manutenção + pruning
```

### Config
```json5
{
  "session": {
    "dmScope": "per-channel-peer",     // main | per-peer | per-channel-peer | per-account-channel-peer
    "reset": {
      "mode": "daily",                // daily | idle | manual
      "atHour": 4,                    // Hora do reset (daily mode)
      "idleMinutes": 120              // Minutos idle antes de reset
    },
    "threadBindings": {
      "enabled": true,
      "idleHours": 24,
      "maxAgeHours": 0                // 0 = sem limite
    },
    "maintenance": {
      "mode": "enforce",
      "pruneAfter": "7d",
      "maxEntries": 500,
      "rotateBytes": "10mb"
    }
  }
}
```

### dmScope
- `main` — todos os DMs compartilham sessão principal
- `per-peer` — isolado por sender
- `per-channel-peer` — isolado por canal + sender (recomendado)
- `per-account-channel-peer` — isolado por account + canal + sender

## Compaction (auto-summarização)

Quando contexto se aproxima do limit do modelo:
1. LLM gera sumário dos segmentos completos de conversa
2. Turns originais substituídos pelo sumário compacto
3. Marker de compaction gravado no JSONL
4. Info crítica preservada, raciocínio verbose cortado
5. **Memory flush** (opcional): promove detalhes importantes para MEMORY.md

Permite conversas infinitas mantendo continuidade semântica.

Config: `agents.defaults.compaction.mode: "safeguard"` (default)

## Memory System

### Arquitetura
- **Database:** `~/.openclaw/memory/<agentId>.sqlite`
- **Search:** Hybrid — vector embeddings (semântico) + BM25 (keyword)
- **Embedding providers (cascata):** local model → OpenAI → Gemini → disabled
- **Auto-reindex:** file watcher com 1.5s debounce

### CLI
```bash
openclaw memory search "<query>"   # Buscar na memória
openclaw memory reindex            # Reindexar embeddings
```

### Tipos de memória
| Tipo | Arquivo | Escopo |
|------|---------|--------|
| Longo prazo curada | MEMORY.md | Apenas sessão principal |
| Notas diárias | memory/YYYY-MM-DD.md | Por sessão |
| Git history | .git/ | Versionamento workspace |
| Transcripts | sessions/*.jsonl | Completos, per-agent |

### Regras de memória
- MEMORY.md só é lido/escrito na sessão principal (não em grupo/shared)
- Notas diárias: carrega hoje + ontem no início de cada sessão
- Para persistir: DEVE escrever em arquivo (não existem "mental notes")
- Memory search via tool `memory_search` (hybrid: vector + FTS)

## Docs oficiais
- Sessions: https://docs.openclaw.ai/concepts/session
- Session deep dive: https://docs.openclaw.ai/reference/session-management-compaction
- Session pruning: https://docs.openclaw.ai/concepts/session-pruning
- Compaction: https://docs.openclaw.ai/concepts/compaction
- Memory: https://docs.openclaw.ai/concepts/memory
- Context: https://docs.openclaw.ai/concepts/context
