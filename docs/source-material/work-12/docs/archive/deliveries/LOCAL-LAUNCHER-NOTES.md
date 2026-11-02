# Local laptop launcher — developer and support notes

## Subsequent owner-authorized development credentials

`Set-Dev-Logins.cmd` is a separate, explicit utility added after the launcher delivery. It applies only to the already active provider and admin/operator pairs in the two named manual demo companies in the independent `platform_sources_browser_<12hex>` control database. It refuses production mode, other DB prefixes/host/port/actual datadir, other checkout, missing explicit flags, inactive/conflicting/unexpected identities and concurrent reset attempts. It does not run on Start-All and does not reset database/device secrets. Normal passwordHash validation in the application stays12–128; only the fixed public fixture identities are encoded with the same salted scrypt-v1 protocol by the isolated development tool. No generic weak-password flag/API is introduced.

Before mutation the tool takes a private hash/identity backup; updates preserve IDs/roles/capacity, increment credential versions, revoke sessions, consume stale invitations and append a secret-free audit event in one transaction. Private local login references are refreshed after commit; a post-commit file failure is reported distinctly. Existing QA-company logins and owner environments are not renamed. Unit/security, actual MariaDB and browser evidence are described in CURRENT-STATE. The fixed values are public fictional development fixtures, not production secrets. Replace these accounts/passwords through normal account management before any real deployment.

Owner request2026-10-16: write a complete human Persian manual and complete launch scripts, but **do not run the actual services**; owner will execute personally. Work stays on `feat/industrial-data-hub-neway` in the independent worktree. No UI/business/permission/password policy change, no merge/deployment and no owner/stash edits.

User entry is `Read-Guide.cmd` → [LOCAL-USER-GUIDE-FA.html](../../LOCAL-USER-GUIDE-FA.html). Root CMD wrappers invoke `tools/local-demo/Manage.ps1` in Check, Start, Status or Stop mode. The default PowerShell action is Check. Script messages are short ASCII English for reliable Windows PowerShell5.1 display; the Persian manual explains READY/NOT READY/port conflicts and all service names.

## Scope and existing setup

This is an **existing-laptop launcher**, not an installer. It requires the pre-existing independent `.local/data-sources/private/state.json`, Node runtime reference, existing vault/encryption key, simulator API config, dependencies and approved Portable MariaDB11.4 at the existing `.local/phase3` location. Missing files or unknown identities fail closed; no download, install, bootstrap, seed or blanket upgrade of ready databases runs. The worker does create/migrate storage for explicitly queued company-provisioning requests, including pending requests from before shutdown. The source fixture's control database must match `platform_sources_browser_<12hex>` and host/port must be127.0.0.1:3317. The old5176/5196 environments are not started or stopped.

Start validates the approved MariaDB path/bind/port and the existing process record if already listening. If stopped, it starts only that approved Portable binary/INI and records the process in the already-used `database-process.json` format. It does not change the INI or database files itself. A separate short Node probe reads actual `@@datadir` and existing control tables; it performs no DDL. This shared database is **never stopped by Stop-All**, even if this launcher started it, to protect other local environments. Windows shutdown naturally stops it.

Private runtime copies/logs go under ignored `.local/local-launcher/private`, ACL-restricted to the current Windows account/System/Admins before writing. The HTTP config contains runtime credentials only. The elevated provisioning config is delivered only to the probe/worker processes; it is not passed to the HTTP process. Existing secrets are reused and never printed, reset or generated on startup. Source encryption-key absence fails rather than silently rotating it. No credentials are in tracked files or public URLs.

## Service contracts

| Component | Entry | Responsibility |
|---|---|---|
| api5207 | `service-host.ts --service api` | Existing `buildAccountsServer`, runtime DB and `TenantStorage`; no fixture creation or control migration |
| worker | `service-host.ts --service worker` | Existing `runWorker`; prepares queued newly created companies using the approved independent control DB |
| demo5198 | `service-host.ts --service demo` | Existing `buildServer` with fresh memory-only `fileStore()` and anonymous demo access; never uses owner pilot storage |
| web5206 | `vite.config.ts` | Existing Vue app, original Phase2 scene; `/api/v1`→5207, `/api`→5198; private files denied |
| api-simulator5208 | existing `tools/edgebox-simulator/index.mjs serve` | Existing fictional authenticated REST feed; pre-existing enabled REST sources may poll it |
| edgebox5210 | existing `console.mjs` | Independent simulator UI with persisted queue/config; automatic sends remain paused on restart |

The old CLI review sender is **not** auto-started. The GUI simulator is the sender that the user configures/starts manually. Existing simulator API and GUI logic are not copied into new implementations.

Manage checks ports before starting anything, serializes Start/Stop with an exclusive file lock and reuses only matching managed processes. Ownership requires PID, creation time, exact quoted entry, service marker and full command fingerprint. A foreign process/old launcher's listener is not adopted or killed. On partial startup failure already-started processes are left identifiable for Status/Stop rather than destructively rolling back data. Stop walks only matching owned processes in reverse order; it never deletes records, DBs, queues or private files. Windows Stop-Process closes Node processes; the user is instructed to save forms and let provisioning finish first.

Readiness requires expected process/port ownership, HTTP200 from API/UI/console, actual DB identity/control-table probe and recent worker heartbeat. A port check alone is not advertised as full readiness. Check only reads files/process/port metadata and runs Node `--version`; it does not connect to MariaDB or start any listener.

## Validation and explicit remaining gap

- PowerShell parser and eight mock ownership cases passed: correct identity, missing process, different PID, reused PID, wrong service, changed command, similarly named path and different checkout. `Test-Launcher.ps1` never launches a service. A Windows-only Node test wraps it; other OSes skip this Windows-specific check.
- A separate short Node `--import tsx` PID test passed without an application/listener. Long-lived services use the direct loader, not the spawning tsx CLI, so port ownership and Stop refer to the actual service PID. Check/Status remain read-only; temp/compile caches for started services stay under the local workspace.
- `tsc --noEmit -p tools/local-demo/tsconfig.json` passed. The normal app typecheck/build are checked separately; they do not execute launch actions.
- Actual `Manage.ps1 -Action Check` passed on the owner's existing files while MariaDB was stopped. It reported no service start, DB connection, migration or password change.
- The static Persian guide passed desktop1366/mobile390 rendering, RTL, anchor and overflow checks with zero JavaScript errors. Only the local file was opened in a headless browser, with HTTP requests blocked; product services were not contacted. Screenshots/results are ignored under .local/qa/local-guide. The guide contains no JavaScript/CDN/secret.
- **Not executed:** Start/Stop actions, actual DB probe, worker heartbeat/readiness, newly created-company provisioning via this launcher, restart persistence and port-conflict execution against live processes. Owner explicitly reserved these steps. Prior product browser/MariaDB/CI success does not replace this pending cold-start acceptance.

First manual run: Check-Setup → Start-All → wait READY → create a fictional company and activate its admin → enter a report → Stop-All → Start-All and verify persistence. If any step fails, capture the exact message/Status-All output, then inspect only the corresponding private log without publishing config/keys. Do not run older launchers in parallel on the same ports, reset passwords or bootstrap another environment to work around a failure.
