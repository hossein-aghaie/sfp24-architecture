# منابع تاریخی — نگهداری متن اصلی، نه مرجع جاری

> **Status:** historical evidence / immutable copies · **Reviewed:** 2026-11-02

**مرجع طراحی جدید:** [START HERE](../START-HERE.md)، [هسته](../core/README.md)، [ماژول‌ها](../modules/README.md)، [تصمیم‌ها](../decisions/README.md).  
شناسه‌های قدیمی فقط برای انتساب منشأ فایل‌اند. هیچ ایجنتی نباید نام برنچ قدیمی را مبنای تصمیم/پیاده‌سازی فعلی بگذارد.

| گروه | مسیر آرشیو داخلی | کاربرد |
|---|---|---|
| هسته و چشم‌انداز | [معماری snapshot](work-12/docs/ARCHITECTURE.md)، [Product Blueprint](work-12/docs/PRODUCT-BLUEPRINT.md)، [Current State](work-12/docs/CURRENT-STATE.md) | فهم زمینه طراحی و وضعیت زمانی |
| هویت/مجوز | [Tenancy](work-12/docs/TENANCY-IDENTITY-DESIGN.md)، [Accounts](work-12/docs/PHASE3-COMPANY-ACCOUNTS-CONTRACT.md) | علت مدل حساب و جای بحث‌های باز |
| داده | [Data and Consumers](work-11/docs/core/DATA-POINTS-AND-CONSUMERS.fa.md)، [Extensions](work-11/docs/core/DEFINITION-EXTENSIONS.md) | بررسی منابع و محدودیت‌های سابق |
| آموزش | [Training originals](work-11/docs/modules/training/README.md) | ۱۰ سند اصلی و فهرست موضوعی |
| تاریخچه میز کار | [Thinking Aloud](work-12/docs/workstreams/work-12/THINKING-ALOUD.fa.md) | بحث تاریخی؛ نه specification |
| ارتباط صنعتی | [Tag publication](work-12/docs/integration/HUB-TAG-PUBLICATION-DESIGN.fa.md)، [Method 4](work-12/docs/integration/method4/README.fa.md) | آزمون استدلال و شواهد قبلی |
| تست/پاک‌سازی قدیمی | [Consolidation manifest](work-12/docs/migrations/DOCUMENT-CONSOLIDATION-2026-10-28.json) | منشأ تغییرات تاریخی |

**محدودیت‌ها:** این archive فقط فایل‌های گزینش‌شده است. لینک‌های نسبی در متن‌های تاریخی ممکن است به فایل‌هایی اشاره کنند که منتقل نشده‌اند. متون در انتقال دست‌نخورده مانده‌اند؛ Git blob SHA با نسخه منبع تطبیق داده شده، ولی محتوای فنی/ادعاهای اجرا مجدداً تست نشده‌اند.

## Snapshot records
- مجموعه تاریخی آموزش/هسته: revision `243aa9b8b161ed1e9b91285068425386f86c5c5c`
- مجموعه تاریخی میز کار/هسته: revision `19b644c791ab3c228513db3aeb6e53b3e7389bd8`

این revisionها **شناسه provenance** هستند، نه مرجع فعلی که بعد از حذف برنچ به آن وابسته باشیم. برای آرشیو صددرصد مستقل، فایل‌های ارجاع‌شده اما هنوز منتقل‌نشده باید جداگانه ممیزی شوند.
