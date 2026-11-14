# SFP24 — بستهٔ اجرایی پیشنهادی هسته، ماژول، میز و دو شرکت آزمایشی

> **Status:** PROPOSED EXECUTABLE SPEC v0.1 — not approved, not implemented, not tested.  
> **Date:** ۲۰۲۶-۱۱-۰۵ · **Branch:** `docs/recovered-session-core-workspace-2026-11-05`.  
> **Code snapshot investigated:** `hossein-aghaie/pouyeshgar-workshop`، `codex/04-core-workspaces-dashboard`، SHA `5c7ac617f95ee8b84cbd32d7fa8e7474a073ec97`.  
> **این بسته مجوز کدنویسی/ادغام نمی‌دهد.** مرحلهٔ Stage04 فعلاً Discovery فقط‌خواندنی است؛ Codex برای تغییر کد نیازمند مجوز تازهٔ صاحب محصول و انتخاب شاخه/مبنای جدید است.

## چه می‌خواهیم؟

بستر مشترک برای ساخت شرکت با حداقل اطلاعات، معرفی Capability و نیاز دادهٔ هر ماژول، ارتباط Module↔Core و Module↔Module، ثبت و پیگیری Request/WorkOrder، Task/Decision/Notification/Evidence بدون تحمیل تأیید صوری، و نمایش واقعی در Desk/Form/Profile/Dashboard/Inbox/3D.

این بسته **کامل نسبت به پایلوت مصوب‌نشدهٔ محدود** است؛ نه وعدهٔ پیاده‌سازی هم‌زمان همهٔ ۴۴ حوزه. دامنهٔ اجرایی مشخص: **Production موجود + Maintenance سبک** با دو Tenant کاملاً ساختگی و سناریوهای کوچک/پیشرفته.

## ترتیب مطالعه و خروجی‌ها

1. [۰۱ — قراردادهای دقیق هسته، رجیستری، داده، Readiness و Action](01-CONTRACTS-AND-DATA.fa.md) — مرز و نوع داده، قابلیت‌های دو ماژول، رفتار خطا و عدم تکرار.
2. [۰۲ — State Machine، Schema، API، Permissions، UX و دستورکار بسته‌به‌بستهٔ Codex](02-CODEX-WORK-PACKAGES.fa.md) — مشخصات افزوده/حفظ‌شده/ممنوع، ۶ Work Package و معیار توقف.
3. [۰۳ — کارخانه‌های ساختگی و ۵۳ آزمون پذیرش](03-DEMO-AND-ACCEPTANCE.fa.md) — دادهٔ نمونه، مسیرهای واقعی، امنیت، UI، Crash/Retry، راه‌های QA و قالب گزارش.

**اسناد منبع و نه سند موازی:** [Domain Interaction Contract Draft v0.1](../../contracts/DOMAIN-INTERACTION-CONTRACT-DRAFT.md)، [Module Contract Draft](../../contracts/MODULE-CONTRACT-DRAFT.md)، [Data Contract Draft](../../contracts/DATA-CONTRACT-DRAFT.md)، [UI Contribution Draft](../../contracts/UI-CONTRIBUTIONS-DRAFT.md)، [گفت‌وگوی این جلسه](../../journal/2026-11-05/CORE-MODULE-REQUIREMENTS-UX-INTEGRATION-SESSION.fa.md)، [نقد ۴۴ حوزه](../../journal/2026-11-05/CORE-OPERATIONS-UX-DESIGN-AND-REVIEW.fa.md).

## تقدم اسناد و حل تعارض

- Reality کد از کد SHA مذکور تعیین می‌شود؛ این Spec وجود ماژول جدید را اثبات نمی‌کند.
- ADR/Contract مصوب در صورت تعارض بر این Spec پیشنهادی اولویت دارد؛ **Codex نباید تعارض را خودش با تغییر Permission/Schema حل کند**.
- نکات نهاییِ این بسته انتخاب‌های مهندسی برای جلوگیری از «حدس Codex» هستند، اما برای اجرا **تأیید مالک** لازم دارند.
- وقتی نسخهٔ کد جلو رفت، WP-00 باید اختلاف را پیش از کدنویسی گزارش دهد و فایل‌های جدید تنها با مبنای تأییدشده اجرا شوند.

## مرز Release و قابلیت‌های عمداً خارج از Pilot

در پایلوت، Maintenance صرفاً درخواست خرابی، ارجاع، ثبت کار و شواهد، تحویل و نتیجه، به همراه Profile/Inbox/Bell/Dashboard است. PM، MRP، APS/Planning، OEE کامل، Inventory/WMS، LIMS، Skill Gap اجرایی، PTW واقعی، فرمان TAG.OUT/PLC، امضای قانونی، پرداخت حقوق، فرم‌ساز آزاد و Plugin Runtime **در این Pilot تحویل داده نمی‌شوند**. قراردادها طوری پیشنهاد شده‌اند که برای این حوزه‌ها در آینده مرز اتصال داشته باشند، ولی پیاده‌سازی‌شان نیازمند Spec جداست.

## به‌جای دستور کلی «کل هسته را بنویس»

**اول WP-00**: فقط خواندن واقعی کد/مهاجرت/تست‌ها و تثبیت SHA مبنای تازه و گزارش وضعیت؛ همان‌طور که Stage04 read-only اعلام کرده است. پس از پذیرش و مجوز صریحِ همان بسته، **WP-01** Registry/Readiness/Typed Reference؛ سپس WP-02 Domain، WP-03 Tasks/Events/Bell، WP-04 UI Runtime، WP-05 دو Fixture و آزمون. هر بسته خروجی/آزمون/شرط توقف دارد.

**قبل از اولین تغییر کد باید چهار اجازه/تصمیم روشن باشد:**
1. تأیید طرح پایلوت و مرزهای Product/Permission/Owner و دو Policy پیشنهادی، یا بیان تغییرهای دقیق.
2. قفل‌کردن نسخهٔ نهایی اسناد/ADR/Contract برای همان دامنه و SHA مبنا.
3. انتخاب برنچ تازهٔ کد، چون Stage04 کنونی read-only است.
4. اجازهٔ تغییر فایل، DB Migration و تست‌ها **فقط برای Work Package نام‌برده**. تأیید WP-01 مجوز WP-02 نیست؛ Merge/Deploy اجازهٔ جدا لازم دارد.

## شواهد پایان کار

این مخزن فقط سند فراهم می‌کند. گزارش PASS زمانی مجاز است که Codex کد را در شاخهٔ خودش بنویسد، تست‌ها را واقعاً اجرا کند، PR بدهد و نتیجهٔ اجرای هر آزمون در [فایل ۰۳](03-DEMO-AND-ACCEPTANCE.fa.md) مطابق PASS/FAIL/NOT_RUN ثبت شود. Mock/PTW Stub نمی‌تواند ایمنی واقعی یا ماژول ساخته‌نشده را اثبات کند.
