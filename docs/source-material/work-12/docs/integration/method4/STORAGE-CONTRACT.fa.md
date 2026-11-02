# تحویل A1: قرارداد دقیق ذخیره‌سازی مشترک

نسخهٔ قرارداد wire و storage: `1.0.0`؛ بستهٔ اسناد: `1.1.0`. این سند، نام‌ها و رفتارهای اجرایی نسخهٔ اول را قطعی می‌کند. `storage-v1.json` خروجی مستقیم `server/telemetry/schema.ts` است؛ نام جدول یا ستون از روی طرح‌های قدیمی حدس زده نشود.

## نصب و مالک migration

کنترل‌پلین migration **۸**؛ tenant migration **۱۰**؛ component مستقل `telemetry_component(id=1,schema_version=1,contract_version='1.0.0')`. فقط provisioner برنامهٔ اصلی DDL اجرا می‌کند. INGEST هیچ migration یا CREATE/ALTER ندارد. `tenant_metadata.company_id` باید با مسیر احرازشده برابر باشد.

`minimum_runtime_schema` کف نسخهٔ برنامهٔ WEB است؛ توسعهٔ افزایشی schema بدون افزایش این کف، WEB قبلی را بی‌دلیل متوقف نمی‌کند. تغییر ناسازگار نیازمند افزایش کف/نسخه و ارتقای هماهنگ است. INGEST باید قرارداد component خودش را پیش از دریافت بررسی کند و نسخهٔ ناشناخته را fail-closed رد کند؛ صرفاً بیشتر بودن شمارهٔ migration دلیل پشتیبانی از آن نیست.

DDL فعلی در این branch روی دیتابیس شرکت‌های مالک اجرا نشده است. SQL JSON یک بستهٔ نصب خودکار نیست.

## مسیر اعتبارسنجی و قفل‌ها

۱. قالب credential: `EdgeKey <key_id>.<secret>`؛ `key_id` از WEB و secret تصادفی ۳۲بایتی است. `secret_hash` برابر SHA-256 متن UTF-8 **فقط secret** است؛ مقایسه زمان‌ثابت، لاگ بدون credential. شرکت/منبع از body یا نام شرکت استخراج نشود.

۲. INGEST یک SQL user کنترل با دسترسی فقط SELECT روی `telemetry_worker_routes` دارد. این view شامل `key_id,company_id,source_id,secret_hash,credential_revision,database_name,tenant_vault_ref` است و شرکت تعلیق‌شده/غیرفعال یا storage آماده‌نشده را حذف می‌کند. برای هر batch، control transaction باز شود و مسیر معتبر با `LOCK IN SHARE MODE` خوانده شود؛ قفل تا پایان tenant commit نگه داشته شود. این نحو با user محدود روی MariaDB واقعی آزمایش شده است. cache مثبت بدون revalidation برای batch مجاز نیست.

۳. مسیر tenant از view معتبر و whitelist نام DB می‌آید، نه کلاینت. credential tenant از **vault مستقل INGEST** با همان ref خوانده می‌شود. برابری ref به معنی اشتراک رمز WEB نیست. قبل از اولین SELECT عادی tenant، `SELECT revision FROM telemetry_clock WHERE id=1 FOR UPDATE` اجرا شود؛ سپس metadata، وضعیت source و signal و `source.credential_revision == route.credential_revision` بررسی شود. تنها active source/signal و definition شناخته‌شده پذیرفته شوند.

۴. تمام نویسندگان registry، INGEST و گزارش تولید از همین clock استفاده می‌کنند. ترتیب worker: control route shared-lock → tenant clock → source/config/sample. WEB برای تغییر credential ابتدا company کنترل و سپس tenant clock را قفل می‌کند. تولید ابتدا tenant_metadata و سپس clock را می‌گیرد؛ INGEST پس از clock درخواست قفل نوشتن metadata نکند. clock یک mutex کوتاه برای هر شرکت است، نه همهٔ شرکت‌ها. I/O شبکه و انتظار پاسخ عامل داخل این تراکنش قرار نگیرد.

۵. در همان tenant transaction، ingestion، sample/conflict، receipt rows و receipt نهایی نوشته شوند. به‌ازای تغییرات، clock افزایش یابد و همان revision در `telemetry_changes.sequence` درج شود؛ AUTO_INCREMENT به‌تنهایی کافی نیست، چون ترتیب commit را تضمین نمی‌کند. برای یک batch می‌توان یک change برای هر signal تغییرکرده نوشت، نه الزاماً هر sample. بعد از tenant commit کنترل آزاد و رسید موفق منتشر شود. شکست DB/commit یعنی هیچ پاسخ `persisted:true` صادر نشود.

۶. rotation دو DB را بدون XA به‌روز می‌کند: ابتدا revision tenant، سپس مسیر کنترل. شکست میان این دو، credential قدیمی را به‌علت عدم تطابق revision مسدود می‌کند؛ اقدام recovery، rotation دوباره است. ساخت source نیز ممکن است پس از commit tenant و قبل از control commit قطع شود: retry با همان UUID، منبع دیگری نمی‌سازد؛ برای کلید ازدست‌رفته، مدیر rotate می‌کند. این مرز fail-closed است، ادعای تراکنش توزیع‌شدهٔ اتمیک نداریم.

## قواعد داده و تکرارگیری

- count: `integer`, `pcs`, `interval_delta`, `interval_ms=60000`؛ start UTC دقیقهٔ کامل و end=start+60000؛ صفر ذخیره می‌شود، نبود دقیقه صفر نیست. مجموع نیز باید safe integer باقی بماند.
- کلید معنایی count، **signal+شروع دقیقه** است؛ تغییر batch/event_id آن را عوض نمی‌کند. UNIQUE سیگنال/identity_hash و UNIQUE سیگنال/بازه در SQL پشتیبان این قاعده‌اند. مقدار متفاوت در همان دقیقه sample قبلی را UPDATE نمی‌کند؛ conflict append می‌شود و دقیقه از جمع قابل‌تأیید کنار می‌رود.
- الگوریتم پیشنهادی قطعی hash برای adapter Node: هویت count، SHA-256 از `JSON.stringify(["interval_delta",event_time_ms])`؛ content، SHA-256 از `JSON.stringify([definition_revision,event_time_ms,period_end_ms,value])`. عنوان، received time و source_event_id در content شمارش نیستند. برای gauge/state/cumulative: identity از `["event",source_event_id]` در صورت وجود، وگرنه `["time",event_time_ms]`؛ period_end باید null باشد. این scalarها به شمارش تولید وصل نمی‌شوند.
- batch hash روی JSON منطقی معتبر با کلیدهای object مرتب‌شدهٔ بازگشتی و ترتیب array حفظ‌شده، سپس SHA-256 UTF-8 محاسبه شود. `batch_id` در hash هست؛ تغییر فاصله/ترتیب کلیدهای object retry را خراب نکند. مقادیر نامعتبر پیش از normalization رد شوند. این canonicalization برای payloadهای محدود همین قرارداد است، نه ادعای پیاده‌سازی عمومی استاندارد JCS.
- `source_event_id` اختیاری و حداکثر۱۶۰ کاراکتر است؛ event ID را فرستنده می‌سازد و در retry حفظ می‌کند. `sample_id` و `receipt_id` UUID سمت worker هستند. batch ID از فرستنده، حداکثر۱۰۰ کاراکتر؛ receipt UNIQUE روی source/batch. batch یکسان/hash یکسان همان رسید؛ hash متفاوت 409.
- در receipt_rows اندیس صفرمبنا و status یکی از accepted/duplicate/conflict/rejected؛ `receipt_json` همان پاسخ wire مستندشده است. دادهٔ ورودی متعارض و received_at آن در conflicts حفظ شود. payload خراب یا وضعیت غیرمجاز خطای مشخص بگیرد؛ SQL خطای خام/secret به کلاینت نرود.
- timestamp نمونه و دریافت BIGINT میلی‌ثانیهٔ Unix، مقدار `value_json` همان scalar JSON است، نه عدد double-encoded. `received_at_ms` زمان سرور است. raw در این نسخه نمونهٔ scalar معتبر به‌همراه hash و provenance است؛ آرشیو کامل packet یا تصویر نداریم.
- source_mode از registry می‌آید؛ SIMULATOR صرفاً برچسب منشأ پیکربندی‌شده است، اثبات سخت‌افزار واقعی نیست. فرستندهٔ آزمایشی رسمی نباید profile LIVE را مصرف کند. دادهٔ تشخیص تصویر/هویت ساختاریافته هنوز مصرف‌کنندهٔ پیاده‌شده ندارد.

## Registry، config و وضعیت

WEB منبع و UUID سیگنال و definition را می‌سازد. `signal_key` کلید منحصربه‌فرد داخل source است. source هیچ machine_id ندارد. نام/عنوان قابل تغییرند؛ قرارداد نوع/واحد/معنا تغییر نمی‌کند و برای تغییر ناسازگار signal جدید لازم است.

config جاری با source.config_revision انتخاب می‌شود. `config_json` فعلی شامل `transport` و `publishIntervalSeconds` است؛ نسخهٔ نخست creationHash خصوصیِ غیرحساس برای idempotency نیز دارد و worker نباید آن را به agent به‌عنوان تنظیم کاری تعبیر کند. فهرست کانال‌ها از signals/definitions خوانده می‌شود. add-signal config revision را افزایش می‌دهد؛ rename/retire نیز source change ایجاد می‌کند و worker باید registry را دوباره بخواند.

فاصلهٔ ارسال با طول پنجرهٔ شمارش متفاوت است. ثبت desired interval به معنی applied نیست؛ فقط پس از پاسخ معتبر عامل، reported_config_revision جلو می‌رود. برای عامل ناسازگار، pending/unsupported واضح بماند.

worker runtime_status را به‌روز می‌کند: last_contact زمان ارتباط سمت سرور، last_sample بیشترین زمان وقوع نمونهٔ پذیرفته‌شده، reported_config_revision، کد خطای محدود، worker_id غیرحساس و heartbeat. شروع کار/تغییر وضعیت runtime یک change با entity_id=source_id ایجاد کند تا WEB مطلع شود؛ هر heartbeat بی‌تغییر لازم نیست change جدید بسازد. heartbeat worker ≠ اتصال دستگاه ≠ وضعیت روشن/خاموش ماشین.

تازه‌سازی WEB از SQL cursor پایدار است. API registry با `changes?after=...&wait=1` تا۲۵ثانیه انتظار دارد؛ DB حداکثر هر۲ثانیه چک می‌شود، نه refresh کل فرم هر۲ثانیه. برای فرم تولید watcher فقط تغییرات resource/signal/source مرتبط را می‌بیند. این نسخه message bus/CDC ندارد؛ ادعای تأخیر صفر یا benchmark ظرفیت نشده است.

## فرمان عامل

WEB فقط get_status / pause_collection / resume_collection را در `telemetry_commands` با UUID، queued و expiry۱۰تا۳۰۰ثانیه می‌گذارد. params فعلاً `{}`؛ هیچ فرمان فیزیکی CNC نداریم. هر source حداکثر۲۰ درخواست معتبر منتظر دارد؛ retry همان id فرمان جدید نمی‌سازد.

worker با clock و قفل ردیف، queued→sent→succeeded/failed/unsupported یا queued/sent→expired را انجام دهد؛ terminal state دوباره ارسال نشود، expiry قبل از ارسال/هر retry بررسی شود، attempts و next_at_ms افزایش کنترل‌شده داشته باشند. timeout/retry با همان command_id است، نه ساخت command جدید. پاسخ دیرهنگام فرمان expired دستگاه را مجدداً فعال نکند؛ عامل نیز command_id را dedup کند. result_json حداکثر۴KiB و بدون secret/echo credential باشد. هر تغییر نتیجه change روی source بسازد. پوشش واقعی این چرخه متعلق به B4 و هنوز با agent جدید تست نشده است.

## مالکیت SQL و خواندن برنامه

- WEB: registry/bindings/config/credentials/commands و گزارش؛ نمونه‌ها، conflicts و receipts فقط SELECT. جدول‌های definitions/config/changes برای WEB append-only هستند.
- INGEST: SELECT view مسیر و جدول‌های telemetry موردنیاز؛ INSERT ingestion/sample/conflict/receipt؛ UPDATE محدود receipt نهایی، clock، runtime و ستون‌های اجرایی command. نه company_users، نه resources، نه تولید، نه DDL/DELETE و نه ویرایش تعریف تگ. grants دقیق در `server/telemetry/provision.ts` است و negative-grant تست واقعی دارد.
- گزارش از `server/telemetry/read.ts` و `resolveTelemetryCount` می‌خواند؛ نمونه‌ها به hub_measurements قدیمی کپی نمی‌شوند. جدول snapshot موجود `hub_count_previews` و `hub_report_count_evidence` عمداً برای evidence تولید استفاده شده است؛ نام پیشنهادی telemetry_report_evidence در طرح اولیه در DDL اجرایی وجود ندارد. claim جدید `telemetry_count_claims` است. worker به این جدول‌های تولید دسترسی ندارد.
- همان سیگنال می‌تواند برای نمودارهای مختلف خوانده شود؛ claim نمونه برای چند گزارش تولید نهایی مجاز نیست. اتصال count به دو ماشین برای دوباره‌شماری در v1 رد می‌شود. OP/قطعه/اپراتور از count استنباط نمی‌شود.

## سطح API فعلی و کار مشترک باقی‌مانده

تمام مسیرها زیر `/api/v1/company/telemetry`، با session شرکت و data_hub.read/manage و محدودیت workspace سمت سرور:

| مسیر                           | رفتار                                                                              |
| ------------------------------ | ---------------------------------------------------------------------------------- |
| GET /                          | منابع، کانال‌ها، bindings، resources، cursor؛ بدون secret                          |
| POST /sources                  | source UUID از کلاینت، نام، kind، transport، sourceMode و signals؛ کلید فقط یک‌بار |
| POST /sources/:id/signals      | افزودن definition جدید                                                             |
| PATCH /signals/:id             | title/status/version؛ optimistic edit                                              |
| POST /sources/:id/key          | rotation و ابطال کلید قبلی                                                         |
| PUT /sources/:id/config        | version/name/status/publishIntervalSeconds                                         |
| POST /bindings                 | batch حداکثر۶۴تایی؛ نیازمند مجوز ماژول production                                  |
| POST /bindings/:id/end         | پایان بازه با version و validTo؛ حفظ گزارش‌های نهایی                               |
| GET /signals/:id/history       | from/to/before، بازه۷روز و۵۰۰ردیف/صفحه                                             |
| GET /signals/:id/aggregate     | جمع معتبر و پوشش دقیقه‌ها                                                          |
| GET /changes                   | after و wait=1، حداکثر۵۰۰ تغییر در پاسخ                                            |
| GET/POST /sources/:id/commands | صف و نتیجه؛ ایجاد ≠ اجرا                                                           |
| GET /health                    | component، worker heartbeat، capabilities و buildSha در صورت تزریق env             |

نسخهٔ اول پنل برای HTTPS/MQTT آمادهٔ registry است؛ listener واقعی و broker را سشن هاب می‌سازد. REST pull و CSV/XLSX و database-read در schema نوع منبع دارند، اما job/config/staging قرارداد مشترک جدید هنوز اجرایی نیست و در UI غیرفعال‌اند. قابلیت‌های فایل/API در مسیر قدیمی آزمایشگاه شاهد اجرای روش۴ نیستند. B3 باید بعد از توافق یک extension نسخه‌دار برای credential خصوصی، allowlist و upload/job بسازد؛ روی config فعلی فیلدهای حدسی ننویسد و هیچ مسیر قدیمی را به‌جای اتصال جدید اعلام نکند.

این تحویل A1/A2/A3 و بخش WEB از A4/A5 را قابل آزمایش می‌کند؛ پذیرش نهایی محصول دوفرایندی فقط بعد از conformance واقعی HTTP/MQTT/قطع‌وصل/receipt/config/command با branch هاب است.
