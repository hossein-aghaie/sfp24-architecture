# Developer guide — Phase 3A modular monolith

## Source-layer extension

Current count transport, production consumer, UI components, migration7, server configuration and future adapter rules are documented together in [PRODUCTION-DATA-SOURCES.md](guides/PRODUCTION-DATA-SOURCES.md). Extend those boundaries without copying account/resource/part logic or allowing transport adapters to write operational reports. Original Phase2 geometry and tenant shell remain shared.

## Product integration update — 2026-10-15

Company sessions now render the same `src/App.vue` as the Phase 2 product. `src/company/tenant-shell.ts` provides licensed/authorized navigation and authenticated context; `useFactory(company=true)` prevents demo data/layout initialization. Reusable company forms live inside the original sidebar pages. `TenantMetrics.vue` is shared content inside the original Analytics/Explore/Device components, not a new application shell; it preserves operation cohorts and uses the existing ECharts/KpiGauge/SceneView components. Do not route customer users back to the superseded CompanyWorkspace home.

Scene API: `GET/PUT /api/v1/company/scene`; `PUT {version,layout}` accepts validated version-1/metre layout JSON using existing operational area/site/resource IDs. `SceneService` and `TenantStorage` determine tenant identity; browser company IDs/database names are never trusted. Geometry edits require company-wide master management without scoped denies, check versions and all referenced locations/resources, then audit before/after. Scoped users can read only their authenticated context. Extend via forward migrations; never edit applied tenant v1–v5 checksums. Company UI preferences use company/user-specific local keys; operational geometry and counts stay in MariaDB. Day filters use report date; `start/end` UTC filters include entire report intervals, without proportional counts.

This is one application with bounded services, not microservices or a plugin engine. Account entry paths are `/owner/login` and `/company/login` (or `/company/<code>/login`); the legacy `/?accounts=1` normalizes to the appropriate entry. API remains `/api/v1`, default port 5185 (approved laptop override 5186). Phase 2 remains `/`, `/api`, port 5184 and its existing simulator/file store. Never send a company bearer token to pilot endpoints or expose the pilot as a customer operational API. No automatic conversion of `.local/pilot-state.json` has happened.

## Ownership

| Path | Responsibility |
|---|---|
| `server/platform/accounts/service.ts` | Account lifecycle, identity/session checks, invitations, users, contractual capacity and entitlements; authorized service entry points |
| `server/platform/security.ts` | Password KDF, random tokens/hashing, input bounds and login rate windows |
| `server/platform/identity/credentials.ts`, `audit.ts` | Personal password changes, one-time recovery, session-bound provider support authorization and redacted audit writes |
| `server/platform/catalog.ts` | Versioned shipped module readiness and initial role templates; no billing rules |
| `server/platform/http.ts` | Fastify `/api/v1` adapter, strict payload validation, bearer extraction, error mapping; no provisioning credentials |
| `server/platform/storage/tenant-storage.ts` | Trusted actor → private storage catalog → tenant runtime credential → scoped connection; separately callable CLI provisioning worker |
| `server/platform/storage/provisioning-worker.ts` | Local privileged queue consumer; invokes the existing provisioner without passing DDL credentials to HTTP |
| `server/platform/db.ts`, `migrations.ts` | Transaction boundary, SQL connections, identifier allowlist, ordered checksummed migrations |
| `server/platform/config.ts`, `cli.ts` | Private configuration/vault ports, offline control migration and one-time bootstrap/provisioning commands |
| `src/accounts/` | Provider metadata/contract forms and separate company user administration; FA/EN, no persistent browser bearer storage |
| `src/pilot/`, `server/app.ts`, `server/store.ts`, `src/phase2/` | Existing Phase 2 industrial demo contracts, scene, reporting and simulator; not yet company-scoped operational services |

## Phase 3B operational seams

First file adapter is now implemented: `server/integrations/adapters/csv.ts` parses/serializes without domain writes; `server/operations/master/parts-import.ts` stages typed rows, revalidates permission/uniqueness and confirms atomically through MasterService. Tenant v4 adds actor-bound replay/expiry state. Its tested template/mapping/preview/error/confirm/export contract is the extension point for later formats; older examples below describing every connector as unimplemented are historical. No generic plugin system, ERP or hardware adapter was added.

`server/operations/master` is now the reusable typed master-data service; `server/operations/production` owns manual report validation, draft/version/idempotency, finalization, correction snapshots and authorized cohort summaries. `server/operations/http.ts` is their Fastify adapter; `src/company` contains bounded UI components. Shared pure scope evaluation lives in `src/company/access-policy.ts`, while server-side identity/access services reload grants and enforce same-tenant IDs. No UI-only permission filtering substitutes for a guard. See [PHASE3B-OPERATIONS.md](guides/PHASE3B-OPERATIONS.md) for exact API/schema and nonimplemented P1/P2 contracts; references to these services as future work below are historical. Call services rather than duplicating master validation or cross-module SQL. Add future fields with forward migrations shared by all tenants, not a per-customer fork.

## Rules at the seams

One independent company is one account/security boundary. Site, hall and factory are future physical resources within its operational DB. Company IDs in browser fields, headers or unverified tokens must never choose a connection. `authenticate` reloads active membership and permissions for every request; `TenantStorage.metadata` also checks account/storage status and validates the stored company binding. Provider authority covers contract metadata and explicitly reauthorized, audited company-user support; it is denied tenant operational data. Support grants bind the provider session, actor, company and expiry; never impersonate a company actor to bypass this boundary.

Use `AccountsService` methods through typed in-process calls for internal administration. Modules should consume future shared **equipment**, **people**, **parts** and **calendar** services once those domains are extracted from the pilot; do not copy those rules into costing or planning. Do not prematurely move/rewrite the tested Phase 2 code to simulate that this extraction is complete.

Account mutations lock the company row before seat/admin decisions. Activation, reactivation and licensed-capacity changes use that same lock. Pending invitations do not reserve seats. Only active human logins count, including first administrator; this is **provisional active-humans-v1**, not final pricing. Reducing capacity below current usage is rejected without deleting users. The last active company administrator is protected.

DDL has separate commits. Company creation records `pending_storage`; restricted CLI provisioning records `pending/provisioning/failed/ready`. Only verified tenant credentials + matching metadata permit `pending_admin`; first activation makes the company `active`. A failed stage preserves its catalog, schema and secret reference and can be resumed. No destructive automatic compensation or DROP is used. An already-ready database can be migrated again through the same CLI.

## Adding one module: illustrative future `costing`

1. Define its domain service, actual prerequisites, actions and data-readiness outcomes before declaring anything ready. A costing calculation must consume authorized production/material/labour inputs; a title alone cannot supply those data.
2. Add an additive catalog migration/seed entry for `costing`, initially `planned`, and explicit permission(s) such as `module.costing.read`. Do not change account/user schema or manufacture an entitlement for existing companies.
3. Add a bounded folder `server/modules/costing/` when implementation is authorized. Its service takes a validated company actor and uses scoped shared services/storage. Internal callers use typed services, not loopback HTTP or arbitrary cross-module SQL.
4. Add versioned migrations to every tenant's **same** schema. Do not create customer-specific columns. Apply/resume offline using the migration runner, and reject checksum drift. Use a forward corrective migration rather than editing an applied version.
5. Add strict `/api/v1` routes; require active membership + purchased/enabled module + action grant + resource ownership before queries. Set module readiness `ready` only after all supported flows are tested; `pilot_only` does not authorize use of the Phase 2 endpoints.
6. Test licensed vs unlicensed, disabled module with preserved data, denied role, A↔B IDs, concurrent writes, migrations and UI. Then enable a provider-selected contract and add applicable company navigation.

`module_catalog` is separate from `company_module_entitlements`. Adding/deprecating a module never deletes tenant history. Removing a shipped permission requires an explicit catalog/role migration; `INSERT IGNORE` seeding is not a permission-revocation mechanism.

## Adding a file connector later (design example, NOT implemented)

Put protocol-specific code under `server/integrations/adapters/csv/`. Its boundary is:

`authenticated company actor + file + mapping version → parse/stage → canonical rows + row-level errors → preview → explicit confirmation → authorized domain service transaction + idempotency/provenance → import result`.

Provide downloadable versioned templates with units/timezone and a mapping from partner column names to canonical field names. Keep parse/mapping/validation separate from writes; validate tenant-owned equipment/person/part IDs through shared services. Do not let input rows select company/database, SQL, credentials or arbitrary URLs. Export uses an authorized domain query first, then a format adapter; import/export may not bypass entitlements or resource scope. Later REST, read-only external DB, ERP, Edge/MQTT and forecast connectors implement protocol adapters around the **same** service contracts. No connector, event bus, generic job engine or future module is implemented in this slice.

## Validation and limits

### Workspace extension boundary

`src/company/workspaces.ts` is the shared typed manifest/resolver; `server/operations/workspaces.ts` persists policy/preferences and authorizes protected workspace routes; `src/company/tenant-shell.ts` consumes the server result. `App.vue` remains the actual Phase2 renderer. Daily capture reuses ProductionEditor/ProductionReports, not copied operational logic. Add registry pages only with an existing or implemented renderer plus domain API checks. `purpose` describes interaction density (task/factory), not a job title or grant. A new workspace can reuse page IDs without changing identity, entitlements or tenant schemas.

Evaluation is module readiness/license → effective action/scope → admin workspace/page policy → allowed personal preferences → safe start fallback. The resolver chooses visible destinations; domain services still check each row/resource. A shared endpoint may serve several permitted pages (e.g. production draft resume and records); page policy is an additional restriction, never an alternative to action checks. Preferences are company/user keyed, have separate optimistic versions from policy, and must never be used as trusted data filters. See the dynamic-workspaces guide for the tested single-module flow and QA commands.

`pnpm test` includes the original tests and new unit/API checks. Real MariaDB tests are opt-in: disposable CI (`isolated-ci` and `CI=true`) or explicitly guarded, approved laptop fixtures (`isolated-local`). The suite never drops owner databases. `pnpm build` includes Vue/TS type checking. The current connected browser acceptance script is `scripts/phase3-admin-qa.mjs`; it creates fictional companies in the approved isolated environment and checks actual API/DB flows. The old `phase3-ui-qa.mjs` describes the earlier mocked UI baseline and is superseded for current panel acceptance. See `COMPANY-ADMIN-QUICKSTART.md` for commands, security rules and remaining limits.
