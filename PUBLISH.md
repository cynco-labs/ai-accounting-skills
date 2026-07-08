# Publish `@cynco/accounting-skills@2.0.0`

You already own this package name on npm (was 1.0.2).  
Publishing **2.0.0** replaces what `npx` / `npm i` get by default.

## Prerequisites

1. Logged into npm on this machine (`npm whoami` → your user)
2. Authenticator app ready for **OTP**
3. Access to the **`@cynco`** org on npm (you already published 1.0.2 under it)

## Steps (on your Mac)

```bash
cd /Applications/Apps-Hazli/cynco-accounting-skills

# 1. Confirm identity
npm whoami
# expect: hazlijohar (or your npm user)

# 2. Confirm package name + version
node -p "require('./package.json').name + '@' + require('./package.json').version"
# expect: @cynco/accounting-skills@2.0.0

# 3. Dry-run (optional)
npm publish --access public --dry-run

# 4. Publish with 2FA code from your authenticator
npm publish --access public --otp=XXXXXX
```

Replace `XXXXXX` with the 6-digit code.

## Verify

```bash
npm view @cynco/accounting-skills version
# expect: 2.0.0

npx @cynco/accounting-skills@2.0.0 doctor
npx @cynco/accounting-skills@2.0.0 demo
```

## If publish fails

| Error | Fix |
|---|---|
| 2FA / otp required | Add `--otp=123456` |
| 403 no permission on `@cynco` | npmjs.com → orgs → cynco → ensure you're Owner/Developer |
| Version already exists | Bump patch in package.json and retry |
| Need new login | `npm login` then publish again |

## After publish (optional)

- Tweet/LinkedIn: `npx @cynco/accounting-skills demo`
- GitHub release notes already track the product; npm is the distribution channel for the CLI
