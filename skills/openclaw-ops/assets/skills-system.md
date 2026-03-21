# Skills System

Skills = runbooks em SKILL.md que ensinam o agente a orquestrar tools. Não são plugins executáveis.

## CLI

```bash
openclaw skills list              # Todas
openclaw skills list --verbose    # Com detalhes
openclaw skills list --eligible   # Apenas prontas
openclaw skills info <name>       # Detalhes
openclaw skills check             # Verificar requisitos
openclaw skills install <slug>    # Instalar do ClawHub
```

## Precedência de carregamento (alta → baixa)

1. **Workspace:** `<workspace>/skills/<skill>/SKILL.md`
2. **Managed:** `~/.openclaw/skills/<skill>/SKILL.md`
3. **Bundled:** incluídas no pacote OpenClaw
4. **Extra dirs:** via `skills.load.extraDirs` em openclaw.json

Skills do workspace sobrescrevem managed que sobrescrevem bundled.

## Formato SKILL.md

```yaml
---
name: skill-name
description: O que a skill faz
homepage: https://example.com                    # Opcional, surfaced em UI
user-invocable: true                             # true = expõe como /slash command
disable-model-invocation: false                  # true = exclui do prompt
command-dispatch: tool                           # Bypassa modelo, dispatch direto
command-tool: tool-name                          # Tool alvo do dispatch
command-arg-mode: raw                            # Modo de argumentos
metadata: {"openclaw":{...}}                     # JSON single-line obrigatório
---

# Nome da Skill

## O que faz
## Inputs necessários
## Workflow (passos numerados)
## Formato de saída
## Guardrails
## Tratamento de falhas
## Exemplos
```

**Constraints:** metadata DEVE ser JSON em uma única linha. Multi-line YAML não suportado.

## Metadata (gating)

```json
{
  "openclaw": {
    "always": true,                    // Bypassa todos os gates, sempre injetada
    "emoji": "🔧",
    "os": ["darwin", "linux"],         // Restrição de plataforma
    "requires": {
      "bins": ["curl", "jq"],          // TODOS devem existir no PATH
      "anyBins": ["ffmpeg", "avconv"], // Pelo menos UM
      "env": ["API_KEY"],             // Env var deve existir ou estar em config
      "config": ["browser.enabled"]    // Paths em openclaw.json devem ser truthy
    },
    "primaryEnv": "API_KEY",           // Mapeado por skills.entries.*.apiKey
    "skillKey": "custom-key",          // Key customizada em config
    "install": [{                      // Spec de instalação automática
      "id": "brew", "kind": "brew",   // Kinds: brew, node, go, uv, download
      "formula": "tool", "bins": ["tool"],
      "os": ["darwin"]
    }]
  }
}
```

## Config de skills (openclaw.json)

```json5
{
  "skills": {
    "entries": {
      "skill-name": {
        "enabled": true,               // false desabilita mesmo se bundled
        "apiKey": { "source": "env", "provider": "default", "id": "VAR" },
        "env": { "MY_VAR": "value" },  // Injeta se var não existe
        "config": { "custom": "val" }
      }
    },
    "allowBundled": ["skill1"],        // Allowlist para bundled only
    "load": {
      "watch": true,                   // Hot-reload quando SKILL.md muda
      "watchDebounceMs": 250,
      "extraDirs": ["/path/to/more"]
    }
  }
}
```

## Injection seletiva

O runtime NÃO injeta todas as skills em todo turno. Injeta apenas as relevantes para o turno atual (exceto `always: true`). Snapshot acontece no início da sessão.

## Token impact

```
total = 195 + Σ(97 + nome + descrição + location)
~24 tokens por skill (overhead fixo)
```

## ClawHub (registry público)

```bash
clawhub install <slug>         # Instala em ./skills/ (workspace)
clawhub update --all
clawhub list
clawhub uninstall <slug>
clawhub login                  # Para publicar
clawhub publish                # Publicar skill
```

13,729+ skills, ~5,400 curadas. Categorias: Coding (1222), Web (938), DevOps (409), Search (352), Browser (335).

## Segurança

- Tratar skills de terceiros como código não-confiável. Ler antes de habilitar.
- `env` e `apiKey` injetam secrets no processo host, não no sandbox.
- Skills não concedem permissões de tools — permissões devem ser habilitadas separadamente.

## Docs oficiais
- Skills: https://docs.openclaw.ai/tools/skills
- Skills config: https://docs.openclaw.ai/tools/skills-config
- Criando skills: https://docs.openclaw.ai/tools/creating-skills
- ClawHub: https://docs.openclaw.ai/tools/clawhub
