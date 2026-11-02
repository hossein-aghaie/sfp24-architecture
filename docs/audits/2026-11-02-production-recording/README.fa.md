# ممیزی مستقل اسناد اجرایی SFP24

> **Status:** Audited observations, proposals not approved · **Date:** 2026-11-02  
> **Snapshot:** [pouyeshgar-workshop @ b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/START-HERE.md)  
> **Authorization:** اسناد کدکس فقط خوانده شده‌اند؛ هیچ فایل، برنچ، migration یا service تغییر نکرده است.

## روش و پوشش

در Git tree نسخه ثابت، ۶۰۱ مدخل وجود دارد. محدوده docs و دو راهنمای ریشه شامل **۱۲۶ فایل (۹۴ Markdown + ۳۲ فایل همراه)** بود. متن تمام فایل‌های Markdown برای یافتن لینک‌های نسبی متعارف بررسی و مسیر مقصد با درخت نسخه ثابت سنجیده شد. اسناد اصلی توسعه و هسته، اسناد فنی هاب و قرارداد و اسناد تاریخچه جدا خوانده و مقایسه شدند. لینک‌های بیرونی، همه شیوه‌های لینک در Markdown/HTML و runtime/QA را نباید از این کنترل نتیجه گرفت. **تست تازه MariaDB یا مرورگر انجام نشده است**.

## فهرست یافته‌های اولویت‌دار

| ID | اولویت | یافته | نوع |
|---|---|---|---|
| DOC-01 | بالا | [DEVELOPER-GUIDE:7](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/DEVELOPER-GUIDE.md#L7) و [CURRENT-STATE:7](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/CURRENT-STATE.md#L7) شاخه مرحله ۰۲ را «جاری» می‌نامند؛ [START-HERE](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/START-HERE.md#L1-L15) و [AGENTS](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/AGENTS.md#L6-L7) مرحله ۰۳ را جاری می‌دانند. | تناقض مستقیم راهنمای جاری |
| DOC-02 | بالا | [CURRENT-STATE:83](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/CURRENT-STATE.md#L77-L85) «میز صرفاً حافظه‌ای» را گزارش می‌کند، اما [CURRENT-STATE:150–154](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/CURRENT-STATE.md#L150-L154) ذخیره و انتساب میز را گزارش می‌کند؛ **محتوای عملیاتی داخل میز هنوز Preview است**. | متن زمانی قدیمی بدون نمای «اکنون» |
| DOC-03 | بالا | در فایل‌های immutable قرارداد rc.4 وضعیت candidate/draft وجود دارد؛ [approval sidecar](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/integration/telemetry-execution-v2-approvals.json) تأیید طراحی اما **عدم مجوز اجرا و عدم runtime acceptance** را می‌گوید. | ابهام تقدم وضعیت، نه الزاماً تعارض واقعی |
| DOC-04 | متوسط | [README:24](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/README.md#L24) «هیچ صفحه عمومی دمو ندارد» اما [operator-preview.html](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/operator-preview.html) و [entrypoint](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/src/operator-preview.ts) موجود و public fictional UI review معرفی شده‌اند. | ابهام «دموی محصول» در برابر Sandbox طراحی؛ نه اثبات Deploy |
| DOC-05 | متوسط | [DECISIONS:46–48](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/DECISIONS.md#L46-L48) امکان چندسایتی را دارد؛ [DECISIONS:92–96](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/DECISIONS.md#L92-L96) یک کارخانه در مدل فعلی را ثبت کرده است. | دو Scope/دوره تصمیم؛ نیازمند precedence صریح |
| DOC-06 | متوسط | [AGENTS:4](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/AGENTS.md#L4) خواندن handoff تاریخی را لازم می‌داند؛ [handoff](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/CODEX-SMART-FACTORY-HANDOFF.md#L1-L6) برنچ قدیمی را نام می‌برد. | خطر خواندن دستور تاریخی به‌جای جاری |
| DOC-07 | متوسط | ارجاعات آرشیو بعد از جابه‌جایی و شش PNG خارج از Git قابل بازکردن نیستند؛ [جزئیات](LINK-REPORT.fa.md). | نقص دسترسی به شواهد تاریخی |
| DOC-08 | متوسط | از ۵۲ فایل غیرآرشیوی منبع، **۲۳ مورد عیناً در این مخزن موجود** و ۲۹ مورد کپی متناظر ندارند؛ [دسته‌بندی](MIGRATION-COVERAGE.fa.md). | پوشش اسناد، نه حکم به کپی همه فایل‌ها |

## موارد درست که باید حفظ شوند

- [ARCHITECTURE](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/ARCHITECTURE.md) حد واقعی modular monolith، ownership WEB/INGEST، Person/Account و Tag/Parameter/Consumer را صریح تفکیک کرده است.
- [Product Blueprint](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/PRODUCT-BLUEPRINT.md) چشم‌انداز متنوع و سناریوهای بدون برنامه، Forecast و Order را از تحویل واقعی جدا می‌کند.
- [DECISIONS](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/DECISIONS.md) بسیاری از اصلاحات قبلی را با تاریخ نگه داشته است. اسناد آرشیو به‌صورت هدفمند hash-preserved هستند؛ تکرار تاریخی را با موازی‌نویسی فعال اشتباه نگیریم.
- اعداد تست در اسناد، **گزارش اجرای قبلی** هستند نه آزمایش انجام‌شده در این ممیزی.

## اقدام پیشنهادی

اصلاح فوری **فقط راهنمای وضعیت جاری** در repo اجرایی، با حفظ آرشیو. سپس یک entrypoint دقیق برای status قرارداد rc.4، یک نقشه «مدل فعلی/هدف چندسایتی»، و navigation overlay برای لینک‌های آرشیوی. تغییر قرارداد امضاشده، حذف آرشیو و اعلام SDK جدید از این گزارش نتیجه نمی‌شود.

[جزئیات اختلاف](DOCUMENT-DRIFT.fa.md) · [گزارش لینک](LINK-REPORT.fa.md) · [پوشش انتقال](MIGRATION-COVERAGE.fa.md) · [معماری هسته](../../core/README.md).
