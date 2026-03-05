---
name: create-repo
description: "Cria um novo repositorio na organizacao Vector Labs via pipeline de criacao de projetos. Coleta informacoes, dispara o workflow e acompanha ate a conclusao."
license: Apache-2.0
compatibility: claude-code, cursor, copilot, gemini
disable-model-invocation: true
allowed-tools: Bash AskUserQuestion
metadata:
  author: vector-labs-foundation
  version: "1.0"
tags: [claude-code, repository, github, devops, pipeline]
featured: false
complexity: beginner
platforms: [windows, macos, linux]
---

# Criar Repositorio na Vector Labs

Cria um novo repositorio na organizacao Vector Labs usando o workflow de criacao de projetos no GitHub Actions.

---

## FASE 0: PRE-REQUISITOS

### 0.1 Verificar gh CLI

```bash
command -v gh >/dev/null 2>&1 && echo "OK" || echo "MISSING"
```

**Se MISSING:**
- Informe: "O comando `gh` (GitHub CLI) e necessario. Instale em: https://cli.github.com/"
- **PARE a execucao.**

### 0.2 Verificar autenticacao

```bash
gh auth status 2>&1 | head -3
```

**Se nao autenticado:**
- Informe: "Voce precisa estar autenticado no GitHub CLI. Execute: `gh auth login`"
- **PARE a execucao.**

---

## FASE 1: COLETAR INFORMACOES

Use a ferramenta AskUserQuestion para coletar as informacoes necessarias:

### Pergunta 1: Dominio/Namespace

- **Pergunta:** "Qual o dominio/namespace do projeto?"
- **Opcoes:**
  - `payments` - Projetos do time de pagamentos
  - `dock` - Projetos do time dock
  - `foundation` - Projetos de infraestrutura/fundacao

### Pergunta 2: Template do projeto

- **Pergunta:** "Qual o tipo de projeto?"
- **Opcoes:**
  - `Raw` - Repositorio vazio (sem template)
  - `Go - API` - API em Go
  - `Go - gRPC` - Servico gRPC em Go
  - `Python` - Projeto Python

### Pergunta 3: Nome do repositorio

- **Pergunta:** "Qual o nome do repositorio? (sem o dominio, ex: exchange-rate)"
- Texto livre

### Pergunta 4: Descricao

- **Pergunta:** "Qual a descricao curta do projeto?"
- Texto livre

---

## FASE 2: DEFINIR CODEOWNER

Baseado no dominio escolhido, defina o time de codeowners:

- `payments` → `gh-payments-credit-transactions`
- `dock` → `gh-dock`
- `foundation` → `gh-foundation-eng`

---

## FASE 3: VERIFICAR EXISTENCIA

```bash
gh repo view vlabsai/{DOMAIN}.{REPO_NAME} --json name 2>/dev/null && echo "EXISTS" || echo "NOT_FOUND"
```

**Se EXISTS:**
- Informe: "O repositorio vlabsai/{DOMAIN}.{REPO_NAME} ja existe: https://github.com/vlabsai/{DOMAIN}.{REPO_NAME}"
- **PARE a execucao.**

---

## FASE 4: EXECUTAR WORKFLOW

```bash
gh workflow run orchestrator-create-project.yml \
  --repo vlabsai/foundation.create-repositories \
  -f domain={DOMAIN} \
  -f repo_name={REPO_NAME} \
  -f description="{DESCRIPTION}" \
  -f template_choice="{TEMPLATE}" \
  -f codeowner_team={CODEOWNER_TEAM}
```

**Se ocorrer erro de permissao:**
- Informe o usuario que ele nao tem permissao para executar o workflow
- Oriente a solicitar acesso no canal `#ask-foundation-eng`
- **PARE a execucao.**

---

## FASE 5: ACOMPANHAR

Aguarde o inicio da execucao e busque o ID:

```bash
sleep 5
gh run list --repo vlabsai/foundation.create-repositories --workflow orchestrator-create-project.yml --limit 1 --json databaseId,status,conclusion,displayTitle --jq '.[0]'
```

Acompanhe ate a conclusao:

```bash
gh run watch {RUN_ID} --repo vlabsai/foundation.create-repositories
```

---

## FASE 6: RESULTADO

**Se a execucao foi bem-sucedida**, exiba:

```
Repositorio criado com sucesso!

Nome: {DOMAIN}.{REPO_NAME}
URL: https://github.com/vlabsai/{DOMAIN}.{REPO_NAME}
Template: {TEMPLATE}
Codeowner: {CODEOWNER_TEAM}

Proximos passos:
1. Clone o repositorio: gh repo clone vlabsai/{DOMAIN}.{REPO_NAME}
2. Configure o ambiente de desenvolvimento
3. Se for um projeto payments/dock, execute /deploy-argocd para configurar o deploy
```

**Se a execucao falhou:**
- Informe o erro
- Forneca o link para os logs: `https://github.com/vlabsai/foundation.create-repositories/actions/runs/{RUN_ID}`

**PARE a execucao apos exibir o resultado.**

---

## NOTAS PARA O AGENTE

1. **Tempo estimado:** O workflow leva cerca de 1-2 minutos para completar
2. **Branch protection:** O repositorio sera criado com branch protection ativo
3. **Permissoes:** O time de codeowners tera permissao de admin no repositorio
4. **Se o usuario cancelar** em qualquer fase, pare e nao execute nada
5. **Substitua os placeholders** ({DOMAIN}, {REPO_NAME}, {DESCRIPTION}, {TEMPLATE}, {CODEOWNER_TEAM}, {RUN_ID}) pelos valores coletados
