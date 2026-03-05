# Contribuindo com Skills

## Anatomia de uma Skill

Uma skill é um diretório em `skills/` com pelo menos um `SKILL.md`:

```
skills/minha-skill/
├── SKILL.md           # Obrigatório — frontmatter + instruções
├── scripts/           # Opcional — scripts executáveis
├── references/        # Opcional — documentação adicional
└── assets/            # Opcional — templates, schemas, imagens
```

Spec completa: [agentskills.io/specification](https://agentskills.io/specification)

## Frontmatter

O `SKILL.md` começa com um bloco YAML entre `---`. Campos definidos pela [spec agentskills.io](https://agentskills.io/specification):

```yaml
---
name: minha-skill
description: O que a skill faz e quando usar. Inclua keywords para ativação pelo agente.
license: Apache-2.0
compatibility: Requires jq and access to the internet
allowed-tools: Bash Read Edit Write
metadata:
  author: seu-time
  version: "1.0"
---
```

| Campo | Obrigatório | Regras |
|-------|:-----------:|--------|
| `name` | Sim | Deve ser igual ao nome do diretório. Lowercase, números e hífens. Max 64 chars. Sem `--` consecutivos, sem começar/terminar com `-`. |
| `description` | Sim | Max 1024 chars. Descreva o que faz **e quando usar**. |
| `license` | Não | Nome da licença ou referência a arquivo. Default no aggregator: `Apache-2.0`. |
| `compatibility` | Não | Max 500 chars. Requisitos de ambiente: ferramenta, pacotes, rede. Ex: `"Designed for Claude Code"`, `"Requires git, docker, jq"`. |
| `allowed-tools` | Não | Lista separada por espaço. Experimental — suporte varia entre agentes. |
| `metadata` | Não | Mapa chave-valor livre. Recomendado: `author`, `version`. |

Campos extras não definidos na spec mas usados pelo aggregator do catálogo (opcionais):

| Campo | Uso |
|-------|-----|
| `tags` | Array de strings para busca no catálogo |
| `featured` | `true` para destaque na home |
| `complexity` | `beginner`, `intermediate`, `advanced` |
| `platforms` | Array: `windows`, `macos`, `linux` (default: todos) |

Qualquer outro campo no frontmatter (ex: `disable-model-invocation`) é preservado e passado para a ferramenta de IA na instalação.

## Corpo do SKILL.md

Instruções em Markdown que o assistente de IA vai seguir. Mantenha abaixo de 500 linhas — mova referências detalhadas para `references/`. Boas práticas:

- **Seja imperativo** — "Faça X", não "Você pode fazer X"
- **Divida em fases** — facilita o acompanhamento do usuário
- **Inclua verificações** — cheque pré-requisitos antes de alterar o sistema
- **Peça confirmação** antes de ações destrutivas
- **Termine com uma mensagem de conclusão** clara

## Categorias

Inferidas automaticamente pelo aggregator a partir do nome e descrição. Categorias no site:

`code-quality` · `testing` · `documentation` · `development` · `observability` · `troubleshooting`

## Validação

O PR é validado automaticamente pela action [Validate Skills](.github/workflows/validate-skills.yml), que roda em todo PR que toca `skills/**`. Ela checa:

- `SKILL.md` existe
- Frontmatter YAML válido
- `name` e `description` presentes e não-vazios (bloqueia PR)
- `name` = nome do diretório, formato kebab-case, max 64 chars, sem `--`
- `description` max 1024 chars
- `license` e `compatibility` recomendados (warn, não bloqueia)
- `license` é SPDX conhecido (warn)

## Processo

1. Crie um branch a partir de `main`
2. Adicione seu diretório em `skills/`
3. Preencha `metadata.author` com o nome do seu time — toda skill deve ter autoria identificada
4. Valide localmente:
   ```bash
   npm run aggregate    # deve listar sua skill sem erros
   npm run dev          # confira no catálogo (localhost:4321)
   ```
5. Abra um Pull Request — a action de validação roda automaticamente
6. Aguarde aprovação — toda skill precisa de review e aprovação antes de ser mergeada

## Contribuindo com o Site ou CLI

- **Site** (`site/`) — Astro, porta 4321. `npm run dev` para rodar local.
- **CLI** (`cli/`) — `node cli/bin/vector-labs-skills.js list --source .` para testar.
- **Aggregator** (`scripts/aggregate-skills.js`) — lê `skills/`, gera `site/src/data/skills.json`.

## License

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a [MIT License](LICENSE).
