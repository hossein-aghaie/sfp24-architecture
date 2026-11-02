# START HERE — Smart Factory documentation map / راهنمای واحد مستندات

**Monorepo migration (2026-10-19):** Owner authorized structural consolidation on `codex/telemetry-monorepo` before rc.4 implementation. Read [the migration record](../../migrations/TELEMETRY-MONOREPO.fa.md). Shared contract is now [packages/telemetry-contract/contract](../../../packages/telemetry-contract/contract/README.fa.md); the previous bundle location is a redirect only. Legacy lab behavior remains isolated and must not be called rc.4 acceptance.

**بستهٔ اجرایی نامزد:** [telemetry-execution-v2](../../integration/telemetry-execution-v2/README.fa.md)، rc.2، API/schema/DDL/grants/تراکنش/CSV و معیار آزمون. وضعیت تأیید جدا از سند محصول و اجرای واقعی است؛ هیچ SQL این بسته اجرا نشده.

**مدل جدید آمادهٔ ممیزی هاب (۲۰۲۶-۱۰-۱۹):** [تعریف، تست، انتشار و مصرف تگ](../../integration/HUB-TAG-PUBLICATION-DESIGN.fa.md)، نسخهٔ محصولی 1.1.1: تنظیمات فنی در پنل هاب، انتشار انتخابی، مصرف در برنامه، دریافت مستقل از WEB، حذف روشن و بازیابی CSV با تصمیم کاربر در تعارض. بخش‌های۱۹ تا۲۲ تصمیم‌های جدید، توسعه‌پذیری، درخواست ممیزی و الزام آمادگی مهاجرت کل دیتابیس را مشخص می‌کنند. مالی/تمدید فعلاً خارج از محدوده‌اند؛ طراحی MQTT/Sparkplug با سشن هاب بررسی می‌شود. هنوز پیاده نشده و دستور شروع نیست. بستهٔ اجرایی method4/1.1.0 بدون تغییر باقی است؛ نسخهٔ محصولی سند، DDL یا wire جدید اجرایی محسوب نمی‌شود.

**روش۴ در branch `codex/integrated-telemetry-v1` — ۲۰۲۶-۱۰-۱۸:** [قرارداد دقیق ذخیره‌سازی](../../integration/method4/STORAGE-CONTRACT.fa.md)، [راهنمای کار و اجرا](../../integration/method4/RUNBOOK.fa.md) و [نتایج/محدودیت‌ها](../../integration/method4/IMPLEMENTATION-STATUS.fa.md) مرجع تغییرات این شاخه‌اند. برنامهٔ WEB و schema پیاده شده‌اند؛ دریافت واقعی جدید هنوز باید با branch سشن هاب آزمایش شود. مسیر قدیمی دریافت در WEB فقط در regression test harness ثبت می‌شود. توضیح‌های اتصال قدیمی در ادامه شاهد قابلیت جدید نیستند و اجرای سرویس‌های مالک تغییر نکرده است.

**الگوهای پوزیشن و نام‌های ماژول‌ها (2026-10-16):** [راهنمای الگوها و فهرست محصول](../../guides/POSITION-TEMPLATES-AND-MODULES.md) روش انتخاب، ذخیره و ویرایش الگوی اختصاصی شرکت و مرز ماژول‌های فعلی/آینده را توضیح می‌دهد. انتخاب الگو، مجوز کاربر را خودکار ذخیره نمی‌کند؛ تغییر الگو به کاربران قبلی سرایت نمی‌کند.

**اصلاح فرم کاربر و تیک صفحه‌ها:** ساخت و ویرایش کاربر هم اکنون همان انتخاب‌گر الگوی پوزیشن را دارند؛ ویرایش عادی دسترسی‌های فعلی را حفظ می‌کند. تیک‌های فضای کاری، صفحه‌اند و وضعیت مجوز/خریدشان کنارشان دیده می‌شود. جزئیات و روش کار در راهنمای بالا؛ فهرست قدیمی نقش‌ها دیگر در فرم نیست.

**شرکت آمادهٔ تست مالک:** [POUYESHGAR1-DEMO.md](../../guides/POUYESHGAR1-DEMO.md) مشخصات `pouyeshgar1`، ۱۰ اپراتور فرضی، شیفت‌های اختصاصی، ۵ قطعه/۱۱ OP، چیدمان اصلی ۱۶ تجهیز و شواهد مرورگر را توضیح می‌دهد. شیفت پیشنهادی هر فرد اکنون در اطلاعات پایه قابل تنظیم است؛ دادهٔ تولید یا منبع شمارنده‌ای Seed نشده است.

**Work periods and local cleanup (2026-10-16):** operator Start/Finish work, persistent pending periods/drafts, independent device counts and source-change notifications now reuse the existing tenant shell. Owner-only permanent company deletion is explicitly limited to the isolated laptop development environment, with confirmation and privileged-worker cleanup. Read [WORK-PERIODS-PROGRESS.md](../deliveries/WORK-PERIODS-PROGRESS.md) for real MariaDB/browser evidence and boundaries; the human guide contains the daily steps. No existing company was deleted by the agent.

**ورود ثابتِ توسعه (2026-10-16):** در محیط مستقل۵۲۰۶، حساب‌های آمادهٔ تست اکنون `dev-admin` برای صاحب نرم‌افزار و `company_admin` / `user-test` برای شرکت‌های آماده‌اند؛ رمز هرکدام همان نام است. این الگو فقط به fixtureهای ساختگی محدود است؛ قانون رمز شخصی عادی تغییر نکرده. جدول کامل و حدود ابزار صریح `Set-Dev-Logins.cmd` در بخش۳ [راهنمای انسانی](../../LOCAL-USER-GUIDE-FA.html) است. Start-All رمزها را Reset نمی‌کند.

**راهنمای انسانی اجرای لپ‌تاپ (2026-10-16):** [LOCAL-USER-GUIDE-FA.html](../../LOCAL-USER-GUIDE-FA.html) راهنمای روزمرهٔ صاحب نرم‌افزار، چهار ورودی، ساخت شرکت، ثبت دستی، شبیه‌ساز، پایان کار و رفع اشکال است. از ریشهٔ Worktree مستقل، `Read-Guide.cmd` را باز کنید. راه‌اندازهای `Check-Setup.cmd`, `Start-All.cmd`, `Status-All.cmd`, `Stop-All.cmd` به همین راهنما تعلق دارند. اجرای کامل راه‌انداز جدید به درخواست مالک برای آزمایش دستی او باقی مانده؛ بررسی‌های بدون سرویس جای آزمون واقعی شروع/توقف را نمی‌گیرند. [مرز فنی و شواهد](../deliveries/LOCAL-LAUNCHER-NOTES.md).

**Device setup usability:** the company source panel now exposes a copyable receiver address, Node ID and masked one-time connection key, with explicit key replacement. A separate local simulator window imports that file, checks the actual receiver, sends at a configurable interval and retains offline minute counts. It feeds the existing operator form. Start with [DEVICE-CONNECTION-QUICKSTART.md](../../guides/DEVICE-CONNECTION-QUICKSTART.md); local review credentials stay outside Git. No real hardware, new business module, merge or deployment is included.

**Production data sources update (2026-10-15):** `feat/industrial-data-hub-neway` now has a simpler Persian/English source wizard, HTTP push + REST pull + actual CSV/XLSX imports, a standalone fictional EdgeBox, and source counts consumed by the existing production report form with immutable evidence and resource-minute reuse protection. Read [PRODUCTION-DATA-SOURCES.md](../../guides/PRODUCTION-DATA-SOURCES.md) for current behavior and limitations and [DATA-SOURCES-INTEGRATION-PROGRESS.md](../deliveries/DATA-SOURCES-INTEGRATION-PROGRESS.md) for evidence/checkpoint. This supersedes the earlier **preview-only** boundary in the initial [Hub contract](../telemetry-v1/INDUSTRIAL-DATA-HUB.md) and [delivery](../deliveries/INDUSTRIAL-DATA-HUB-DELIVERY.md). No real firmware/device, MQTT/SCADA integration, merge or deployment is claimed. The independent worktree and old owner environments remain separate.

**Dynamic workspaces (2026-10-15):** Daily work and the preserved Factory shell now share a typed capability registry, per-user company policy and persisted personal preferences. Production-only companies start with actionable setup; operators can record production without Monitoring or Reports. See [DYNAMIC-WORKSPACES-PROGRESS.md](../deliveries/DYNAMIC-WORKSPACES-PROGRESS.md) for manual review, exact evidence and limits. This supersedes the unconditional Monitoring navigation in the earlier unified-shell delivery.

**Owner-directed product correction (2026-10-15):** development is on `feat/unify-phase2-tenant-shell`. Company login now mounts the original Phase 2 `App.vue`; master/user/production forms live inside its navigation. Tenant scene mappings and manual summaries use the company's MariaDB, while root `/` remains the separate, labelled simulator demo. Read [UNIFIED-SHELL-DELIVERY.md](../deliveries/UNIFIED-SHELL-DELIVERY.md) and [UNIFIED-SHELL-PROGRESS.md](../deliveries/UNIFIED-SHELL-PROGRESS.md). Older statements below about a separate operational UI describe the pre-integration state.

**Phase 3B P0 + parts CSV (2026-10-15):** [PHASE3B-OPERATIONS.md](../../guides/PHASE3B-OPERATIONS.md) describes company master data, editable individual permissions and the real manual production/report/correction workflow, API boundaries, run/QA and explicit P1/P2 gaps. Read its supported scope before the historical limitations below; [PHASE3B-PROGRESS.md](../deliveries/PHASE3B-PROGRESS.md) is the execution checkpoint.

**تحویل و تست دستی:** [PHASE3B-DELIVERY.md](../deliveries/PHASE3B-DELIVERY.md) — خلاصهٔ فارسی، ۶۸ تست موفق واقعی MariaDB، لینک CI، مسیر ورود و قابلیت‌های باقی‌مانده.

**Company administration usability update:** see [COMPANY-ADMIN-QUICKSTART.md](../../guides/COMPANY-ADMIN-QUICKSTART.md) for the simple add/edit company and no-email user/password workflow, local worker setup and connected browser QA. This authorized extension supersedes the original Phase 3A invitation-only/password-reset-not-built limitations; operational Phase 2 remains separate.

**Separate login entries:** `/owner/login` for the software owner, `/company/login` for company users, `/company/<code>/login` for the company's dedicated link. The old `/?accounts=1` entry/activation links remain compatible. See the quickstart above; frontend route selection never replaces server permissions.

**Latest implementation:** Phase 3A on `feat/phase3-company-accounts`; read `PHASE3-DELIVERY.md`, `DEVELOPER-GUIDE.md` and the update in `CURRENT-STATE.md`. Company-account API/database isolation passed real MariaDB CI (42 tests, no skips). Phase 2 remains independent. The consolidation baseline and historical caveats below describe the earlier pilot, not the full current Phase 3A capability.

**Consolidation date:** 2026-10-14; **baseline:** `e19016d` (`feat/smart-factory-pilot-next`, v0.6.0-pilot). Documentation consolidated into active branch `feat/smart-factory-pilot-next` after owner approval; no production code changes. This file is the preferred entry point for new ChatGPT/Codex sessions.

## What we are building / هدف اصلی

A **configurable, saleable industrial operations and monitoring platform**; Pouyeshgar's 16-machine job shop is the **first pilot, not the product boundary**. It must accommodate no-IoT manual counts/stoppages, assisted inputs and fully automated Edge/API data, as well as lines, jobs, orders and optional forecast/planning/inventory/logistics. Modules may be enabled independently. Do not force planning, QA, BOM, warehouse or OEE prerequisites on customers who only need daily counts.

## Canonical documents (read in this order)

1. **[PRODUCT-BLUEPRINT.md](../../PRODUCT-BLUEPRINT.md)** — full owner-approved vision, detailed examples and explicitly OPEN architecture/business choices. Read sections 16–30 in particular before designing modules. Long by intention: never turn it into a terse list of feature names.
2. **[CURRENT-STATE.md](../../CURRENT-STATE.md)** — implementation facts vs reported browser QA vs not tested; CI baseline and storage limitation.
3. **[ARCHITECTURE.md](../../ARCHITECTURE.md)** — _current_ modules/API/storage and _proposed_ future bounded contexts. Do not treat proposed designs as shipped.
4. **[UI-UX-SPEC.md](../../UI-UX-SPEC.md)** — approved interaction, layout, layers, graphs, visual QA and themes, with exact original references.
5. **[DECISIONS.md](../../DECISIONS.md)** — agreed decisions, unresolved options and rule for changes.
6. **[RUNBOOK.md](../../RUNBOOK.md)** — authoritative entry for pilot local execution and verification; deep operational commands in [PHASE2-DELIVERY.md](../deliveries/PHASE2-DELIVERY.md) and [PILOT-RUNBOOK.md](../research/PILOT-RUNBOOK.md).

## Historical source material, not competing authority

- [CODEX-SMART-FACTORY-HANDOFF.md](../../CODEX-SMART-FACTORY-HANDOFF.md), [UI-VISUAL-IMPLEMENTATION-CONTRACT.md](../research/UI-VISUAL-IMPLEMENTATION-CONTRACT.md): original implementation contract. Preserve as acceptance history; current working UX contract is UI-UX-SPEC.
- [PHASE2-DELIVERY.md](../deliveries/PHASE2-DELIVERY.md): evidence and details of completed v0.6 Phase 2; never delete while consolidating.
- [PHASE2-PROGRESS.md](../deliveries/PHASE2-PROGRESS.md): in-progress checkpoint (historical, superseded as current status).
- [PILOT-QA.md](../deliveries/PILOT-QA.md): v0.5 QA (historical); current QA described in PHASE2-DELIVERY.
- [PILOT-RUNBOOK.md](../research/PILOT-RUNBOOK.md): extended v0.5/v0.6 run commands and sample credentials/storage warnings; consulted via RUNBOOK.
- [workshop-brief.md](../research/workshop-brief.md), [first-milestone.md](../research/first-milestone.md), [dashboard-layers.md](../../dashboard-layers.md), [3d-operational-visualization.md](../research/3d-operational-visualization.md), [peer-layer-comparison.md](../research/peer-layer-comparison.md): original research, layout and history. In particular _workshop-brief_ said other-company support was only a future possibility; owner's newer explicit decision in PRODUCT-BLUEPRINT makes this a **confirmed product direction** while implementation remains incremental.
- [archive/DECISIONS-EARLY-PILOT.md](../DECISIONS-EARLY-PILOT.md): early historical decision notes; see canonical **DECISIONS.md** for current classification.
- [idea-inbox.md](../research/idea-inbox.md): raw unapproved suggestions and open questions; do not silently convert ideas into requirements.
- [hall-01-layout.md](../../hall-01-layout.md): physical workshop truth, NOT obsolete; preserve carefully.

## Important owner correction, 2026-10-14

**Company Account = one independent company = one tenant.** Provider sells selected modules and user-login seats, creates the first company admin; company admin manages internal users and permissions within purchased entitlements. Multiple sites/factories may belong to the one account, but three independent companies buy three separate accounts. See **[TENANCY-IDENTITY-DESIGN.md](../../TENANCY-IDENTITY-DESIGN.md) v0.2**. The previous v0.1 premise of several independent companies inside one tenant is rejected; do not implement it.

## Non-negotiable interpretation

- Reported/CI-tested != industrially validated. Pilot default storage is local JSON; MariaDB adapter uses one `pilot_state` JSON payload row and is NOT integration-tested on a real DB.
- Current authentication is local-pilot admin/viewer/edge and scoped to allowed equipment, NOT multi-tenant organizational RBAC.
- Simulator industrial data are 15-minute intervals; separate legacy minute-ingestion simulator exists. Not live Edge, ERP or PLC.
- OEE requires valid data and definitions; room/hall physical grouping is not a valid default KPI aggregation boundary. Explain gaps rather than invent values.
- Production without an order or plan is a first-class permitted path. Tenant-enabled modules, available data and user authorization are **different axes**.
- Current UX is substantially approved. Preserve real Three.js geometry, compact desktop layouts, three monitoring modes and Layer Manager; avoid a full visual rewrite.
- Never conflate company vs technology brand: pilot factory **Pouyeshgar**, platform/provider brand **SFP24** only where verified.

## Hand-off checklist for a future agent

1. Inspect **latest Git branch/HEAD**, read this map + canonical docs, inspect code and CI; never assume this document auto-updated after 2026-10-14.
2. Capture latest source-of-truth status in CURRENT-STATE, with tested/not-tested; identify any source drift.
3. Review business rule proposals with owner; decide one real workflow at a time. First useful vertical slice: factory/site → asset → shift/operator → flexible OP → manual or simulated count/stop → API/DB → time-scoped report.
4. Write/adjust decisions explicitly, including owner approval and consequences. No generic “build all modules” task.
5. Keep secrets, photos, local database, exported QA PNGs under ignored paths. Do not touch `main`, `next`, local deployment or stash without permission.

**Integration status (2026-10-14):** Canonical documents have been fast-forwarded into the active pilot branch. Do not merge the historical `docs/platform-product-blueprint` branch; its product text is already incorporated. Development continues only after owner-reviewed business decisions, and old code branches must not be resurrected.
