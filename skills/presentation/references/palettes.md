# Catálogo de Paletas

Cada paleta define CSS custom properties que fazem override das variáveis do engine em `base.css`.
Aplicar via bloco `<style>` no `index.html` do deck ou num arquivo `styles/theme.css`.

## Vector Labs (default)

**Vibe**: Dark profissional com acento laranja vibrante
**Uso**: Pitch decks Vector Labs, propostas comerciais, apresentações de produto

```css
:root {
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
}
```

## Mise (Sage + Argila)

**Vibe**: Orgânico, sofisticado, terroso
**Uso**: Produto Mise, apresentações com identidade Mise

```css
:root {
  --primary-dark: #1A2E22;
  --accent: #C4725A;
  --neutral: #8A9A8F;
  --surface-0: #F5F2EE;
  --surface-1: #EBE6E0;
  --surface-2: #DDD6CC;
  --surface-3: #C4B8AA;
  --surface-4: #A89888;
  --text-primary: #1A2E22;
  --text-secondary: #3D5A47;
  --text-dim: #8A9A8F;
}
```

## Tech Slate

**Vibe**: Moderno, tech, confiável
**Uso**: Demos de SaaS, pitches de tecnologia, apresentações técnicas

```css
:root {
  --primary-dark: #0F172A;
  --accent: #3B82F6;
  --neutral: #64748B;
  --surface-0: #F8FAFC;
  --surface-1: #F1F5F9;
  --surface-2: #E2E8F0;
  --surface-3: #CBD5E1;
  --surface-4: #94A3B8;
  --text-primary: #0F172A;
  --text-secondary: #334155;
  --text-dim: #64748B;
}
```

## Corporate Clean

**Vibe**: Formal, neutro, institucional
**Uso**: Propostas formais, relatórios, apresentações corporativas

```css
:root {
  --primary-dark: #1E293B;
  --accent: #2563EB;
  --neutral: #6B7280;
  --surface-0: #FFFFFF;
  --surface-1: #F9FAFB;
  --surface-2: #F3F4F6;
  --surface-3: #E5E7EB;
  --surface-4: #D1D5DB;
  --text-primary: #111827;
  --text-secondary: #374151;
  --text-dim: #6B7280;
}
```

## Creative Bold

**Vibe**: Energético, vibrante, ousado
**Uso**: Projetos criativos, workshops, apresentações de brainstorm

```css
:root {
  --primary-dark: #1A0A2E;
  --accent: #F43F5E;
  --neutral: #A78BFA;
  --surface-0: #FFF7ED;
  --surface-1: #FFEDD5;
  --surface-2: #FED7AA;
  --surface-3: #FDBA74;
  --surface-4: #FB923C;
  --text-primary: #1A0A2E;
  --text-secondary: #4C1D95;
  --text-dim: #7C3AED;
}
```

## Minimal Light

**Vibe**: Clean, arejado, minimalista
**Uso**: Apresentações internas, documentação, updates de equipe

```css
:root {
  --primary-dark: #18181B;
  --accent: #18181B;
  --neutral: #A1A1AA;
  --surface-0: #FAFAFA;
  --surface-1: #F4F4F5;
  --surface-2: #E4E4E7;
  --surface-3: #D4D4D8;
  --surface-4: #A1A1AA;
  --text-primary: #18181B;
  --text-secondary: #3F3F46;
  --text-dim: #71717A;
}
```

## Warm Earth

**Vibe**: Acolhedor, natural, artesanal
**Uso**: Lifestyle, hospitalidade, marcas com identidade orgânica

```css
:root {
  --primary-dark: #292524;
  --accent: #C2410C;
  --neutral: #A8A29E;
  --surface-0: #FAFAF9;
  --surface-1: #F5F5F4;
  --surface-2: #E7E5E4;
  --surface-3: #D6D3D1;
  --surface-4: #A8A29E;
  --text-primary: #1C1917;
  --text-secondary: #44403C;
  --text-dim: #78716C;
}
```

## Criar Paleta Custom

Se nenhuma paleta se encaixa, ajudar o usuário a criar uma. Perguntar:

1. **Cor principal da marca** (hex ou nome) — vira `--accent`
2. **Tom de fundo** (escuro, claro, neutro) — define `--primary-dark` e `--surface-*`
3. **Mood** (formal, casual, energético, minimalista) — ajusta contraste e intensidade

Gerar as variáveis seguindo a mesma estrutura: primary-dark, accent, neutral, surface-0..4, text-primary/secondary/dim.

## Tokens Estruturais (opcional por paleta)

As variáveis estruturais abaixo têm defaults definidos em `document-sections.md`. Paletas podem fazer override quando necessário:

```css
/* Defaults — só fazer override se a paleta exigir */
--radius: 12px;
--shadow-sm: 0 1px 4px rgba(45, 45, 45, 0.06);
--shadow-md: 0 2px 8px rgba(45, 45, 45, 0.08);
--shadow-lg: 0 4px 16px rgba(45, 45, 45, 0.12);
```

### Quando ajustar

- **Paletas com `surface-0` claro (ex: Corporate Clean, `#FFFFFF`)**: shadows precisam ser mais fortes para criar separação. Considerar `--shadow-md: 0 2px 8px rgba(0, 0, 0, 0.1)`.
- **Paletas com surfaces de alto contraste (ex: Creative Bold)**: borders sutis podem desaparecer. Considerar shadows mais fortes ou borders mais visíveis.
- **Documentos com fundo escuro** (`body { background: var(--primary-dark) }`): inverter a lógica de shadow — usar `rgba(0, 0, 0, 0.25)` ou mais, já que shadows claras são invisíveis em fundos escuros.
