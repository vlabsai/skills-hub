# Tools & Permissões

## Tools built-in (~25)

| Categoria | Tools |
|-----------|-------|
| Shell | `bash`, `exec` |
| Filesystem | `read`, `write`, `edit`, `apply_patch` |
| Browser | `browser_*` (via Playwright/Chrome CDP) |
| Web | `web_search`, `web_fetch` |
| Media | `image`, `tts` |
| Control plane | `gateway`, `cron`, `message` |
| Sessions | `sessions_list`, `sessions_send`, `sessions_history`, `sessions_spawn` |
| Memory | `memory_search` |
| Outros | `nodes`, `canvas`, `elevated` |

## Profiles de permissão

| Profile | Pode | Não pode |
|---------|------|----------|
| `coding` | ler, escrever, executar | UI, gateway, cron |
| `analysis` | ler, explorar | escrever, editar |
| `verification` | ler, executar | escrever |
| `testing` | ler, executar, browser | escrever |
| `pr` | ler, executar (gh) | escrever |
| `scanning` | ler, executar, web search/fetch | escrever |
| `messaging` | set restrito para assistentes | quase tudo |

## Tool policy precedence (narrowing — só restringe, nunca expande)

```
Tool Profile → Provider Profile → Global Policy → Provider Policy → Agent Policy → Group Policy → Sandbox Policy
```

Cada camada pode apenas REMOVER acesso, nunca adicionar.

## Config por agente

```json5
{
  "agents": {
    "list": [{
      "id": "dev-agent",
      "tools": {
        "profile": "coding",
        "deny": ["gateway", "cron", "message", "sessions_send"],
        "alsoAllow": ["web_search", "browser"]
      }
    }]
  }
}
```

## Exec security

```json5
{
  "tools": {
    "exec": {
      "security": "ask",       // deny | ask | allow
      "ask": "dangerous"       // always | dangerous | never
    },
    "fs": {
      "workspaceOnly": true    // Restringe read/write/edit ao workspace
    },
    "elevated": {
      "enabled": false,        // Escape hatch para exec no host
      "allowFrom": []          // Manter tight
    }
  }
}
```

## Exec approvals

```bash
openclaw approvals allowlist       # Editar allowlist por agente
openclaw approvals get             # Snapshot do estado
openclaw approvals set             # Restaurar
```

Approvals vinculam "contexto exato do request + operandos de arquivo locais". São guardrails de intenção do operador, não boundary multi-tenant.

## Sandbox (Docker)

```json5
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",     // off | all | non-main
        "scope": "agent",       // agent | session | shared
        "docker": {
          "setupCommand": "apt-get install -y curl"  // Roda 1x na criação
        }
      }
    }
  }
}
```

### Workspace access no sandbox
- `"none"` (default) — workspace inacessível
- `"ro"` — mount read-only em /agent
- `"rw"` — mount read-write em /workspace

### CLI sandbox
```bash
openclaw sandbox list                         # Status containers
openclaw sandbox recreate [--all|--agent|--session]  # Reset
```

## Tools de alto risco (deny por default)

```json5
{ "deny": ["gateway", "cron", "sessions_spawn", "sessions_send", "group:automation", "group:runtime", "group:fs"] }
```

## Docs oficiais
- Tools overview: https://docs.openclaw.ai/tools/index.md
- Exec: https://docs.openclaw.ai/tools/exec
- Exec approvals: https://docs.openclaw.ai/tools/exec-approvals
- Elevated: https://docs.openclaw.ai/tools/elevated
- Browser: https://docs.openclaw.ai/tools/browser
- Sandboxing: https://docs.openclaw.ai/gateway/sandboxing
- Sandbox vs tools vs elevated: https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated
- Multi-agent sandbox: https://docs.openclaw.ai/tools/multi-agent-sandbox-tools
