## Contents

1. Principle
2. What varies per environment
3. Choosing a mechanism
4. Feature flags
5. Secrets handling
6. Review checklist
7. Pitfalls

# Environment configuration, feature flags and secrets

## 1. Principle

Configuration deserves the same care as code, but unlike code it legitimately differs per environment. Anything bound to one environment (a localhost database URL, a sandbox key, a debug log level) must be injected from outside rather than written into source. The anti-pattern to flag in review is a class or module with literal connection strings or credentials; the fix is to receive them through a configuration object or loader.

```python
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class DbSettings:
    url: str
    user: str
    password: str

def load_db_settings(env=os.environ) -> DbSettings:
    missing = [k for k in ("DB_URL", "DB_USER", "DB_PASSWORD") if not env.get(k)]
    if missing:
        raise RuntimeError(f"missing config: {', '.join(missing)}")  # fail fast at startup
    return DbSettings(env["DB_URL"], env["DB_USER"], env["DB_PASSWORD"])
```

## 2. What varies per environment

Use this as an inventory when asking "what changes between my laptop and the next stage?":

- log levels and destinations
- URLs of downstream services and APIs
- database connection details and pool sizes
- cache settings
- email or notification providers
- security settings (TLS, CORS origins, auth providers)
- feature flags and behavior switches

## 3. Choosing a mechanism

| Need | Mechanism | Why |
|---|---|---|
| Non-sensitive settings that differ by stage | One readable config file per environment (base plus per-environment override) | Easy to review, diff and version |
| Values that are sensitive or rotate | Placeholders in the file resolved from environment variables, or a secrets manager | Keeps secrets out of version control; rotating a key does not require a redeploy |
| Behavior that must change at runtime | Feature flags | Toggle without shipping code |
| Credentials for production | Dedicated secrets manager | Encryption, access control, rotation, audit |

Two reasons the chapter gives for moving sensitive values out of per-environment files: those files get committed, exposing the secret, and scheduled key rotation would otherwise force a full redeploy.

Configuration management is also a deployment concern: promoting a build from one stage to the next means knowing and supplying exactly what differs for the target stage.

## 4. Feature flags

A feature flag (toggle) switches a capability on or off at runtime with no new deployment.

Benefits:

- Ship dark: code reaches production hidden, separating code deployment from feature release.
- Gradual exposure to chosen user groups before everyone.
- A/B comparisons of alternative experiences.
- Instant rollback of a feature by turning it off.

Three types and when to use each:

| Type | Purpose | Expected lifespan |
|---|---|---|
| Release | Hide unfinished work so the main branch stays deployable | Short; remove once fully launched |
| Experiment | Compare experiences and collect behavior data | Duration of the experiment |
| Permission | Gate features by role or subscription tier | Long; part of the product model |

Hygiene rules:

- At creation, record purpose, owner, type and an expiry date.
- Run a recurring cleanup on a cadence the team agrees.
- Do not let temporary flags quietly become permanent; dead branches of logic accumulate complexity.
- Practice habit: before deploying, know how you would switch the feature off.

The script `scripts/audit_feature_flags.py` applies these rules to a flag registry file.

## 5. Secrets handling

Secrets are configuration values such as API keys, passwords and tokens that need special treatment.

1. **Never in code or version control.** A leaked commit costs money and trust, and removing it means rewriting Git history; it also makes sharing the codebase with outside parties risky.
2. **Use a secrets manager** (for example AWS Secrets Manager, HashiCorp Vault, Azure Key Vault) for encrypted storage and access control.
3. **Rotate routinely**, ideally automated by the manager, to shrink the exposure window of any compromise.
4. **Least privilege**: only people who truly need production secrets can read them, behind proper authentication and authorization.
5. **Separate per environment**: development, staging and production never share credentials, so a dev or test mistake cannot touch production.

The script `scripts/scan_config_risks.py` flags literal secrets, localhost endpoints, plain HTTP URLs and outdated TLS settings in a repository.

## 6. Review checklist

- [ ] No environment-specific literals in source.
- [ ] Every setting that differs by stage is listed and supplied for the target stage.
- [ ] Sensitive values come from environment variables or a secrets manager, never a committed file.
- [ ] App fails fast with a clear message when required config is missing.
- [ ] Each flag has type, owner, purpose and expiry; expired release flags are scheduled for removal.
- [ ] Production credentials are unique to production and access is restricted.

## 7. Pitfalls

- A per-environment YAML file with real production passwords checked in.
- Reusing a staging API key in production "temporarily".
- Flags with no owner that nobody dares remove.
- Debug-level logging left on in production config.
- Rotating a secret that is baked into the build artifact, forcing an emergency redeploy.
