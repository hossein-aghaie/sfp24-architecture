# ARCHITECTURE — as built vs candidate target

## Method 4 experimental branch — 2026-10-18

The owner selected one product with separate WEB and INGEST executables sharing the existing control directory and per-company MariaDB storage. On `codex/integrated-telemetry-v1`, WEB now owns the telemetry registry, credentials, config, effective signal bindings and production evidence; the separate hub repository implements INGEST. Sources have no machine foreign key. Dedicated SQL users/vaults enforce separate write ownership. Exact implemented tables, transactions, API paths and upgrade constraints are in [STORAGE-CONTRACT](../../integration/method4/STORAGE-CONTRACT.fa.md); actual acceptance and pending features are in [IMPLEMENTATION-STATUS](../../integration/method4/IMPLEMENTATION-STATUS.fa.md). The older in-WEB receive/pull/file routes below are disabled in the default runtime of this experimental branch and retained only in an explicit regression harness. No running environment or existing tenant was migrated; end-to-end acceptance with INGEST is pending.

## Current source-layer implementation — 2026-10-15

The independent source branch retains the modular monolith and company database separation. Typed transport adapters (HTTP/REST/file) feed the durable Hub; `production-source.ts` resolves a resource/time count, and the existing Production service owns report interpretation, scrap, finalization, immutable evidence and minute claims. The source UI configures a semantic input, never a DOM field or arbitrary expression. Future meanings/connectors need their own typed contracts and tests; none are automatically supported by a registry label. See [PRODUCTION-DATA-SOURCES.md](../../guides/PRODUCTION-DATA-SOURCES.md) for current boundaries, tables, versioned APIs and extension points. Historical proposals below do not supersede the shipped account/database decisions documented in START-HERE.

**Unified tenant shell (2026-10-15):** company authentication in `src/accounts/AccountsWorkspace.vue` mounts the existing `src/App.vue` with an in-memory tenant session/API function. Owner administration remains in AccountsWorkspace. `src/phase2/useFactory.ts` has an explicit company mode: no pilot layout, simulator requests or pilot bearer are used. Operational forms remain in `src/company`; the existing Phase 2 components accept company-data slots. `server/operations/master/scene.ts` validates scene resource/location IDs against the authenticated tenant, filters reads with the existing context, and permits whole-document replacement only with unrestricted company-wide master management. Tenant migration 5 adds `scene_layout` with optimistic versioning and audit; geometry JSON is not a replacement for normalized operational master/report tables. See [UNIFIED-SHELL-DELIVERY.md](../deliveries/UNIFIED-SHELL-DELIVERY.md). Statements below about a separate company UI describe the earlier implementation.

**Phase 3B P0:** `server/operations/master` and `production` now use the shared authenticated `TenantStorage.connection` boundary and typed relational tenant schema. Pure scope policy is shared in `src/company/access-policy.ts`; authorization is reloaded/enforced server-side. HTTP remains an adapter to domain services; no microservices or plugin system. Read [PHASE3B-OPERATIONS.md](../../guides/PHASE3B-OPERATIONS.md) for current seams, migration versions, supported manual reporting and future device/ERP/attendance adapter contracts. Phase 2 scene and simulator remain independent; the old architectural diagrams below are historical baselines.

**Phase 3A shipped increment:** `server/platform/` adds a separate company-account control plane and minimal per-company MariaDB storage. HTTP `/api/v1` delegates to account services; restricted CLI owns DDL/provisioning; tenant storage resolves only from authenticated company context and the private catalog/vault. Original Phase 2 remains independent. Real MariaDB two-company isolation and lifecycle tests passed in [CI](https://github.com/hossein-aghaie/pouyeshgar-workshop/actions/runs/38596701887); see `DEVELOPER-GUIDE.md` for ownership/seams and `PHASE3-DELIVERY.md` for limits. Historical baseline/proposals below must not be read as undoing this verified increment.
**Baseline 2026-10-14 / e19016d.** Clear separation of observation, verified implementation and future architecture. Full domain explanation in [PRODUCT-BLUEPRINT.md](../../PRODUCT-BLUEPRINT.md).

## Implemented today
```text
Vue3/TS/Vite/Three.js + ECharts
  └── src/phase2/* (visuals, filters, layers, dashboards)
      └── src/pilot/api.ts HTTP /api
          └── Fastify server/app.ts (local accounts + equipment scopes)
              └── server/store.ts
                  ├── DEFAULT .local/pilot-state.json
                  └── OPTIONAL MariaDB: pilot_state(id, JSON payload), NOT tested on server
Simulators: server/simulator.ts (minute ingestion), server/seed-industrial.ts (15-min scenarios)
```
- Domain validation: `src/pilot/domain.ts`, `industrial.ts`, `simulator-config.ts`; migration in `server/migrate.ts`.
- No production enterprise authentication, source-adapter registry or relational analytical data store. No automatic live Edge linkage. Tests covered local pilot route behavior and valid simulator semantics.

## Target hypothesis for discussion, NOT an instruction to deploy
- **Modular monolith** instead of premature microservices: (a) tenant/security/audit, (b) physical asset and organization registry, (c) workforce, calendar, capabilities, (d) observations/events and source provenance, (e) execution, product/part/OP and routing, (f) reporting/KPI engine, (g) optional quality/CMMS/planning/materials, (h) integrations/API and messaging.
- **Source-independent event envelope**: tenant/site/resource identity, event type, source and idempotency ID, schema/mapping version, event time/ingest time, quantity and unit, quality/freshness. Simulators, manual forms, CSV, MQTT/HTTP/SCADA/ERP adapters normalize through validated ingestion. Actual vs inferred vs corrected vs simulated remains identifiable.
- **Relational data redesign before scaling**: explicitly model tenants/sites/assets/people/shift revisions/jobs/operations/event records rather than a single JSON blob row; plan migration and benchmark minute-scale data, historical queries, indexing and retention. MariaDB remains a reasonable candidate; no automatic switch to a time-series database.
- **Flexible execution**: actual counts and stops work without order, plan, QC module or sensor. Optional order/forecast/replenishment, MPS, MRP, finite scheduling and inventory are *separate concepts*. Keep policy effective dates/history.
- **Module capability / data readiness / user permission** are independent axes; true server-side tenant isolation and RBAC are future work.
- **Equipment state dimensions**: connectivity, technical status, operational activity, work assignment and dispatch eligibility are not aliases, and OEE Availability is a separate time-based KPI.
- **Extensibility**: documented access-controlled API + exports, safe read-only DB connectors and Grafana compatibility without making Grafana or AI an authoritative writer.
- **Design for both** Pouyeshgar job-shop and fixed bottling/packaging lines; verify second scenario before freezing schemas.
- **Security standards** and industrial protocol/scale claims require later testing; see blueprint for ISA-95/88, ISO 22400, SCOR, GS1 scope.

## Confirmed customer model — one account per independent company (corrected 2026-10-14)
The owner has clarified an earlier architectural assumption: **ONE INDEPENDENT CUSTOMER COMPANY = ONE COMPANY ACCOUNT = ONE TENANT**. Do not implement a multi-company holding tenant for three independent subsidiaries; three companies require three separately sold and configured company accounts, even if the same natural person owns them. One physical server/application may run many separate company accounts; on-premise single-company use should remain possible. Hosting infrastructure and physical DB tenant isolation are not yet chosen.

Within one company account there may be **many** operational sites/factories, warehouses, halls, lines, equipment, staff and shifts. The initial identity/provisioning relationship is:
- Provider/Platform administrator: provisions individual Company Accounts, sets which modules the company has purchased, sets permissible **user login seat counts** and activates/invites the first Company Admin; no default unrestricted access to customer production.
- Company/Tenant administrator: invites/manages users, memberships, site/equipment roles, within its company's licensed modules and user-seat allowance; cannot elevate itself to provider authority or see other accounts.
- User account: a login identity, distinct from an operational employee/person record that may never log in. One natural person owning three independent companies does NOT make them a single tenant. Cross-company single-sign-on is an optional later UX question with separate scoped memberships, not a cross-company privilege.
- Modules: entitlement/purchase status separate from company-user authorization and from data availability/setup. Company user's job title “finance” does not enable an unpurchased Finance module.
- The Tenant object may directly store the purchasing company's legal/display profile; optional 1:1 CompanyProfile is permissible. **A compulsory 1:N independent-companies-inside-tenant relation is explicitly rejected.**

**Example:** Pouyeshgar purchases one account with maintenance, production statistics and production reports, plus 14 logins (1 company admin, 1 finance user, 1 production supervisor, 1 maintenance user and 10 operator users). Its sites/16 machines remain within this account. Mihan independently purchases one account with its own entitlement and login seats, potentially covering several sites; sample fixtures should use a fictional second company instead of assuming Mihan is a real customer.

**Storage design OPEN:** shared tables with tenant/account IDs and enforced scoped API/repository queries (MariaDB has no automatic RLS from a column) vs separate tenant databases on the same server. Test cross-tenant isolation including exports, background jobs, cached KPI and devices. Do not migrate production or build sales/billing without owner approval. Draft full model and tests are in [TENANCY-IDENTITY-DESIGN.md](../../TENANCY-IDENTITY-DESIGN.md) v0.2.

**Phase-3 first slice after approval:** provision one company account + purchased module/seat entitlements + first company admin; provision a second fictional company on the same test server; prevent any unauthorized cross-company access. Only then build site/equipment/manual production flows. Site is optional at first signup; one company can create several sites later.

## Proposed implementation gates
1. Confirm tenancy model, site/physical vs operational scopes, event envelope, time/freshness and approval/audit vocabulary with owner.
2. Test actual MariaDB in isolated database. Version migration and document backup/restore.
3. Implement one end-to-end vertical slice: manually recorded counts and downtime for one CNC (possibly supplemented by simulator), shift/operator attribution, persistence, report with time filters and source drill-down.
4. Add independent module/readiness configuration and ensure permission checks on API, imports, exports and charts.
5. Only then progressively add job/OP/order/forecast, quality, maintenance, inventory/logistics as approved.

## API/schema governance
Adopt versioned contracts, validations, idempotency, effective-date handling, revisions, import error reporting, source attribution, tenant enforcement, ownership semantics and structured error codes. Do not silently treat unimplemented target features as current functionality.
