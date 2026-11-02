# راهنمای توسعهٔ جاری — ۲۰۲۶-۱۰-۲۸

ابتدا [START-HERE](START-HERE.md)، [معماری](ARCHITECTURE.md)، [وضعیت واقعی](CURRENT-STATE.md) و [تصمیم‌ها](DECISIONS.md) را بخوانید. نسخهٔ کامل راهنمای پیشین با قواعد تاریخی در [آرشیو](archive/state-2026-10-28/DEVELOPER-GUIDE.md) است؛ نشانی‌ها/شاخه‌های آن دستور اجرای جاری نیستند.

## محل کار و ابزار

شاخهٔ جاری codex/02-structure-audit در ریشهٔ مخزن است. main و demo/phase2 تاریخی/ارائه‌اند؛ merge/deploy/start خودکار نکنید. Node24 و pnpm11 طبق manifest و lockfile ریشه‌اند. WEB src/server، HTTP جاری services/ingest/edgebox و http-channels، lab حفظ‌شده services/ingest/server و labs/data-hub است. Graphify آزمایشی بیرون مخزن در D:/git/graphiify قرار دارد و مرجع حذف یا منبع حقیقت نیست.

## درزهای اجرایی

| موضوع | مرجع کد |
|---|---|
| هویت، خرید، ظرفیت ورود و نشست | server/platform/accounts/service.ts، identity و storage |
| تعاریف مشترک/فیلد ماژولی/کارت | src/company/definition-catalog.ts، definition-cards.ts، server/operations/master/definitions.ts |
| workspace | src/company/workspaces.ts، tenant-shell.ts، server/operations/workspaces.ts |
| قطعه، OP، منبع کاری و محل | server/operations/master/service.ts، scene.ts و resource-location.ts |
| ثبت/اصلاح/خلاصهٔ تولید | server/operations/production/service.ts، validation.ts، work.ts |
| پارامتر | server/operations/data-parameters.ts، src/company/DataDefinitionsPanel.vue |
| هاب و پروندهٔ اتصال | server/telemetry، src/telemetry/HubSourceWizard.vue و MessageStructurePrototype.vue |
| دریافت و پردازش | services/ingest/http-channels/structures.ts، projection.ts و edgebox/receiver.ts |
| فایل شرکت/کتابخانه | server/platform/storage/company-files.ts و server/operations/master/model-library.ts |

App.vue و SceneView.vue همان viewer واقعی‌اند؛ layout version1/metre، هویت تجهیز، تاریخ/شیفت و گزارش OP را برای بازآرایی ظاهری تغییر ندهید. ثبت تولید و گزارش‌های موجود مسیرهای عملیاتی دارند؛ title یک ماژول جدید را آماده نمی‌کند. تعریف عمومی پارامتر هنوز جای مصرف تخصصی موجودِ شمارش تولید ننشسته است.

## قواعد سرویس و امنیت

- actor از نشست سرور و اتصال از tenant_storage می‌آید؛ ID/DB ارسالی کاربر اتصال یا اختیار جدید نمی‌سازد. scoped deny، خرید و readiness قبل از query/mutation بررسی شوند. عنوان شغلی و تنظیم workspace مجوز نیستند.
- تغییر هویت/ظرفیت/فعال‌سازی زیر lock شرکت انجام می‌شود؛ آخرین مدیر فعال محافظت دارد. دعوت pending ظرفیت ورود اشغال نمی‌کند. active-humans-v1 سیاست فعلی آزمایشی است، نه قیمت‌گذاری قطعی.
- provider دادهٔ عملیاتی tenant را عادی نمی‌خواند؛ پشتیبانی از حساب با تأیید مجدد، دلیل، نام دقیق و grant محدود/زمان‌دار و audit است. برای دورزدن این مرز actor جعلی نسازید.
- lifecycle ساخت شرکت و آماده‌سازی pending/provisioning/failed/ready قابل ادامه است. DDL حساب provision از API جداست؛ خطا DROP خودکار ایجاد نمی‌کند. applied migration/checksum را ویرایش نکنید؛ اصلاح ساختار با migration افزوده و آزمون محیط خالی/ارتقا است.
- اطلاعات پایه در service مشترک بماند؛ ماژول دیگر قواعد قطعه/OP/افراد را کپی نکند و جدول‌هایش را بی‌قرارداد تغییر ندهد. جدول، سرویس، API و UI مرز مشخص داشته باشند؛ modular monolith فعلی را به موتور plugin عمومی تبدیل نکنید.
- optimistic version، transaction و audit قبل/بعد برای تغییر مؤثر حفظ شوند. اصلاح گزارش نهایی permission و دلیل می‌خواهد؛ ارسال گزارش فعلی همان تأیید چندمرحله‌ای نیست. محدودهٔ زمان/محصول/OP/واحد برای شمارش حفظ شود؛ OPهای متوالی به‌عنوان محصول نهایی جمع نشوند و مقدار ناموجود صفر نشود.
- frame، stage و timestampها مستقل‌اند؛ رخداد فرستنده، دریافت و گزارش را یکی نکنید. retry و تعارض نباید تاریخچه را خاموش overwrite کنند. API نمایش، به raw/credential خصوصی دسترسی عمومی نمی‌دهد.

## افزودن یک قابلیت

ابتدا سناریوی واقعی، ورودی/خروجی، مالک داده، prerequisite و permission را بنویسید. برای فیلد ساده contribution همان entity و برای موجودیت مستقل API/storage/scope خودش لازم است. قابلیت با readiness planned شروع می‌شود؛ registry/cart مجوز readiness یا خرید به شرکت اضافه نمی‌کند. فقط renderer موجود/ساخته‌شده به workspace وارد شود. [راهنمای extension](guides/DEFINITION-EXTENSIONS.md) و [سؤال‌های باز فرم ماژولی](product-notes/DATA-POINTS-AND-CONSUMERS.fa.md) ملاک‌اند.

اسکیما برای شرکت خاص یا job title خاص کپی نشود. migration افزوده، قواعد خاموش‌شدن ماژول با حفظ سابقه، دادهٔ ناقص و scope خروجی محاسباتی تست شوند. هیچ فیلد سفارشی منطق مهارت/OEE/هزینه را خودکار پیاده نمی‌کند.

آداپتور فایل/ERP آینده: actor معتبر + فایل/پاسخ + mapping version → parse/stage/خطای ردیف → preview → تأیید → transaction سرویس دامنه + idempotency/provenance. واردات نباید DB/SQL/credential/URL دلخواه بسازد یا خرید/مجوز را دور بزند. اتصال رسمی به ERP مشخص، spec و آزمون واقعی جدا می‌خواهد.

## اعتبارسنجی و پاک‌سازی

pnpm test:all، build:all و check:edgebox مرجع‌اند؛ شبیه‌سازها node --test مستقل دارند. تست شبکه‌ای به localhost موقت نیاز دارد؛ EACCES sandbox را با باگ محصول اشتباه نگیرید. DB integration با schemaهای تصادفیِ جدا و پایان‌پاک‌سازی خود تست انجام شود. browser/screenshot QA فقط پس از اجرای واقعی گزارش شود.

قبل از حذف فایل، import/dynamic registration/API/tool/test بررسی شود؛ Graphify وابستگی را کمک می‌کند ولی برخورد نام و routeهای رشته‌ای را کامل نمی‌فهمد. تست قدیمی صرفاً به خاطر سنش حذف نشود. benchmark/QA موقت، build/cache و دادهٔ شرکت را یکی نگیرید. هیچ رمز یا اطلاعات قابل شناسایی کاربر commit نشود.
