# Vector Labs Skills Hub

## Estrutura

- `skills/` — Skills source (cada skill e um diretorio com SKILL.md)
- `site/` — Astro site (porta 4321, base path /skills-hub/)
- `scripts/aggregate-skills.js` — Le skills de ./skills/, gera site/src/data/skills.json
- `cli/` — Pacote npm `@vector-labs/skills` (CLI isolado, publicavel)
- `.github/workflows/deploy.yml` — Deploy GitHub Pages

## Desenvolvimento

```bash
npm run dev          # aggregate + astro dev
npm run build        # aggregate + astro build
npm run aggregate    # so regenerar skills.json
node cli/bin/vector-labs-skills.js --help  # testar CLI
```

## Principios

- Mudancas de branding: global.css (cores), Layout.astro (textos)
- Categorias Vector Labs adicionadas: observability, troubleshooting (em 5 arquivos de pagina)
- Skills ficam neste repo em skills/, aggregate-skills.js le daqui

## Git remotes

- `origin` — **fonte principal** (`vlabsai/skills-hub`). Push e PRs vao para ca.

### Workflow correto para feature branches

```bash
git checkout main
git pull origin main
git checkout -b feat/nome
# ... trabalhar ...
git push -u origin feat/nome
gh pr create --repo vlabsai/skills-hub --base main --head feat/nome
```

## Artefatos gerados (nao commitar)

- `site/src/data/skills.json` — gerado por `npm run aggregate`, ja no `.gitignore`. O CI (deploy.yml) regenera automaticamente.

## Publicar CLI (`@vector-labs/skills`)

O CLI vive em `cli/` e e publicado no npmjs.com (publico). Publicar **sempre de dentro do diretorio `cli/`** (nao da raiz).

```bash
# 1. Bump version em cli/package.json
# 2. Publicar
cd cli && npm publish
```

- publishConfig no package.json aponta para `https://registry.npmjs.org`
- Para publicar, precisa de token npm com permissao de publish
- **NUNCA rodar `npm publish` da raiz** — publica o pacote errado (`vector-labs-skills-hub` em vez de `@vector-labs/skills`)

## Dependencias

- Node >= 18
- gray-matter (parse SKILL.md frontmatter)
- Astro 5.17.x
