# Segurança

## Modelo de confiança

OpenClaw = personal assistant. **1 operador trusted por gateway.** NÃO é multi-tenant hostil. Para usuários adversários, rodar gateways separados.

## Auditoria

```bash
openclaw security audit            # Básica
openclaw security audit --deep     # Profunda
openclaw security audit --fix      # Auto-corrigir
openclaw security audit --json     # Saída JSON
```

### Prioridade de findings
1. `open` + tools habilitados → travar DMs/grupos primeiro
2. Exposição pública (LAN bind, Funnel, sem auth) → corrigir imediatamente
3. Browser control remoto → tratar como acesso de operador
4. Permissões de arquivos (state/config/credentials não group/world-readable)
5. Plugins → só código trusted
6. Modelo → preferir modernos, instruction-hardened

## Autenticação

| Mode | Recomendação |
|------|-------------|
| `token` | Recomendado. `openclaw doctor --generate-gateway-token` |
| `password` | OK. Via `OPENCLAW_GATEWAY_PASSWORD` |
| `trusted-proxy` | Para reverse proxy com identity |
| `none` | Apenas dev local |

### Device pairing
- Ed25519 challenge-response
- Local (loopback/tailnet own) = auto-approved
- Remoto = requer approval explícita
- Devices aprovados recebem tokens persistentes
- Rotação: `device.token.rotate`, revogação: `device.token.revoke`

## DM & Channel access

- **Pairing** (default): código 1h, max 3 pendentes
- **Allowlist**: bloqueia desconhecidos
- **Open**: requer `"*"` explícito
- Responder a mensagens do bot NÃO bypassa allowlists

## Sandbox

```json5
{
  "sandbox": {
    "mode": "non-main",   // off | all | non-main
    "scope": "agent"       // agent | session | shared
  }
}
```

Workspace access: `"none"` | `"ro"` (/agent) | `"rw"` (/workspace)

## Permissões de arquivos

- `~/.openclaw/openclaw.json` → modo 600
- `~/.openclaw/` → modo 700
- `openclaw doctor` avisa e corrige

## Prompt injection

**Não resolvido.** System prompt = soft guidance. Hard enforcement via:
- Tool policy + deny lists
- Exec approvals
- Sandbox (Docker)
- Channel allowlists
- **Modelos maiores/recentes = mais robustos**

Fontes de conteúdo não-confiável: search results, browser pages, emails, attachments. Blast radius típico: exfiltração ou tool calls não intencionais.

## Browser security

- Usar perfil dedicado (não daily-driver)
- SSRF default: `dangerouslyAllowPrivateNetwork: true`
- Modo estrito: `false` + `hostnameAllowlist`
- Remote browser = acesso de operador

## Plugins

- Rodam in-process com Gateway = tratar como código trusted
- npm lifecycle scripts executam código na instalação
- Preferir `plugins.allow` allowlist
- Auditar `tools.profile` quando plugins instalados

## Flags perigosas (auditadas por `security audit`)

- `gateway.controlUi.allowInsecureAuth`
- `gateway.controlUi.dangerouslyDisableDeviceAuth`
- `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback`
- `hooks.*.allowUnsafeExternalContent`
- `tools.exec.applyPatch.workspaceOnly: false`
- `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork`
- `sandbox.docker.dangerouslyAllow*`

Manter unset/false em produção.

## Baseline seguro (config recomendada)

```json5
{
  "gateway": {
    "mode": "local", "bind": "loopback",
    "auth": { "mode": "token", "token": "long-random-token" }
  },
  "session": { "dmScope": "per-channel-peer" },
  "tools": {
    "profile": "messaging",
    "deny": ["group:automation", "group:runtime", "group:fs", "sessions_spawn", "sessions_send"],
    "fs": { "workspaceOnly": true },
    "exec": { "security": "deny", "ask": "always" },
    "elevated": { "enabled": false }
  },
  "channels": {
    "whatsapp": { "dmPolicy": "pairing", "groups": { "*": { "requireMention": true } } }
  }
}
```

## Incident response

1. **Conter:** stop gateway ou `bind: "loopback"`, desabilitar DMs/grupos
2. **Rotacionar:** gateway token, remote token, provider keys, channel tokens
3. **Auditar:** `/tmp/openclaw/openclaw-YYYY-MM-DD.log` + `sessions/*.jsonl`
4. **Verificar:** `openclaw security audit --deep`

## Logging & Transcripts

- Transcripts em disco: `~/.openclaw/agents/<id>/sessions/*.jsonl`
- Acesso ao disco = trust boundary
- Redaction: `logging.redactSensitive: "tools"` (default on)
- Usar `openclaw status --all` (redacted) para diagnóstico

## Docs oficiais
- Security: https://docs.openclaw.ai/gateway/security/index.md
- Threat model: https://docs.openclaw.ai/security/THREAT-MODEL-ATLAS
- Sandboxing: https://docs.openclaw.ai/gateway/sandboxing
