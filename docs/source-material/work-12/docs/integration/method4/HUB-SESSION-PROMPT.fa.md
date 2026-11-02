# دستور کار سشن هاب — روش ۴

تصمیم مالک: هاب دیگر محصول مستقل با شرکت/کاربر/پنل و SQLite جدا برای حالت integrated نیست. یک محصول با WEB و INGEST جدا، روی MariaDB اصلی با دیتابیس مجزای هر شرکت داریم. کد فعلی checkpoint گیت است؛ سازگاری مصنوعی با فرم‌های آزمایشی قبلی لازم نیست.

branch `codex/shared-telemetry-runtime-v1` از b9c43c162bc5be826f568a41e580f8cac17214ea ساخته شده؛ checkout آن خودکار انجام نشده تا کار جاری سشن قطع نشود. ابتدا status/HEAD را بررسی کن، تغییرات جاری را حفظ کن و فقط در همین branch یا worktree مستقل ادامه بده. main را تغییر/merge نکن. اگر branch موجود است آن را reset نکن.

بستهٔ مرجع را فقط از این مسیر بخوان:
`D:\git\pouyeshgar-workshop\.local\worktrees\integrated-telemetry-v1\docs\integration\method4`

همین بسته را با version/hash در `contracts/pouyeshgar-telemetry/1.1.0/` پروژه خودت ثبت کن؛ wire/storage همچنان1.0.0 است. README، SCENARIO، STORAGE-CONTRACT، storage-v1.json، device-batch، receipt و IMPLEMENTATION-STATUS لازم‌اند. برای فهم برنامه اصلی نیازی به خواندن کل repo نیست. دسترسی read-only این پوشه برای هماهنگی از سوی مالک مجاز شده؛ هیچ فایل/DB/سرویس برنامه اصلی را تغییر نده.

این پرامپت جهت روش مستقل AGENTS فعلی را در branch آزمایشی تصحیح می‌کند؛ ممنوعیت دست‌زدن به محیط زنده، secret و تست تجهیزات واقعی همچنان پابرجاست. در branch خودت سند معماری را مطابق همین تصمیم به‌روز کن، نه با کپی‌کردن کلی تاریخچه چت.

وظیفه تو B1–B5 در README قرارداد است: adapter async MariaDB، process INGEST، HTTP/MQTT/receipts، مصرف config نسخه‌دار، connectorهای محدود، worker health، فرمان عامل و simulator خارجی. API عمومی مدیریت شرکت و login جدید نساز. انتقال SQLite fixture/فرستادن داده به API قدیمی production انجام نده.

سشن اصلی مالک DDL/grant، identity/registry UI، bindings، خواندن و گزارش است. A1 اکنون در STORAGE-CONTRACT و storage-v1.json تحویل شده؛ adapter را دقیقاً بر همین نام‌ها و grants بنویس. ترتیب قفل، کنترل revision کلید در هر batch، vault مستقل و تفاوت schema1 با tenant migration10 را رعایت کن. SQL پیشنهادی تغییر را به سشن اصلی تحویل بده؛ migration applied را ویرایش نکن. DDL در runtime worker ممنوع.

پنل و صف فرمان و desired config سمت WEB حاضر است، اما ثبت queued/applied نباید موفقیت agent فرض شود. B3 مربوط به REST/file/database هنوز job/staging extension اجرایی مشترک ندارد و در UI جدید غیرفعال است؛ برای آن ابتدا پیشنهاد extension بده، سپس هر دو طرف نسخه‌دار بسازیم. مسیر قدیمی HTTP/REST/file در runtime پیش‌فرض WEB ثبت نمی‌شود و فقط regression test harness آن را فعال می‌کند؛ آن مسیر را مقصد integration جدید نگذار.

fixture دوطرفه با ابزار `tools/telemetry/Create-Fixture.ps1` برنامهٔ اصلی تولید می‌شود و خروجی آن زیر `.local/telemetry/private/fixture-platform_test_<run-id>/` است. برای تست هماهنگ، خواندن محلی فقط `ingest-runtime-private.json`، `ingest-vault/` و `device-profiles-private.json` همان fixture مجاز است؛ محتوای secret را در چت/گیت/لاگ نگذار. WEB vault، config دارای admin و دیتابیس شرکت‌های مالک را نخوان/تغییر نده. این fixture شرکت و۱۷ماشین/۱۸کانال دارد اما sample/binding ندارد. runtime profile قرارداد ورودی adapter است، نه ادعای اینکه loader هاب فعلی همین شکل را می‌خواند؛ loader خودت را صریح مطابق آن بساز و تست کن.

ورودی عمومی source است نه machine؛۱source→۱۶signal→۱۶resource و۲source→۲input یک resource سناریوی اجباری‌اند. شرکت از credential معتبر، نه topic/body/نام. تگ جدید ابتدا در پنل تعریف و export می‌شود. نوع اتصال آینده OPC UA discovery مجاز در معماری، ولی بدون implementation PASS نیست.

هر دو طرف schema/contract capabilities و build SHA را در health می‌دهند؛ قرارداد incompatible را fail-safe رد کن. shared-storage یعنی webhook داخلی برای کپی همه sensor sampleها لازم نیست؛ outbox خارجی می‌تواند قابلیت جدا بماند، نه مسیر اصلی پویشگر.

هر تغییر با commit روی branch خودت، conformance fixture مشترک و گزارش pass/fail/unverified. read/write فقط DB disposable موردتأیید، listener loopback؛ هیچ نصب جدید/تغییر service جاری/credential واقعی نیاز نیست. اگر برای اجرای fixture دسترسی لازم نیست، مانع را دقیق ثبت و کار مستقل را ادامه بده.

در پاسخ اول: SHA مبنا، version/hash بسته، قبول/ابهام قرارداد، گام B1 و interface موردنیاز از A1 را کوتاه بده؛ سپس کار مستقل مجاز را پیش ببر. با دریافت اسناد ادعای اتصال واقعی/تکمیل نکن. Merge/Deploy و migration روی شرکت‌های فعلی مرحله بعد با اجازه مالک است.
