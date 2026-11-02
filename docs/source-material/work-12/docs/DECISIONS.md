# DECISIONS — owner-approved vs open design hypotheses

## تصمیم جاری و تقدم بر سابقه — ۲۰۲۶-۱۰-۲۸

شاخهٔ کار پس از تأیید شروع مرحلهٔ۰۳، codex/03-production-recording است؛ شماره‌گذاری stage شروع تازه دارد و main/demo تاریخی‌اند. متن‌های تاریخ‌دار پایین دربارهٔ branch/port/وضعیت پیاده‌سازی سابقه‌اند؛ START-HERE، ARCHITECTURE و CURRENT-STATE وضعیت جاری را مشخص می‌کنند.

- هستهٔ قابل تنظیم با ماژول اختیاری و مجوز سرور حفظ می‌شود؛ ثبت تولید بدون پلان/شیفت ثابت مسیر درجه‌اول است. [شرح آخرین گفتگو و موارد باز](PRODUCT-BLUEPRINT.md#جهت-ادامه-پس-از-هاب--بازبینی-مالک-۲۰۲۶-۱۰-۲۸).
- INGEST فرایند مستقل و مخزن فعلی raw/sample در DB همان tenant است؛ خام جدا هدف آینده است. قرارداد امضاشده rc.4 بدون تغییر می‌ماند.
- CompanyFiles تنها root فعال عکس/draft/library و scene است؛ fallbackهای قدیمی پس از انتقال کنترل‌شده حذف می‌شوند.
- پاک‌سازی تأییدشده، حذف مستند فایل بدون مصرف و تست‌های تاریخیِ رهاشده را مجاز می‌کند؛ محیط/شرکت جاری و وابستگی‌ها محافظت شوند. متن کامل اسناد پیش از تجمیع حفظ و هر بخش به مرجع جاری یا سابقه ارجاع شود.
- کارتابل/اعلان و بررسی اختیاری پیشنهادی‌اند؛ ثبت/اصلاح فعلی با زنجیرهٔ تأیید جدید جایگزین نشده است. خرید ماژول، workspace و مجوز سه مرز جدا هستند.

**تکمیل ۲۰۲۶-۱۰-۲۹:** توضیحات مالک دربارهٔ شیفت‌های متنوع، انتساب زمانی، بازکاری، شمارش دقیقه‌ای و ورودی‌های آینده در [همان مرجع محصول](PRODUCT-BLUEPRINT.md#تکمیل-سناریوی-کارگاه-و-مرزهای-توسعه--۲۰۲۶-۱۰-۲۹) تکمیل شد؛ متن قواعد در این دفتر تکرار نمی‌شود. این‌ها عمدتاً دقیق‌کردن جهت قبلی‌اند، نه تصمیم به بازنویسی محصول یا ساخت مخزن جدید. شاخهٔ مرحلهٔ۰۳ از checkpoint۰۲ با کامیت 7d31e30 ساخته و منتشر شد؛ جزئیات حل تعارض داده، تقسیم بازهٔ شمارش و قرارداد کنترل CNC باز مانده‌اند.


## ۲۰۲۶-۱۰-۲۴ — ذخیرهٔ خام قابل جداسازی در INGEST

مالک ثبت و حفظ امکان مخزن خام مستقل و مصرف‌کننده مستقل مانند Grafana را تأیید کرد. پیاده‌سازی فعلی MariaDB مشترکِ شرکت می‌ماند؛ مرز gate/خام/پردازش از موتور ذخیره مستقل تعریف می‌شود و دریافت منتظر پردازش به تگ نمی‌ماند. انتخاب PostgreSQL یا مخزن جدا، مهاجرت و اتصال Grafana هنوز کار آینده‌اند؛ مجوز ساخت یا استقرار آن‌ها از این تصمیم استنباط نشود. دسترسی هاب به هویت شرکت محدود به view مجاز و نوشتن به محدودهٔ تله‌متری است. جزئیات و الزامات تحویل پایدار بین دو DB در ARCHITECTURE ثبت شد.

**2026-10-14.** This is the current decision register. Early history remains in [تصمیم‌های تاریخی / Early decisions](archive/DECISIONS-EARLY-PILOT.md). Do not convert suggestions into decisions.

## 2026-10-18 — Method 4: authorized experimental implementation

The owner chose one product, separate WEB/INGEST executables and shared existing control/per-company MariaDB storage, and authorized new branches in the two existing repositories. WEB owns company identity, source/signal definitions, bindings and business reports; INGEST owns protocol collection and telemetry writes with separate SQL credentials. EdgeBox/source identity is independent of a machine, and signal-to-input bindings carry effective periods. Historical code is a Git checkpoint rather than a requirement to expose two concurrent ingestion paths. Implementation and coordination use [the versioned handoff](integration/method4/README.fa.md). This authorizes branch implementation, tests and push after testing; it does not approve merge, deployment, migration of current company data, or untested hub capabilities. End-to-end acceptance and the REST/file/database job extension remain pending as recorded in the handoff status.

## Confirmed by owner

**D-018 — product shell correction (2026-10-15):** Phase 2 `App.vue` is the approved primary product, not a disposable demo UI. Company login must open that shell with the same Three.js and monitoring modes. Reuse Phase 3 domain services and forms within it. Never auto-seed a new customer with Pouyeshgar's 16 demo assets or simulator production. Scene geometry/mappings belong to that company database; manual summaries retain cohort/period semantics and unavailable telemetry/OEE remains unknown. Owner authorized the separate `feat/unify-phase2-tenant-shell` branch from `f629caa`, normal commits/push, no merges/deploy.

**Operational mission, 2026-10-14/15:** job title is independent of authorization; role is only an initial template, editable per-user action grants and scoped denies are authoritative. Multiple full managers are permitted within active-login capacity; retain the last effective active user manager. Physical sites/areas are distinct from equipment/lines/stations. Manual production is first class without IoT/orders/plans: good output + final irreparable scrap = processed, grouped by resource/part/OP/unit. Preserve blank vs zero; never sum sequential OPs as finished goods or infer OEE/attendance/runtime. Final changes need explicit correction permission, reason and before/after history; normal readers may request correction, with no mandatory approval chain. Five readiness axes remain independent. P0 precedes P1; HTTP device/ERP/attendance integrations are P2 contracts only. Implementation scope and remaining limits: [PHASE3B-OPERATIONS.md](guides/PHASE3B-OPERATIONS.md).

| ID | Decision | Consequence |
|---|---|---|
| D-001 | **Pouyeshgar first pilot, generic product long-term**; SFP24 separate brand | No hardcoded job-shop-only architecture |
| D-002 | Manual, assisted, automated and imported data all supported **conceptually** | One normalized provenance-aware source model; no EdgeBox prerequisite |
| D-003 | Tenant may enable **only desired modules**, including only counts/stops or OEE | Module capability, data readiness, permission distinct |
| D-004 | Jobs without formal plan or order **must be recordable** | Real observations independent from schedule; no fabricated targets |
| D-005 | Physical location ≠ operational scope; no naïve hall OEE | Separate asset/line/cell/product/OP metrics with valid formula |
| D-006 | Current Phase 2 visual direction substantially approved | Preserve real Three.js workshop, compact desktop, layers, charts; targeted fixes only |
| D-007 | First pilot data are SIMULATOR, not physical production telemetry | Label source/period/freshness and unknown states |
| D-008 | Existing running ERP/SFP/hardware environments protected | No deploy or integration without owner consent |
| D-009 | Multi-customer identity/isolation is future product requirement | Design for tenant scope; do not claim current pilot has it |
| D-010 | Order-driven, forecast-driven, replenishment and ad-hoc paths must coexist | Demand/forecast/MPS/job/actual are different concepts |
| D-011 | Open data integrations/API/Excel/Grafana desired, not one fixed vendor interface | Versioned adapters, secure imports and exports |
| D-012 | Record full narrative examples and decisions in docs for next sessions | Blueprint remains detailed, this decision log is compact index |
| D-013 (2026-10-14) | **One running application/server should be able to host multiple independent customer organizations**; some customers may prefer dedicated/on-premises installation. Owner has not chosen a single default hosting business model. | Design tenant-aware identities, permissions, persistence and APIs from the first real backend phase, while keeping hosting mode configurable. This does NOT decide shared-DB vs separate-DB-per-tenant or require building SaaS billing now. |

| D-014 (2026-10-14) | **One independent company purchases ONE company account/Tenant.** A company account has purchased modules, licensed user seats, a first company administrator and its own employees/sites/factories. Three independent companies owned by one person buy THREE separate company accounts. Provider controls entitlements/seat limits; company admin controls internal user roles within those limits. | **Supersedes the prior tentative multi-company-within-tenant proposal in TENANCY-IDENTITY-DESIGN v0.1.** No 1:N independent legal-company accounts underneath one tenant. See [TENANCY-IDENTITY-DESIGN.md](TENANCY-IDENTITY-DESIGN.md) v0.2 for detailed examples and two-company isolation tests. |

## Not yet decided: seek owner's business input before schema/implementation

**Phase 3A owner update (2026-10-14, D-015):** the current narrow implementation uses one central MariaDB control database and a separate operational database/runtime credential per independently purchasing company, initially on one MariaDB service. This supersedes the older storage-choice-open wording below for this slice. The active-human-account capacity policy includes the first administrator and remains provisional, not pricing. Only isolated test environments are authorized; no laptop database installation or existing service change without confirmation.

**D-016 — maintainability:** use a lightweight modular monolith with explicit services, versioned API and adapter boundaries; do not build future modules, all connectors, microservices or a complex plugin engine in Phase 3A. See `DEVELOPER-GUIDE.md`.

**D-017 — owner-authorized usability/security extension (2026-10-14):** simplify company creation/editing and reuse the existing invitation mechanism as no-email, single-use expiring sign-in cards. Recipient sets their own password; administrators may reset but never view it. Company administrators manage only their own users; provider user-support requires password reconfirmation, a reason, typed company confirmation and a bounded session/company grant. Original/company-administrator resets need stronger reconfirmation. Password changes/recovery revoke prior sessions and are audited. A separate local privileged queue worker automates the existing provisioner; HTTP retains no DDL credential. No arbitrary custom-role system, billing or production-data support access is implied. See `COMPANY-ADMIN-QUICKSTART.md`.
- **Confirmed cardinality:** one independent company = one separately purchased Company Account / Tenant; sites/factories under it can be multiple. **Still open:** hosting location, physical tenant isolation (shared MariaDB tables vs separate databases), hybrid sync, subscription billing and exact licensed-seat counting (named/concurrent, per-role, admin and service account rules). Multiple customer company accounts on one server is the product goal, not yet implemented.
- Exact equipment-state inference rules, EdgeBox firmware/protocol, manual edits and late-data reconciliation.
- OEE calculation exclusions/targets, formula editor language and source-quality requirements.
- OP/work order semantics for service parts, customer-provided material ownership/weight/scrap, traceability and outsourced steps.
- Shift/attendance/time-clock connector, night boundaries, personnel skills and staffing approval.
- Inventory system-of-record native or ERP; batch/serial/WIP/warehouse/logistics depth.
- Forecast consumption policy, MPS/APS algorithms and quality inspection/CMMS workflows.
- Light-theme visual spec, AI assistance, notifications, external APIs and enterprise security model.

## Evidence vs decisions

### 2026-10-20 — One definitions entry, one catalog per destination

The administrator's sidebar exposes one «تعاریف شرکت» entry instead of parallel home/structure/master/layout entries. Its cards use names from the same catalog definitions as their destination headings. Each card opens one catalog, without cross-catalog tabs or generic selectors; layout is a card in the same entry. Hub and login-user management remain separate sidebar destinations, without duplicate cards on the definitions page. Internal routes and their permission/module eligibility remain independent; hiding a menu entry does not remove the route or grant permissions. Users without access to the definitions home retain their authorized standalone catalog navigation. Detail pages highlight the parent entry, support a back action and keep the mobile selector on the parent. Physical data remains company → one or more sites → areas; every resource has a site and optionally an area. No schema change, factory-count product cap, single-factory restriction or claim of validated large-scale capacity follows from this UI change.

### 2026-10-20 — Tenant administrator identity and physical structure deletion

Company Admin means administrator of the company's software environment, not company owner, plant manager or platform-wide superadmin. The management workspace is labeled «مدیریت سامانهٔ شرکت». A fresh company_admin defaults to this workspace only; Operations/Analysis require explicit workspace policy opt-in plus their existing action/module rights. Stored explicit policies remain authoritative; no automatic role-based revocation of action permissions. A single workspace has no switcher. Existing operational acceptance fixtures explicitly opt in to operational workspaces rather than relying on the old full-menu default.

Physical structure uses three visible sections: independent site, physical hall/area, machine/workstation. Buttons and descriptions identify the entity being created; parent site is explicit and area optional for machines. Unused site/area/resource definitions can be hard-deleted with version check, server-side scope authorization and audit. FK dependencies, stored scene references and control access rules/templates block deletion; they are not cascaded or detached. Deletion serializes with scene writes and access-rule changes. In-use definitions retain the existing deactivation path. This adds no schema migration and does not automatically reinterpret existing names such as «سالن۱» into another entity type.

### 2026-10-20 — Company management, operations and analysis

Owner authorized three task-oriented workspaces in the existing application. Management (`management`) contains setup home, physical structure, production master data, users, Data Hub and layout; Operations (`task`) contains capture and records; Monitoring & reports (`analysis`) contains monitoring and summaries. Company Admin starts at management home while retaining its separately granted operational rights. Cross-workspace links select the matching space; workspace choice never grants permissions or licensed modules. Physical site/area/resource catalogs are separated from production catalogs in the same existing master-data component. Home gives an actionable next step and describes minimum readiness without claiming all module requirements or hardware connectivity are satisfied. No placeholder settings menus or new licensing/billing system were added. Old `factory` workspace policies must be replaced through the workspace editor if encountered; no silent expansion of stored per-user policy. Current clean local company uses default policy.

### 2026-10-15 — capability-shaped workspaces (owner approved)

Keep one application, one tenant database and the original Phase2 shell. Daily work is a simpler interaction mode using existing production services/forms; Factory retains the scene and specialist views. Neither mode belongs to a fixed job title. Provider licensing, effective per-user action/resource permissions, administrator workspace/page policy and personal preferences are independent. A workspace/page choice never grants data rights. Production capture/basic records do not require Reports or Monitoring; a manager starts at setup when monitoring is unlicensed. Settings use additive control migration5; no tenant data is moved. See [dynamic workspace implementation and tests](archive/deliveries/DYNAMIC-WORKSPACES-PROGRESS.md).

The latest GitHub CI proved 26 unit/API tests and build; not industrial DB, IoT, SaaS isolation, performance or ISO certification. Detailed historical decisions/suggestions: [تصمیم‌های تاریخی / Early decisions](archive/DECISIONS-EARLY-PILOT.md), [idea-inbox.md](archive/research/idea-inbox.md). Upon new owner approval, append dated ADR/change with rationale, alternatives, effects, tests and migration notes.

## D-2026-10-19 — یک محصول، دو runtime، دو دموی ثابت

مالک تجمیع ساختاری پیش از پیاده‌سازی rc.4، pnpm workspace واحد و توسعهٔ مستقل WEB/INGEST را تأیید کرد. پاک‌سازی پس از push/checkpoint: محصول در پوشهٔ اصلی، فاز۲ و هاب قبلی فقط برای پرزنت در دو پوشهٔ مستقل، برنچ‌های قدیمی با tagهای archive محفوظ و از فهرست فعال حذف می‌شوند. اسناد جاری از تاریخچه جدا شدند. هیچ تغییر مالی، دیتابیس یا firmware از این تصمیم نتیجه نمی‌شود؛ rc.4 هنوز نیازمند پیاده‌سازی و پذیرش runtime است.

## 2026-10-21 — Single factory per company and role-neutral workspaces (owner approved)

The company account represents one factory. Its complete name, address, email, phone, contact person/phone and time zone live in the factory profile, independently of the short company sign-in code. Halls/areas and work resources belong to that factory; hall remains a physical location, never an inferred OEE cohort. This replaces the earlier multi-site product assumption. Existing site identities/FKs/scopes remain; migration 11 only adds optional contact columns. API creation locks tenant metadata and rejects a second row, including inactive existing profiles. Historical multiple rows are surfaced for explicit resolution, never silently deleted or merged.

The company definitions home is one continuous card grid with descriptions, counts where meaningful and distinct icons. Factory profile is edited in place rather than treated as a multi-factory list. Company Admin defaults to administration with three sidebar destinations (definitions, users/access, Data Hub). Other workspaces are named «میز کار» and «نمای جامع» independently of role. Workspace IDs, page/action grants and module gating remain unchanged. No fourth workspace, task system, messages or widget builder is implemented by this UI change; a customizable dashboard can later be a page within the overview workspace.


### ۲۰۲۶-۱۰-۲۱ — قرارداد ورودی تجهیزات و واحدها

با درخواست مالک، ورودی تجهیز دیگر به دو شمارش یا یک اقدام پنهان در فهرست ماشین محدود نیست. کارت عمومی و فهرست typed مشترک، با محدودیت نوع واحد کاری و خرید ماژول، افزوده شد. ورودی سفارشی شرکت با مشخصات نوع/واحد/روش و CAS در tenant ذخیره می‌شود؛ پس از استفاده، معنای فنی آن تغییر نمی‌کند. نگاشت عمومی با مصرف عملیاتی ماژول یکی نیست و در فرم این مرز اعلام می‌شود. واحد آزاد منابع/قطعات با کاتالوگ قابل افزودن جایگزین شد؛ مقدار مستقل است و تبدیل خودکار وجود ندارد. schema۱۳ افزایشی است؛ قرارداد امضاشده و دریافت صنعتی دست‌نخورده‌اند.


### ۲۰۲۶-۱۰-۲۱ — پارامتر مستقل و منابع دستی/هاب (ساخت تأیید شد)

مالک ساخت کارت عمومی تعریف داده را تأیید کرد: پارامتر نوع و واحد خروجی دارد و می‌تواند منبع دستی و چند تگ هاب داشته باشد؛ interval دریافت و ذخیره در هاب می‌ماند. انتخاب معنای تگ و کالیبراسیون با مدیر است ولی سرور type/measurement/واحد و دامنهٔ شرکت را کنترل می‌کند؛ اختلاف واحد تبدیل صریح و توضیح/تأیید می‌خواهد. تبدیل تک‌ورودی امن، نسخه‌دار و هنگام خواندن اجرا می‌شود؛ خام هاب تغییر یا تکثیر نمی‌شود. منابع در این مرحله سری‌های جدا هستند و تقدم/جمع/جایگزینی خودکار ندارند. schema۱۴ تعریف/نسخه/ثبت دستی را به tenant اضافه می‌کند. فرم‌ساز/شاخص چندپارامتری/داشبوردساز و قرارداد INGEST خارج از این برش‌اند.

### ۲۰۲۶-۱۰-۲۳ — نوع منبع حسگر و کتابخانهٔ جانمایی

مالک «حسگر / ابزار اندازه‌گیری» را به‌عنوان نوع مستقل منبع پذیرفت. این نوع برای ثبت هویت و محل حسگر است؛ داده همچنان از پارامتر و ورودی دستی/هاب تأمین می‌شود. حسگر در ثبت تولید و شمارش تولید انتخاب‌پذیر نیست. کتابخانهٔ جانمایی یک انتخاب گروهی برای تجهیزات، خط، حسگر، در و پنجره دارد؛ مدل سه‌بعدی فقط ظاهر منبع را تعیین می‌کند. در و پنجره به دیوار مقیدند و حرکتشان فقط در امتداد دیوار است. مدل فعلی خط پیوسته یک نوار نقالهٔ شماتیک است. مدل سه‌بعدی خصوصیِ واردشده و ترکیب چندجزئی خطوط صنعتی نیاز به قرارداد بارگذاری/ذخیرهٔ دارایی جداگانه دارد و در این برش وجود ندارد.
