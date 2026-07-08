#!/usr/bin/env node
/**
 * @cynco/ai-accounting — thin CLI over the Python scripts in this repo.
 * Works via: npx @cynco/ai-accounting <cmd>
 */
import { spawn, spawnSync } from "node:child_process";
import {
  existsSync,
  mkdirSync,
  cpSync,
  writeFileSync,
  readFileSync,
  readdirSync,
  statSync,
} from "node:fs";
import { createRequire } from "node:module";
import { dirname, join, resolve, basename } from "node:path";
import { fileURLToPath } from "node:url";
import { homedir } from "node:os";

const __dirname = dirname(fileURLToPath(import.meta.url));
const PKG_ROOT = resolve(__dirname, "../..");
const VERSION = JSON.parse(
  readFileSync(join(PKG_ROOT, "package.json"), "utf8"),
).version;

const c = {
  reset: "\x1b[0m",
  bold: "\x1b[1m",
  dim: "\x1b[2m",
  cyan: "\x1b[36m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  red: "\x1b[31m",
  magenta: "\x1b[35m",
};

function log(msg) {
  console.log(msg);
}
function info(msg) {
  console.log(`${c.cyan}→${c.reset} ${msg}`);
}
function ok(msg) {
  console.log(`${c.green}✓${c.reset} ${msg}`);
}
function warn(msg) {
  console.log(`${c.yellow}!${c.reset} ${msg}`);
}
function fail(msg) {
  console.error(`${c.red}✗${c.reset} ${msg}`);
}

function banner() {
  log("");
  log(`${c.bold}${c.cyan}AI Accounting${c.reset} ${c.dim}v${VERSION}${c.reset}`);
  log(`${c.dim}folder → books → Beancount → Fava${c.reset}`);
  log("");
}

function usage(code = 0) {
  banner();
  log(`${c.bold}Usage${c.reset}
  npx @cynco/ai-accounting <command> [options]

${c.bold}Commands${c.reset}
  ${c.green}demo${c.reset}              Golden mini ledger + Fava (instant wow)
  ${c.green}init${c.reset} [name]       Scaffold a client engagement workspace
  ${c.green}extract${c.reset} <path>    Bank PDF/CSV → Excel (+ optional JSON)
  ${c.green}ledger${c.reset} <client>   Journals → Beancount system of record
  ${c.green}fava${c.reset} [path]       Open Fava UI on a ledger or client dir
  ${c.green}check${c.reset} [client]    Validate engagement artifacts or full CI
  ${c.green}doctor${c.reset}            Check Python / deps / tools
  ${c.green}version${c.reset}           Print version

${c.bold}Examples${c.reset}
  npx @cynco/ai-accounting demo
  npx @cynco/ai-accounting extract ~/Downloads/CJT-BS-2026
  npx @cynco/ai-accounting ledger ./clients/acme --fava
  npx @cynco/ai-accounting init acme-sdn-bhd

${c.bold}Claude Code plugins${c.reset}
  /plugin marketplace add https://github.com/cynco-labs/ai-accounting-skills
  /plugin install accounting-engagement@claude-for-accounting

Docs: https://github.com/cynco-labs/ai-accounting-skills
`);
  process.exit(code);
}

function findPython() {
  for (const bin of ["python3", "python"]) {
    const r = spawnSync(bin, ["--version"], { encoding: "utf8" });
    if (r.status === 0) return bin;
  }
  return null;
}

function findOnPath(names) {
  for (const name of names) {
    const r = spawnSync("which", [name], { encoding: "utf8" });
    if (r.status === 0 && r.stdout.trim()) return r.stdout.trim();
  }
  // common user installs
  const extras = [
    join(homedir(), "Library/Python/3.12/bin"),
    join(homedir(), "Library/Python/3.11/bin"),
    join(homedir(), ".local/bin"),
  ];
  for (const dir of extras) {
    for (const name of names) {
      const p = join(dir, name);
      if (existsSync(p)) return p;
    }
  }
  return null;
}

function run(cmd, args, opts = {}) {
  const r = spawnSync(cmd, args, {
    stdio: "inherit",
    cwd: opts.cwd || PKG_ROOT,
    env: { ...process.env, ...opts.env },
  });
  return r.status ?? 1;
}

function runCapture(cmd, args) {
  return spawnSync(cmd, args, { encoding: "utf8" });
}

function ensurePythonDeps(py, mods) {
  const missing = [];
  for (const m of mods) {
    const r = runCapture(py, ["-c", `import ${m}`]);
    if (r.status !== 0) missing.push(m);
  }
  if (missing.length === 0) return true;
  warn(`Missing Python packages: ${missing.join(", ")}`);
  info(`Install: ${py} -m pip install -r "${join(PKG_ROOT, "requirements.txt")}"`);
  info(`Or:      ${py} -m pip install ${missing.join(" ")}`);
  return false;
}

function script(name) {
  const p = join(PKG_ROOT, "scripts", name);
  if (!existsSync(p)) {
    fail(`Script not found: ${p}`);
    process.exit(1);
  }
  return p;
}

/** ---------- commands ---------- */

function cmdDoctor() {
  banner();
  log(`${c.bold}Environment${c.reset}`);
  const py = findPython();
  if (py) {
    const v = runCapture(py, ["--version"]);
    ok(`Python: ${py} (${(v.stdout || v.stderr || "").trim()})`);
  } else {
    fail("Python 3 not found (required)");
  }

  const checks = [
    ["openpyxl", "openpyxl"],
    ["pdfplumber", "pdfplumber"],
    ["beancount", "beancount"],
  ];
  if (py) {
    for (const [label, mod] of checks) {
      const r = runCapture(py, ["-c", `import ${mod}`]);
      if (r.status === 0) ok(`${label}`);
      else warn(`${label} missing`);
    }
  }

  const fava = findOnPath(["fava"]);
  const beanCheck = findOnPath(["bean-check"]);
  if (fava) ok(`fava: ${fava}`);
  else warn("fava not on PATH (pip install fava)");
  if (beanCheck) ok(`bean-check: ${beanCheck}`);
  else warn("bean-check not on PATH (pip install beancount)");

  ok(`Package root: ${PKG_ROOT}`);
  ok(`Node: ${process.version}`);
  log("");
  info("Full install: pip install -r requirements.txt");
  return 0;
}

function cmdInit(name) {
  banner();
  const slug = (name || "my-client")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
  const root = resolve(process.cwd(), "clients", slug);
  if (existsSync(root)) {
    fail(`Already exists: ${root}`);
    return 1;
  }
  for (const d of [
    "source/bank",
    "workpapers/reconciliations",
    "outputs/fs",
    "outputs/tax",
    "ledger",
  ]) {
    mkdirSync(join(root, d), { recursive: true });
  }

  const state = {
    schema_version: "0.0.1",
    client_slug: slug,
    legal_name: slug,
    entity_type: "unknown",
    fy_start: null,
    fy_end: null,
    framework: "MPERS",
    jurisdiction_pack: "malaysia",
    currency: "MYR",
    industry_overlay: null,
    engagement_type: "year_end",
    current_stage: "setup",
    status: "not_started",
    stages_completed: [],
    artifacts: {},
    blockers: [],
    open_queries: [],
    provisional: true,
    updated_at: new Date().toISOString(),
    notes: "Scaffolded by npx @cynco/ai-accounting init",
  };
  writeFileSync(join(root, "engagement_state.json"), JSON.stringify(state, null, 2) + "\n");
  writeFileSync(
    join(root, "README.md"),
    `# ${slug}

Scaffolded engagement workspace.

## Next

1. Drop bank PDFs/CSVs into \`source/bank/\`
2. \`npx @cynco/ai-accounting extract ${root}/source/bank --out ${root}/outputs/bank.xlsx --json ${root}/workpapers/transactions.json\`
3. Use Claude Code + accounting-engagement skills for classify → YE → FS
4. \`npx @cynco/ai-accounting ledger ${root} --fava\`

See https://github.com/cynco-labs/ai-accounting-skills
`,
  );
  writeFileSync(join(root, "source/register.md"), `# Source register — ${slug}\n\n| Doc | Status |\n|---|---|\n| source/bank/ | pending |\n`);
  ok(`Created ${root}`);
  info("Drop statements into source/bank/ then run extract");
  return 0;
}

function cmdExtract(inputPath, opts) {
  banner();
  if (!inputPath) {
    fail("Usage: extract <folder-or-pdf> [--out file.xlsx] [--json file.json]");
    return 1;
  }
  const input = resolve(inputPath);
  if (!existsSync(input)) {
    fail(`Not found: ${input}`);
    return 1;
  }
  const py = findPython();
  if (!py) {
    fail("python3 required");
    return 1;
  }
  if (!ensurePythonDeps(py, ["pdfplumber", "openpyxl"])) return 1;

  const outXlsx =
    opts.out ||
    resolve(process.cwd(), `bank_extract_${Date.now()}.xlsx`);
  const outJson = opts.json || null;

  const args = [
    script("extract_maybank_islamic_pdf.py"),
    "--input",
    input,
    "--output",
    outXlsx,
    "--fail-on-error",
  ];
  if (outJson) {
    args.push("--also-json", resolve(outJson));
    args.push("--client-slug", opts.slug || "client");
  }

  info(`Extracting Maybank-style PDFs from ${input}`);
  const code = run(py, args);
  if (code === 0) {
    ok(`Excel: ${outXlsx}`);
    if (outJson) ok(`JSON: ${resolve(outJson)}`);
  }
  return code;
}

function cmdLedger(clientDir, opts) {
  banner();
  if (!clientDir) {
    fail("Usage: ledger <client-dir> [--out path.beancount] [--fava]");
    return 1;
  }
  const client = resolve(clientDir);
  if (!existsSync(client)) {
    fail(`Not found: ${client}`);
    return 1;
  }
  const py = findPython();
  if (!py) {
    fail("python3 required");
    return 1;
  }

  const out =
    opts.out ||
    join(client, "ledger", "main.beancount");
  mkdirSync(dirname(out), { recursive: true });

  const coaDefault = join(PKG_ROOT, "references/coa_templates/coa_sdn_bhd.json");
  const args = [
    script("export_to_beancount.py"),
    "--client-dir",
    client,
    "--output",
    out,
    "--bean-check",
  ];
  if (existsSync(coaDefault) && !existsSync(join(client, "workpapers/coa.json"))) {
    args.push("--coa", coaDefault);
  }

  info(`Exporting Beancount ledger → ${out}`);
  const code = run(py, args);
  if (code !== 0) return code;
  ok(`Ledger: ${out}`);
  if (opts.fava) return cmdFava(out, {});
  info(`Open UI: npx @cynco/ai-accounting fava ${out}`);
  return 0;
}

function cmdFava(pathArg, opts) {
  banner();
  let ledger = pathArg ? resolve(pathArg) : null;

  // client dir → ledger/main.beancount
  if (ledger && existsSync(ledger) && statSync(ledger).isDirectory()) {
    const candidate = join(ledger, "ledger/main.beancount");
    if (existsSync(candidate)) ledger = candidate;
    else {
      fail(`No ledger at ${candidate} — run: ledger ${pathArg}`);
      return 1;
    }
  }

  if (!ledger) {
    // try golden demo ledger inside package
    const golden = join(PKG_ROOT, "fixtures/golden-mini-sdn-bhd/ledger/main.beancount");
    if (existsSync(golden)) ledger = golden;
  }

  if (!ledger || !existsSync(ledger)) {
    fail("Usage: fava <main.beancount|client-dir>");
    return 1;
  }

  const port = opts.port || "5000";
  const fava = findOnPath(["fava"]);
  if (!fava) {
    fail("fava not found. Install: pip install fava beancount");
    return 1;
  }

  const beanCheck = findOnPath(["bean-check"]);
  if (beanCheck) {
    info("bean-check…");
    const chk = run(beanCheck, [ledger]);
    if (chk !== 0) {
      fail("bean-check failed — fix ledger before Fava");
      return 1;
    }
    ok("bean-check PASS");
  }

  log("");
  ok(`Fava → ${c.bold}http://127.0.0.1:${port}${c.reset}`);
  info(`Ledger: ${ledger}`);
  info("Stop with Ctrl+C");
  log("");

  const child = spawn(fava, ["--host", "127.0.0.1", "--port", String(port), ledger], {
    stdio: "inherit",
  });
  child.on("exit", (code) => process.exit(code ?? 0));
  return 0;
}

function cmdDemo(opts) {
  banner();
  log(`${c.bold}Demo${c.reset} — synthetic Golden Mini Sdn. Bhd. ledger in Fava`);
  log("");

  const golden = join(PKG_ROOT, "fixtures/golden-mini-sdn-bhd");
  const ledger = join(golden, "ledger/main.beancount");

  if (!existsSync(ledger)) {
    // try to build it
    const py = findPython();
    if (!py) {
      fail("python3 required for demo");
      return 1;
    }
    info("Building golden ledger…");
    const code = run(py, [
      script("export_to_beancount.py"),
      "--client-dir",
      golden,
      "--output",
      ledger,
      "--coa",
      join(PKG_ROOT, "references/coa_templates/coa_sdn_bhd.json"),
      "--bean-check",
    ]);
    if (code !== 0) return code;
  } else {
    ok(`Golden ledger: ${ledger}`);
  }

  const fava = findOnPath(["fava"]);
  if (!fava) {
    warn("fava not installed — showing ledger path only");
    info("pip install fava beancount");
    info(`Then: npx @cynco/ai-accounting fava ${ledger}`);
    // still print a taste of the file
    const head = readFileSync(ledger, "utf8").split("\n").slice(0, 24).join("\n");
    log("");
    log(`${c.dim}${head}${c.reset}`);
    return 0;
  }

  log(`${c.magenta}What you're looking at${c.reset}`);
  log("  Synthetic mini Sdn Bhd · balanced journals · Beancount SoR");
  log("  Not a real client — for demo / CI only");
  log("");
  return cmdFava(ledger, { port: opts.port || "5000" });
}

function cmdCheck(clientOrEmpty) {
  banner();
  const py = findPython();
  if (!py) {
    fail("python3 required");
    return 1;
  }

  if (!clientOrEmpty) {
    info("Running full repo CI (scripts/ci_check.sh)…");
    const sh = join(PKG_ROOT, "scripts/ci_check.sh");
    return run("bash", [sh], { cwd: PKG_ROOT });
  }

  const client = resolve(clientOrEmpty);
  if (!existsSync(client)) {
    fail(`Not found: ${client}`);
    return 1;
  }
  info(`Validating engagement: ${client}`);
  return run(py, [script("validate_engagement_artifacts.py"), client]);
}

/** ---------- argv ---------- */

function parseArgs(argv) {
  const args = argv.slice(2);
  if (args.length === 0 || args[0] === "-h" || args[0] === "--help") {
    usage(0);
  }
  const cmd = args[0];
  const rest = args.slice(1);
  const opts = {};
  const positional = [];
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a === "--out" || a === "-o") opts.out = rest[++i];
    else if (a === "--json") opts.json = rest[++i];
    else if (a === "--slug") opts.slug = rest[++i];
    else if (a === "--fava") opts.fava = true;
    else if (a === "--port") opts.port = rest[++i];
    else if (a.startsWith("-")) {
      fail(`Unknown flag: ${a}`);
      usage(1);
    } else positional.push(a);
  }
  return { cmd, positional, opts };
}

function main() {
  const { cmd, positional, opts } = parseArgs(process.argv);

  switch (cmd) {
    case "version":
    case "-V":
    case "--version":
      console.log(VERSION);
      return 0;
    case "help":
      usage(0);
      break;
    case "doctor":
      return cmdDoctor();
    case "init":
      return cmdInit(positional[0]);
    case "extract":
      return cmdExtract(positional[0], opts);
    case "ledger":
      return cmdLedger(positional[0], opts);
    case "fava":
      return cmdFava(positional[0], opts);
    case "demo":
      return cmdDemo(opts);
    case "check":
      return cmdCheck(positional[0]);
    default:
      fail(`Unknown command: ${cmd}`);
      usage(1);
  }
}

const code = main();
if (typeof code === "number") process.exit(code);
