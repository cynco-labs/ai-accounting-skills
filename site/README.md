# Landing — AI Accounting Skills

Astro + Vite static site for Cloudflare Pages.

## Design source (required)

**Follow [opencode.ai/data](https://opencode.ai/data) — not the main marketing lander.**

| Repo path | Role |
|-----------|------|
| `packages/stats/app/src/routes/index.css` | Design system (tokens, shell, sections) |
| `packages/stats/app/src/routes/stats-shell.tsx` | Header / footer / theme |
| `packages/stats/app/src/routes/index.tsx` | Page structure (hero, sections, bridges) |

Key traits:

- **IBM Plex Mono**
- Tokens: `--stats-bg`, `--stats-text`, `--stats-line`, `--stats-layer`, `--stats-accent`…
- `data-page="stats"` + `data-component` / `data-slot` styling
- Square controls (0 radius), sticky header, section bridges, 6px bit pattern masks
- Theme: `localStorage["opencode:stats-theme"]` = dark | light | system

Local CSS:

- `src/styles/stats-shell.css` — extracted shell from stats `index.css`
- `src/styles/stats.css` — dark theme + landing compositions on those tokens

## Commands

```bash
cd site
npm install
npm run dev          # http://localhost:4321
npm run build        # → dist/
npm run deploy       # build + wrangler pages deploy
```

## Cloudflare Pages (Git)

| Setting | Value |
|---------|-------|
| Root directory | `site` |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Node version | 20+ |
