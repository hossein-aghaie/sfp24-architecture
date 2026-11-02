# Phase 3A — company accounts delivery and runbook

**Usability extension, owner-authorized 2026-10-14:** [COMPANY-ADMIN-QUICKSTART.md](../../guides/COMPANY-ADMIN-QUICKSTART.md) supersedes the invitation-only UI, manual per-company provisioning and password-reset-not-implemented limitations in this original delivery record. Add/edit dialogs, no-email sign-in cards, a separate automatic provisioner, personal password change, company resets and bounded provider support are implemented. The owner separately approved a portable loopback-only MariaDB environment; this does not authorize installation or mutation of other databases/services. See `PHASE3-USABILITY-PROGRESS.md` for current local test evidence. The original delivery below remains a historical baseline, including its original CI results.

Working branch: `feat/phase3-company-accounts`. The existing Phase 2 baseline, 16-machine scene, simulator and file data remain independent and unchanged. One independent company = one independent account. Multiple factories within that company are not additional company accounts.

## What this slice contains

- Provider-only metadata listing, account creation, purchased-module/capacity editing and first-admin invitation reissue.
- Separate company administration: own account, module entitlement/readiness, active usage, invite/reissue, role change, disable/reactivate, and dedicated-connection verification.
- Local one-time provider bootstrap, salted scrypt password hashing, hashed expiring single-use invitation tokens, hashed expiring bearer sessions, per-request permission reload and session invalidation.
- Versioned normalized MariaDB control schema; a separately versioned database/credential per company, minimal tenant metadata only. No operational planning/logistics/quality tables or automatic site creation.
- Two-company isolation, least-privilege database and concurrency acceptance suite for disposable CI MariaDB. Without the CI flag the real database suite is deliberately skipped.
- No billing/renewal/concurrent-session pricing, SSO, password reset/email delivery, site/equipment scoped roles, live manufacturing integration or deployment.

## Local UI without a database

```powershell
./scripts/dev.ps1 dev
./scripts/dev.ps1 accounts:api
```

Open `http://127.0.0.1:5174/?accounts=1`. The API listens only at `127.0.0.1:5185`; Vite proxies `/api/v1` there. Missing `PLATFORM_RUNTIME_CONFIG` produces a real **MariaDB not configured** state; registration/sign-in cannot succeed using made-up data. The Phase 2 API remains `127.0.0.1:5184`. Its local credentials cannot authenticate against the new company API.

**No MariaDB installation, Docker/WSL, Windows service change or owner database mutation is authorized by this runbook.** A separately approved isolated local DB is still needed for connected laptop use. Real database testing is delegated to a temporary GitHub Actions service on this branch. Never point the config at ERP/production.

## Setup after an isolated environment is explicitly approved

Keep private files under `.local/phase3` (ignored). Owner-only OS permissions must be applied and verified on Windows before storing database credentials. POSIX file modes used by the vault do not set Windows ACLs. For shared/production environments replace the local vault with a managed secret provider; never commit passwords or expose them in UI, browser storage, arguments or logs.

Provisioner configuration (`PLATFORM_PROVISION_CONFIG` points to a private JSON file):

```text
isolatedEnvironment: true
admin: { host, port, user, password }                  # restricted offline DDL/provisioning credential
controlDatabase: platform_control_test               # approved NEW isolated control DB
runtimeControl: { user: pc_<24 random hex>, password: <random secret> }
tenantHost: { host, port }                            # TLS settings required for nonlocal use
vaultDirectory: D:/git/pouyeshgar-workshop/.local/phase3/tenant-secrets
```

Use real private values, not this descriptive template. It is not executable JSON or a default account. The runtime account must be newly generated; do not reuse a broad existing DB user. On the approved isolated environment:

```powershell
$env:PLATFORM_PROVISION_CONFIG = "$PWD/.local/phase3/provision.json"
pnpm accounts:cli migrate-control
pnpm accounts:cli bootstrap
```

Bootstrap demands a local interactive terminal, prompts username and accepts a hidden password (12–128 characters); no password flags or pipes. Once any provider exists, repeat bootstrap is refused. Record recovery securely; account/password recovery is not implemented.

Runtime JSON referenced by `PLATFORM_RUNTIME_CONFIG` contains **only**:

```text
control: { host, port, database: platform_control_test, user: pc_<24 random hex>, password: <runtime secret> }
tenantHost: { host, port }
vaultDirectory: <same private tenant-secret directory>
```

The HTTP server does not load the provisioner configuration or receive its credential. Clear the provisioner environment variable in the runtime terminal. Keep all cache/TEMP paths inside the repository as established by `scripts/dev.ps1`.

```powershell
$env:PLATFORM_RUNTIME_CONFIG = "$PWD/.local/phase3/runtime.json"
./scripts/dev.ps1 accounts:api
```

1. Sign in as provider. Create a completely fictional company A, choose modules/capacity, record its opaque ID and deliver the one-time invitation securely. Copy the token before dismissing it; token plaintext is not retrievable later.
2. On the **restricted local provisioner terminal**, run `pnpm accounts:cli provision <company-id>`. This creates only a generated `tenant_<opaque-id>` DB and separate `tu_<random>` runtime user, runs tenant migrations, verifies binding, then marks storage ready. The web handler cannot run CREATE DATABASE or GRANT.
3. Activate the invitation through `/?accounts=1`, choose a password, then sign in using company code + user name. No site or equipment is required. Activation depends on storage ready and a remaining active-user seat.
4. Company admin can invite users and change company roles. A role titled finance cannot unlock an unpurchased finance module. `pilot_only` and `planned` catalog statuses block module access in company mode even if selected in a contract. The accounts core is implemented; operating dashboards are still the separately labelled Phase 2 pilot.
5. Repeat with wholly fictional company B. Provider may see both **account metadata** but cannot use their `storage-health` or company user APIs.

Failed provisioning preserves schema/secret/catalog stages and records a non-sensitive audit event; retry the same command. No DROP or automatic credential reset is performed. Missing credentials for already-ready storage require deliberate recovery. Re-run provision to apply later tenant migrations; changed checksums/unknown schema versions fail closed.

## Schema and API map

Control tables: `schema_migrations`, `platform_users`, `company_accounts`, `tenant_storage`, `module_catalog`, `company_module_entitlements`, `company_seat_entitlements`, `company_users`, `roles`, `permissions`, `role_permissions`, `company_user_role_assignments`, `company_invitations`, `auth_sessions`, `control_audit_events`.

Tenant tables: `schema_migrations`, `tenant_metadata` (binding to exactly one company). No giant operational JSON payload. Database identifiers and runtime credentials are private; public responses never include them.

| `/api/v1` path | Access / purpose |
|---|---|
| `GET /health` | Public configuration state only |
| `POST/GET/DELETE /session` | Sign in / validated actor / revoke bearer |
| `POST /activation` | Expiring one-time invitation + new password |
| `GET /provider/catalog` | Provider module metadata |
| `GET/POST /provider/companies` | Provider metadata listing / company creation |
| `GET/PATCH /provider/companies/:id/entitlements` | Provider current contract / change audited capacity and modules |
| `POST /provider/companies/:id/invitations/:userId/reissue` | Provider replacement invitation for an invited first admin |
| `GET /company` | Own account/profile, capacity, permissions |
| `GET /company/modules` | Own licensed/enabled/readiness metadata |
| `GET /company/modules/:key/access` | Real capability gate; no invented operational payload |
| `GET /company/users` | Own administrator's user listing |
| `POST /company/invitations` | Own administrator invites user |
| `POST /company/invitations/:id/reissue` | Replace unconsumed invitation of own invited user |
| `PATCH /company/users/:id` | Own user role/status; last-admin and capacity protection |
| `GET /company/storage-health` | Own admin's real tenant connection/binding probe |

All new endpoints use validated sessions/server-owned account context, strict JSON payloads, no-store responses and parameterized SQL. Scope headers are rejected. Missing company access returns 401/403/404; unconfigured/DB failures produce explicit 503 without leaking SQL or connection strings. Login/activation have process-local IP rate limiting (not distributed enterprise protection).

## Evidence and remaining gates

Local unit/API tests, TypeScript and build are run during development. Actual unconfigured UI and browser fixtures are captured under ignored `.local/qa/phase3/`; screenshots with `fixture-` in their names are intentionally mocked browser responses. The actual unconfigured screenshot is `actual-not-configured-fa-1366.png`. Do not present these as real MariaDB-backed browser onboarding evidence.

The MariaDB CI job provisions a fresh service only for this feature branch; validates repeated migrations, one-time bootstrap, staged recovery, two independent companies/databases, database-level denial, activation/replay/expiry, role/provider denial, capacity race, last admin, immediate revocation, license/readiness and preservation. **Verified on commit `9b1a3a6`: 42 tests passed, zero failed, zero skipped on MariaDB 11.4; TypeScript/build passed.** [Real MariaDB CI](https://github.com/hossein-aghaie/pouyeshgar-workshop/actions/runs/38596701887) and [standard test/build CI](https://github.com/hossein-aghaie/pouyeshgar-workshop/actions/runs/38596701728) both completed successfully. This proves the included API/database scenarios on disposable CI, not production readiness or connected laptop browser onboarding.

Not yet industrial/production validated: connected laptop browser onboarding, Windows vault ACL setup, TLS/reverse-proxy deployment, password recovery, distributed brute-force limits, backup/restore verification, secret rotation, fleet migration monitoring, pool/load/retention testing, support access, whole-company suspension UI, site/equipment RBAC and normalized company production/report endpoints. Future integrations are documented in `DEVELOPER-GUIDE.md`; they are not implemented.

The old Start/Stop commit `4bad5f8` is preserved on the local pilot branch and was not applied to Phase 3. The historical stash and untracked image-reference guide remain untouched. The historical lower-case decisions file was first preserved as `decisions-legacy.md`, then moved intact to `archive/DECISIONS-EARLY-PILOT.md` by owner instruction; `DECISIONS.md` is the sole canonical decision-register path. Its original Git blob/history and verification commands are recorded in `archive/README.md`.

## Synchronization completed after explicit owner authorization

The earlier hold was lifted by the owner. Remote documentation commit `0a2fe68` and all four local implementation commits were preserved by same-branch merge `9b1a3a6`, followed by local test/build and normal Push. No Force Push, cross-branch merge, stash mutation, server change or deployment occurred. The historical archive remains content-identical to its original Git blob.

Local verification: **33 tests passed, zero failed, one real-MariaDB suite deliberately skipped; TypeScript and Vite build passed**. The real MariaDB suite subsequently ran without skips in CI as recorded above. `PHASE3-LOCAL-VERIFICATION.md` retains the archive integrity proof and the earlier synchronization plan as history.
