# قراردادهای مشترک هسته — Core & Shared

**مالکیت مشترک:** Identity، User/Person، Tenant، Seat/Entitlement، Permissions، Workspace، UI Shell، CompanyFiles، تعریف داده، سرویس‌های WEB و قراردادهای WEB/INGEST از آنِ ماژول خاصی نیستند. توسعه‌دهندهٔ ماژول به این اسناد **ارجاع** می‌دهد؛ با کپی‌کردن آنها هستهٔ دوم نمی‌سازد. فایل‌های سراسری زیر به‌خاطر ارجاع‌های فراوان در مسیر رسمی قبلی باقی مانده‌اند.

| مرجع هسته‌ای | مسیر معتبر |
|---|---|
| معماری، مالکیت و ذخیره‌سازی | [ARCHITECTURE](../ARCHITECTURE.md) |
| هویت و جداسازی Tenant | [TENANCY-IDENTITY-DESIGN](../TENANCY-IDENTITY-DESIGN.md) |
| حساب، دعوت، ظرفیت و مجوز | [PHASE3-COMPANY-ACCOUNTS-CONTRACT](../PHASE3-COMPANY-ACCOUNTS-CONTRACT.md) |
| Workspace و رابط مشترک | [UI-UX-SPEC](../UI-UX-SPEC.md) |
| وضعیت **واقعاً پیاده‌شده** | [CURRENT-STATE](../CURRENT-STATE.md) |
| چشم‌انداز و دامنهٔ کل محصول | [PRODUCT-BLUEPRINT](../PRODUCT-BLUEPRINT.md) |
| تصمیم‌های مشترک | [DECISIONS](../DECISIONS.md) |
| راهنمای توسعه/اجرای محیط | [DEVELOPER-GUIDE](../DEVELOPER-GUIDE.md)، [RUNBOOK](../RUNBOOK.md) |
| فایل‌ها و مسیر CompanyFiles | [LOCAL-FOLDERS](LOCAL-FOLDERS.fa.md) |
| داده، تعریف و فرم ماژولی | [DATA-POINTS-AND-CONSUMERS](DATA-POINTS-AND-CONSUMERS.fa.md)، [DEFINITION-EXTENSIONS](DEFINITION-EXTENSIONS.md) |
| حساب و شروع کار شرکت | [COMPANY-ADMIN-QUICKSTART](COMPANY-ADMIN-QUICKSTART.md) |
| نقش/پوزیشن و اختیار | [POSITION-TEMPLATES-AND-MODULES](POSITION-TEMPLATES-AND-MODULES.md) |
| قرارداد امضاشدهٔ دریافت داده | [packages/telemetry-contract](../../packages/telemetry-contract/README.md) — جای قرارداد تغییر نمی‌کند |

**ترتیب خواندن:** [START-HERE](../START-HERE.md) ← هستهٔ مشترک ← [README ماژول](../modules/README.md) ← سند موضوعی و کد واقعی. اگر سند تخصصی نیازمند اصلاح در هسته بود، قبل از تغییر Identity/DB/API/Permission با مالک هسته هماهنگ شود. کد و تست واقعی بر ادعای پیاده‌سازی در اسناد طرح مقدم‌اند.
