# نقشهٔ جاری داده و فایل‌ها — ۲۰۲۶-۱۰-۲۸

> نسخهٔ راهنمای موضوعی؛ کد مبنا b3f203b، بازبینی انتقال ۲۰۲۶-۱۱-۰۲. متن اولیه در [کاتالوگ منابع](../../sources/CATALOG.md) محفوظ است. دستورها برای مخزن محصول و محیط مشخص همان نسخه‌اند؛ خود مخزن اسناد اجرا نمی‌شود.


این سند محل نوشتن/خواندن فعلی را مشخص می‌کند. اندازه‌ها و محل‌های تاریخی با متن کامل در [آرشیو](../../source-material/work-12/docs/archive/state-2026-10-28/guides/LOCAL-FOLDERS.fa.md) حفظ شده‌اند؛ مسیر قدیمی دستور اجرای تازه نیست.

## فایل شرکت

ریشهٔ فعلی D:/git/pouyeshgar-workshop/.local/companies است؛ با companyFilesDirectory یا COMPANY_FILES_ROOT می‌توان محل استقرار را عوض کرد. مسیر بر اساس UUID ثابت است، نه نام قابل ویرایش:

```text
<company-files-root>/
  <company-uuid>/
    telemetry/sources/<source-or-draft-uuid>/
      draft.enc
      images/<sha256>.png|jpeg|webp
    library/models/
      <model-uuid>.glb
      <model-uuid>.json
```

CompanyFiles مرجع واحد است. draft AES-256-GCM با AAD شرکت/ID، سقف۱MiB، version/CAS و rename اتمی دارد؛ عکس تا۱۵۰KiB و۲۰۴۸×۲۰۴۸ با بایت اصلی/شفافیت حفظ می‌شود. تصویر و GLB خصوصی و tenant-scoped‌اند؛ این root را public/static نکنید. حذف یا تعویض عکس خودکار فایل immutable قبلی را پاک نمی‌کند؛ حذف فایل بی‌مرجع سیاست جدا لازم دارد. این پوشه cache نیست.

پس از پاک‌سازی، library، API مدل و اعتبارسنجی scene همگی همین ریشه را می‌خوانند. فایل‌های قدیمی شرکت جاری از .local/company-models به مقصد واحد کپی و hash تأیید شدند؛ fallback خواندن آن پوشه و vault/telemetry-wizards حذف شده است. فایل‌های بازنشستهٔ قبلی فقط در آرشیو خصوصی cleanup هستند، نه مسیر فعال. ریشهٔ سفارشی در تست‌ها بررسی شده است.

## بقیهٔ اطلاعات کجا هستند؟

| داده | محل/مالک |
|---|---|
| حساب‌ها، خرید، ظرفیت ورود، مجوز | DB مرکزی platform؛ رمز ورود کاربر hash نمک‌دار scrypt است |
| قطعه، OP، تجهیز، scene، پارامتر و گزارش | DB مستقل tenant همان شرکت؛ نگاشت در tenant_storage مرکزی |
| raw، تشخیص و نمونهٔ معتبر هاب | جدول‌های DB همان tenant؛ فرایند INGEST جداست |
| عکس منبع، draft و کتابخانه | root واحد CompanyFiles بالا |
| لوگوی کارخانه | data URL محدود در sites؛ این فیلد کتابخانهٔ رسانهٔ عمومی نیست |
| credential اتصال DB | vaultDirectory در تنظیمات خصوصی؛ برای سرور قابل بازیابی، نه hash رمز کاربر |
| کلید دستگاه | vaultDirectory/telemetry-keys رمزگذاری‌شده، وابسته به HUB_ENCRYPTION_KEY |
| کلید رمزگذاری | .local/data-sources/private/encryption-key در این محیط؛ گم‌شدن آن با DB جبران نمی‌شود |
| تنظیم API/worker | .local/local-launcher/private/runtime.json و provision.json؛ اعتبار DDL جدا |
| فایل زندهٔ MariaDB | .local/phase3/data طبق mariadb-test.ini؛ مدیریت با خود MariaDB، نه حذف پوشه |
| نرم‌افزار MariaDB | .local/phase3/mariadb؛ برای اجرای محیط لازم است و cache نیست |
| build/cache وابستگی | dist، node_modules/.vite، pnpm-store؛ قابل تولید مجدد ولی نصب ممکن است به شبکه وابسته شود |
| شواهد QA و آرشیو خصوصی | .local/qa و .local/archive؛ credential/دادهٔ خصوصی ممکن است داشته باشند و وارد Git نشوند |
| Graphify مستقل | D:/git/graphiify؛ محصول به آن وابسته نیست |

## انتقال به سرور

فایل‌های دائمی از نسخهٔ کد جدا باشند و rootها از config بیایند. DB مرکزی، DBهای tenant، root فایل شرکت، vault و کلیدها باید هماهنگ و با دسترسی محدود منتقل شوند؛ فقط ZIP سورس یا پوشهٔ عکس، شرکت را بازسازی نمی‌کند. credentialهای provision وارد API نشوند. dump/restore معتبر جای کپی datadir زنده است. صرف ساخت پوشهٔ backup، پشتیبان یا آزمون restore نمی‌سازد؛ backup زمان‌بندی‌شده و بستهٔ بازیابی کامل هنوز اجرا نشده‌اند.

وجود raw در DB شرکت، مانع جداسازی آینده نیست؛ آداپتور و migration/test لازم است و عوض‌کردن صرف connection string کافی نیست. هدف چندکارخانه‌ای محصول با محدودیت فعلی رابط یک کارخانه/شرکت فرق دارد.

## حدود پاک‌سازی

.local را یکجا حذف نکنید. pnpm-store ممکن است با نصب دموی فاز۲ مشترک باشد و node_modules hardlink داشته باشد؛ جمع اندازه‌ها، فضای آزادشدنی واقعی نیست. برای دادهٔ آزمایشی، اول control/tenant/reference/live connection شناسایی، سپس SQL DROP محدود؛ پوشهٔ schema را دستی پاک نکنید. حساب‌ها و فایل‌های مرتبط باید با هم بررسی شوند. ابزار/دموهای checkout دیگر در پاک‌سازی محصول تغییر نمی‌کنند.
