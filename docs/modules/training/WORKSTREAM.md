# وضعیت اجرا و ادغام ماژول آموزش

**مرجع جاری وضعیت ماژول؛ آخرین کد بررسی‌شده snapshot 243aa9b8 از work/11-skill-gap است.** توسعهٔ هسته با b3f203b مقایسه می‌شود؛ این دو شاخه merge نشده‌اند.

| موضوع | وضعیت |
|---|---|
| پیش‌نمایش تألیف مرحلهٔ سوم | JSON محلی + صفحه و Permission اختصاصی، تحویل گزارش‌شده در f57e23e |
| موتور LMS، آزمون، Skill Gap و Onboarding | طراحی تفصیلی؛ Runtime عملیاتی اجرا نشده |
| AI و RAG واقعی، upload/package importer | ساخته نشده |
| نیازمندی حساب شخصی فراگیر | جهت محصول ثبت‌شده؛ سیاست تجاری Seat و تغییر Identity باز |
| مجوز مرحلهٔ اجرایی بعد، merge و deployment | از مرتب‌سازی اسناد صادر نمی‌شود |

## قواعد هماهنگی

هویت Person/Account و Tenant از [هسته](../../core/IDENTITY-AND-ACCESS.fa.md) می‌آید؛ دادهٔ تخصصی و اعتبارسنجی متعلق به Training است. دیتابیس مستقل برای شرکت دیگر ایجادکردن، با ساخت Login/Person موازی فرق دارد. ماژول نباید به خرید Production/CMMS وابسته باشد تا آموزش پایه کار کند.

ادغام آینده باید تغییرهای محدود در registry/permission/shell/API و migrationها را فهرست کند؛ شمارهٔ migration شاخه‌ها قبل از merge تطبیق داده شود. هستهٔ درحال‌توسعه با نسخهٔ مبنای شاخهٔ آموزش یکی فرض نشود. [قرارداد ماژول پیشنهادی](../../contracts/MODULE-CONTRACT-DRAFT.md).

شواهد قدیمی build/typecheck/MariaDB در [WORKSTREAM اصلی](../../source-material/work-11/docs/modules/training/WORKSTREAM.md) حفظ شده‌اند؛ این فایل ادعای اجرای تازهٔ آن‌ها نمی‌کند. [مانیفست کد همان snapshot](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/243aa9b8b161ed1e9b91285068425386f86c5c5c/src/company/training/README.md).
