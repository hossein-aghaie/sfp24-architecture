# RUNBOOK — canonical entry, Phase 2 local demo

**Current independent laptop source branch (2026-10-16):** for the owner's day-to-day start/stop and four browser entries use [the Persian user manual](../../LOCAL-USER-GUIDE-FA.html), opened with root `Read-Guide.cmd`. Root `Check-Setup/Start-All/Status-All/Stop-All.cmd` operate the existing independent5206/5207 environment with the shared approved Portable MariaDB3317; they do not start the older5176/5196 stacks. Start-All also supplies the company provisioner and the memory-only Phase2 demo backend. Stop-All leaves the shared database running. No bootstrap/installation or blanket upgrade of ready databases runs on startup; the worker does create/migrate storage for explicitly queued company-provisioning requests. Full cold-start execution has deliberately NOT been performed: the owner requested to run it personally. Read [LOCAL-LAUNCHER-NOTES.md](../deliveries/LOCAL-LAUNCHER-NOTES.md) for tested checks and exact boundaries. Older launch paths below are historical/current for their respective older environments, not the preferred new-branch entry.

**Unified company entry (2026-10-15):** the approved laptop login `http://127.0.0.1:5176/company/pouyeshgar-test/login` now opens the Phase 2 shell with authenticated company data. Tenant schema v5 is required. A private backup was taken before the additive upgrade of the five existing laptop test databases; existing passwords/records and the separate Phase 2 store were preserved. Read [UNIFIED-SHELL-DELIVERY.md](../deliveries/UNIFIED-SHELL-DELIVERY.md) for setup/manual checks. `/` still opens the labelled simulator demo and does not inherit a company token. Use existing local launchers; do not bootstrap/reset existing owner credentials.

**Phase 3B manual operations:** use the same approved Portable test launcher and existing company login at `http://127.0.0.1:5176/company/pouyeshgar-test/login`; see [PHASE3B-OPERATIONS.md](../../guides/PHASE3B-OPERATIONS.md). Do not seed Phase 2 simulator records into company DBs. Control v4 / tenant v4 require an offline, backed-up additive upgrade; no bootstrap/reset on existing accounts. Full DB tests and disposable browser QA should run sequentially under the laptop's 32-connection test limit.

**Phase 3A accounts:** [COMPANY-ADMIN-QUICKSTART.md](../../guides/COMPANY-ADMIN-QUICKSTART.md) describes the approved isolated laptop environment, simple account/user administration, automatic provisioning worker and password recovery. Its real MariaDB tests concern the normalized company-account control plane, **not** the experimental Phase 2 JSON adapter discussed below.
**Baseline:** `feat/smart-factory-pilot-next` commit `e19016d`, package `0.6.0-pilot`.
This file points to verified detailed commands; it is not a claim that a real hardware or MariaDB deployment was tested.

## Startup on owner's development PC
Work under `D:\git\pouyeshgar-workshop`; do not modify working servers or Raspberry Pi. Install Node >=22.12 and pnpm per [PILOT-RUNBOOK.md](../research/PILOT-RUNBOOK.md). Set temporary/cache paths inside `.local` using that document. Start separate PowerShell terminals:

```powershell
./scripts/dev.ps1 api
./scripts/dev.ps1 dev
./scripts/dev.ps1 simulate:industrial
```

Web `http://127.0.0.1:5174`; Fastify API `http://127.0.0.1:5184`; **both loopback only**. For continuous *demo* industrial reseeding, `pnpm run simulate:industrial --watch` (15-minute scenario cadence). The other `pnpm simulate --watch` is a different **one-minute demo ingestion** script; do not confuse them. See [PHASE2-DELIVERY.md](../deliveries/PHASE2-DELIVERY.md) for seed semantics.

Pilot credentials in ignored `.local/pilot-login.json`; do not copy into commits, logs, screenshots or shared docs. Local state `.local/pilot-state.json`. The simulator is NOT connected to a real Edge/ERP system.

## Validation
```powershell
pnpm test
pnpm build
pnpm run qa:phase2
```
The browser QA requires the local services, browser and fixture as specified in the full Phase 2 runbook. GitHub Actions at [38559243397](https://github.com/hossein-aghaie/pouyeshgar-workshop/actions/runs/38559243397) passed **26/26 tests + build/typecheck** on `e19016d`; this is not live DB test.

## MariaDB **EXPERIMENTAL, NOT PROVEN**
Adapter and migration exist: inspect `server/migrate.ts` and `server/store.ts`. They store a JSON state payload in one `pilot_state` row. Do not point this at existing ERP or production databases. Provision isolated DB and least-privilege user only after owner approval, then independently test migration, rollback and persistence; no blind reconfiguration.

## Baseline & recovery
Branch `feat/smart-factory-pilot-next` exists in GitHub at `e19016d`. The documentation consolidation has been integrated into the pilot development branch; it is **not** an application release. Historical stash `codex-pilot-before-review` on owner's PC must not be dropped or auto-applied. Never auto-merge `main`/`next`, create release, deploy or delete historical QA/docs without owner's request.
