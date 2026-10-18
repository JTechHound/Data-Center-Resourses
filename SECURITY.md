# Security Policy

## Supported Versions

This project follows a simple version scheme: **v1, v2, v3…** — one number line, no fractures. Security fixes go into the latest version.

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |
| older   | :x:                |

If you're on an older version, update to the latest before reporting — the issue may already be fixed.

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.** Public issues tip off everyone before a fix exists.

Instead, report privately:

- **Email:** arthurjones@trialityresearch.org
- **Subject line:** `[SECURITY] <brief description>`

Include in your report:
1. What you found and where (file, line, or endpoint)
2. Steps to reproduce it
3. What you think the impact is
4. Anything you've already tried

## What Happens Next

1. **Acknowledgment** — you'll hear back within 7 days.
2. **Assessment** — the report gets reviewed and the severity assessed.
3. **Fix** — a patched version ships as the next v-number on the same line. No silent fixes; the fix is logged in the release notes.
4. **Credit** — reporters who want it get credited by name in the release notes. If you'd rather stay anonymous, say so and that's respected.

## Scope Notes

- This is open research code, published for provenance and reproducibility. There are no production secrets, credentials, or private user data in these repositories.
- The most useful reports concern code that other people will run: simulation scripts, install tooling, and anything that touches the network or the filesystem.
- Theoretical disagreements with the framework itself are not vulnerabilities — open an issue or start a discussion for those. They're welcome too, just in the right place.

## Philosophy

Everything here is open source, mistakes included. A vulnerability found is a vulnerability fixed — reporting one makes the work stronger, and that's always appreciated.
