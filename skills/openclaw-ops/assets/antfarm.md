# Antfarm (Multi-Agent Workflows)

CLI TypeScript que orquestra times de agentes AI no OpenClaw. YAML + SQLite + cron, zero infraestrutura extra. Roda nativamente em cima do OpenClaw.

- **Repo:** github.com/snarktank/antfarm (MIT, por Ryan Carson)
- **Docs:** antfarm.cool

## Arquitetura (Ralph Loop)

- Cada agente roda numa sessão OpenClaw 100% fresh (sem memória herdada)
- Contexto persiste via: git commits, progress.txt, e KEY:VALUE no SQLite
- Two-phase polling: fase 1 (modelo barato, peek) → fase 2 (claim + spawn sessão)
- Cron a cada 5 min, staggered por agente
- DB: ~/.openclaw/antfarm/antfarm.db (SQLite WAL mode)

## Comandos CLI

```bash
antfarm workflow list                          # Listar workflows
antfarm workflow run <id> "<task>"             # Iniciar run
antfarm workflow status "<query>"              # Status por busca
antfarm workflow runs                          # Listar todos os runs
antfarm workflow resume <run-id>               # Retomar run falhado
antfarm workflow install <id>                  # Instalar workflow
antfarm workflow uninstall <id> [--force]      # Remover workflow
antfarm dashboard                              # Iniciar dashboard (porta 3333)
antfarm dashboard stop / status
antfarm install / uninstall [--force]          # Todos os workflows
antfarm update                                 # Atualizar versão
```

## Workflows Bundled

- **feature-dev** (7 agentes): plan → setup → implement (loop) → verify → test → PR → review
- **bug-fix** (6 agentes): triage → investigate → setup → fix → verify → PR
- **security-audit** (7 agentes): scan → prioritize → setup → fix (loop) → verify → test → PR

## 6 Roles de Agentes

| Role | Pode | Não pode |
|------|------|----------|
| analysis | Ler, explorar | Escrever, editar |
| coding | Ler, escrever, executar | UI, system tools |
| verification | Ler, executar | Escrever (integridade) |
| testing | Ler, executar, browser | Escrever |
| pr | Ler, executar (gh) | Escrever |
| scanning | Ler, executar, web search | Escrever |

Todos SEMPRE negam: gateway, cron, message, nodes, canvas, sessions_send.

## Criar Workflow Customizado

Estrutura:
```
workflows/meu-workflow/
├── workflow.yml
└── agents/
    └── meu-agente/
        ├── AGENTS.md      # Instruções operacionais + output format
        ├── SOUL.md        # Personalidade (10-20 linhas)
        └── IDENTITY.md    # Nome e role (2-5 linhas)
```

workflow.yml:
```yaml
id: meu-workflow
name: Meu Workflow
version: 1
description: O que faz

polling:
  model: default
  timeoutSeconds: 600       # 120s é insuficiente para steps que criam arquivos

agents:
  - id: agente-id
    name: Nome
    role: analysis|coding|verification|testing|pr|scanning
    workspace:
      baseDir: agents/agente-id
      files:
        AGENTS.md: agents/agente-id/AGENTS.md
        SOUL.md: agents/agente-id/SOUL.md
        IDENTITY.md: agents/agente-id/IDENTITY.md

steps:
  - id: step-name
    agent: agente-id
    input: |
      Prompt com {{task}} e {{variavel_do_step_anterior}}

      Reply with:
      STATUS: done
      MINHA_KEY: valor
    expects: "STATUS: done"
    max_retries: 2
    on_fail:
      escalate_to: human
```

## Padrões Críticos para Output Format

1. **O output format DEVE estar no `input:` do step no workflow.yml** com `Reply with:` seguido das keys exatas. O AGENTS.md sozinho NÃO garante compliance — o modelo pode ignorar.
2. Keys em UPPERCASE no output do agente → viram lowercase como `{{key}}` no step seguinte
3. Seguir o padrão dos workflows default (feature-dev, bug-fix)
4. Escrever instruções em inglês (melhor compliance do modelo)
5. `expects: "STATUS: done"` em todos os steps

## Features Avançadas

- **Loop steps:** `type: loop`, `loop.over: stories`
- **Verify each:** `loop.verify_each: true`
- **Template vars:** `{{task}}` sempre disponível; KEY:VALUE de steps anteriores viram `{{key_lowercase}}`
- **Retry com feedback:** `on_fail.retry_step` roda step anterior com `{{verify_feedback}}`
- **Agentes compartilhados:** `agents/shared/` (setup, verifier, pr) — reusáveis entre workflows

## Dashboard

- Web UI vanilla JS em localhost:3333
- Kanban board, detail panel, timeline, medic indicator
- Auto-refresh: 30s (board), 5s (panel aberto)
- Acesso remoto via SSH tunnel: `ssh -f -N -L 3333:127.0.0.1:3333 user@host`

## Bugs Conhecidos (v0.5.1) e Patches Necessários

### 1. Token do gateway não passado ao CLI subprocess
**Arquivo:** `src/installer/gateway-api.ts`, função `runCli`
**Problema:** O Antfarm chama o CLI do OpenClaw via `execFile` sem passar `OPENCLAW_GATEWAY_TOKEN` no env. O CLI não consegue autenticar no gateway.
**Fix:** Adicionar leitura do token do config e injeção no env:
```typescript
const config = await readOpenClawConfig();
const env = { ...process.env };
if (config.token) env.OPENCLAW_GATEWAY_TOKEN = config.token;
execFile(bin, finalArgs, { timeout: 30_000, env }, ...);
```

### 2. Flag --timeout vs --timeout-seconds
**Arquivo:** `src/installer/gateway-api.ts`
**Problema:** Antfarm passa `--timeout` que o OpenClaw interpreta como milissegundos (120ms timeout). Issue snarktank/antfarm#307.
**Fix:** Trocar `--timeout` por `--timeout-seconds`.

### 3. Output format hardcoded no cron prompt
**Arquivo:** `src/installer/agent-cron.ts`, funções `buildWorkPrompt` e prompt de polling
**Problema:** O template de conclusão hardcoda `CHANGES: what you did / TESTS: what tests you ran`. Agentes usam essas keys ao invés das definidas no workflow.
**Fix:** Trocar pelo template genérico:
```
STATUS: done
<include all KEY: value pairs exactly as specified in the Reply with: section of the input instructions above>
```

**Após aplicar patches:** `npm run build` no diretório do Antfarm.
**Após `antfarm update`:** Re-aplicar os 3 patches e rebuildar.

## Operação Correta

1. **Sempre iniciar o gateway de um diretório estável** (ex: `/root`) — se iniciar do workspace de um agente e depois fizer uninstall, o gateway perde o cwd (erro `uv_cwd: ENOENT`)
2. **`antfarm workflow run` pode precisar de retry** (2-3 tentativas) por causa do bug de WebSocket flaky do OpenClaw (#45222)
3. **Bug de crons parciais:** O Antfarm às vezes falha em registrar todos os crons (ex: cria 2 de 3). Verificar com `openclaw cron list` e criar manualmente se faltar
4. **Criar cron manual:** `openclaw cron add --name 'antfarm/<workflow>/<agent>' --agent <workflow>_<agent> --every 5m --session isolated --timeout-seconds 600 --message '<prompt>'`
5. **Após uninstall+reinstall:** Reiniciar o gateway para evitar cwd invalidado
6. **Não reiniciar o gateway repetidamente** — cada restart invalida crons existentes
7. **Limpar runs:** Usar Node.js com `node:sqlite` (DatabaseSync)
8. **CRÍTICO: Crons ficam ativos após workflow completar.** O Antfarm deveria limpar crons automaticamente via `teardownWorkflowCronsIfIdle`, mas isso pode falhar (ex: se o step foi completado manualmente via SQLite). Crons órfãos consomem API rate limit (cada peek = 1 chamada de API, ~36/hora com 3 agentes a cada 5 min). **Após workflow completar, sempre verificar e deletar crons órfãos:**
   ```bash
   openclaw cron list                    # Verificar crons ativos
   openclaw cron delete --id <job-id>    # Deletar cada um
   # Ou desinstalar o workflow:
   antfarm workflow uninstall <id>       # Remove agents + crons
   ```
9. **Dashboard é somente leitura** — não permite ativar/desativar crons pela UI. Gerenciamento de crons é apenas via CLI.

## Diretórios Padrão

```
~/.openclaw/workspace/antfarm/           # Fonte do Antfarm
~/.openclaw/antfarm/antfarm.db           # SQLite database
~/.openclaw/workspace/antfarm/workflows/ # Workflows (bundled + custom)
~/.openclaw/workspaces/workflows/        # Agent workspaces provisionados
~/.openclaw/antfarm/dashboard.pid        # Dashboard PID
```

## Docs
- Repo: https://github.com/snarktank/antfarm
- Site: https://www.antfarm.cool/
