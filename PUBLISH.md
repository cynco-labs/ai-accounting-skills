# Publish `@cynco/accounting-skills`

## Status

| Version | npm | Notes |
|---|---|---|
| **2.0.0** | ✅ Live | Full CLI + marketplace identity |
| **2.0.1** | ✅ Live (`latest`) | Fixes `npx` multi-bin (`accounting-skills` bin name) |

```bash
npm view @cynco/accounting-skills version
# expect: 2.0.1
```

## Publish next version (on your Mac)

```bash
cd /Applications/Apps-Hazli/cynco-accounting-skills

npm whoami
node -p "require('./package.json').name + '@' + require('./package.json').version"
# expect: @cynco/accounting-skills@2.0.1

npm publish --access public --otp=XXXXXX
```

Replace `XXXXXX` with the 6-digit authenticator / recovery-flow code.

## Verify

```bash
npm view @cynco/accounting-skills version
# expect: 2.0.1

npx --yes @cynco/accounting-skills@2.0.1 doctor
npx --yes @cynco/accounting-skills doctor
```

## If publish fails

| Error | Fix |
|---|---|
| 2FA / otp required | Add `--otp=123456` |
| 403 no permission on `@cynco` | npmjs.com → orgs → cynco → Owner/Developer |
| Version already exists | Bump patch in `package.json` and retry |
| Need new login | `npm login` then publish again |

## After publish

- GitHub release tag `v2.0.1` (this repo)
- Optional: share `npx @cynco/accounting-skills demo`

---

## skills.sh (not npm)

[skills.sh](https://skills.sh) lists **GitHub agent skills**, not npm packages.

There is **no separate publish form**. Skills appear when people install:

```bash
npx skills add cynco-labs/ai-accounting-skills
```

| Item | Value |
|---|---|
| Directory | https://skills.sh/cynco-labs/ai-accounting-skills |
| Source | Public repo `cynco-labs/ai-accounting-skills` with `SKILL.md` files |
| Ranking | Anonymous install telemetry from the skills CLI |
| Badge | `https://skills.sh/b/cynco-labs/ai-accounting-skills` |

To boost ranking: share the install one-liner; installs are what surface skills on the leaderboard.
