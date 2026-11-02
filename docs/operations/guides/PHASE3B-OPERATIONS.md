# Phase 3B — company production workflow (P0 + first CSV adapter)

> نسخهٔ راهنمای موضوعی؛ کد مبنا b3f203b، بازبینی انتقال ۲۰۲۶-۱۱-۰۲. متن اولیه در [کاتالوگ منابع](../../sources/CATALOG.md) محفوظ است. دستورها برای مخزن محصول و محیط مشخص همان نسخه‌اند؛ خود مخزن اسناد اجرا نمی‌شود.


## First P1 adapter — parts CSV v1 (2026-10-15)

In **Master data → Parts and products**, authorized users can **Import CSV** or **Export CSV**. Download the header template, upload UTF-8 CSV (up to 500 rows / 200 KB), choose comma/semicolon/tab, map code/name/unit, validate and review row/field errors, then explicitly confirm. Imports create new active parts only: no existing part is updated or deleted. Preview saves only a staging batch, not catalog records. Same file/mapping replay returns the original result. Existing/duplicate codes are rejected; if the catalog changes before confirmation, the whole batch rolls back. Validate again for fresh errors; confirmation expires after 30 minutes. Export includes inactive status and neutralizes spreadsheet-formula prefixes. XLSX and report-data imports are not implemented.

`server/integrations/adapters/csv.ts` handles bounded parse/escaping independently of `server/operations/master/parts-import.ts` (mapping, validation, batch lifecycle and shared MasterService writes). Tenant **forward migration 4** adds `import_batches`: actor-bound source hash, canonical preview, errors, expiry and original committed result. Only its creator with current import + master-write permission may confirm. Cross-tenant batch IDs are denied. No file can select database, company, SQL or URL.

API `/api/v1`: `POST /company/imports/parts/inspect` with `{content,delimiter}`; `POST .../preview` additionally takes `mapping:{code,name,unit}`; `POST .../:id/confirm` with `{}`; `GET /company/exports/parts` returns filename/content/MIME for a real download. Import requires company-wide `data.import` + `master.manage`; export requires `data.export` plus authorized master reads. `scripts/phase3b-csv-qa.mjs` tested real browser download/upload, Persian column mapping, invalid/valid preview, confirmation/replay and actual export in desktop/mobile. Full isolated MariaDB suite reached **68 passed, zero skips**, with preview isolation, concurrent replay, expiry renewal, atomic rollback and formula escaping. Backup + tenant v4 upgrade also completed on the approved laptop test DBs; existing credentials and Phase 2 data preserved.

Owner-authorized scope: pasted operational mission of 2026-10-14, implemented on `feat/phase3-company-accounts`. This document supersedes earlier statements that individual permissions and tenant operational reports do not exist. Historical Phase 2 / Phase 3A evidence remains intact.

## Usable workflow / مسیر استفاده

1. Open `http://127.0.0.1:5176/company/pouyeshgar-test/login` and use your existing company administrator credentials. Passwords were not reset. Provider entry remains `/owner/login` and never grants access to tenant production.
2. In **اطلاعات پایه / Master data**, add a site/workshop and an equipment, production line or station. A physical hall is optional and distinct from an operational line. Add parts/units and optional OPs, people, shifts, calendar days and scrap reasons as needed. A new company starts empty; no fake workshop is created.
3. In **کاربران و دسترسی‌ها / Users and permissions**, add a login and privately deliver its one-time card. Open **Permissions** to apply the operator preset or edit actions and company/site/area/resource scopes. A viewer template may have full independently delegated authority; a person's job title grants nothing. Link the login to an optional people record.
4. The operator signs in through the company's own link. **ثبت تولید / Enter production** supports multiple rows, optional shift/person/OP, editable report period and optional row periods. For example, good **120**, final scrap **3**, Other explanation and reason quantity **3** gives processed **123**. Missing quantities stay blank; a valid zero remains zero. Duplicate row clears counts/reasons.
5. Save a draft and resume it in **سوابق تولید / Production records**, including after a new login. Submit when complete. A user without catalog-write permission can use a temporary part name, without creating an official part. Authorized users can create a part directly in the form.
6. Final reports require **production.correct** plus a reason to change. Previous/current values and actor/version remain in revision history. Other readers can request correction; no compulsory approval workflow was added. Disabling a master record preserves historical report snapshots.
7. **گزارش تولید / Production summary** queries submitted records in the same tenant DB. Date/site/area/resource/part/OP/shift and authorized-person filters affect actual SQL results. A cohort is resource + part/proposed name + OP + unit. Good, final scrap, processed, daily chart and scrap reasons belong to that cohort. Sequential OP counts are never a finished-goods total.

Shift presets can cross midnight; start/end dates remain explicit and editable. Breaks and work calendar are configuration, not inferred attendance or machine productive time. Daily analysis uses **report date**, not a fabricated hourly distribution. This slice computes no OEE, efficiency, targets, machine rate or live equipment state from manual counts.

## Current implementation

| Boundary | Responsibility |
|---|---|
| `server/platform/identity/permission-catalog.ts` | Extendable action registry and initial templates |
| `src/company/access-policy.ts` | Pure shared scope evaluation; server reloads current grants per request |
| `server/platform/identity/access.ts` | Safe per-user rules, reauthentication, last-effective-manager protection, session revocation and audit |
| `server/operations/master/` | Shared typed sites, areas, resources, parts, OP, people, shifts/calendar and scrap-reason service |
| `server/operations/production/` | Validation, idempotent drafts, optimistic versions, finalization/corrections, scope-filtered reads and cohort summaries |
| `server/operations/http.ts` | Versioned Fastify adapter; no provisioning credentials or browser-selected database |
| `server/platform/storage/tenant-storage.ts` | Authenticated company → private mapping/vault → bound tenant DB; shared opening pool for concurrent requests |
| `src/company/` | Bounded Vue components using those APIs, FA/EN, mobile forms and real ECharts summaries |

Control migration **4** adds `company_user_permission_rules`. Tenant migration **2** adds `sites`, `areas`, `resources`, `resource_members`, `parts`, `operations`, `people`, `shifts`, `calendar_days`, `scrap_reasons`, `production_reports`, `production_lines`, `production_scrap`, `report_revisions`, `correction_requests` and `tenant_audit_events`. Tenant migration **3** adds request fingerprints, historical area scope and nullable draft quantities. Resource membership table is reserved; no line-composition editor or line aggregation has been implemented.

Migrations are ordered, checksummed and repeatable. Never edit an applied migration. Runtime credentials have only specific table CRUD; the separate offline provisioner owns schema changes. Back up first, initialize/migrate control with the existing private config, then rerun provision for each trusted tenant catalog entry using its existing vault credential. Do not run bootstrap again, copy operational data between companies, or give DDL rights to the API. The approved laptop environment was privately backed up (control + five existing tenant DBs) before these additive migrations.

### HTTP contracts (`/api/v1`)

- `GET /company/operations/context`, `GET /company/readiness`: authorized selectors and five distinct readiness axes (implementation, license, permission, prerequisites, data).
- `GET/POST /company/master/:kind`, `PUT /company/master/:kind/:id`: whitelist typed fields, active flag and expected version. No hard delete endpoint.
- `GET /company/access-scopes`, `GET/PUT /company/users/:id/access`: catalog/templates/direct rules. Save requires the acting administrator's current password; changes revoke target sessions. Provider counterpart requires the existing temporary, reasoned support grant and only accepts company-wide edits; operational scope names stay with the company.
- `POST /company/production/reports` with `{input}`: creates a draft with a client key and payload fingerprint. Same key/payload returns the original record; changed payload conflicts.
- `GET/PUT /company/production/reports/:id`: authorized detail / `{input,version,reason?}` update.
- `POST .../:id/submit` with `{version}`, `POST .../:id/correction-requests` with `{reason}`, `GET .../:id/history`.
- `GET /company/production/reports` and `/company/production/summary`: `from`, `to` (inclusive Gregorian report dates), `site`, `area`, `resource`, `part`, `operation`, `person`, `shift`, `status`. Person filtering has its own action and scope. Summary uses only submitted rows. Revision values need correction permission; ordinary readers see revision metadata.

Types for manual reports are in `src/company/contracts.ts`. Internal consumers call services, not loopback HTTP or copies of SQL/validation. A direct rule replaces the template only for that action; matching explicit deny wins. The server validates same-tenant scope IDs. Multiple company-wide user managers are allowed within active-login capacity; the last effective active manager is protected independently of role title. People without logins do not consume login seats. No pricing or concurrent-user business rule was invented.

## Evidence and repeatable checks

- Local full suite: `PHASE3_MARIADB_TEST=isolated-local`, `PHASE3_LOCAL_CONFIG=<private provision config>`, then `./scripts/dev.ps1 test`. Latest verified suite before final delivery: **68 passed, no skips**; final commit CI links are recorded in the delivery report.
- `./scripts/dev.ps1 typecheck` and `./scripts/dev.ps1 build`.
- Connected Chromium `scripts/phase3b-operations-qa.mjs`: real isolated MariaDB API at 5187, fictional company, UI master data/scoped permissions, overnight shift, 390px capture, 120+3, multirow draft/resume/final, correction/history, date-filter change, quick part/soft disable and RTL/tablet. Requires explicit fixture opt-in and private fixture-owner login file. It never uses the owner's real login.
- Stop/restart **that disposable API**, resume its same private config, then `scripts/phase3b-chart-qa.mjs`: fresh browser login, persisted report/revision, five stored days, hover, interactive series, actual ECharts data zoom/reset and responsive RTL chart.
- `scripts/phase3-admin-qa.mjs`: existing company creation/edit, private activation/reset, password change, suspension and provider support regression, adapted to the new users navigation.
- `scripts/phase3b-pilot-regression.ts`: original Phase 2 Immersive/Explore/Analytics at 1366 and 1920, no document overflow, actual canvas raycasting and camera zoom, using a fresh in-memory simulator API on 5188 that is closed afterwards. It never changes the owner's stored Phase 2 data. Company summary also has first-viewport/document-height assertions in the chart QA.
- Credentials, database dumps, fixture config and screenshots are ignored under `.local`. Screenshots: `.local/qa/phase3b`, `.local/qa/phase3-usability`; share only deliberately reviewed images. No secrets or local DB data belong in Git.

The Portable MariaDB instance has a **32-connection local test cap**. Run full DB integration tests separately from disposable browser-fixture API tests; a parallel run hit that cap and was rerun successfully after stopping only the fixture. No MariaDB service setting was changed.

## Honest remaining scope

**P1 remaining:** XLSX/other entity import-export, persisted dashboard-builder settings and controlled linkage of tenant data to the existing Phase 2 scene/dashboards. The first **parts CSV** adapter is delivered above. Daily production analysis here is real; Phase 2's 16-device scene/simulator remains separate and unchanged. No unlicensed/unimplemented module menu pretends to work. The company-settings permission key reserves a future guard; it does not imply a dashboard builder exists.

**Other limits:** record list is limited to 200 matching recent headers, master selectors to 2,000 entries; narrow date ranges for older reports. No large-data/load or independent security assessment, production TLS/MFA/secret-manager deployment, provider recovery workflow, audit-browser module, backup restore drill, automatic draft autosave/offline sync or Jalali date-input widget is claimed. Dates are explicitly Gregorian for data entry; site's timezone accompanies periods. Historical reports retain snapshots, but references to disabled master records must be reselected if creating/editing operational input. Provider cannot read tenant production. Production statistics/reports readiness refers to this supported manual P0 slice, not every future product capability.

## P2 adapter contracts — design only

Future protocol adapters live under `server/integrations/adapters/<protocol>/` and invoke the same authorized domain services. They must not choose tenant from an untrusted payload or write directly to report tables.

- **Device HTTP polling (about one minute, configurable):** explicitly approved device endpoint/authentication and protocol/version; trusted company/resource binding; message ID or counter epoch + sequence for idempotency; event time/timezone and received time; cumulative-vs-interval semantics; counter rollover/reset and late/out-of-order handling; OP/part/unit mapping; disconnect/freshness status. Raw cumulative increments cannot silently become good/scrap, machine runtime or OEE. Define reconciliation with manual counts before mixing sources. No IP was contacted.
- **CSV/Excel extension:** parts CSV v1 above implements this boundary. Future XLSX/other entity adapters must retain versioned templates, explicit mapping, bounded parse, validation, preview without catalog writes, confirmation transaction, idempotent provenance and error reports. Export queries authorized services first and escapes spreadsheet formulas. ERP, REST and read-only external DB adapters reuse this boundary; no arbitrary SQL, credentials or URL supplied by a row.
- **Attendance/time clock:** separate future domain. Bind external card/person IDs inside one company; store device/event IDs, event/receive times, configurable polling cadence, late/missing/duplicate events and overnight shift rules. Never infer attendance from report duration or machine powered-on time. Missing SDK/API authorization exposes not-configured state; no decorative menu.
- Planning, costing, inventory and prediction remain independently licensed future modules. Add a service/guard, same versioned tenant schema, API adapter and tests; do not redesign company accounts or fork a customer-specific schema.
