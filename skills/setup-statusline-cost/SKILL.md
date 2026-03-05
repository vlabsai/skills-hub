---
name: setup-statusline-cost
description: Configura statusline no Claude Code que exibe custo da sessao, modelo, duracao, tokens e uso de contexto em tempo real. Use quando o usuario quiser monitorar custo ou configurar a statusline.
license: Apache-2.0
compatibility: claude-code
disable-model-invocation: true
allowed-tools: Bash Read Edit Write AskUserQuestion
metadata:
  author: vector-labs-payments
  version: "1.0"
---

# Setup Statusline de Custo

Configura uma statusline no rodape do Claude Code que exibe metricas de custo e uso em tempo real.

Formato exibido:

```
Opus 4.6 | $0.42 | 3m 12s | in 45.2k / out 8.7k | 32% ctx
```

---

## FASE 0: PRE-REQUISITOS

### 0.1 Verificar jq

```bash
command -v jq >/dev/null 2>&1 && echo "OK" || echo "MISSING"
```

**Se MISSING:**
- Informe: "O comando `jq` e necessario. Instale com: `brew install jq` (macOS) ou `apt install jq` (Linux)."
- **PARE a execucao.**

### 0.2 Verificar se ja existe statusline configurada

```bash
jq -r '.statusLine // empty' "$HOME/.claude/settings.json" 2>/dev/null
```

**Se ja existe**, pergunte ao usuario:
- **Pergunta:** "Ja existe uma statusline configurada. Deseja substituir?"
- **Opcoes:**
  - `Sim` - Substituir pela statusline de custo
  - `Nao` - Cancelar
- **Se `Nao`:** **PARE a execucao.**

---

## FASE 1: INSTALAR SCRIPT

### 1.1 Copiar script para ~/.claude/

Leia o conteudo do arquivo `scripts/statusline.sh` que esta nesta skill e escreva em `$HOME/.claude/statusline.sh`.

### 1.2 Tornar executavel

```bash
chmod +x "$HOME/.claude/statusline.sh"
```

---

## FASE 2: CONFIGURAR SETTINGS

### 2.1 Criar settings.json se nao existir

```bash
mkdir -p "$HOME/.claude"
[ -f "$HOME/.claude/settings.json" ] || echo '{}' > "$HOME/.claude/settings.json"
```

### 2.2 Adicionar statusLine (merge nao-destrutivo)

Use jq para fazer merge preservando TODAS as chaves existentes:

```bash
TEMP_FILE=$(mktemp)
jq '.statusLine = {"type": "command", "command": "~/.claude/statusline.sh"}' "$HOME/.claude/settings.json" > "$TEMP_FILE" && mv "$TEMP_FILE" "$HOME/.claude/settings.json"
```

---

## FASE 3: CONFIRMAR

Exiba esta mensagem EXATA:

```
Statusline de custo configurada!

Arquivo instalado:
  ~/.claude/statusline.sh

Configuracao adicionada em:
  ~/.claude/settings.json → statusLine

Reinicie o Claude Code para ativar.
Saia com /exit ou Ctrl+C e inicie novamente com `claude`.

Formato exibido:
  Opus 4.6 | $0.42 | 3m 12s | in 45.2k / out 8.7k | 32% ctx

Cores do contexto:
  Verde  → < 50%
  Amarelo → 50-74%
  Vermelho → >= 75%

Para personalizar, edite ~/.claude/statusline.sh
```

**PARE a execucao apos exibir esta mensagem.**

---

## NOTAS PARA O AGENTE

1. **Nao sobrescreva** configuracoes existentes no settings.json - use jq merge
2. **Se o usuario cancelar** em qualquer fase, pare e nao altere nada
3. **Use SEMPRE `$HOME`** ao inves de `~` em variaveis bash para evitar problemas de expansao
4. **SEMPRE informe sobre o restart** ao final
