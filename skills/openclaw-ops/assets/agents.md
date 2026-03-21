# Agentes

Cada agente = contexto de execução 100% isolado: workspace, auth, sessions, tools.

## CLI

```bash
openclaw agents list              # Listar agentes
openclaw agents list --bindings   # Com routing bindings
openclaw agents add <id>          # Wizard criação (workspace, auth, sessions)
openclaw agents delete <id>       # Remover
openclaw agents set-identity <id> # Alterar identidade
```

## Estrutura de um agente

- **Workspace:** diretório de trabalho (git repo). Path: `~/.openclaw/workspace` (main) ou `~/.openclaw/workspace-<id>`
- **agentDir:** credentials em `~/.openclaw/agents/<id>/agent/` — NUNCA compartilhar entre agentes (causa collision)
- **Sessions:** histórico em `~/.openclaw/agents/<id>/sessions/` (JSONL)
- **Tools profile:** perfil de permissões + deny/allow lists

## Workspace files (Soul-Based System)

| Arquivo | Função | Precedência no prompt |
|---------|--------|-----------------------|
| AGENTS.md | Regras operacionais, baseline não-negociável | Alta (após PI Core) |
| SOUL.md | Personalidade, tom, idioma (não afeta tools) | Média |
| IDENTITY.md | Nome, criatura, emoji, avatar | Metadata |
| USER.md | Perfil do humano (nome, timezone, contexto) | Contexto |
| TOOLS.md | Notas sobre ferramentas locais (não é registry) | Contexto |
| HEARTBEAT.md | Tarefas periódicas (checklist a cada N min) | Cron |
| MEMORY.md | Memória curada de longo prazo | Contexto |
| BOOTSTRAP.md | Guia inicial (deletar após primeiro run) | Apenas 1x |

Templates oficiais: https://docs.openclaw.ai/reference/templates/

Composição do system prompt: `Base PI Core → AGENTS.md → SOUL.md → Skills relevantes → Memory → Tool defs`

## Routing de mensagens (precedência alta → baixa)

1. Peer match exato (DM/grupo/canal ID)
2. Parent peer (thread inheritance)
3. Guild + role (Discord)
4. Guild ID only
5. Team ID (Slack)
6. Account ID
7. Channel wildcard
8. **Default agent (fallback)**

Bindings com múltiplos campos usam AND. Primeiro match no mesmo nível ganha.

## Multi-agent config

```json5
{
  "agents": {
    "list": [
      { "id": "main", "default": true, "workspace": "~/.openclaw/workspace" },
      { "id": "work", "workspace": "~/.openclaw/workspace-work",
        "model": { "primary": "anthropic/claude-sonnet-4-5" },
        "tools": { "profile": "coding", "deny": ["gateway"] },
        "groupChat": { "mentionPatterns": ["@work", "work"] }
      }
    ]
  },
  "bindings": [
    { "agentId": "work", "match": { "channel": "slack", "teamId": "T123" } }
  ]
}
```

## Inter-agent communication

```json5
{
  "tools": {
    "agentToAgent": { "enabled": false, "allow": ["agent1", "agent2"] }
  }
}
```

Session tools: `sessions_list`, `sessions_send`, `sessions_history`, `sessions_spawn`

## Sandbox por agente

```json5
{
  "sandbox": { "mode": "all", "scope": "agent" },
  "tools": { "profile": "coding", "deny": ["gateway", "cron"] }
}
```

Modes: `off`, `all`, `non-main`. Scopes: `agent`, `session`, `shared`.

## Docs oficiais
- Multi-agent: https://docs.openclaw.ai/concepts/multi-agent
- Agent workspace: https://docs.openclaw.ai/concepts/agent-workspace
- Agent runtime: https://docs.openclaw.ai/concepts/agent
- System prompt: https://docs.openclaw.ai/concepts/system-prompt
