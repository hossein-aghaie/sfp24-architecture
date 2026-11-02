# ممیزی قرارداد داده و توسعه تعاریف شرکت

> **Status:** Evidence-based audit / Proposed boundaries · **Owner:** Core/Data · **Updated:** 2026-11-02

## منابع موجود در همین مخزن
- [مرجع کامل تگ، پارامتر، مصرف‌کننده و فرمول](../source-material/work-11/docs/core/DATA-POINTS-AND-CONSUMERS.fa.md)
- [گسترش تعریف و فرم، نسخه اصلی](../source-material/work-11/docs/core/DEFINITION-EXTENSIONS.md)
- [Data Hub workflow](../source-material/work-12/docs/guides/DATA-HUB-WORKFLOW.fa.md)
- [قرارداد طراحی انتشار تگ](../source-material/work-12/docs/integration/HUB-TAG-PUBLICATION-DESIGN.fa.md)
- [قرارداد Storage Method 4](../source-material/work-12/docs/integration/method4/STORAGE-CONTRACT.fa.md)
- [معماری اجرایی snapshot](../source-material/work-12/docs/ARCHITECTURE.md)

## مرزهایی که نباید از دست بروند

| مرز | دلیل |
|---|---|
| INGEST vs WEB | دریافت و مدیریت داده خام/valid با اختیار کسب‌وکار و مصرف UI یک مسئولیت نیستند |
| raw signal vs typed tag | ثبت مقدار خام به معنای معتبر بودن صنعتی نیست |
| tag vs parameter | Parameter دارای معنا، نوع/واحد، موضوع، منبع و نسخه تبدیل است |
| parameter vs official report | منطق رسمی شمارش/کیفیت/بازه به ماژول مربوط تعلق دارد |
| module extension vs new business entity | افزودن فیلد ساده به Person با موتور کامل شایستگی و آزمون یکی نیست |
| widget vs KPI engine | نمایش یک مقدار به معنی داشتن شاخص صنعتی معتبر و audit-ready نیست |

## وضعیت مستند Extension
در طراحی موجود دو مسیر مستقل هستند: **Extension تعریف موجود** و **Entity/فهرست تخصصی مستقل**. Registry تعریف در کد قابل اعتماد است؛ metadata مشتری به‌صورت خودکار schema/SQL امن تولید نمی‌کند. ذخیره فیلد پایدار نیازمند Migration و سرور/اعتبارسنجی متناظر است. hidden UI ≠ backend authorization. `requiredFor` نباید همه شرکت‌ها را به پرکردن فیلد یک ماژول اختیاری مجبور کند.

## مسائل باز
- واحد/بازه/کیفیت/نسخه قرارداد محاسبات چندپارامتری چیست؟
- وقتی ماژول غیرفعال می‌شود، داده Extension و projection آن چه وضعیتی می‌یابد؟
- مالکیت Version و Transform کجاست؛ Core Data یا Domain Module؟
- دسترسی سایر ماژول‌ها چگونه فقط از typed contract باشد، نه Query پایگاه داده مجاور؟

این تحلیل **اجرای جدیدی را ادعا نمی‌کند**. [Data Draft](../contracts/DATA-CONTRACT-DRAFT.md) · [Module Draft](../contracts/MODULE-CONTRACT-DRAFT.md).
