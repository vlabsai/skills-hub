# OAuth (OpenAI Codex)

## Token Lifecycle

- Access token expira a cada ~10 dias
- Refresh automático: quando access expira, OpenClaw usa o refresh_token para renovar (sob file lock)
- Tokens armazenados em `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- Formato: `{ access, refresh, expires, accountId }`

## Verificar Status

```bash
openclaw models status
```

Mostra: provider, auth store, profiles, e resultado do token refresh.

## Quando Auto-Refresh Falha

O erro mais comum é `refresh_token_reused`:
```
"Your refresh token has already been used to generate a new access token. Please try signing in again."
```

Isso acontece quando o refresh token foi usado (por outro processo ou tentativa anterior) e o novo par de tokens não foi salvo.

## Re-autenticação Manual

O `models auth login` precisa de TTY interativo e um tunnel para a porta do callback OAuth.

### Passo a passo

```bash
# 1. Criar tunnel para a porta do callback (geralmente 1455)
ssh -f -N -L 1455:127.0.0.1:1455 user@host

# 2. Rodar login interativo (precisa de terminal real, não funciona via scripts)
ssh -t user@host "openclaw models auth login --provider openai-codex"
```

O CLI mostra um link OAuth. Fluxo:
1. Abrir o link no browser local
2. Autorizar na OpenAI
3. O browser redireciona para `localhost:1455/auth/callback?code=...`
4. Se o tunnel estiver ativo, o CLI recebe o callback automaticamente
5. Se pedir "Paste the redirect URL", copiar a URL completa da barra do browser e colar no terminal

### Após sucesso
- Reiniciar o gateway para que pegue o novo token
- Verificar com `openclaw models status`

### Importante
- **Não usar `openclaw onboard`** para renovar auth — ele reconfigura tudo do zero
- O `models auth login` **não pode** ser rodado via scripts/automação (precisa de TTY)
- A porta do callback pode variar (1455 é comum, verificar na URL do link)

## Bug Conhecido: Token Não Sincronizado Entre Agentes

Issue openclaw/openclaw#12685: quando múltiplos agentes compartilham o mesmo OAuth profile, o token renovado pode não ser sincronizado para todos os agents' `auth-profiles.json`. Se um agente de workflow falhar com OAuth error mas o main funciona, pode ser necessário copiar o token manualmente.

## Docs oficiais
- OAuth: https://docs.openclaw.ai/concepts/oauth
- Providers: https://docs.openclaw.ai/providers/index.md
