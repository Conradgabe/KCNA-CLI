# Security Policy

## Reporting a vulnerability

Please do **not** open a public GitHub issue for security problems.

Email **evobsidianops@gmail.com** with:

- A clear description of the issue
- Steps to reproduce
- The affected version (`kcna version`)
- Your OS and Python version
- Whether a patch or mitigation is already known

You can expect an acknowledgement within a reasonable time. Once the issue is
validated and fixed, we will credit the reporter in the release notes unless
anonymity is requested.

## Scope

This project is a local CLI study tool. There is no hosted service, no network
API, and no account system. Reasonable security concerns still apply and are
welcome, including:

- Arbitrary-file-read or code-execution via malicious question bank JSON
- Supply-chain issues in dependencies
- PII leakage in saved session files beyond what the user knowingly stores
- Local privilege escalation through the installed console script

Out of scope:

- Social-engineering of the repo owner or maintainers
- Automated scanner findings without a demonstrated impact
- Issues that require the attacker to already have full local access to the
  user's machine
