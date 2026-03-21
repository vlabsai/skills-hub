# Configuration (openclaw.json)

Formato JSON5 (suporta comentários). Localização: `~/.openclaw/openclaw.json`. Defaults seguros se ausente.

## CLI

```bash
openclaw config get <key>          # Ler (dot notation: agents.defaults.model.primary)
openclaw config set <key> <value>  # Definir
openclaw config unset <key>        # Remover
openclaw config validate           # Validar schema
openclaw onboard                   # Wizard interativo
openclaw configure                 # Config wizard
```

## Root-level keys

| Key | Função |
|-----|--------|
| `agents` | Defaults, lista de agentes, model, workspace, concurrency |
| `channels` | Configs por canal (WhatsApp, Telegram, Discord...) |
| `gateway` | Port, bind, auth, reload, push notifications |
| `session` | DM scope, thread bindings, reset, maintenance |
| `cron` | Jobs, retention, concurrency |
| `hooks` | Webhooks endpoints e routing |
| `tools` | Permissões, exec security, fs restrictions, elevated |
| `browser` | Headless, noSandbox, SSRF policy |
| `skills` | Entries, load config, extra dirs |
| `audio` / `talk` | Voz e TTS |
| `ui` | Customização de interface |
| `logging` | Levels, redaction, output |
| `identity` | Device identity config |
| `bindings` | Multi-agent routing rules |
| `env` | Environment vars e secrets |
| `$include` | Incluir configs de outros arquivos |

## Estrutura agents

```json5
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "openai-codex/gpt-5.4",
        "fallbacks": ["anthropic/claude-sonnet-4-5"]
      },
      "workspace": "~/.openclaw/workspace",
      "compaction": { "mode": "safeguard" },
      "maxConcurrent": 4,
      "subagents": { "maxConcurrent": 8 },
      "heartbeat": {
        "every": "30m",
        "target": "last",
        "directPolicy": "allow"
      },
      "sandbox": {
        "mode": "non-main",
        "scope": "agent"
      },
      "imageMaxDimensionPx": 1200
    },
    "list": [
      {
        "id": "main", "default": true,
        "name": "Bot Name",
        "workspace": "~/.openclaw/workspace",
        "tools": { "profile": "coding", "deny": ["gateway"] },
        "groupChat": { "mentionPatterns": ["@bot"] }
      }
    ]
  }
}
```

## $include (split de config)

```json5
{
  "agents": { "$include": "./agents.json5" },
  "channels": { "$include": "./channels.json5" },
  "broadcast": {
    "$include": ["./clients/a.json5", "./clients/b.json5"]  // Array: deep-merge
  }
}
```

- Single file: replace no objeto
- Array de files: deep-merge (último ganha)
- Nesting até 10 níveis
- Paths relativos resolvem do arquivo que inclui

## Environment & Secrets

```json5
{
  "env": {
    "API_KEY": "value",                         // Direto
    "vars": { "OTHER_KEY": "value" },           // Namespace
    "shellEnv": { "enabled": true, "timeoutMs": 15000 }  // Herdar do shell
  }
}
```

### Secret refs (em qualquer campo)

```json5
{ "source": "env", "provider": "default", "id": "ENV_VAR" }
{ "source": "file", "id": "/path/to/secret" }
{ "source": "exec", "id": "command-to-run" }
```

## Hot-reload

`gateway.reload.mode`:
- `hybrid` (default) — hot-apply mudanças seguras, auto-restart para críticas
- `hot` — apenas mudanças seguras (ignora críticas)
- `restart` — restart para toda mudança
- `off` — manual only

Mudanças críticas (requerem restart): port, bind, auth mode.

## Cron config

```json5
{
  "cron": {
    "enabled": true,
    "maxConcurrentRuns": 2,
    "sessionRetention": "24h",
    "runLog": { "maxBytes": "2mb", "keepLines": 2000 }
  }
}
```

## Models config

```json5
{
  "agents": {
    "defaults": {
      "model": { "primary": "provider/model", "fallbacks": ["..."] },
      "models": {
        "provider/model": { "alias": "ShortName" }
      }
    }
  },
  "auth": {
    "profiles": {
      "provider:default": {
        "type": "oauth",
        "provider": "openai-codex"
      }
    }
  }
}
```

## Docs oficiais
- Config: https://docs.openclaw.ai/gateway/configuration
- Config reference: https://docs.openclaw.ai/gateway/configuration-reference
- Config examples: https://docs.openclaw.ai/gateway/configuration-examples
- Secrets: https://docs.openclaw.ai/gateway/secrets
- Environment: https://docs.openclaw.ai/help/environment
