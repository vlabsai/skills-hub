# Seções Base — Documentos Visuais

Padrões reutilizáveis para documentos HTML verticais. Usar como base e adaptar livremente conforme o conteúdo. Novas seções podem ser inventadas seguindo os mesmos tokens de design.

## Estrutura HTML Base

Cada documento visual é um HTML único self-contained:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Título do Documento</title>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,600;9..144,800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    /* Palette — replace with chosen palette from palettes.md */
    :root {
      /* Example: Vector Labs (swap entire block per palette) */
      --primary-dark: #2D2D2D;
      --accent: #E04B1A;
      --neutral: #8A8085;
      --surface-0: #F5F0EB;
      --surface-1: #EDE6DF;
      --surface-2: #E0D8D0;
      --surface-3: #D4CBC2;
      --surface-4: #C8BEB4;
      --text-primary: #2D2D2D;
      --text-secondary: #5A5A5A;
      --text-dim: #8A8085;

      /* Structural tokens — consistent across palettes */
      --doc-width: 900px;
      --radius: 12px;
      --gap-section: 56px;
      --gap-section-sm: 32px;
      --gap-card: 24px;
      --gap-element: 12px;
      --shadow-sm: 0 1px 4px rgba(45, 45, 45, 0.06);
      --shadow-md: 0 2px 8px rgba(45, 45, 45, 0.08);
      --shadow-lg: 0 4px 16px rgba(45, 45, 45, 0.12);
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      color: var(--text-primary);
      background: var(--surface-0);
      line-height: 1.6;
    }

    .doc {
      max-width: var(--doc-width);
      margin: 0 auto;
      padding: 64px 32px;
    }

    /* Typography */
    .doc h1 { font-family: 'Fraunces', serif; font-weight: 800; font-size: 40px; letter-spacing: -0.02em; line-height: 1.15; margin-bottom: 16px; }
    .doc h2 { font-family: 'Fraunces', serif; font-weight: 600; font-size: 28px; letter-spacing: -0.01em; line-height: 1.25; margin-bottom: 12px; }
    .doc h3 { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700; font-size: 18px; margin-bottom: 8px; }
    .doc p { font-size: 16px; margin-bottom: 16px; color: var(--text-secondary); }
    .doc .label { font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.15em; color: var(--accent); }
    .doc .mono { font-family: 'JetBrains Mono', monospace; font-size: 13px; }

    /* Section spacing */
    .section { margin-bottom: var(--gap-section); }
    .section-sm { margin-bottom: var(--gap-section-sm); }
  </style>
</head>
<body>
  <div class="doc">
    <!-- seções aqui -->
  </div>
</body>
</html>
```

## Dark variant

Para documentos com fundo escuro, trocar body styles:

```css
body {
  background: var(--primary-dark);
  color: #fff;
}
.doc p { color: rgba(255,255,255,0.7); }
.doc h1, .doc h2, .doc h3 { color: #fff; }
```

## Seções Base

### Hero / Header

Título principal com metadata. Primeira coisa do documento.

```html
<header class="section hero">
  <span class="label">Tipo do Documento</span>
  <h1>Título Principal do Documento</h1>
  <p class="hero-subtitle">Subtítulo ou descrição breve do que se trata</p>
  <div class="hero-meta">
    <span class="mono">Vector Labs</span>
    <span class="meta-sep">·</span>
    <span class="mono">Fev 2026</span>
  </div>
</header>
```

```css
.hero-subtitle { font-size: 20px; color: var(--text-secondary); max-width: 640px; }
.hero-meta { display: flex; gap: 8px; align-items: center; margin-top: 24px; color: var(--text-dim); }
.meta-sep { color: var(--neutral); }
```

### Stat Block

1 a 4 números grandes em linha. Bom pra métricas, KPIs, highlights.

```html
<div class="section stats-grid">
  <div class="stat-card">
    <span class="stat-value">R$ 2.4M</span>
    <span class="stat-label">Receita Anual</span>
  </div>
  <div class="stat-card">
    <span class="stat-value">47%</span>
    <span class="stat-label">Crescimento YoY</span>
  </div>
  <div class="stat-card">
    <span class="stat-value">12</span>
    <span class="stat-label">Clientes Ativos</span>
  </div>
</div>
```

```css
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: var(--gap-card); }
.stat-card { background: var(--surface-1); border-radius: var(--radius); padding: 24px; border: 1px solid var(--surface-2); border-top: 2px solid var(--accent); box-shadow: var(--shadow-md); }
.stat-value { font-family: 'Fraunces', serif; font-weight: 800; font-size: 36px; display: block; color: var(--accent); }
.stat-label { font-family: 'JetBrains Mono', monospace; font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-dim); margin-top: 8px; display: block; }
```

### Card Grid

Cards com ícone, título e descrição. 2-3 colunas.

```html
<div class="section">
  <span class="label">Seção</span>
  <h2>Título da Seção</h2>
  <div class="card-grid">
    <div class="card">
      <div class="card-icon"><!-- Lucide SVG inline --></div>
      <h3>Card Title</h3>
      <p>Descrição do card com informações relevantes.</p>
    </div>
    <!-- mais cards -->
  </div>
</div>
```

```css
.card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: var(--gap-card); margin-top: var(--gap-card); }
.card { background: var(--surface-1); border-radius: var(--radius); padding: 28px; border: 1px solid var(--surface-2); box-shadow: var(--shadow-md); }
.card-icon { width: 40px; height: 40px; background: var(--accent); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #fff; margin-bottom: 16px; }
.card-icon svg { width: 20px; height: 20px; }
.card h3 { margin-bottom: 8px; }
.card p { font-size: 14px; margin-bottom: 0; }
```

### Texto com Label

Seção de texto corrido com label de categoria.

```html
<div class="section">
  <span class="label">Contexto</span>
  <h2>Título da Seção</h2>
  <p>Parágrafo com texto corrido explicando o conteúdo em detalhe...</p>
  <p>Mais parágrafos conforme necessário.</p>
</div>
```

### Callout / Quote

Destaque visual para citações ou informações importantes.

```html
<div class="callout">
  <p>"Citação ou informação em destaque que merece atenção especial."</p>
  <span class="callout-attr">— Atribuição</span>
</div>
```

```css
.callout { border-left: 3px solid var(--accent); padding: 24px 28px; background: var(--surface-1); border-radius: 0 var(--radius) var(--radius) 0; margin: var(--gap-section-sm) 0; border-top: 1px solid var(--surface-2); border-right: 1px solid var(--surface-2); border-bottom: 1px solid var(--surface-2); box-shadow: var(--shadow-sm); }
.callout p { font-family: 'Fraunces', serif; font-size: 20px; font-weight: 400; color: var(--text-primary); margin-bottom: 8px; }
.callout-attr { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--text-dim); }
```

### Tabela

Tabela estilizada para dados estruturados.

```html
<div class="section">
  <span class="label">Dados</span>
  <h2>Título</h2>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Coluna A</th><th>Coluna B</th><th>Coluna C</th></tr></thead>
      <tbody>
        <tr><td>Valor</td><td>Valor</td><td>Valor</td></tr>
      </tbody>
    </table>
  </div>
</div>
```

```css
.table-wrap { overflow-x: auto; margin-top: 16px; }
table { width: 100%; border-collapse: collapse; }
th { font-family: 'JetBrains Mono', monospace; font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-dim); text-align: left; padding: 12px 16px; border-bottom: 2px solid var(--surface-2); }
td { padding: 12px 16px; border-bottom: 1px solid var(--surface-2); font-size: 14px; }
```

### Divider

Separação visual entre seções.

```html
<hr class="divider">
```

```css
.divider { border: none; height: 1px; background: var(--surface-3); margin: var(--gap-section) 0; }
```

## Princípios para Novas Seções

Ao inventar seções não catalogadas, seguir:

- **Containers**: `border-radius: var(--radius)`, `background: var(--surface-1)`, `padding: 24-28px`, `border: 1px solid var(--surface-2)`, `box-shadow: var(--shadow-md)`
- **Spacing**: usar as variáveis `--gap-card`, `--gap-section`, `--gap-element` — nunca valores hardcoded
- **Depth**: todo card/container precisa de border + shadow para separar do fundo. Sem isso, cards se perdem no background.
- **Accent borders**: usar `border-top: 2px solid var(--accent)` em cards de destaque (stats, KPIs). Usar `border-left: 3px solid var(--accent)` em cards sequenciais (métodos, steps) e callouts.
- **Internal separators**: cards com múltiplas zonas (ex: descrição + prós/contras) devem ter `border-top: 1px solid var(--surface-2)` separando as zonas.
- **Labels**: sempre JetBrains Mono 11px uppercase, cor `--accent`
- **Títulos**: Fraunces para h1/h2, Plus Jakarta Sans para h3+
- **Dados/números**: Fraunces bold para destaque, JetBrains Mono para meta
- **Ícones**: Lucide icons, inline SVG, stroke-width 2, 16-24px
- **Cores de fundo**: usar a escala surface-0..4 para backgrounds. Cards usam `var(--surface-1)` com border para contraste.
