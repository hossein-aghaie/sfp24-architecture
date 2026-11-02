# Phase 3 — Company Account, Users, Purchased Modules and Permissions
**Version v0.2, 2026-10-14 — corrected to OWNER'S EXPLICIT BUSINESS MODEL.**
**Status:** Core commercial cardinality CONFIRMED by owner. Schema, billing details, security implementation and UI particulars remain DRAFT and require review.
**Corrects and supersedes v0.1** (commit b48e70b). The prior version incorrectly proposed multiple independent legal companies under one customer account. That interpretation is **REJECTED**. The previous text remains recoverable in Git history but MUST NOT be used as an implementation specification.

## 1. Decisive business rule — one independent company buys one independent company account

**The user explicitly said:** «یک شرکت یک اکانت شرکت بیشتر نداره روی برنامه ما ... آقای ایکس سه تا شرکت مجزا داره سه تا اکانت شرکت می‌خره نه یکی برای چند شرکت».

This means:
- **One independent customer company = one Company Account (اکانت شرکتی) = one Tenant security boundary.** A tenant is NOT a parent containing multiple independent customer companies.
- If Mr X owns three separate companies, he buys/provisions **THREE independently licensed company accounts/tenants**. Ownership by the same person does NOT merge accounts or data.
- **One company can own multiple sites/factories/warehouses, departments, halls, lines and equipment under its single company account.** These are operational locations/units, NOT extra independently licensed companies merely because they have different addresses.
- **One physical or cloud server/application installation may serve many separate company accounts/tenants.** Alternatively one customer can run the same code on its own server. Hosting model is undecided and must not be hardcoded.
- The software PROVIDER creates the company account, assigns its purchased enabled modules and permissible user seats according to contract, and provisions or invites a **first company administrator**. The company administrator subsequently manages its company users, their roles and internal permissions, within purchased entitlements.
- Business customer/client/contractor records INSIDE an ERP or work order are **not** software-company accounts unless each independently buys the platform. A Pouyeshgar customer's production order does not make that customer another tenant.
- No parent-level 'holding company account' that grants blanket access to independent subsidiaries is in scope. A parent owning three companies gets three independent accounts. Centralized payment, invoicing, same-login multiple memberships or group-level reports are optional later design questions and do not violate the one-account-per-company rule.

### Semantic shortcut used throughout the UI

The owner uses “اکانت شرکت” as the product/commercial term. In backend technical language, it is acceptable to call its strict data boundary **Tenant**. Avoid asking users to understand Tenant terminology. The UI should display “شرکت / اکانت شرکتی”; internally the record may be named tenants/organization_accounts. There is **no mandatory additional many-to-one Company table** merely to represent an independent company.

A separate 1:1 CompanyProfile/LegalEntity detail record *may* be useful for legal/contact/address fields. If introduced, the constraint is 1 company profile to 1 tenant account for the initial commercial model — NOT multiple independent companies within a tenant. Decide table normalization during DDL design.

## 2. Real examples, as described by the owner

### A — Pouyeshgar / پویشگر
Provider provisions exactly **one company account** called Pouyeshgar. Contract example:
- Enabled modules: maintenance, production statistics and production reports (and any required underlying monitoring/report functions); modules are purchased entitlements and individually enabled.
- 14 user login seats requested:
  - 1 company manager/administrator
  - 1 finance-oriented user
  - 1 production supervisor
  - 1 maintenance user
  - 10 operator users
- **Sum = 1+1+1+1+10 = 14 login accounts.**
- Company admin can invite/create users up to licensed allowance and grant permissions within purchased modules.
- Pouyeshgar can define its own factory/site, current 16 machines, shift systems, production events and future multiple workshops *within that ONE company account*.
- A finance-oriented user exists because the customer purchased a login seat and has an internal staff role. If the finance module is NOT purchased, a 'finance' role does NOT unlock finance screens: that user can still be authorized for purchased reports/exports as appropriate. Never infer purchase of module from role title.
- Operational employee/operator record is distinct from software login account: possible 40 staff but 10 paid operator logins; attendance and shift attribution may be entered by supervisors for staff without logins. Pricing of named vs concurrent seats is NOT decided.
- Even without orders/planning/IoT/QC, permitted users may manually enter daily production and downtime within enabled modules. No mandatory plan, ERP or EdgeBox.

### B — Mihan / company example given by owner (illustrative, not an actual customer record)
Provider provisions **one company account** for Mihan, with the contracted selection of modules, seat count and role distribution. Mihan may have several factories or warehouses in different locations under the **same Mihan account**, with site-level access restrictions.
- A Mihan site administrator may only manage that factory if granted a site-scoped administrative role; company admin may oversee all authorized sites.
- Enabling, for example, OEE and QC for Mihan does not enable them for Pouyeshgar.
- Mihan's assets, personnel, orders, alerts, logs, user accounts and analytics never appear in Pouyeshgar's reports.

**Use a fully fictional company (e.g. نوش‌آوران نمونه) instead of any real company name in test seeds**, to avoid pretending a real business is a contracted customer.

### C — Mr X / three companies
Mr X owns three independent companies A, B and C. The provider sells and provisions **three company accounts**, with separate contracts/entitlements/seat limits, datasets and tenant administrators. If Mr X personally needs access to all three, this is a later identity UX question: separate login credentials or one global identity with **three explicitly scoped independent memberships** may be allowed; either way there is **no unified super-company tenant** and no inherited cross-company permission.

## 3. Product model — what is bought vs who may do it vs available data

Three non-interchangeable axes plus setup:
1. **Commercial Entitlements / امکانات خریداری‌شده:** which company account is active, which product modules it has purchased, how many licensed login seats and any contractual per-role/per-site quota. Set/adjusted by **platform provider** or a separately authorized billing/provisioning process.
2. **Internal Authorization / مجوز داخلی:** which company member can view, record, edit, approve, export or manage a specific site/device/module. Configured by tenant/company admin, bounded by available entitlements.
3. **Data Availability & Provenance / وجود و اعتبار داده:** manual entry, Excel, API/Edge, simulator; whether required fields exist and how old/valid they are.
4. **Setup Readiness / تکمیل راه‌اندازی:** installed module could still lack machines, shifts, cycle-time definition or other prerequisites.

**Effective permission** = authenticated session bound to ONE active company account + active account + licensed active module/action + enabled active user seat/membership + authorized role/action/site/equipment + valid ownership/scope. Deny by default. A module permission does not create a missing license; a purchased module does not grant every operator full access; no amount of role selection manufactures data for an OEE chart.

Disabled module should be hidden or clearly unavailable in company UI, always blocked in API and should not delete historical records. Valid zero, absent data, stale, unconfigured, unauthorized and simulated must be rendered distinctly.

## 4. Business onboarding — provider side vs company side

### Provider-level: selling and provisioning ONE company account
1. Authorized provider administrator opens **Create Company Account / ایجاد اکانت شرکتی** (initially it can be a protected internal provisioning screen or CLI; no public anonymous signup required).
2. Enters customer company name and optionally contact/identity fields, preferred language/timezone as known, and unique account identifier.
3. Chooses purchased product modules and records licensed user seat limit (e.g. 14), with an effective date and auditable entitlement history. Role-specific pricing/quotas, trial plans, renewal/expiry and billing are product policy questions, NOT silently invented.
4. Records initial company admin invitation target; creates the account/entitlements/first membership/invitation atomically in an isolated database transaction. Account is not live until initial admin proves identity and accepts invitation (exact authentication mechanism to be designed).
5. Company administrator signs in and may only configure **their own** company. Provider operator cannot silently browse company production data just because they can provision accounts.
6. The provider can later upgrade/downgrade modules or licensed seats per contract with auditable effective dates. Reducing seats below current active usage requires a defined resolution policy; never silently delete accounts/history.

### Company-level: first admin after first login
1. View own company name, enabled modules, user-seat usage/allowance, incomplete setup and quick steps; never see other customers.
2. Create/invite other users: admin checks remaining licensed seats and appropriate role/permissions. Operator, maintenance, supervisor, quality, finance, viewer etc. are permission templates, not mandatory billing products by default.
3. Define its **sites/factories** (zero or more sites initially), optional halls/lines, equipment, shifts and staff according to activated modules. No factory must be auto-created merely by creating the company account.
4. Configure data source per machine/signal: manual, Excel import, external software/ERP, EdgeBox, or mixture. Basic reports must function without an IoT or fixed production plan.
5. Activate operational flows progressively. Permission changes/audit stay within company limits.
6. Suspension and deactivation policies for company accounts/users require separate documented rules; no destructive deletion of production history.

### User seats vs employee records — avoid a hidden licensing trap
A login seat corresponds to a **user able to authenticate**, not all employees stored in shift/skill/production records. Decide later whether seats mean **named active users**, concurrent sessions or another commercial rule, and whether platform staff/Edge service accounts and initial admin count toward the limit. The 14-seat example uses 14 distinct accounts, not necessarily a committed pricing formula.

## 5. Proposed entities and cardinalities — draft for actual MariaDB schema review

| Entity / candidate table | Meaning | Relationship |
|---|---|---|
| company_accounts / tenants | Purchased independent company account, display/legal name, unique code, status | 1 account = 1 independent customer company = 1 security tenant |
| company_profile (optional 1:1) | Legal/tax/contact details if required | at most one profile per company account; **not** child list of independent companies |
| sites | Factories, workshops, depots, warehouses and other physical facilities | Many sites under 1 company account; may be zero at bootstrap |
| areas/halls | Physical areas inside a site | Many per site, optional |
| users | Login identity and credential/identity-provider linkage | User identity not equal to company account or employee record |
| company_memberships | User's membership/authorization in ONE company account | Multiple members per company; each membership assigned own roles/scopes |
| roles + permissions | Action/site/equipment level RBAC (scoped role-based access control) | Role assignment through company membership, not global user.role |
| user_role_assignments | Links memberships to scoped roles with effective dates | No grant may cross company boundary |
| module_entitlements | Licensed/enabled modules for the company | Controlled by provider according to contract, effective dates |
| seat_entitlements/limits | Purchased allowed login accounts / seat policy | Controlled by provider; enforce on account activation/invite based on approved rule |
| employee/person | Employee/operator/technician master record | Many within company account; may have NO user login |
| audit_events | Immutable log of account provisioning, licenses, users, modules and permission changes | Every event bound to actor and affected company (or platform-scoped) |

**Not selected yet:** UUID/ULID, final DDL, composite foreign keys, same global login reused across distinct companies, password/email workflow and physical MariaDB isolation. Decide these before coding. All tenant-bound resources/events/queries must be strictly scoped; a simple tenant_id column alone is not sufficient.

**Avoid building table companies as a mandatory 1-to-many daughter of tenants.** If a distinct company record exists for compliance, make it one-to-one with the company account for the currently agreed model.

## 6. Two company data-isolation proof and test cases

Create two fictional separately contracted company accounts A and B on a single test server:
- A modules = production reports + maintenance, seat limit 14.
- B modules = monitoring + OEE, seat limit 5.
- A company admin creates authorized users; B company admin can only add B users within 5 seats. One company cannot change another's subscriptions, role mappings or staff.
- Requesting A equipment, reports, users, module/seat entitlements with B token returns 403 or 404. Cover writes, exported CSV/Excel, charts, long-running background tasks and device/source credentials.
- Forged company account IDs in URL, body or header never determine authority; server validates account from authenticated trusted context.
- If a global login has membership in A and B, it selects active company; permissions/seat use/data scope differ. Under no circumstance is it authorized as 'owner of parent account'.
- A finance user cannot see finance modules if A did not purchase them even if internal role is called 'finance'; it may receive approved production report exports if authorized.
- Logging out, revoking membership or disabling a user removes access according to session lifecycle; audit cannot be rewritten.
- A company can define 2 factories under its one account; a report scoped to factory 1 must not accidentally show factory 2, except for approved company-wide aggregated views.
- A shift operator without login can appear in time/production/personnel records but must not consume software login seat unless later licensing rules define it otherwise.
- Under basic manual data entry, A can record quantity and stoppages without order/OP/Edge. B cannot show OEE unless valid planned time, ideal cycle, good/total and applicable state inputs are present.
- Module disabling must preserve A/B historical operational data. Cross-tenant negative tests are required at API, repository, export, ingestion and report levels.
- Phase-2 regressions: 16 original workshop machines and Three.js geometry, simulator, UI, 26 historical tests and local/demo workflows remain intact.

**These are prospective acceptance tests and are NOT currently passing.** Current Phase 2 roles (admin/viewer/edge) and single JSON payload do not implement company accounts or subscription enforcement.

## 7. Proposed technical implementation gates

**Before coding:** Confirm 1 company account per independent company (DONE), independent purchased modules and user-seat quotas (DONE), site multiplicity (DONE); discuss outstanding entitlement/seats and deployment data-isolation choices. Never infer a SaaS-only hosting plan.

**First deliverable to Codex only after owner approves:** design and test an isolated MariaDB relational schema and safe migrations for company_accounts, user identities, memberships, effective module/seat entitlements, roles/permissions and audit minimum. Provide secure create-company-account + first-admin flow, with no real contact/employee data in fixtures.

**Second deliverable:** tenant admin user management within licensed seat budget; audit role assignments; two-company API isolation and negative tests. Keep the provider-versus-company admin control distinct.

**Third deliverable:** site/area/equipment and one real manual count/stop case connected to tenant/scopes, without mandatory order, QC or EdgeBox. Maintain compatibility with existing simulator and workshop geometry.

**Hosting/data strategy decision remains open:** shared application + MariaDB tenant_id-scoped tables OR separate databases per company on same server (and on-prem installations). Evaluate isolation/operational support cost and potential failure modes before freezing physical deployment.

## 8. Explicitly open decisions, NOT blockers to understand the concept

- Seat pricing and counting: named active vs concurrent, initial admin included in 14?, service/device principals included?, role-specific limits? Is the finance user licensed while finance module disabled? (Yes if granted general user account seat; actual visibility depends on purchased modules.)
- Whether one login identity may access separate independently licensed company accounts, or separate sign-in per company. This does NOT change three accounts for three companies.
- Company admin invite vs internal provisioning, authentication, offline onboarding and password reset/SSO.
- Subscription duration, renewal, expansion, downgrade, suspension and grace-period policy.
- Site/factory level permission defaults; separate sites of one company may share some user permissions, company-wide dashboards only where approved.
- Database-per-company vs shared tables, backups, restore and provider support access.
- Distinguish a legal entity from business units, branches or independent subsidiaries: **an independently contracted legal company requires its own company account**; only physical/organizational units of the same purchasing company live inside it.
- What minimal optional fields for contract/company legal identity are needed on day 1.

## 9. Clear handoff for any future session

**USER-CORRECTED BUSINESS TRUTH:**
«ما برای هر شرکت یک اکانت شرکتی مستقل می‌فروشیم. شرکت از ما ماژول‌های موردنیاز و تعداد حساب‌های کاربری موردنیاز را می‌خرد؛ ما این امکانات و سقف کاربران را فعال می‌کنیم و مدیر اولیهٔ شرکت را ایجاد می‌کنیم. خود آن مدیر به کارکنان شرکت نقش و مجوز می‌دهد، البته فقط در امکانات خریداری‌شده. پویشگر مثلاً یک اکانت با ۱۴ کاربر (مدیر، مالی، سرپرست تولید، تعمیرات و ده اپراتور) و چند ماژول مشخص می‌خواهد. شرکت میهن یک اکانت شرکتی خودش را می‌خرد؛ اگر چند کارخانه داشته باشد، آن کارخانه‌ها زیر همان اکانت می‌آیند. کسی که سه شرکت مستقل دارد، سه اکانت جداگانه می‌خرد، نه یک اکانت شامل سه شرکت. می‌خواهیم چند اکانت شرکتی مستقل روی یک سرور قابل اجرا باشند، اما محل استقرار نزد ما یا مشتری هنوز قطعی نیست.»

**No hidden reinterpretation:** The previous v0.1's “one tenant → multiple independent companies” was explicitly corrected. Do not re-introduce holding tenants, implicit global-company admins, free cross-company access or forced finance/QC/planning just because a user role name sounds related.

**Source of truth:** `docs/DECISIONS.md` (D-014), this full updated document v0.2, `docs/PRODUCT-BLUEPRINT.md`, `docs/CURRENT-STATE.md`. Any future Codex prompt must cite this section and explain still-open database/license choices. NO CODE is authorized by this document.
