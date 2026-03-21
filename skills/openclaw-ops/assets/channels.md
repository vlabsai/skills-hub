# Channels

40+ canais suportados. Cada um tem adapter próprio, auth específica, e políticas configuráveis.

## CLI

```bash
openclaw channels list               # Canais configurados
openclaw channels status             # Status de cada canal
openclaw channels status --probe     # Com health check ativo
openclaw channels login --channel <name>   # Setup/pair de canal
openclaw channels logout <channel>         # Desconectar
```

## Canais principais

| Canal | Adapter | Auth |
|-------|---------|------|
| WhatsApp | Baileys (WhatsApp Web) | QR code / pairing code |
| Telegram | grammY | Bot token |
| Discord | discord.js | Bot token |
| Slack | Slack SDK | App token + bot token |
| Signal | signal-cli | Phone number |
| iMessage | imsg CLI (macOS only) | Native |
| Matrix | matrix-js-sdk | Homeserver + token |
| Google Chat | Google API | Service account |
| MS Teams | Bot Framework | App registration |

Lista completa: https://docs.openclaw.ai/channels/index.md

## Políticas de DM

| Policy | Comportamento |
|--------|---------------|
| `pairing` (default) | Desconhecidos recebem código (expira 1h, max 3 pendentes) |
| `allowlist` | Bloqueia desconhecidos, aceita apenas listados |
| `open` | Aceita todos (requer `"*"` explícito em allowFrom) |
| `disabled` | Ignora DMs |

```bash
openclaw pairing list <channel>            # Requests pendentes
openclaw pairing approve <channel> <code>  # Aprovar contato
```

## Políticas de grupo

- `requireMention: true` — só responde se mencionado
- `groupPolicy`: `"open"`, `"allowlist"`, `"disabled"`
- `groupAllowFrom`: lista de IDs ou `["*"]`

## Config de canal (openclaw.json)

```json5
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "dmPolicy": "pairing",
      "groupPolicy": "open",
      "allowFrom": ["+5511999999999"],
      "groups": {
        "*": { "requireMention": true },
        "group-id-123": { "requireMention": false }
      },
      "mediaMaxMb": 50,
      "debounceMs": 0
    },
    "telegram": {
      "enabled": true,
      "botToken": "${TELEGRAM_BOT_TOKEN}",
      "dmPolicy": "pairing",
      "allowFrom": ["tg:123456"],
      "groups": { "*": { "requireMention": true } }
    }
  }
}
```

## Mention patterns

```json5
{
  "agents": {
    "list": [{
      "id": "main",
      "groupChat": {
        "mentionPatterns": ["@bot", "bot", "hey bot"]
      }
    }]
  }
}
```

## Broadcast groups

Enviar mesma mensagem para múltiplos canais/grupos simultaneamente.
Doc: https://docs.openclaw.ai/channels/broadcast-groups

## Enviar mensagens via CLI

```bash
openclaw message send --target <id> --message "texto"
openclaw directory resolve --channel <ch> --name <peer>  # Lookup de ID
```

## Re-pair WhatsApp

WhatsApp pode desconectar. Re-pair:
```bash
openclaw channels login --channel whatsapp
```

## Troubleshooting

- Canal desconectado: `openclaw channels status --probe` → re-login
- WhatsApp single-device: apenas 1 gateway por conta
- Health monitor: `channelHealthCheckMinutes: 5` (default)
- Auto-restart: `channelMaxRestartsPerHour: 10` (default)

## Docs oficiais
- Overview: https://docs.openclaw.ai/channels/index.md
- WhatsApp: https://docs.openclaw.ai/channels/whatsapp
- Telegram: https://docs.openclaw.ai/channels/telegram
- Discord: https://docs.openclaw.ai/channels/discord
- Slack: https://docs.openclaw.ai/channels/slack
- Pairing: https://docs.openclaw.ai/channels/pairing
- Groups: https://docs.openclaw.ai/channels/groups
- Routing: https://docs.openclaw.ai/channels/channel-routing
- Troubleshooting: https://docs.openclaw.ai/channels/troubleshooting
