# اجرا و نگهداری جاری — ۲۰۲۶-۱۰-۲۸

این راهنما اجرای محیط فعلی است. دستورها سرویس/داده را فقط در محدودهٔ مشخص خودشان تغییر می‌دهند؛ [شرح‌های پیشین](archive/state-2026-10-28/RUNBOOK.md) سابقه‌اند.

## اجرای روزمره

از D:/git/pouyeshgar-workshop روی شاخهٔ مجاز جاری codex/03-production-recording (checkpointهای قدیمی با runtime/schema خودشان):

1. Check-Setup.cmd پیش‌نیاز و پیکربندی را بررسی می‌کند.
2. Start-All.cmd را دستی اجرا کنید؛ ممکن است MariaDB محلی و worker آماده‌سازی را هم بالا بیاورد.
3. Status-All.cmd وضعیت، Stop-All.cmd فقط فرایندهای متعلق به همین launcher را کنترل می‌کند؛ پوشهٔ دیتابیس را پاک نمی‌کند.

تشخیص پورت لانچر از `netstat` با PID استفاده می‌کند. در Windows PowerShell، `Get-NetTCPConnection` ممکن است برای پورت واقعاً فعال نتیجهٔ خالی بدهد؛ گاهی حالت اتصال در جرد نیز نادرست است یا ردیف listener دیده نمی‌شود. در این وضعیت اتصال TCP واقعی loopback باز می‌شود و PID سمت سرور از همان جفت endpoint دقیق خوانده می‌شود؛ اتصال موفق به‌تنهایی کافی نیست. PID همچنان باید با رکورد پردازش تطبیق کند. Check/Status نیز ممکن است این اتصال کوتاه و بدون احراز هویت/SQL را برقرار کنند. این نتایج نباید باعث اجرای نسخهٔ دوم MariaDB شوند. خروجی نامعتبر، timeout یا مالک نامشخص راه‌اندازی را متوقف می‌کند. بررسی PID/زمان ایجاد/مسیر دیتابیس همچنان برقرار است؛ رکورد مالکیت را دستی حذف یا جایگزین نکنید.

| جزء | آدرس/پورت |
|---|---|
| WEB محصول | http://127.0.0.1:5206 |
| API محصول | 5207 |
| INGEST HTTP جاری، در صورت آماده‌سازی runtime شرکت | 5208 |
| MariaDB آزمایشی جدا | 127.0.0.1:3317 |
| شبیه‌ساز خارجی v1 / v2 | 5251 / 5252؛ Start.cmd در external-simulator/v1 یا v2 |

ورود مالک /owner/login و شرکت /company/<code>/login است. نشست در همان تب پس از refresh می‌ماند؛ logout/401/ابطال آن را پاک می‌کند. خطای شبکه را خطای رمز ننامید. after code change، سرورهای بدون watch باید با Stop/Start دستی بازخوانی شوند؛ install/build خودشان deploy یا restart نیستند.

دموی فاز۲ در D:/git/pouyeshgar-demo-phase2 با launcher خودش و WEB5240/API5184 و هاب مستقل تاریخی در D:/git/pouyeshgar-industrial-platform با پورت‌های خودش هستند. دستور محصول آن‌ها را اداره نمی‌کند؛ برای پاک‌سازی محصول حذف/جابجا نمی‌شوند.

## پیکربندی خصوصی

launcher، runtime/provision را زیر .local/local-launcher/private می‌سازد؛ منبع تنظیم محیط .local/data-sources/private/state.json است. API اعتبار runtime و worker اعتبار provision جدا دارند. هیچ‌کدام وارد مرورگر/Git نشوند. مدل‌سازی/پارامتر/کلید دستگاه پس از پاک‌سازی منبع config فعال خود را از دست ندهند.

companyFilesDirectory یا COMPANY_FILES_ROOT، ریشهٔ عکس/draft/library است؛ vaultDirectory برای credential DB و مخزن رمز‌شدهٔ کلید source مستقل است. HUB_ENCRYPTION_KEY از فایل خصوصی به runtime داده می‌شود. انتقال فایل شرکت به‌تنهایی کافی نیست؛ [نقشهٔ داده و انتقال](guides/LOCAL-FOLDERS.fa.md).

HTTP عمومی یک Bearer منبع دارد؛ parser semantic کسب‌وکار انجام نمی‌دهد. خطای service_unavailable را با خاموش بودن دستگاه یکی نکنید. در محیط جاری، WEB باید TELEMETRY_RECEIVER_BASE_URL مربوط به INGEST داشته باشد. شروع setup session امضای داخلی دارد و setup-control.key credential دستگاه نیست.

## آماده‌سازی و ارتقا

مصرف پارامتر در تولید به migration افزایشی۱۷ نیاز دارد. این migration روی fixtureهای تست تأیید شده، ولی شرکت جاری خودکار ارتقا نمی‌یابد. قبل از اعمال روی شرکت جاری، backup سازگار DB و vault موجود را حفظ و سرویس‌های همان محصول را با هماهنگی مالک متوقف کنید. برای ارتقای شرکت موجود از provision پلتفرم با شناسهٔ دقیق همان شرکت و credentialهای موجود استفاده کنید؛ فایل vault گم‌شده را با credential تازه جایگزین نکنید:

```powershell
$env:PLATFORM_PROVISION_CONFIG = (Resolve-Path .local/local-launcher/private/provision.json).Path
pnpm exec tsx server/platform/cli.ts provision <company-uuid>
```

پس از تأیید نسخهٔ schema و مجوز جدول جدید، Stop/Start دستی محصول و تست کاربری انجام شود. Stop/Start به‌تنهایی migration شرکت ready را اجرا نمی‌کند. تا ارتقا، runtime جدید می‌تواند storage_schema_outdated بدهد؛ runtime قدیمی با minimum_runtime_schema جدید سازگار فرض نشود. این دستور با provision-worker تله‌متری پایین یکی نیست؛ برای این migration نیازی به ساخت/چرخاندن کلید دستگاه یا runtime جدید INGEST نیست.

یادداشت‌های دستگاه به migration۱۸ نیاز دارند. روی شرکت آزمایشی پویشگر در آماده‌سازی ۲۰۲۶-۱۰-۲۹، پس از dump، schema۱۸ اعمال شد و credentialهای قبلی حفظ شدند. برای tenant دیگر همان provision موجود را با شناسهٔ دقیق و backup اجرا کنید؛ runtime جدید خودکار ready-tenant را ارتقا نمی‌دهد. برای این مرحله، Stop/Start دستی فقط کد تازه را بارگذاری می‌کند. برگهٔ ورود حساب تازه خصوصی است، کد موقت آن برای تعیین رمز شخصی مصرف می‌شود؛ حساب موجود را برای تست رمز reset نکنید.

ایجاد/مهاجرت معمول شرکت توسط ابزارهای platform/provision و worker است؛ checksum migration قبلی تغییر نکند. برای آماده‌سازی HTTP در محیط مجاز، ابزار موجود:

```powershell
pnpm exec tsx tools/telemetry/provision-worker.ts --config .local/data-sources/private/state.json --company <company-uuid>
```

این دستور جدول/حساب محدود و فایل runtime خصوصی می‌سازد؛ فقط برای شرکت و محیط تأییدشده اجرا شود، فایل موجود را بی‌دلیل overwrite نکنید. user/API به اعتبار DDL دسترسی نگیرد. نصب ابزار Graphify بیرون پروژه در D:/git/graphiify و مستقل از اجرای محصول است.

## آزمون و بازیابی

```powershell
pnpm install --frozen-lockfile
pnpm test:all
pnpm build:all
pnpm check:edgebox
node --test external-simulator/v1/test.mjs external-simulator/v2/test.mjs
```

DB مرکزی + DBهای tenant + فایل شرکت + vault + کلید encryption اجزای بازیابی‌اند. datadir زنده را دستی کپی/حذف نکنید؛ dump سازگار بگیرید و restore را در محیط جدا بیازمایید. dump زمان‌بندی‌شده/restore یک‌کلیکی هنوز محصول آماده نیست. آرشیو cleanup پشتیبان موردی خصوصی است، نه سامانهٔ backup.

## پاک‌سازی مرحلهٔ۰۲

دیتابیس‌های QA قدیمی فقط پس از بررسی ارجاع/اتصال و snapshot خصوصی با SQL حذف شدند؛ کنترل و شرکت جاری باقی‌اند. جدول‌های فعال دستی پاک یا migrationها squash نشدند. فایل‌های کتابخانهٔ قدیمیِ شرکت جاری با hash تطبیق به CompanyFiles منتقل شدند؛ reader fallback حذف شده است. سرویس‌ها در این کار خودکار restart نمی‌شوند؛ پس از پایان، مالک Stop/Start و آزمون میدانی انجام دهد. شواهد در [گزارش پاک‌سازی](migrations/STRUCTURE-AUDIT-2026-10-28.json) است.

## فعال‌سازی و آزمون میزهای نام‌دار
این نسخه migration کنترل۹ و grant جدول company_work_desks می‌خواهد. ابتدا با Stop-All سرویس‌های محصول را متوقف کنید، از دیتابیس مرکزی dump سازگار بگیرید و با فایل خصوصی provisioning همان محیط، ابزار موجود را اجرا کنید؛ این دستور سرویس‌ها را راه نمی‌اندازد و tenant را seed/reset نمی‌کند:

```powershell
$env:PLATFORM_PROVISION_CONFIG = (Resolve-Path '.local/local-launcher/private/provision.json').Path
pnpm accounts:cli migrate-control
```

پس از موفقیت، Start-All را دستی اجرا کنید. migration افزایشی، تعریف میز متصل قبلی را به فهرست مشترک منتقل می‌کند؛ حساب‌ها و رمزهای کاربر را reset نکنید.
در Company Admin ← میزهای کار و داشبوردها، میز بسازید یا از الگو آغاز کنید، نام و محتوا را تنظیم و «ذخیرهٔ میز» را بزنید؛ رمز مجدد یا انتخاب مخاطب در این فرم نیست. سپس کاربران و دسترسی‌ها ← حساب مقصد ← میزهای کار: میزها و یکی به‌عنوان میز شروع را انتخاب و ذخیره کنید. با ورود مجدد همان حساب، «میز کار من» و در صورت چند میز، انتخابگر میز باید دیده شود. دادهٔ داخل میزها فعلاً نمایشی است. برداشتن همهٔ میزها، شروع قبلی فرد را برمی‌گرداند؛ مجوزهای کاری تغییر نمی‌کنند. تغییر تعریف مشترک به همهٔ استفاده‌کنندگان می‌رسد؛ برای تفاوت یک نفر، ابتدا کپی مستقل بسازید. بایگانی میز فقط پس از برداشتن اتصال همهٔ افراد ممکن است.

اجازهٔ مالک در ۲۰۲۶-۱۱-۰۱: عامل می‌تواند Stop/Start همین محصول محلی را برای بررسی و فعال‌سازی تغییرهای تأییدشده انجام دهد. shared MariaDB باید طبق روال Stop-All روشن بماند؛ محیط سرور یا Raspberry Pi مشمول این اجازه نیست. اگر inventory ویندوز حالت CLOSED بدهد، لانچر اتصال و PID تخصیص‌یافتهٔ ثابت را با هم بررسی می‌کند؛ مالکیت نامشخص همچنان خطای توقف است، نه اجازهٔ kill یا اجرای دیتابیس دوم.
