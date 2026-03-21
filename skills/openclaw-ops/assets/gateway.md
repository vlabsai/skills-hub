# Gateway

Processo central Node.js — WebSocket server, control plane único. Tudo depende dele.

## Lifecycle

```bash
# Serviço (systemd/launchd)
openclaw gateway install       # Registrar como serviço
openclaw gateway start|stop|restart
openclaw gateway uninstall

# Foreground (debug)
openclaw gateway run

# Background sem serviço
nohup openclaw gateway --force --port 18789 &>/tmp/gw-out.log & disown
```

Demora ~15-20s para responder ao health check após iniciar.

## Health & Status

```bash
openclaw gateway status        # Estado do serviço + health probe
openclaw gateway health        # Health check direto
openclaw health                # Resumo rápido
openclaw gateway usage-cost    # Tokens consumidos
openclaw logs                  # Tail logs em tempo real via RPC
```

Logs em disco: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`

## Configuração

```json5
{
  "gateway": {
    "port": 18789,                          // Porta padrão
    "bind": "loopback",                     // loopback | lan | tailnet | auto | custom
    "mode": "local",
    "auth": {
      "mode": "token",                      // token | password | trusted-proxy | none
      "token": "${OPENCLAW_GATEWAY_TOKEN}"
    },
    "reload": {
      "mode": "hybrid",                     // hybrid | hot | restart | off
      "debounceMs": 300
    },
    "channelHealthCheckMinutes": 5,
    "channelMaxRestartsPerHour": 10
  }
}
```

`hybrid` = hot-apply mudanças seguras, auto-restart para críticas (porta, bind, auth).

## Protocolo WebSocket

### Handshake
1. Gateway envia `connect.challenge` (nonce + timestamp)
2. Cliente envia `connect` (protocol versions, role, scope, device identity + assinatura Ed25519)
3. Gateway responde `hello-ok` (protocol version, policies, tick interval 15s)

### Frame types
- **Request:** `{type:"req", id, method, params}` — client → server
- **Response:** `{type:"res", id, ok, payload|error}` — server → client
- **Event:** `{type:"event", event, payload, seq?}` — push async

Métodos side-effecting requerem idempotency keys.

### Roles
- **Operator** (CLI, Web UI, apps): scopes `operator.read/write/admin/approvals/pairing`
- **Node** (iOS/Android, headless): declara capabilities (camera, screen, canvas, exec)

## Bind modes

| Mode | Acesso | Uso |
|------|--------|-----|
| `loopback` | 127.0.0.1 only | Default, seguro |
| `lan` | Rede local | Com firewall |
| `tailnet` | Via Tailscale | Recomendado para remoto |
| `auto` | Auto-detect | Conveniência |
| `custom` | Manual | Avançado |

## Auth modes

| Mode | Descrição |
|------|-----------|
| `token` | Bearer token (recomendado). Gerar: `openclaw doctor --generate-gateway-token` |
| `password` | HTTP Basic via `OPENCLAW_GATEWAY_PASSWORD` |
| `trusted-proxy` | Delega auth para reverse proxy |
| `none` | Sem auth (apenas dev local) |

## Discovery

```bash
openclaw gateway discover      # Bonjour (LAN) + Tailscale wide-area
```

## Acesso remoto

- **SSH tunnel (recomendado):** `ssh -f -N -L 28789:127.0.0.1:18789 user@host`
- **Tailscale Serve:** HTTPS dentro do tailnet, gateway fica loopback
- **Tailscale Funnel:** HTTPS público (requer password auth)

## RPC direto

```bash
openclaw gateway call <method> [params...]
```

## Docs oficiais
- Config: https://docs.openclaw.ai/gateway/configuration
- Config reference: https://docs.openclaw.ai/gateway/configuration-reference
- Protocol: https://docs.openclaw.ai/gateway/protocol
- Security: https://docs.openclaw.ai/gateway/security/index.md
- Remote: https://docs.openclaw.ai/gateway/remote
- Troubleshooting: https://docs.openclaw.ai/gateway/troubleshooting
- Health: https://docs.openclaw.ai/gateway/health
