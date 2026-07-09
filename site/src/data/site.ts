export const site = {
  name: "AI Accounting Skills",
  title: "AI Accounting Skills — from a folder of statements to balanced books",
  description:
    "Open-source skills for your coding agent. Drop bank statements and receipts; get organized books, a balancing trial balance, and an optional full year-end pack — with every figure tied to a source.",
  ogDescription:
    "Drop a folder. Get balanced books. Optional year-end pack. Beancount + Fava. No invented numbers.",
  version: "v2.3.1",
  github: "https://github.com/cynco-labs/ai-accounting-skills",
  skills: "https://skills.sh/cynco-labs/ai-accounting-skills",
  license: "https://github.com/cynco-labs/ai-accounting-skills/blob/master/LICENSE",
  docs: "https://github.com/cynco-labs/ai-accounting-skills#readme",
} as const

export const installMethods = [
  {
    id: "skills",
    label: "Any agent",
    command: "npx skills add cynco-labs/ai-accounting-skills",
    parts: [
      { text: "npx skills add " },
      { text: "cynco-labs/ai-accounting-skills", highlight: true },
    ],
  },
  {
    id: "cli",
    label: "Try a demo",
    command: "npx @cynco/accounting-skills demo",
    parts: [
      { text: "npx " },
      { text: "@cynco/accounting-skills", highlight: true },
      { text: " demo" },
    ],
  },
  {
    id: "claude",
    label: "Claude Code",
    command: "/plugin marketplace add https://github.com/cynco-labs/ai-accounting-skills",
    parts: [
      { text: "/plugin marketplace add " },
      { text: "cynco-labs/ai-accounting-skills", highlight: true },
    ],
  },
] as const

/** Four pillars — plain English for owners, bookkeepers, and firms */
export const pillars = [
  {
    id: "intake",
    title: "Organize",
    body: "We sort your files by company and month, then confirm who and what period we’re booking.",
    icon: "folder",
  },
  {
    id: "books",
    title: "Book",
    body: "Extract lines, code them, post journals, and reconcile the bank to zero difference.",
    icon: "scale",
  },
  {
    id: "close",
    title: "Close (if you need it)",
    body: "Optional year-end pack: adjustments, statements, notes, and checks — only when you ask.",
    icon: "file",
  },
  {
    id: "ledger",
    title: "Ledger",
    body: "Export a real double-entry ledger you can open in the browser (Beancount + Fava).",
    icon: "ledger",
  },
] as const

/** Six jobs users can learn — not a 9-stage firm checklist */
export const pipeline = [
  { n: "01", title: "Do the books", hint: "Start or continue" },
  { n: "02", title: "Extract", hint: "Bank lines" },
  { n: "03", title: "Classify", hint: "What the money is" },
  { n: "04", title: "Post", hint: "Journals + TB" },
  { n: "05", title: "Present", hint: "Statements" },
  { n: "06", title: "Prove", hint: "QC + lock" },
] as const

export const agents = [
  { name: "Claude Code", logo: "/brands/claude.svg", href: "https://claude.com/product/claude-code" },
  { name: "Codex", logo: "/brands/openai.svg", href: "https://openai.com/codex" },
  { name: "Cursor", logo: "/brands/cursor.svg", href: "https://cursor.com" },
  { name: "Grok", logo: "/brands/x.svg", href: "https://x.ai" },
  { name: "OpenCode", logo: "/brands/opencode.svg", href: "https://opencode.ai" },
  { name: "Windsurf", logo: "/brands/windsurf.svg", href: "https://windsurf.com" },
  { name: "Copilot", logo: "/brands/githubcopilot.svg", href: "https://github.com/features/copilot" },
  { name: "Gemini", logo: "/brands/google.svg", href: "https://gemini.google.com" },
] as const

export const stack = [
  { name: "Beancount", logo: null, hint: "Ledger" },
  { name: "Fava", logo: null, hint: "Browse" },
  { name: "skills.sh", logo: null, hint: "Install" },
  { name: "GitHub", logo: "/brands/github.svg", hint: "Source" },
] as const

export const faqs = [
  {
    q: "What do I actually do?",
    a: "Install the skills, point your agent at a folder of bank statements (and receipts if you have them), and say <strong>do the accounting</strong>. We organize the files, book the months you have, and stop when that job is done — unless you ask for a full year-end pack.",
  },
  {
    q: "Who is this for?",
    a: "Business owners doing their own books, bookkeepers, and accounting firms. Same tools for everyone; we adjust the language and how far we go (books only vs year-end).",
  },
  {
    q: "Which country?",
    a: "Malaysia first (MPERS / MFRS and local tax forms). Other countries can be added as data packs — we don’t hard-code one firm’s branding.",
  },
  {
    q: "Will it make up numbers?",
    a: "No. Every figure must come from a document, a prior signed set of accounts, or a formula on those. If something is missing, we ask or mark a limitation — we never invent balances.",
  },
  {
    q: "I only have a few months of banks. Can I still start?",
    a: "Yes. We book the months you have thoroughly. A full-year financial statement pack is optional when coverage (or your choice) supports it.",
  },
] as const
