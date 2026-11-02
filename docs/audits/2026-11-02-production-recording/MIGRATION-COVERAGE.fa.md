# پوشش انتقال منابع به معماری

> **Status:** Git blob SHA comparison · **Source commit:** b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f

در محدوده ۵۲ فایل غیرآرشیویِ docs + AGENTS/README، **۲۳ فایل** با همان Git blob SHA در `sfp24-architecture` پیدا شدند؛ **۲۹ فایل** فاقد کپی برابر بودند. این عدد به معنی ضرورت انتقال همه ۲۹ فایل نیست؛ بسیاری سند اجرای محیط یا فایل اسکریپت و fixture هستند.

## قبلاً حفظ‌شده با SHA یکسان

- [معماری هسته](../../source-material/work-12/docs/ARCHITECTURE.md)، [وضعیت واقعی](../../source-material/work-12/docs/CURRENT-STATE.md)، [تصمیم‌ها](../../source-material/work-12/docs/DECISIONS.md)، [Product Blueprint](../../source-material/work-12/docs/PRODUCT-BLUEPRINT.md).
- [Data/Parameters](../../source-material/work-11/docs/core/DATA-POINTS-AND-CONSUMERS.fa.md)، [طرح هاب](../../source-material/work-12/docs/integration/HUB-TAG-PUBLICATION-DESIGN.fa.md)، [Method4 storage](../../source-material/work-12/docs/integration/method4/STORAGE-CONTRACT.fa.md).

## مدارک مهمِ بدون کپی در معماری

| سند با revision ثابت | ارزش تاریخی یا مرز مالکیت |
|---|---|
| [Approval records](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/integration/telemetry-execution-v2-approvals.json) | روشن‌کردن تأیید طراحی rc.4؛ status مستقل از package امضاشده |
| [Structure Audit](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/migrations/STRUCTURE-AUDIT-2026-10-28.json) | دلیل تغییرات پاک‌سازی و جلوگیری از تکرار تصمیم‌های شکست‌خورده |
| [Company Administration](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/guides/COMPANY-ADMIN-QUICKSTART.md) | محدودیت‌های Seat، Invitation و Support |
| [Hall 01 layout](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/hall-01-layout.md) | زمینه صنعتی واقعی و حفاظت هویت منابع |
| [Local folders](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/guides/LOCAL-FOLDERS.fa.md) | چرایی CompanyFiles و مکان داده خصوصی |
| [Monorepo transition](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/migrations/TELEMETRY-MONOREPO.fa.md) | استدلال جدایی دو Runtime و مرز WEB/INGEST |
| [Canonical signed telemetry contract](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/packages/telemetry-contract/README.md) | **فقط لینک؛ نسخه رسمی دوم از contract امضاشده نسازیم** |

**نقشه انتقال مطلوب:** سندهای تصمیم‌سازِ تاریخی می‌توانند با حفظ متن/منشأ/هش در بخش Historical Evidence نگهداری شوند. ابزارها، secretها، SQL/Migration اجرایی و اسناد لازم برای شروع همان کد، زیر مالکیت repo اجرایی باقی بمانند. تا تکمیل فهرست و رفع وابستگی‌های آرشیوی، ادعای «تمام اسناد تاریخی قابل حذف‌اند» مجاز نیست.
