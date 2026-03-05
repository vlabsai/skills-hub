# Vector Labs Skills Hub

Fork de samueltauil/skills-hub customizado para a Vector Labs.

## Estrutura

- `skills/` — Skills source (cada skill e um diretorio com SKILL.md)
- `site/` — Astro site (porta 4321, base path /skills-hub/)
- `scripts/aggregate-skills.js` — Le skills de ./skills/, gera site/src/data/skills.json
- `cli/` — Pacote npm `@vlabsai/skills` (CLI isolado, publicavel)
- `.github/workflows/deploy.yml` — Deploy GitHub Pages

## Desenvolvimento

```bash
npm run dev          # aggregate + astro dev
npm run build        # aggregate + astro build
npm run aggregate    # so regenerar skills.json
node cli/bin/vector-labs-skills.js --help  # testar CLI
```

## Principios

- Manter customizacoes minimas do upstream para facilitar merge
- Mudancas de branding: global.css (cores), Layout.astro (textos)
- Categorias Vector Labs adicionadas: observability, troubleshooting (em 5 arquivos de pagina)
- Skills ficam neste repo em skills/, aggregate-skills.js le daqui

## Git remotes

- `origin` — **fonte principal** (`vlabsai/skills-hub`). Push e PRs vao para ca.
- `upstream` — repo original (`samueltauil/skills-hub`). Upstream puro.

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

## Publicar CLI (`@vlabsai/skills`)

O CLI vive em `cli/` e e publicado no GitHub Packages. Publicar **sempre de dentro do diretorio `cli/`** (nao da raiz).

```bash
# 1. Bump version em cli/package.json
# 2. Publicar
cd cli && npm publish
```

- Requer `.npmrc` com `//npm.pkg.github.com/:_authToken=<TOKEN>` configurado
- publishConfig no package.json ja aponta para `https://npm.pkg.github.com`
- **NUNCA rodar `npm publish` da raiz** — publica o pacote errado (`vector-labs-skills-hub` em vez de `@vlabsai/skills`)

## Dependencias

- Node >= 18
- gray-matter (parse SKILL.md frontmatter)
- Astro 5.17.x
