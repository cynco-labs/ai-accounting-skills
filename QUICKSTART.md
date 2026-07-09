# Quick Start

**Install once · throw a folder · say “do the accounting.”**

Works for owners, bookkeepers, and firms. Docs can be messy — the agent shelves them, then books.

Works with **Claude Code · Codex · Cursor · Grok/xAI · GLM · Kimi** and [40+ agents](https://github.com/vercel-labs/skills#supported-agents) via skills.sh.

---

## 1 · Install

```bash
npx skills add cynco-labs/ai-accounting-skills
```

That’s the front door. [skills.sh/cynco-labs/ai-accounting-skills](https://skills.sh/cynco-labs/ai-accounting-skills)

---

## 2 · Throw work

Point the agent at a folder (or `@` files) and say:

> Do the accounting.

**What happens:** one intake (organize → register → soft-confirm) → extract → classify → post → recon → trial balance.  
**Books-only** stops there unless you ask for year-end / FS / tax. Prove with:

```bash
npx @cynco/accounting-skills score ./clients/yours   # depth scorecard
npx @cynco/accounting-skills close ./clients/yours   # full prove for that depth
```

Optional control: `/do-books` · `/extract` · `/classify` · `/post` · `/present` · `/prove`

---

## 3 · CLI (agent tools — optional for you)

```bash
npx @cynco/accounting-skills demo          # golden sample + Fava
npx @cynco/accounting-skills doctor        # deps check
npx @cynco/accounting-skills extract ./banks --json ./txns.json
npx @cynco/accounting-skills close ./clients/acme
```

Agents should run these **for** you. You don’t need the full command list to start.

---

## 4 · Claude Code plugins (optional)

```text
/plugin marketplace add https://github.com/cynco-labs/ai-accounting-skills
/plugin install accounting-engagement@claude-for-accounting
```

Then: “do the accounting” or `/do-books`  
(Plugin form: `/accounting-engagement:do-books`.)

**Firm letterhead** (practices only, when needed):

```text
/accounting-engagement:cold-start-interview
```

Owners doing their own books can skip firm setup.

---

## 5 · More

- Agent recipes: [docs/agents/](./docs/agents/)  
- Runtime rules: [`shared/runtime-brief.md`](./shared/runtime-brief.md)  
- Full README: [README.md](./README.md)
