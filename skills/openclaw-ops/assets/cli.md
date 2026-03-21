# CLI Reference

60+ comandos. `openclaw <command> --help` para detalhes de qualquer um.

## Core

```bash
openclaw gateway run|start|stop|restart|status|health|discover|install|uninstall|call|usage-cost
openclaw agent                     # Turno único de execução
openclaw agents add|delete|list|set-identity
openclaw acp client [--session <key>]   # Agent Control Protocol bridge
openclaw sessions [--agent|--all-agents|--active N] | cleanup
openclaw config get|set|unset|validate
openclaw models set|list|aliases|fallbacks|set-image|scan|status
```

## Chat & Mensagens

```bash
openclaw channels list|login|logout|status [--probe]
openclaw pairing list|approve <channel> <code>
openclaw directory resolve --channel <ch> --name <peer>
openclaw message send --target <id> --message "texto"
openclaw message read [--channel <ch>]
```

## Skills & Extensões

```bash
openclaw skills list [--verbose|--eligible]
openclaw skills info <name>
openclaw skills check
openclaw skills install <slug>
openclaw plugins install|list|enable|disable|doctor
openclaw hooks list|enable|disable|install|check
```

## Browser

```bash
openclaw browser start|stop|status
openclaw browser open|navigate <url>
openclaw browser screenshot [--full-page]
openclaw browser snapshot [--format aria]
openclaw browser click|type|fill|scroll|hover|drag|wait
openclaw browser cookies|storage
openclaw browser pdf
```

## Automação

```bash
openclaw cron add|list|run|status|enable|disable|edit|runs
openclaw system                    # Events, heartbeat, presence
```

## Administração

```bash
openclaw doctor [--generate-gateway-token]
openclaw security audit [--deep|--fix|--json]
openclaw health
openclaw status [--all]
openclaw logs                      # Tail via RPC
openclaw memory search|reindex
openclaw devices
openclaw approvals allowlist|get|set
openclaw backup create|verify <path>
openclaw update check|download|apply|channel
openclaw sandbox list|recreate [--all|--agent|--session]
openclaw reset
openclaw --version
```

## Interfaces

```bash
openclaw dashboard                 # Control UI (browser)
openclaw tui                       # Terminal UI
openclaw onboard                   # Wizard interativo
openclaw configure                 # Config wizard
```

## Nodes (dispositivos remotos)

```bash
openclaw node run|start|stop|restart|status
openclaw nodes                     # Listar nodes conectados
openclaw dns                       # Tailscale + CoreDNS
```

## Docs oficiais
- CLI index: https://docs.openclaw.ai/cli/index.md
- Cada comando: https://docs.openclaw.ai/cli/<command>
