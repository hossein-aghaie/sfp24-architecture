# قرارداد اجرایی روش ۴ — بستهٔ هماهنگی 1.1.0

تاریخ: ۲۰۲۶-۱۰-۱۸. وضعیت: **بخش WEB و schema مشترک پیاده شده؛ دریافت دوفرایندی هنوز نیازمند آزمون مشترک با هاب است.** جزئیات اجرایی در `STORAGE-CONTRACT.fa.md`، DDL دقیق در `storage-v1.json` و نتایج در `IMPLEMENTATION-STATUS.fa.md` مرجع‌اند. این README هم تصمیم‌های اجراشده و هم مسیر تکمیل دوطرفه را نشان می‌دهد.

این بسته، تصمیم مالک دربارهٔ «یک محصول، دو برنامهٔ اجرایی، ذخیره‌سازی مشترک» را مشخص می‌کند. مسیر مستقل قبلی فقط checkpoint گیت است؛ حفظ API نیمه‌تمام آن الزام نیست. رکوردهای واقعی/محیط‌های جاری خودکار مهاجرت یا حذف نمی‌شوند.

## ۱. مبنا و شاخه‌ها

- برنامهٔ اصلی: branch جدید `codex/integrated-telemetry-v1` از `c0241d83a2d3a64668088f2b958232a002e1b1d1`؛ مسیر `D:\git\pouyeshgar-workshop\.local\worktrees\integrated-telemetry-v1`.
- هاب: branch ایجادشدهٔ `codex/shared-telemetry-runtime-v1` از `b9c43c162bc5be826f568a41e580f8cac17214ea`؛ checkout سشن هاب تغییر داده نشده است.
- مرجع قرارداد این پوشه در مخزن اصلی است؛ سشن هاب بستهٔ یکسان را در `contracts/pouyeshgar-telemetry/1.1.0/` نگه دارد؛ wire/storage همچنان1.0.0 است. تغییر پنهانی نسخهٔ کپی ممنوع؛ تغییر قرارداد نیازمند نسخه، changelog و آزمون دو طرف است.
- جدول‌ها و مسیرهای اجرایی WEB در STORAGE-CONTRACT فهرست شده‌اند. ویژگی‌های آینده/سشن هاب در IMPLEMENTATION-STATUS جدا هستند؛ وجود نام در طرح به معنی اجرای کامل نیست.

## ۲. تصمیم معماری نهایی

یک محصول و یک پنل اصلی، با دو فرایند: WEB و INGEST. مرورگر به WEB وصل می‌شود. INGEST مسئول MQTT/HTTPS/خواندن منابع است. هر دو از همان MariaDB و همان هویت شرکت استفاده می‌کنند. INGEST پنل عمومی شرکت/کاربر و دیتابیس مستقل عملیاتی SQLite ندارد؛ آزمایش مستقل آن می‌تواند fixture موقت داشته باشد.

MariaDB مرکزی هسته و MariaDB مجزای هر tenant حفظ می‌شوند؛ «مشترک» یعنی WEB و INGEST جدول‌های مربوط را در دیتابیس همان شرکت مصرف می‌کنند، نه ادغام شرکت‌ها در یک دیتابیس بدون جداسازی. اطلاعات خام یک‌بار ذخیره می‌شوند؛ حلقهٔ webhook هاب→گیرندهٔ داخلی پویشگر حذف می‌شود.

INGEST فایل‌های Vue/Three.js، نقش‌های کاربران، جداول تولید، ماشین/شیفت/افراد و entitlement را بازنویسی نمی‌کند. WEB پروتکل‌ها و منطق تکرارگیری موازی نمی‌سازد. منابع خارجی از API عمومی WEB می‌خوانند؛ این API با رابط خواندن داخلی ماژول‌ها پیاده می‌شود.

## ۳. مالکیت و اجازهٔ نوشتن

| داده                                        | نویسنده و مرجع                                     | خواننده                                         |
| ------------------------------------------- | -------------------------------------------------- | ----------------------------------------------- |
| شرکت/وضعیت/قرارداد/حساب/مجوز                | هستهٔ WEB در control DB                            | INGEST فقط نمای محدود مسیریابی/وضعیت            |
| ماشین/خط/ایستگاه/شیفت/افراد/قطعه/OP         | سرویس‌های فعلی WEB در tenant DB                    | ماژول‌های عملیاتی؛ INGEST نیازمند فهرستشان نیست |
| منبع، تگ، تعریف نسخه‌دار و تنظیمات درخواستی | API مدیریتی WEB از طریق سرویس telemetry-management | INGEST به‌صورت خواندنی                          |
| credential دستگاه                           | هستهٔ WEB؛ hash در control directory               | INGEST نمای محدود اعتبارسنجی، بدون رمز کاربران  |
| نمونه/دریافت/تعارض/وضعیت فنی و نتیجهٔ اجرا  | INGEST در tenant DB                                | WEB از TelemetryReadService                     |
| binding تگ→ورودی ماشین/ماژول                | WEB، با بازهٔ اعتبار و audit                       | مصرف‌کنندهٔ مربوط؛ INGEST مستقل از binding      |
| گزارش نهایی/شواهد/claim/اصلاح               | سرویس تولید WEB                                    | گزارش‌های مجاز                                  |

هر دو نویسنده credential SQL جدا و محدود دارند. WEB و INGEST هرگز credential با DDL یا دسترسی نامحدود tenantها دریافت نمی‌کنند. provisioning worker آفلاین هسته مالک ایجاد DB، migration و grant است؛ worker هاب فقط credential محدود tenantهای تخصیص‌یافته را از vault خصوصی خودش می‌خواند. سرور/port/DB از payload یا header مرورگر انتخاب نمی‌شود.

هستهٔ اصلی تنها مالک migration است. سشن هاب SQL پیشنهادی و آزمون adapter می‌دهد؛ شماره/checksum migration عملیاتی را خودش اعمال نمی‌کند. نسخه‌های اعمال‌شده تغییر نمی‌کنند. SQLite هاب به MariaDB اصلی تبدیل نمی‌شود؛ adapter جدید MariaDB در branch هاب ساخته می‌شود، بدون انتقال خودکار fixtureها.

## ۴. پنل و هویت‌ها

۱. Dev Admin شرکت و ماژول‌های خریداری‌شده و سقف **حساب‌های ورود فعال** را می‌سازد؛ نه سقف افراد شناسایی‌شده با دوربین.
۲. Company Admin منابع کاری را در اطلاعات پایه می‌سازد، حتی بدون اتصال/هاب فعال.
۳. کاربر دارای `data_hub.manage` در همان پنل بخش «منابع، اتصال‌ها و تگ‌ها» را تنظیم می‌کند. داشتن این مجوز، superuser شرکت‌های دیگر نیست. provider به دادهٔ عملیاتی مشتری دسترسی خودکار ندارد؛ کمک فنی با مسیر دسترسی صریح و audited طراحی شود.
۴. منبع عمومی است: EdgeBox، SCADA، نرم‌افزار یا فایل. منبع→ماشین اجباری نیست.
۵. هر signal شناسهٔ UUID ثابت، key یکتا در همان source، عنوان، تعریف و وضعیت دارد. binding مستقل است؛ یک تگ می‌تواند در چند نمایش/ماژول مصرف شود یا بدون مصرف بماند.

مبدأ ID: company/resource/person/OP توسط هسته/اطلاعات پایه؛ source/signal توسط WEB telemetry-management؛ source_event_id توسط فرستنده (در retry ثابت)، sample/receipt ID توسط INGEST. device_id معرفی‌شده برای EdgeBox همان source_id است؛ نوع source تعیین می‌کند دستگاه فیزیکی هست یا نه. key صرفاً کانال است؛ عنوان/نام شرکت مجوز نیست.

برای نسخهٔ اول: اول ثبت source و تگ‌ها در پنل، سپس export پروفایل و تنظیم عامل. کلید فقط یک‌بار با مجوز نمایش/صادر و سپس پوشیده می‌شود. معرفی خودکار tag/OPC UA browse مسیر آینده دارد؛ در آن مسیر تگ‌های کشف‌شده draft هستند تا تأیید شوند، نه auto-bind.

تگ active از لحظهٔ ثبت در combo سازگار دیده می‌شود؛ دریافت اولین داده شرط نیست. UI وضعیت no-data/last-received/invalid/disabled را نشان می‌دهد. نام صفحه/نمایش مستقل از شناسه است. اپراتور معمولی tag picker فنی ندارد؛ ورودی تنظیم‌شده را می‌بیند.

## ۵. قرارداد ذخیره‌سازی مشترک

DDL و indexهای گام A1 تحویل شده‌اند؛ جدول زیر مدل مفهومی است و نام دقیق ستون‌ها و تفاوت evidence در STORAGE-CONTRACT مشخص شده است. این نام‌ها روی جداول قدیمی بازنویسی نمی‌شوند.

### Control DB، مالک هسته

- `telemetry_routes`: key_id، company_id، source_id، secret_hash، active، credential_revision و مرجع worker-vault. نمای SQL فقط‌خواندنی برای worker، وضعیت active/suspended/storage-ready شرکت را به آن join می‌کند. نام حساب، رمز، role و secretهای سایر سرویس‌ها در view نیست.
- در tenant: credential_revocations نیز باید با revision فعلی worker قابل تشخیص باشد. هر ingest تراکنش، اعتبار active source و revision را دوباره بررسی می‌کند؛ revoke/suspend نسبت به تراکنش‌های در جریان باید ترتیب مشخص داشته باشد. هدف «دادهٔ تازه پس از تأیید revoke پذیرفته نشود» است؛ قفل‌گذاری control-first→tenant-first یکسان و تست هم‌زمانی الزامی است. قفل cache-only کافی نیست.
- برای هر شرکت credential مجزای writer هاب؛ افتادن یک credential نباید سایر tenantها را باز کند. هیچ query از سرور دستگاه با DB name دلخواه ساخته نشود.

### Tenant DB

| جدول منطقی                           | حداقل داده/قاعده                                                                                                                                                                   |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `telemetry_sources`                  | id، kind، name، status، config_revision؛ بدون resource_id اجباری                                                                                                                   |
| `telemetry_signals`                  | id، source_id، key، title، status، current_definition_revision؛ UNIQUE(source_id,key)                                                                                              |
| `telemetry_signal_definitions`       | signal_id/revision، value_type، measurement، unit، interval_ms، semantic_hint؛ append-only                                                                                         |
| `telemetry_source_configs`           | source_id/revision، transport، mapping، desired settings؛ secretها رمزگذاری‌شده خارج پاسخ عمومی                                                                                    |
| `telemetry_ingestions`               | receipt_id، source_id، received_at_ms، payload hash، منشأ/حالت آزمایشی، خلاصهٔ batch؛ دادهٔ حساس redact                                                                            |
| `telemetry_samples`                  | sample_id، signal_id، definition_revision، source_event_id اختیاری، event_time_ms، period_end_ms اختیاری، typed value، received_at_ms، content_hash، semantic identity، receipt_id |
| `telemetry_conflicts`                | ارجاع sample/receipt، مقدار ورودی متفاوت و زمان دریافت؛ بدون overwrite خاموش                                                                                                       |
| `telemetry_receipt_rows`             | receipt_id/index، signal/sample ID، accepted/duplicate/conflict/rejected و code                                                                                                    |
| `telemetry_runtime_status`           | source_id، last_contact، last_sample، reported_config_revision، last_error، worker health؛ ارتباط ≠ روشن/خاموش ماشین                                                               |
| `telemetry_changes`                  | sequence پایدار افزایشی، entity_id/type/revision، نوع تغییر و زمان؛ payload بدون secret                                                                                            |
| `telemetry_input_bindings`           | id/revision، signal_id، consumer، input_key، resource_id، valid_from/to، enabled؛ نویسنده WEB                                                                                      |
| `telemetry_report_evidence` و claims | snapshot گزارش و نمونه‌های مصرف‌شده؛ نویسنده فقط تولید                                                                                                                             |

واحد canonical شمارش `pcs`، نوع `integer`، measurement=`interval_delta` و interval_ms=60000 است. برچسب دلخواه input در EdgeBox با adapter صریح تبدیل می‌شود. gauge/boolean/string نیز schema دارند، ولی به ورودی شمارش متصل نمی‌شوند. cumulative بدون reset/rollover/late policy به delta تبدیل خودکار نمی‌شود.

type/unit/measurement/طول بازهٔ signal فعالِ دارای نمونه immutable است؛ تغییر ناسازگار یعنی signal جدید و retire قبلی. rename عنوان با optimistic revision مجاز است. definition revision برای annotation/توسعه سازگار است؛ بازتفسیر تاریخچه ممنوع.

## ۶. ورودی عامل — قرارداد device-ingest نسخهٔ 1.0.0 جدید

این قرارداد مستقل از HTTP قدیمی schema_version=1 و مستقل از schema_version=2 پیشنهادی سشن قبلی است. نام namespace مانع اشتباه می‌شود.

- HTTP: `POST /ingest/v1/samples` روی listener INGEST؛ `Authorization: EdgeKey <key_id>.<secret>`؛ فقط TLS در نصب شبکه‌ای. localhost آزمایش می‌تواند HTTP باشد.
- MQTT: topic `sources/{source_id}/telemetry` و هویت credential مشابه؛ ACL فقط source خود؛ broker کتابخانهٔ آماده است. ماندگاری session با ماندگاری application sample یکی نیست. Sparkplug یک adapter آینده است، نه مجوز استخراج شرکت از topic دلخواه.
- body و fixture دقیق در `device-batch.example.json`. fieldهای company_id، DB، resource_id و OP ورودی مجوز نیستند و در این قرارداد پذیرفته نمی‌شوند.
- signal_key در source authenticated resolve می‌شود. actor دستگاه اجازهٔ ساخت tag ناشناخته ندارد.
- v1 حداکثر 256KiB و 1000 نمونه/batch؛ UTF-8، timestamp UTC/offset و precision میلی‌ثانیه. integer امن و نامنفی برای count؛ NaN/null/رشتهٔ خالی شمارش نیست.
- count فقط دقیقهٔ تمام‌شده با start منطبق به UTC minute و period_end=start+60000. بازه نیمه‌باز [start,end). partial count در این نسخه ورودی گزارش نهایی نیست.
- backlog پیش‌فرض ۳۰ روز؛ config محدود سرور می‌تواند تغییر دهد. future completed-minute پذیرفته نمی‌شود. مرجع now سرور است.
- semantic identity count: tenant+signal_id+period_start، مستقل از batch/source_event_id. مقدار مساوی duplicate؛ متفاوت conflict. شمارش hash شامل received_at یا عنوان نمی‌شود. سایر انواع: signal+source_event_id یا event_time با قاعدهٔ مستند.
- سیگنال ناشناخته یا نوع غلط با reason برگردد؛ هیچ fallback به تگ/شرکت پیش‌فرض نداریم.
- نمونه‌ها، conflicts، receipt rows و change notification در **یک tenant transaction** ثبت شوند؛ ACK بعد از commit. DB قطع/timeout یعنی no-success، فرستنده retry کند.
- batch_id ثابت در retry: همان payload hash، همان receipt؛ payload متفاوت با batch_id یکسان=409. همان نمونه در batch جدید نیز semantic dedup دارد.
- ingest batch می‌تواند row-level outcome داشته باشد؛ accepted receipt با successful report یکی نیست. کلاینت فقط rejectedهای قابل اصلاح را بررسی کند، acceptedها دوباره جمع نشوند. نتیجهٔ conflict خودکار پاک نمی‌شود.
- MQTT PUBACK به‌تنهایی نتیجهٔ هر ردیف نیست. receipt کاربردی روی topic مجاز `sources/{id}/receipts` یا query authenticated با batch_id در دسترس باشد؛ دریافت هر batch به اندازه محدودیت ACL است. invalid packet و broker ACK semantics دقیق با تست مستند شود، نه ادعای exactly-once.
- فرستنده batch/time/ID را در قطعی حفظ کند. نمونهٔ ساختگی با ساعت تسریع‌شده برچسب SIMULATOR داشته باشد؛ ساعت واقعی production از آن ساخته نشود.

## ۷. خواندن داده و مصرف تولید

WEB یک `TelemetryReadService` درون‌فرایندی دارد: catalog، latest، history(cursor,limit)، aggregate(signal,from,to)، changes(after). فقط همین سرویس query قراردادی و tenant-scoped می‌زند؛ فرم‌ها و ماژول‌ها SQL آزاد روی جدول worker ندارند. دادهٔ خام دوباره از INGEST به WEB POST نمی‌شود.

aggregate برمی‌گرداند: total از نمونه‌های معتبر، expected/valid/missing/conflicted/explicit-zero، sourceMode، from/to، signal/definition revision و sample refs یا snapshot قابل audit. بازه حداکثر۷روز و history صفحه‌بندی‌شده با سقف۱۰۰۰ ردیف؛ export جدا stream/bounded است.

ورودی تولید: `processed_count`؛ ورودی ضایعات: `final_scrap_count`. فیلتر combo از نوع/واحد/معناست، نه نام count/wast. semantic_hint ارسالی عامل به‌تنهایی کسب مجوز یا اثبات مناسب‌بودن نیست؛ مدیر قرارداد منبع را تأیید می‌کند.

یک source چند signal و چند resource دارد؛ یک resource چند input دارد. هر resource/input در هر لحظه یک binding مرجع. یک signal در چند نمودار/ماژول قابل استفاده است؛ اتصال همان count به دو resource برای دو بار ثبت تولید در v1 ممنوع؛ fan-out خواندن با دو بار ادعای تولید یکی نیست.

نگاشت بر event_time ارزیابی می‌شود. تغییر binding فقط از زمان مشخص و بدون بازنویسی شواهد نهایی. گزارش عبوری از مرز تغییر binding باید با پیام روشن تقسیم شود؛ ترکیب ضمنی منابع ممنوع. mapping اجباری OP از sensor نتیجه نمی‌شود.

تعداد متصل کامل و بدون تعارض + ضایعات دستی یا متصلِ معتبر → سالم=processed-scrap، scrap<=processed. snapshot و claim در تراکنش نهایی تولید و با قفل ترتیب ثابت. اگر count یا scrap متصل ناقص است ثبت نهایی connected رد شود؛ draft و ورودی دستی با مجوز/دلیل جدا باقی است. تگ ضایعات فقط final reject count یکتای همان جمعیت است؛ تعداد تصویر/عیب خودکار ضایعات نیست.

علیت ضایعات منبع می‌تواند با reason استاندارد «بازرسی خودکار» از تنظیمات مجاز ثبت شود؛ کاربر مجبور به تکرار دستی تمام مقادیر دوربین نشود. raw structured inspection/operator events مرحلهٔ بعدند و با scalar string پیاده‌شده اعلام نمی‌شوند.

شواهد نهایی شامل مقدار، بازه، binding/definition revision، sourceMode، هویت نمونه و hash/نسخه snapshot است. late arrival/rename/retire گزارش نهایی را خودکار تغییر نمی‌دهد. اصلاح با مجوز و audit. یک نمونهٔ مصرف‌شده از دو report نهایی دوباره مصرف نشود، حتی با تغییر binding/source alias.

## ۸. تازه‌سازی، پیکربندی و فرمان

تعریف/ویرایش در WEB، commit در shared tenant DB و درج change sequence. INGEST فقط revisionهای جدید را دریافت و config را reload می‌کند؛ SQL تغییرات با cursor، نه bootstrap کامل هر۵ثانیه. cursor consumer/reconnect و snapshot در صورت compaction لازم است.

در نسخه اول wake-up reader حداکثر هر۲ثانیه جدول changes/status را bounded query می‌کند؛ این کشف داخلی تغییر است، نه بازخوانی کامل همه داده‌ها. notification بین processها قابل بهینه‌سازی آینده است؛ Kafka/Redis/NATS جدید پیش‌شرط نیست.

مرورگر از long-poll موجودِ WEB با cursor پایدار و scope مجاز استفاده کند؛ حداکثر۲۵ثانیه انتظار و پس از تغییر فقط بخش لازم refresh. برنامهٔ فعلی updates.ts حافظه‌ای است و باید cross-process شود. SSE الزام نسخه اول نیست. catch-up با خواندن DB انجام می‌شود نه اعتماد به notification حافظه‌ای.

فرمان‌های عامل get_status/pause_collection/resume_collection با command_id/expiry/result؛ تنظیم interval ماندگار در desired_config_revision با reported/applied revision. TTL فرمان جای ثبت desired نیست. sampling، window، publish و UI refresh جدا. pause_collection توقف ماشین نیست. کنترل فیزیکی دستگاه خارج از محدوده.

مدیریت از WEB دستور/desired را ثبت می‌کند؛ INGEST فقط وضعیت ارسال/نتیجه را با transition مجاز می‌نویسد. عامل باید command_id را dedup کند؛ آزمایش سیمولاتور اثبات firmware واقعی نیست.

## ۹. ارتقای مستقل و قرارداد دسترسی

- contract_version=1.0.0 برای interface؛ schema component version مستقل از شماره migration عمومی tenant. جدول metadata component و worker support-range قبل از شروع بررسی شوند.
- WEB مالک DDL؛ worker نقش DDL ندارد. startup worker نسخهٔ نامعتبر/قابلیت ناشناخته را fail-safe با خطای واضح متوقف کند؛ گزارش دستی و WEB باید برای failure بخش telemetry قابل استفاده باشند.
- تغییر additive در minor: ستون nullable/default و field اختیاری، نگه‌داری رفتار reader قدیم. fieldهای required جدید/تغییر معنا/نام جدول یا نوع یعنی major و migration هماهنگ.
- ابتدا schema افزایشی+WEB سازگار، سپس worker سازگار، تست، سپس فعال‌کردن feature. حذف ستون/مسیر تنها پس از خروج مصرف‌کننده قبلی؛ این هماهنگی upgrade است نه الزام حفظ دائمی مسیر قدیمی.
- هر دو برنامه health می‌دهند: build SHA، contract supported، schema status، capabilities، lag و آخرین heartbeat بدون secret.
- دسترسی داده خارجی فقط API خواندنی WEB با اعتبارنامه scopeدار؛ API عمومی worker برای مدیریت شرکت نداریم. browser به DB/worker secret دسترسی ندارد.
- status تعلیق، key revoke و source disable در همه ingest و config guards بررسی شوند. worker خاموش/DB قطع را با صفر تولید یا خاموشی ماشین یکی نکنید.

## ۱۰. منابع، نگهداری و استقرار

تنها یک instance INGEST در پذیرش اول؛ HA و multiple writers بدون lease/locking جدا ساخته‌شده اعلام نشوند. connection pool، body/rate، صف bounded و batch write تنظیم‌پذیر. payload در RAM نامحدود نگه‌داری نشود. receipt/backlog در restart حفظ شود.

بودجهٔ تست اولیه: ۵ شرکت مصنوعی ×۵۰ source ×۱۶ signal، نمونه در هر دقیقه و موج ارسال مجدد ۲۴ساعت. این سقف قرارداد فروش یا ظرفیت اثبات‌شده نیست؛ throughput، p95 commit/query، peak RSS، DB/disk و timeoutها اندازه‌گیری شوند. هدف آزمایشی نمایش شمارش پس از دریافت/commit حداکثر۳ثانیه در بار سناریوی میهن، نه SLA صنعتی قطعی. شمارش نهایی قبل از بسته‌شدن دقیقه وجود ندارد.

retention را بی‌اجازه فعال نکنید. پیشنهاد قابل تنظیم raw۷روز و samples۹۰روز فقط مقدار اولیه آزمایش است؛ تأیید گزارش‌ها باید مستقل از پاک‌سازی خام باقی بماند و داده هنوز موردنیاز draft/claim/correction بی‌ردپا حذف نشود. policy، export/archive، delete job bounded و backup/restore قبل از بهره‌برداری واقعی تعیین و تست شوند.

Launcher واحد WEB و INGEST را روشن و وضعیت هر دو را نشان دهد. Stop تنها PID همین محیط را متوقف کند و داده حذف نکند. localhost و DBهای disposable در تمام تست‌ها؛ اتصال به شرکت واقعی «میهن» یا EdgeBox واقعی مجاز نیست.

## ۱۱. دامنه و تقسیم کار اجرایی

### سشن اصلی، شاخه integrated-telemetry-v1

A1. shared contract+DDL/control directory+tenant grants و adapter/interface خواندن؛ component schema version، health و fixture generator. تنها owner migration.
A2. APIهای مدیریتی source/signal/config و key rotation با session/permission، strict validation، revision و audit؛ registry UI فارسی/انگلیسی در shell اصلی؛ machine مستقل از source.
A3. جدول تخصیص گروهی ۱۶ کانال؛ فیلتر ورودی‌ها، valid-from و status روشن؛ processed+scrap، evidence/claims و late/correction.
A4. database changes/long-poll، worker-health در پنل و launcher و راهنمای انسانی؛ حفظ geometry و ماژول مستقل دستی.
A5. آزمون real MariaDB disposable، scope، migrations/restarts/negative grants و browser QA.

### سشن هاب، شاخه shared-telemetry-runtime-v1

B1. Store انتزاعی async و MariaDB adapter طبق قرارداد A1، حذف وابستگی اجرایی integrated به SQLite/user/company registry مستقل؛ استفاده از fake port برای توسعه مستقل تا fixture آماده شود. SQL/migration خودسر روی DB اصلی ممنوع.
B2. process دریافت standalone، HTTP+MQTT و credentials resolver، receipts/dedup/conflict/changes atomic، محتوای خطا امن؛ company/source از credential نه body.
B3. REST polling و CSV/XLSX با mapping/preview و confirm/job قرارداد WEB؛ ورودی file از API مجاز WEB stage و worker پردازش کند. اتصال read-only DB یک connector با allowlist/credential جداست، نه تغییر منبع اصلی. روش موجود lab را با production integration یکی ندانید.
B4. config watcher، worker status، command lifecycle و desired/applied؛ فرستنده مستقل با۱۰منبع و EdgeBox۱۶کاناله و صف قطعی.
B5. تست روی MariaDB disposable و consumer/read-service fixture، performance/restart، deliver report و API بدون secret. پنل مستقیم هاب در lab فقط diagnostic باشد؛ در محصول پنل دوم یا login تکراری نداریم.

OPC UA value/event، کشف tag و Sparkplug قابلیت آینده با adapter interface هستند؛ unsupported واضح. در OPC UA، collector معمولاً client است. worker جای نصب نزدیک OT را در تنظیمات deployment محفوظ می‌گذارد ولی agent/gateway محلی جدید در این مرحله اجباری نیست. RFID/بینایی فقط پس از schema و سیاست مصرف؛ ایجاد اپراتور/شیفت خودکار از مشاهده ممنوع.

## ۱۲. ترتیب تحویل و شرایط ورود به اجرای مشترک

۱. هر دو سشن این بسته و fixtureها را بخوانند؛ contract version/hash و ابهام‌های blocking را ثبت کنند. خلاصه‌های چت جای قرارداد نیستند.
۲. سشن اصلی A1 را با schema/port دقیق تحویل دهد؛ هاب تا آن زمان port/fake adapter و simulator را پیش ببرد، نه حدس schema.
۳. هر دو fixture و conformance test یکسان را اجرا کنند؛ hash متفاوت یعنی NOT ALIGNED، اتصال مشترک متوقف.
۴. branchهای هر طرف commit مستقل، تست‌های همان SHA و گزارش capability/limits داشته باشند. اجرای integration روی clone/DB disposable، نه برنامه مالک.
۵. HTTP count→تولید و سپس MQTT۱۶کاناله→تخصیص گروهی اثبات شوند؛ scrap channel، config و disconnect/restart اضافه شوند.
۶. Merge فقط پس از بازبینی مالک؛ پرامپت مأموریت اجازهٔ Deploy/Migrate شرکت‌های فعلی نیست. تکمیل WEB یا A1 به معنی تکمیل B1 و دریافت واقعی نیست.

## ۱۳. ماتریس پذیرش مشترک

- شرکت A با کلید/شناسه/کانال شرکت B از HTTP/MQTT/UI/API/DB-grant راه نداشته باشد؛ روی revoked/suspended همزمان آزمون شود.
- source بدون machine،۱۶ signal روی۱۶resource،دو source روی count/scrap یک resource، signal بدون مصرف، fan-out چند نمودار.
- مجموع fixture۱۲۳؛ replay همان batch و batch جدید مجموع را عوض نکند؛ مقدار متفاوت همان دقیقه conflict؛ صفر≠missing؛ out-of-order و source_event_id تغییرکرده.
- پس از restart receipt/config و cursor معتبر؛ قطع DB ACK موفق ندهد؛ commit-before-ACK و lost-response retry تست failure injection.
- event-time binding، rename، retirement، تغییر ناسازگار signal و تغییر config کهنه، grace/update ترتیب‌دار.
- ضایعات دستی و متصل، کامل/ناقص، scrap>processed، reason و snapshot، درخواست تکراری report و double-claim همزمان.
- قطع worker: WEB و تولید دستی فعال، connected report با خطای روشن؛ DB قطع: failure صادقانه بدون نمایش صفر.
- cross-process تغییر tag و نمونه در پنل بدون Sync، long-poll reconnect و restart worker/web.
- ارتقا/عقب‌گرد binary با schema-compatible، incompatible schema fail-safe؛ applied migration rollback خودکار ندارد.
- TLS/real firmware/OPC UA غیرساخته با UNVERIFIED/UNSUPPORTED، نه PASS.

## ۱۴. سناریوی پذیرش انسانی میهن

نام میهن اینجا فقط نقش سناریوی ساختگی است؛ هیچ دادهٔ مشتری واقعی استفاده نمی‌شود. مراحل دقیق در SCENARIO.fa.md؛ دستور سشن هاب در HUB-SESSION-PROMPT.fa.md.
