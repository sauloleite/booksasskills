## Contents

1. Stance
2. Transport security (HTTPS and TLS)
3. Authentication and authorization
4. Protecting user data and PII
5. Encryption at rest
6. Compliance regimes
7. SBOM and dependency hygiene
8. Pitfalls

# Security and compliance essentials

## 1. Stance

Security is continuous work built in from the start of development, not a coat of paint before release. Developers need not be specialists, but they must know the basics, lean on OWASP guidance, and pull in the organization's security people at design time. No single control suffices; stack several so an attacker must defeat all of them (defense in depth).

## 2. Transport security (HTTPS and TLS)

Mental model: HTTP is a postcard anyone handling it can read; HTTPS seals it in an envelope. TLS provides encryption and integrity (data cannot be read or silently altered in transit). Certificates act as a server's identity document, issued by certificate authorities that verify ownership.

Rules:

- Test with HTTPS before production; locally trusted development certificates exist, so convenience is no excuse.
- Encrypt every page and API, not only authentication screens.
- Auto-redirect plain HTTP requests to HTTPS.
- Automate certificate renewal so nothing expires unnoticed.
- Allow only TLS 1.2 or newer.
- "SSL" in conversation usually means TLS; verify that real SSL protocols are disabled, since they are broken.

HTTPS is one layer only; it does not fix application flaws.

## 3. Authentication and authorization

Authentication proves who someone is; authorization decides what they may do.

**Rule zero: never build your own security mechanisms.** Use a mature framework (the chapter cites Spring Security, with two decades of hardening) and its vetted password encoders (for example bcrypt). Storing plaintext passwords is never acceptable.

Password policy (example values from the chapter):

- Minimum length 12 with mixed character classes.
- Reject known-common and breached passwords; block reuse of previous ones.
- Modern adaptive hashing with a unique random salt per password (defeats rainbow tables).
- Support password managers and autofill.
- Remember that human behavior (sticky notes, sharing) undermines any policy, hence the need for MFA.

Account protection:

- Exponential backoff after failed logins, from a few seconds (5 s) growing to half an hour or more.
- Watch for one IP failing across many accounts and one account attacked from many places.
- CAPTCHA after several failures.
- Notify users about logins from new devices or locations.
- Account recovery with real verification steps.

Session management:

- Session tokens from a cryptographically secure generator with enough entropy.
- Both idle and absolute timeouts (example: 30 minutes idle, 8 hours total), shorter for high-risk operations such as banking.
- Keep revoked tokens on a blocklist until they would have expired naturally.

Multifactor authentication:

- Offer authenticator apps, hardware security keys and biometrics; SMS and email codes are convenient but weaker (SIM swapping).
- Step up verification on unusual signals (new device or location).
- Require MFA during account recovery, otherwise recovery becomes the bypass.
- Provide backup codes; allow trusted-device remembering with sensible controls.

Small illustration of backoff timing (example policy, tune per risk):

```python
def lockout_seconds(failures: int, base: int = 5, cap: int = 1800) -> int:
    """0 for the first failure, then 5, 10, 20, ... capped at 30 minutes."""
    if failures <= 1:
        return 0
    return min(cap, base * 2 ** (failures - 2))
```

## 4. Protecting user data and PII

Protecting user data is a legal requirement and an ethical one; developer choices affect people's finances and safety.

PII covers obvious identifiers (name, national ID number) and less obvious ones (IP address, device ID), plus data that becomes identifying only when combined.

Practices:

- Mark sensitive fields explicitly in the model (an annotation, decorator or metadata tag) so serializers, loggers and exports can mask them automatically.
- Collect only what is needed.

## 5. Encryption at rest

Financial and similar data (cards, bank accounts, tax records) must never be stored in plaintext. Treat encryption as the vault that still protects data after a breach.

- Use AES in an authenticated mode such as GCM, a fresh random IV (nonce) per encryption, and store the IV alongside the ciphertext.
- 128-bit keys are strong for most uses; 256-bit is a common choice for longer-term margin.
- Keys live in a key or secrets manager, never next to the data.
- Minimize how long decrypted values sit in server memory.

## 6. Compliance regimes

Compliance means obeying internal policy plus external law and standards. Daily coding habits: privacy by design, secure coding standards, encryption in transit (HTTPS) and at rest, working deletion and export paths for user data, and documentation of every touchpoint with sensitive data. You do not need to memorize regulations; you need to notice when code handles regulated data and ask for help.

| Regime | Triggers | Developer obligations |
|---|---|---|
| GDPR (EU), CCPA (California) | Personal data of covered users | Explicit consent, right to erasure, data minimization, sound handling and security |
| HIPAA | Any health data, including insurance and fitness tracking | Encrypt in storage and transit, users see only their own records, audit log of who accessed what and when, compliant third parties only, retain no longer than needed |
| PCI DSS | Card data | Never store sensitive authentication data such as CVV, encrypt cardholder data in transit and at rest, strong access control, maintained secure systems |

## 7. SBOM and dependency hygiene

A software bill of materials lists every library, framework and dependency with versions. When a vulnerability is announced in a popular library, the SBOM tells you within minutes whether you are affected. Most build tools generate one automatically.

- Review the SBOM for known vulnerabilities on a fixed cadence (monthly or quarterly) and upgrade.
- Log security actions but never their sensitive payloads; consult the security team when unsure.

## 8. Pitfalls

- Homegrown password hashing or token schemes.
- SMS as the only second factor for high-value accounts.
- Recovery flow that skips MFA.
- Sessions with no absolute timeout.
- Encrypting with a fixed IV or keeping the key in the same database.
- Storing CVV "temporarily".
- Treating compliance as someone else's job until an audit.
