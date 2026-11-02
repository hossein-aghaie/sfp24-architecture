# وضعیت اجرایی روش۴ — ۲۰۲۶-۱۰-۱۸

branch برنامهٔ اصلی: `codex/integrated-telemetry-v1` از `c0241d83a2d3a64668088f2b958232a002e1b1d1`؛ worktree: `D:\git\pouyeshgar-workshop\.local\worktrees\integrated-telemetry-v1`. SHA تحویل را از آخرین commit همین branch بخوانید؛ این سند همراه کد نگهداری می‌شود.

بستهٔ هماهنگی **1.1.0**، wire/storage **1.0.0**، component schema **1**، control migration **8** و tenant migration **10**. CHANGELOG و manifest جدید باید کامل به سشن هاب برسد.

| مورد                                                          | وضعیت واقعی                                                                                          |
| ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| DDL دقیق و grants WEB/INGEST                                  | پیاده‌شده؛ storage-v1.json خروجی مستقیم schema.ts؛ فقط provisioner مالک DDL                          |
| registry، config، rotation، rename/retire                     | API و UI فارسی/انگلیسی؛ کلید یک‌بار، optimistic revision و audit                                     |
| source مستقل از ماشین                                         | پیاده‌شده؛۱منبع→۱۶کانال→۱۶ماشین، تخصیص گروهی و اعتبار زمانی تست شده                                  |
| count و wast مستقل برای یک ماشین                              | معنا/واحد بررسی می‌شود؛۱۲۳ تولید و۳ ضایعات→۱۲۰ سالم تا ثبت نهایی و بازیابی PASS                      |
| تعداد متصل/ضایعات دستی یا برعکس                               | هر دو ترکیب روی DB واقعی تا گزارش نهایی PASS                                                         |
| raw و evidence                                                | نمونه فقط telemetry_samples؛ evidence شامل مجموع و reference/hash است؛ کپی به hub_measurements نشده  |
| تکرار گزارش و late conflict                                   | claim/قفل/snapshot؛ گزارش تکراری رد می‌شود؛ preview منتظر commit می‌ماند و گزارش نهایی قبلی ثابت است |
| تازه‌سازی cross-process                                       | SQL clock/changes پایدار و long-poll؛ message bus/CDC ندارد                                          |
| desired/reported و health                                     | منبع ثبت‌شده به معنی متصل نیست؛ heartbeat worker با روشن‌بودن ماشین یکی نیست                         |
| صف درخواست عامل                                               | get_status/pause/resume با UUID/TTL و idempotency؛ اجرای agent جدید NOT VERIFIED                     |
| receiver قدیمی WEB                                            | در runtime پیش‌فرض ثبت نمی‌شود؛ فقط harness صریح regression tests فعالش می‌کند                       |
| fixture و credential worker                                   | ابزار guarded و vault مستقل؛ فایل‌های خصوصی زیر .local و خارج از Git                                 |
| listener HTTP/MQTT و adapter هاب                              | متعلق به branch سشن هاب؛ در این تحویل NOT VERIFIED                                                   |
| wire dedup/MQTT receipt/قطع شبکه/config applied/agent timeout | نیازمند conformance مشترک؛ SQL/read tests اثبات این‌ها نیستند                                        |
| REST/CSV/XLSX/database-read جدید                              | job/staging extension مشترک هنوز ساخته نشده؛ گزینه‌ها در UI جدید غیرفعال‌اند                         |
| OPC UA/Sparkplug/رویداد ساختاریافتهٔ دوربین و هویت            | آینده؛ پیاده‌شده اعلام نشده‌اند                                                                      |
| ظرفیت و فشار عملیاتی                                          | benchmark نشده؛ mutex کوتاه per-tenant و query محدود جای اندازه‌گیری را نمی‌گیرد                     |
| launcher نهایی دوفرایندی                                      | پس از مشخص‌شدن دستور و پورت branch هاب؛ Start-All قدیمی برای fixture جدید نیست                       |
| شرکت‌ها/سرویس‌های فعلی و geometry                             | تغییر، migration یا seed روی آن‌ها انجام نشد؛ صحنه و چیدمان محفوظ‌اند                                |
| repo و چت هاب                                                 | کد/checkout آن تغییر داده نشد و پیامی به آن چت ارسال نشد                                             |

## شواهد

- مجموعهٔ کامل: **۱۳۳ تست PASS، صفر fail/skip** با MariaDB واقعی ایزوله، browser QA و fixture export. این مجموعه تست‌های تاریخی را هم شامل می‌شود؛ PASS آن‌ها ادعای receiver جدید نیست. مقادیر سناریوی جدید از fixture SQL با credential محدود worker آمده‌اند.
- typecheck، build و storage export --check: PASS. tools/telemetry به محدودهٔ TypeScript اضافه شده است. اسکریپت PowerShell سازندهٔ fixture از نظر syntax بررسی شده و مسیر export از تست واقعی اجرا شده است.
- negative grants: worker نه کاربران/ماشین‌ها را می‌خواند، نه گزارش یا تعریف تگ را تغییر می‌دهد، نه نمونه حذف می‌کند و نه DDL می‌زند. route view و shared lock با user محدود تست شدند.
- rollback و fresh connection: retry نامعتبر receipt/sequence نیمه‌کاره باقی نمی‌گذارد؛ اتصال تازه تغییرات durable را می‌بیند. schema افزایشی با کف سازگار پذیرفته و کف ناسازگار رد شده است.
- Chrome واقعی: ساخت۱۶کانال، مشاهدهٔ تخصیص‌ها، فارسی/انگلیسی در۱۳۶۶×۷۶۸ و۳۹۰×۸۴۴، بدون pageerror و overflow افقی کل صفحه. پس از بازبینی تصویر، نمایش موبایل به کارت تبدیل و روی fixture با runtime پیش‌فرض WEB دوباره تست شد. این QA کامپوننت واقعی+API+DB است، نه تأیید کل shell یا receiver هاب.
- تصاویر/نتیجهٔ محلی: `.local/qa/telemetry-browser/`، ignored. هیچ credential یا fixture تولیدی در Git نیست.

fixture تمیز این تحویل: `.local/telemetry/private/fixture-platform_test_3bfc020c2044/`؛۱۷ماشین و۱۸کانال، بدون sample/binding اولیه. fixture با suffix `019c31537c48` برای QA نهایی مصرف شد و source اضافی دارد؛ برای شروع تمیز از مورد نخست یا Create-Fixture تازه استفاده کنید. سشن هاب فقط ingest-runtime-private.json، ingest-vault و device-profiles-private.json همان fixture را بخواند؛ مقدار secret در این سند نیست.

## مرز تحویل

بخش WEB و schema لازم برای B1/B2 آماده است؛ دریافت end-to-end روش۴ هنوز پذیرفته‌شده نیست. سشن هاب بستهٔ جدید را با hash بخواند، adapter را دقیق بسازد و نتیجهٔ HTTP/MQTT/retry/conflict/config/command را برگرداند؛ سپس هر دو branch روی fixture مشترک آزمایش شوند. B3 به extension نسخه‌دار مشترک نیاز دارد و نباید schema/job حدسی در repo هاب ساخته شود.

Merge، deploy و migration شرکت‌های مالک انجام نشده‌اند. Push/HEAD از Git بررسی شود و به معنی فعال‌شدن سرویس نیست. hash بسته اثبات یکسان‌بودن اسناد است، نه آزمون receiver یا تأیید مالک برای deployment.
