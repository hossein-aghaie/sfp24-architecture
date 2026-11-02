# Phase 3A — Company Accounts, Licensing & Tenant-Isolated MariaDB
**Draft implementation contract · 2026-10-14 · Branch:** `feat/phase3-company-accounts`
**Status:** Engineering direction for the first narrow executable increment. Some commercial/authentication details are provisional; do not invent production-grade business rules.
**Parent baseline:** `0ade7f59baa483b476cf94f5d56c36f7fd9c4cbf` on `feat/smart-factory-pilot-next`.
**Read together:** `docs/START-HERE.md`, `docs/DECISIONS.md` D-013 and D-014, `docs/TENANCY-IDENTITY-DESIGN.md` v0.2, `docs/PRODUCT-BLUEPRINT.md`, `docs/CURRENT-STATE.md`, `docs/ARCHITECTURE.md`, `docs/archive/deliveries/PHASE2-DELIVERY.md`. Actual implementation and tests take precedence over old progress snapshots.

## 1. Short business truth / معنای تجاری

Each independently purchasing company has exactly **ONE Company Account / Tenant** and its own contract entitlements, purchased module set, login-user seats and an initial Company Administrator. Three independently registered companies owned by Mr X buy **three independent accounts**. A single company can have multiple factories/sites, halls, warehouses and production lines *within its single account*. Provider/Platform Admin creates company accounts and sets entitlements; company admin can manage own users/roles within purchased limits. Operators/personnel records may exist **without** a paid login account.

**Example contract, not actual billed customer data:** Pouyeshgar — modules for production statistics, production reports, downtime, maintenance; 14 login seats: 1 company admin, 1 finance-role user, 1 production supervisor, 1 maintenance user and 10 operator logins. Finance role alone does NOT enable an unpurchased finance module. Sample Company B should be entirely fictional; do not use Mihan/Nestlé as supposedly real demo customers.

The final software must support optional manually captured daily production and downtime without IoT, order/job plan, full QC or ERP; companies and modules are not required to use the same scheduling, manufacturing or automation modes. For example, future job-shop orders/OPs and forecast-driven continuous lines require configurable *different operations models* while using the same platform, source provenance and permission infrastructure.

## 2. Recommended first storage pattern (not an irreversible scalability claim)

**One MariaDB server/instance may host multiple logical databases:**
- `platform_control` database — identity/security and license **control plane**. Tenant/company-account registry, tenant-to-storage mapping, contract entitlements/modules and seat allowances, platform admin, tenant user identities and memberships, role grants and auditing. The company-account registry should have exactly one independently purchasing company per tenant. Optional legal profile is 1:1, NOT 1-to-many subsidiaries.
- `tenant_<opaque_id>` database **per independent company account** — company business/operations plane. In later slices: sites/plants, halls, 16 existing Pouyeshgar equipment identities, operators, shifts, production/stop events, source mapping, QC/maintenance and planning as individually enabled. It may start with minimal `tenant_metadata` / `schema_migrations` structure and then grow by versioned migrations.
- All tenant databases run on the **same MariaDB service/server**, initially; this does NOT imply separate machines, containers, or MariaDB servers. An on-prem customer can use the same code/configuration against only its own tenant DB.
- The application resolves a database exclusively from the **server-validated company account context** and the private control catalog. Never trust a client-supplied DB name, raw tenant ID, HTTP header or JWT claim without validation against active authenticated access. Do not interpolate arbitrary identifiers into SQL.
- Use **separate least-privilege DB runtime credentials** per tenant and a restricted control-plane connection. Provisioning/migrations require separately controlled elevated credentials; never expose GRANT/CREATE DATABASE to ordinary web request handlers.
- Provision company metadata, tenant DB and initial admin with an **explicit auditable staged lifecycle**. MariaDB DDL isn't transactional the same way row INSERTs are: design idempotent, resumable state transitions/compensation for partial failure. Do not falsely claim multi-database atomicity.
- Run same **versioned schema** for all tenant databases. Factory differences are CONFIGURATION (modules, signal mappings, process/OP/routing definitions, sites, shift calendars, view settings), not ad-hoc per-customer columns or separate code forks.
- A single MariaDB instance shares CPU/RAM, network and failure domain across tenant DBs. Per-tenant DB improves logical privilege isolation, export, targeted backup and future migration, but does **not** provide host-level resilience or eliminate noisy-neighbor issues.
- Per-tenant DB requires managed migrations for every tenant, provisioning/rotation/connection-pool lifecycle, backup + verified restore, schema version monitoring and safe onboarding/offboarding. Put hooks in place during this slice, not every enterprise service.
- This is a pragmatic phase-3 choice for an initially **limited number** of customers, not a claim that it remains cheapest for thousands. Preserve a server-side `tenant_storage` abstraction/catalog so pooled or dedicated deployments can be evaluated later. No need to implement multiple physical topologies now.

**Do not copy the Phase 2 pilot's single `pilot_state(id=1,payload JSON)` row as the production company schema.** That is only a demo fallback and must not become one giant JSON document per customer. Build normalized relational foundations and migrations.

## 3. Provider vs company administration — minimal workflow

### Provider/Platform administrator
- Create once via a **restricted one-time local bootstrap command** with a securely entered password; no public self-registration or default password in Git, terminal arguments or logs. Rate-limit authentication, strong salted password hashing (Argon2id preferable; scrypt acceptable when implemented correctly), robust session invalidation, no credential echo.
- Provide a minimal provider-only admin UI: list *company account metadata only*, create one company account, set allowed module entitlements, seat allowance, appoint/invite first company admin, view tenant provisioning status.
- Provider rights **do not imply access to raw customer equipment/production/personnel information**. Any support/impersonation mechanism is out of scope.
- Protect provider operations from ordinary company credentials on the server. Audit provider's create/entitlement/change actions.
- Do not implement billing, purchase processing, subscription payment, unlimited provider backdoor or anonymous registration.

### Company administrator
- First company admin is securely activated/invited. Avoid assuming SMTP exists; provide secure one-time bootstrap/invitation token with expiration and hashed storage, displayed only to authorized provisioner or written to an ignored local path in development. One-time activation/credential setup; disable or expire token after use. Require approval before exposing public remotely.
- After login, can view its own company name, licensed modules and seat allowance; invite/manage company users and assign scoped roles. A minimal first iteration may only support a few role templates; enumerate unimplemented permissions honestly.
- Active authenticated login accounts consume licensed seats. **Provisional Phase-3A rule:** licensed limit counts active human login users, INCLUDING the initial company admin; employee records without logins and Edge service principals do not consume human seats. The real pricing policy (named vs concurrent / role-based price / renewal) is still a business decision and must be explicitly revisited before invoicing. This policy is not a declaration of commercial pricing.
- A user may be fully legitimate even when the company lacks their department's specialized module; a role name (e.g. finance) cannot grant an unpurchased module.
- Maintain server-side audit of user activation, role and entitlement changes; revocation must invalidate permissions without requiring app restart.
- Site creation is OPTIONAL during account registration; allow zero sites initially. A company may define multiple sites later. Do not provision a fake factory/hall for every company.

## 4. First slice schema candidate — design before migration

Control DB:
- `schema_migrations` (version, applied_at, migration checksum).
- `company_accounts` (opaque PK, code/slug unique, company name, status, created_at, version).
- `tenant_storage` (company PK, logical storage key, DB identifier and status; DB connection secret reference rather than password). Identifier generated on server.
- `provider_admins` / `platform_users` separate from tenant accounts, with login metadata/password hash and status.
- `company_users` (opaque identity, company_account_id, unique username per company; password hash or invitation state; status, created_at). First release can use an identity per-company; optional single human login across multiple company accounts is deferred and must **NOT** create a shared parent company. Identity structure should permit later iteration.
- `roles`, `permissions`, `company_user_role_assignments` scoped to company and intended actions. Company admin cannot grant provider powers; no user global `admin` shortcut.
- `company_module_entitlements` (company_account_id, module key, status, effective_from/changed_by, version).
- `company_seat_entitlements` (company_account_id, limit, policy version, effective_from/changed_by).
- `company_invitations` (target company/user reference, hashed token, expiry, consumed_at).
- `control_audit_events` (actor/provider-or-company-admin, target company, action, timestamp, non-sensitive change summary/correlation ID).

Tenant DB:
- `schema_migrations` and minimal metadata; later normalized `sites`, `assets`, `events`, `shifts`, `operators` etc. Avoid premature tables for MRP/forecast/logistics. Site belongs to that tenant DB; `site_id` does NOT mean company.
- All secrets require ignored, appropriately permissioned secret storage. No hard-coded real passwords, no real employee records or photos in git/fixtures.

**Integrity and tests:** Unique company codes, uniqueness of username per company, active seat-count check implemented transactionally/concurrency-safe, last-company-admin protection, module/provider changes effective-dated and auditable. Server-side tenant-to-DB routing and no account enumeration on login failure. API schemas validate all input, error types intentional, no arbitrary SQL execution. Administrative UI no decorative/no-op buttons.

## 5. Red lines for implementation

- **DO NOT** modify `main`, old `next`, the `docs/platform-product-blueprint` branch, historical stash, other projects (accounting_erp / SFP24), Raspberry Pi or any live running environment.
- **DO NOT** install or run MariaDB on the owner's actual local/production machine, overwrite an existing DB, use Docker/WSL or change Windows services **without explicit confirmation**. If no isolated MariaDB test instance is available, produce migrations and mocks/tests honestly, and report real DB integration as NOT TESTED. Prefer a dedicated GitHub Actions MariaDB service for CI when technically possible and opt-in only for test branch.
- Existing demo Phase 2 must still render and run from `.local/pilot-state.json`, with 16 equipment and the prior browser QA. New company features can run in a separate explicit mode until migration is proven; NO implicit conversion of stored demo state or fake live data.
- No customer app sharing of database credentials. Never expose tenant database identifiers/credentials via API or UI. Secrets not in source/commits or browser localStorage.
- No browser-selected tenant used directly to pick a DB. All tenant scope determined by trusted authenticated session and membership.
- All provider/company permission checks on backend plus UI visibility. Missing purchased module = inaccessible even if a user knows endpoint.
- **No claim of compliance** (ISO, ISA, security standards) or enterprise readiness without tested conformance.
- Avoid large rewrites of the approved UI, scene and industrial reporting; build narrow routes/pages with same FA RTL and EN LTR design system.

## 6. Acceptance criteria — no fake 'passing'

1. Feature branch from baseline and clean tracked commits; production code changes only on `feat/phase3-company-accounts`.
2. Schema creation is versioned, idempotent and repeatable on an **isolated test DB**. Existing pilot DB and file state intact. If a real test DB unavailable, mark real integration UNTESTED.
3. First provider admin bootstrap secure/repeatable and cannot be abused for self-registration. No default static login.
4. Provider creates fictitious company A and B on the same server with own DBs; each configured modules and licensed seat limits. Partial creation failure leaves a recoverable state (never a ghost ACTIVE tenant pointing to missing DB).
5. First company admin securely activates; can create own users and assign permitted roles; active seat limit enforced with concurrency-safe tests.
6. A admin **cannot read/write/modify B company profile, modules, users, sites, data**, even when spoofing IDs, URL params, request body, or cookies. Device/service accounts cannot impersonate a human.
7. B admin cannot change provider entitlements, increase licensed seat limit, provision companies or grant provider permissions.
8. No data from A appears in B's queries, exports, chart APIs, cached or asynchronously handled results. At minimum test all routes implemented in this slice; future report routes must have explicit tenancy gate.
9. Company A has only basic monitoring/production/downtime modules; company's title 'finance' doesn't enable unpurchased finance. Company B has a different module/seat selection; both independent.
10. Initial company onboarding works without defining site, factory, hall, equipment, job, QC or Edge. Optional site flow can be implemented later.
11. UI workflows functional at 1366x768, 1920x1080, FA/EN, separate provider vs company admin surfaces.
12. Existing baseline **26 tests**, Phase 2 scene/selection/3-mode dashboards, simulation and local runbook remain valid. Any deliberate test updates explained; no weakening of assertions.
13. CI checks type/build/unit, and a MariaDB integration job only if provisioned. Browser screenshots/evidence and no-layout regression where test environment permits.
14. Deliver concise report: branch, commits, exact schema/API/files, screenshots/tests, limitations and next step; no Merge/PR/Tag/Deploy unless requested.

## 7. Next slice explicitly NOT included

Do not implement now: comprehensive order-driven / forecast-driven APS, MRP, WMS/logistics, QC and CMMS workflows, live PLC/Edge protocol, employee clock LAN connector, external ERP, payment gateway, SaaS subscription billing, multi-site dashboards or full asset migration. The future domain architecture must ALLOW all these without hard-coding a simple workshop, but the first coding task must be usable and limited.

## 8. Open decisions for the owner

- Counts of licensed seats: named active humans incl. first admin is a **provisional simple default**, not final price formula. Later choose role-specific tiers and the upgrade/downgrade policy.
- Identity across separate company accounts: initially independent user account per company; shared SSO is future optional.
- Multi-tenancy scaling: DB per company on one MariaDB service is a reasonable initial choice; later consider shared table pools for thousands of small tenants, dedicated instances for enterprise customers.
- Whether to introduce an actual provider admin UI in the FIRST slice or begin with a protected CLI+minimal company admin UI based on available local MariaDB testing.
- Offline installation, provider support and license activation; avoid inventing phone-home licensing or dependencies on constant internet.
- Deployment to a real production server needs explicit security review, TLS, backup/restore evidence and field acceptance.

**Future-agent comprehension check:** the software seller can create ONE account for Pouyeshgar with 14 paid login users and purchased modules. Another company buys its own separate account; both can run on one server but cannot see each other's data. A single company can have several factories under its one account. Factory processes can be flexible job-shop or continuous line with manual/IoT inputs, but that does NOT justify forcing every customer to define planning/QC/ERP during company onboarding. The current project contains only a pilot JSON store and locally scoped credentials; this document is a scoped development plan, not a claim these features already exist.

## 9. Maintainable modular code and optional integrations — owner clarification, 2026-10-14

**Owner intent:** Do NOT turn everything into dozens of packages/microservices, but do not build a monolithic tangle where a new developer must read the whole codebase before adding one costing module or personnel connector. Work with a light **modular monolith**, high cohesion, clean interfaces, meaningful filenames/folder boundaries, succinct explanations of WHY and extension points, and shared core service functions instead of duplicated business logic. Do not create unused abstractions or rewrite approved Phase 2 code gratuitously.

- **Functional domains own their logic:** company accounts, identities/permissions, staff/skills, physical assets, production/events, maintenance, planning and future product costing/forecasting should have defined responsibility and internal service contracts; modules may evolve separately. A future product-costing module is NOT the same as forecasting or planning; it can consume authorized production, material, labour, machine and overhead data when those sources exist. Forecasting can be an optional local algorithm **or an external provider/connector**.
- **Reuse within the application:** settings screens, machine dashboards, operators and reporting call a domain service/typed contract instead of replicating entity rules or reading arbitrary other modules' tables directly. For internal module-to-module calls, don't require unnecessary HTTP: use typed services/ports, domain events only when warranted. Apply authorization and tenancy centrally and at persistence boundaries.
- **External interoperability = independently extendable adapter layer:** present one stable, versioned and authorized API surface outward; allow optional connectors to file import/export, Excel/CSV templates, REST APIs, approved read-only external database connections, ERP, edge telemetry and eventually external forecasting/logistics services. This does NOT mean every internal function needs its own external endpoint.
- **Common ingestion/import pipeline:** source adapter -> staging/parse -> configurable mapping from external columns/names/codes to canonical domain schema -> validate (types, units, source, equipment/site IDs, tenant and permissions, duplicates, dates) -> preview with **row-level comprehensible errors** -> confirm -> idempotent transactional write -> provenance/audit. For Excel/CSV provide downloadable blank/annotated templates and export, but also accept partner-shaped files through versioned mappings where practical; don't demand one rigid fixed file forever. Data retrieval from external DB/API needs explicit credentials, scoped read policy, polling/sync/idempotency and ownership rules. No direct SQL client connection to customer's production databases without permission.
- **Common egress/export pipeline:** authorized report/query -> documented format/version/unit/timezone -> CSV/Excel or authorized API; future webhooks/MQTT/etc only when use cases justify them. Shared export infrastructure prevents every module implementing another ad hoc file download.
- **Extension guide:** create/update a short `docs/DEVELOPER-GUIDE.md` when writing code: where to add a new module, entity service, permission, migration, route, connector, import template/mapping and test; include one representative example for a new module and one for a file connector. Explain domain vocabulary, folder layout and ownership boundaries; comment *non-obvious intent* and delicate invariants, not every line.
- **Phase 3A scope guard:** this paragraph sets maintainability and **future interface constraints**, NOT a request to implement costing, future forecast integrations, all Excel/API/MQTT adapters, an event bus, plugins, code generators or microservices NOW. Build only the necessary seams (interfaces/ports and coherent folders) as Phase 3 company-admin code is implemented; record deferred adapter contracts as design ideas.

