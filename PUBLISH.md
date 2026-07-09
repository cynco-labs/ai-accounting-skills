# Publish & release (CI/CD)

## How a release ships (automatic)

```text
1. Bump VERSION + package.json version (same number)
2. Add a ## [X.Y.Z] section to CHANGELOG.md
3. Merge / push to main
4. GitHub Actions workflow "release":
     - runs full CI (ci_check.sh)
     - if tag vX.Y.Z does not exist → create tag + GitHub Release
     - if NPM_TOKEN secret is set → npm publish @cynco/accounting-skills@X.Y.Z
```

| Artifact | Automatic? | Where |
|---|---|---|
| CI validate | Yes | `.github/workflows/validate.yml` + release job |
| Git tag `vX.Y.Z` | **Yes** | `.github/workflows/release.yml` |
| GitHub Release | **Yes** | same (notes from CHANGELOG) |
| npm `@cynco/accounting-skills` | Yes **if** `NPM_TOKEN` repo secret | same |

Default branch: **`main`**. Always push release bumps there (not only `master`).

## One-time GitHub setup

### 1. Repo secrets

Settings → Secrets and variables → Actions:

| Secret | Required for | Value |
|---|---|---|
| `NPM_TOKEN` | npm publish from CI | npm classic **Automation** token with publish on `@cynco` (no OTP) |

`GITHUB_TOKEN` is provided by Actions (contents: write) — no setup for tags/releases.

### 2. Branch protection (recommended)

Protect `main`: require `validate` / `release / validate` green before merge.

## Manual version bump checklist

```bash
# 1) versions in lockstep
echo 2.2.5 > VERSION
# edit package.json "version": "2.2.5"
# 2) CHANGELOG.md — add ## [2.2.5] — YYYY-MM-DD with notes
# 3) commit + push to main
git checkout main
git add VERSION package.json CHANGELOG.md
git commit -m "chore: release v2.2.5"
git push origin main
# 4) Watch Actions → "release" workflow
```

Verify:

```bash
gh release view v2.2.5
npm view @cynco/accounting-skills version   # if NPM_TOKEN set
```

## Manual fallback (if CI cannot publish npm)

Automation token preferred. If you must use a 2FA user token locally:

```bash
npm whoami
npm publish --access public --otp=XXXXXX
```

GitHub release should still have been created by CI when the tag was cut.

## Force re-run notes

Actions → **release** → Run workflow → optional force flag (notes only; does not move tags).

## Local checks before push

```bash
python3 scripts/version_check.py
python3 scripts/changelog_section.py $(cat VERSION)   # preview release body
bash scripts/ci_check.sh
```

## skills.sh

Not npm. Public GitHub skills install:

```bash
npx skills add cynco-labs/ai-accounting-skills
```
