# سهم هاب برای ادغام در بستهٔ اجرایی مشترک

شناسهٔ تحویل: `HUB-C01` — بازنگری `draft-1` — تاریخ: ۲۰۲۶-۱۰-۱۹.

**وضعیت: پیشنهاد دقیق برای ادغام؛ قرارداد نهایی یا بستهٔ اجرایی دوم نیست.** مرجع محصول سند مشترک نسخهٔ۱٫۱٫۱ است. سشن برنامه بستهٔ واحد را کنار همان سند منتشر می‌کند؛ نام‌های پیشنهادی این تحویل پس از ادغام فقط از بستهٔ واحد خوانده خواهند شد. هیچ کد، migration، سرویس یا firmware در این مرحله ساخته یا اجرا نشده است.

## ۱. مبنا و تفاوت با بستهٔ قدیمی

منابع مستقیماً خوانده‌شده:

- `D:/git/pouyeshgar-workshop/.local/worktrees/integrated-telemetry-v1/docs/integration/HUB-TAG-PUBLICATION-DESIGN.fa.md` نسخهٔ۱٫۱٫۱؛ SHA256 برابر `E0F7A5A95C186565789FFB5BEA8E99E1D8C38988C88DBC0290B4A7E48C00043B`.
- فایل‌های README، STORAGE-CONTRACT، storage-v1.json، receipt.example و package-manifest در پوشهٔ `method4` همان مسیر. بستهٔ تاریخی اسناد۱٫۱٫۰ / storage و wire۱٫۰٫۰ است؛ نسخهٔ محصول با آن یکی نیست.
- شواهد firmware در `docs/EDGEBOX-SFP-READONLY-REVIEW.fa.md`؛ تفاوت source با binary نصب‌شده هنوز آزموده نشده است.

بستهٔ تاریخی minute-exact، رسید جزئی و registry بدون انتشار انتخابی را توصیف می‌کند؛ برای مدل فعلی کافی نیست. DDL آن کیفیت/پوشش مستقل، هویت کانال غیرقابل بازاستفاده، correction/void، درخواست recovery، lease/fence و lifecycle operation را کامل ندارد. گزارش‌های PASS تاریخی آن به معنای تأیید قرارداد تازه نیستند. فایل‌های تاریخی و شماره/checksum migration آن‌ها بی‌صدا تغییر نکنند. شمارهٔ نسخهٔ بسته، schema و migration جدید را ناشر مرکزی تعیین می‌کند.

## ۲. مالکیت و رابط داخلی پیشنهادی

تمام portها async، tenant-scoped و بدون SQL، pool، نام schema یا خطای driver در ورودی/خروجی هستند. `TenantContext` فقط از مرجع معتبر core می‌آید؛ هیچ adapter از company_id موجود در packet مجوز نمی‌گیرد.

| port / عمل پیشنهادی | مالک | ورودی و تعهد |
|---|---|---|
| `RegistryRead.resolveCredential` | core | credential محرمانه → route معتبر، source، credential revision، مرجع vault؛ بدون HTTP WEB |
| `RegistryRead.snapshot` | core | tenant/source → config، تعریف و publication تگ‌ها، channel identity و gate revision |
| `TelemetryWrite.acceptBatch` | هاب | context معتبر + normalized observations + expected registry revisions + acceptance mode → receipt پایدار |
| `RecoveryRequest.create` | WEB | preview ثابت، تصمیم‌ها، actor/scope، idempotency key → درخواست تغییرناپذیر |
| `RecoveryExecution.claim/apply/finish` | هاب | tenant، lease/fence، request، chunk → effect/progress پایدار و قابل تکرار |
| `RuntimeObservation.patch` | هاب | فقط last-contact، last-sample، reported-state، heartbeat و خطای محدود؛ بدون بازنویسی config |
| `DurableExternalOperations.claim/recordOutcome` | هاب | عملیات disconnect/config/command با revision/expiry/fence؛ I/O خارج تراکنش |
| `TelemetryRead.catalog/history/changes/aggregate` | برنامه | همان storage استاندارد و نمای مؤثر؛ بدون parser تجهیز و بدون کپی raw |

registry write، API کاربر، authorization، support-access، provision و migration متعلق به WEB/core است. transaction/gate و envelope مشترک‌اند. schema و grant نهایی از همان ناشر مرکزی می‌آیند؛ هاب migration عملیاتی جدا صادر نمی‌کند.

## ۳. مدل استاندارد مشاهده برای تثبیت در schema مرکزی

نام‌های زیر پیشنهاد ادغام‌اند. زمان‌های داخلی Unix millisecond صحیح و safe هستند؛ نمایش HTTP تاریخ ISO8601 با Z/offset صریح است. event time از sender و received time از ساعت سرور جدا می‌مانند. از timezone رایانه یا حدس واحد عدد استفاده نمی‌شود.

| فیلد | قاعدهٔ پیشنهادی |
|---|---|
| `sampleId`, `receiptId` | UUID سمت INGEST؛ sampleId در retry عوض نمی‌شود |
| `companyId`, `sourceId`, `signalId` | از context و registry معتبر، نه payload ادعایی |
| `channelIdentityId` | هویت پایدار کانال فنی در اتصال؛ rename/config revision آن را عوض نمی‌کند |
| `definitionRevision`, `mappingRevision`, `profileId/profileRevision` | منشأ تفسیر ثبت‌شده؛ تغییر سازگارشان هویت نمونه را تازه نمی‌کند |
| `valueType`, `value`, `measurement`, `unit` | مطابق تعریف نسخه‌دار signal؛ صفر با null/empty متفاوت است |
| `eventTimeMs`, `periodStartMs`, `periodEndMs` | برای observed_delta هر دو period=null؛ برای interval_delta بازهٔ صریح start<end و نیمه‌باز؛ eventTime قرارداد زمانی جدا دارد |
| `nominalIntervalMs` | فاصلهٔ اسمی در صورت اطلاع؛ مدرک بازهٔ دقیق نیست |
| `identityKind`, `identityToken`, `contentHash` | دامنه و الگوریتم ثابت بخش۴؛ received time و revision نمایشی در هویت نیستند |
| `timeBasis`, `clockQuality`, `measurementQuality`, `coverage` | محورهای مستقل؛ unknown صریح، بدون ارتقای حدسی به good/complete |
| `sourceMode`, `ingressMethod`, `receivedAtMs` | mode از registry؛ LIVE/SIMULATOR مستقل از HTTP/MQTT/CSV و دیررس‌بودن است |
| `originalSampleId`, `effectiveRevision` | در reader برای provenance اصلاح؛ رکورد اولیه immutable می‌ماند |

پیشنهاد representation بدون اتلاف: integer به رشتهٔ ده‌دهی canonical با الگوی `^-?(0|[1-9][0-9]*)$`، بدون `-0`، حداکثر۶۴رقم؛ decimal رشتهٔ ده‌دهی بدون exponent، بدون صفر پیشرو/صفر انتهای بخش اعشاری و بدون منفی صفر، حداکثر۶۴رقم و scale حداکثر۱۸؛ boolean مقدار JSON boolean و string رشتهٔ UTF-8 حداکثر۴KiB. این انتخاب باید یک‌بار در schema مرکزی تصویب شود؛ پذیرش integer بزرگ در هاب به معنی توان جمع آن در production نیست. reader مصرف فعلی باید overflow/precision را صریح رد کند. هیچ parser ابتدا عدد بزرگ را به Number تبدیل نکند و سپس رشته نسازد. نوع object/تصویر/ویدئو در این تحویل وعده داده نمی‌شود؛ event متنی/شناسه‌ای نیز بدون استنباط person/OP ثبت می‌شود.

تعریف measurement پیشنهادی: `observed_delta`، `interval_delta`، `gauge`، `cumulative` و `event`. cumulative بدون قرارداد reset/rollover به delta تبدیل نشود. observed_delta با پوشش unknown قابل ثبت/خواندن است؛ برچسب good/scrap و تأیید گزارش تولید متعلق به برنامه است. برای SFP فعلی مقدار شمارش integer نامنفی، واحد تعریف‌شدهٔ شمارش، eventTime=t*1000، period=null و nominalInterval=60000 است. کیفیت ساعت از داشتن عدد epoch به‌تنهایی good نمی‌شود.

## ۴. هویت، canonicalization و تکرارگیری

برای یک signal، نوع identity در تعریف فنی تثبیت شود و با تغییر transport/CSV عوض نشود:

- `observed_delta`: هویت کانال پایدار + timestamp اصلی مشاهده؛ برای SFP دقت مبدأ ثانیه است و ms تبدیل دقیق آن است.
- `interval_delta`: signal + ابتدای بازهٔ صریح؛ انتهای بازه در content است تا تغییر بازه در همان آغاز conflict شود، نه شمارش دوباره. اندازهٔ بازه از تعریف می‌آید.
- `event`: source event ID پایدار لازم است؛ زمان به‌تنهایی برای RFID و چند رخداد هم‌زمان کافی نیست.
- gauge/cumulative: سیاست signal یا event ID پایدار است یا timestamp؛ انتخاب در profile صریح و ثابت می‌ماند.

پیشنهاد الگوریتم محدود و قابل انتقال: `identity_hash=SHA256(UTF8(JSON.stringify(["id-v1",signalId,identityKind,identityToken])))`. identityToken برای زمان رشتهٔ integer ms، برای event ID رشتهٔ دقیق case-sensitive است. برای SFP immutable mapping تضمین می‌کند signalId و channel identity قابل بازاستفاده نیستند؛ کانال قبلی به signal جدید remap نمی‌شود. rotation کلیدِ همان source هویت تاریخی را عوض نمی‌کند.

`content_hash=SHA256(UTF8(JSON.stringify(["content-v1",valueType,canonicalValue,measurement,unit,eventTimeMs,periodStartMs,periodEndMs])))`. null صریح است؛ کلید/مقدار undefined و NaN مجاز نیست؛ canonicalValue از representation بخش۳ می‌آید. profile revision، عنوان، received time، filename، HTTP/MQTT و revision annotation در hash نیستند. تغییر semantics/unit برای signal دارای داده ناسازگار است و به signal تازه نیاز دارد. provenance و quality جدا از fingerprint مقدار ثبت می‌شوند تا CSV همان مشاهده را به اثر تازه تبدیل نکند. hash جای مقایسهٔ محتوای canonical در اختلاف احتمالی را نمی‌گیرد.

همان identity/content → duplicate اولیه؛ identity یکسان/content متفاوت → conflict، بدون UPDATE نمونه. صفر در دو timestamp دو نمونه است. replay مقدار اولیه بعد از correction با محتوای اولیه مقایسه می‌شود، نه مقدار مؤثر اصلاح‌شده. مشاهدهٔ متفاوت با timestamp/value یکسان در SFP قابل تشخیص نیست؛ این محدودیت profile مستند است، نه conflict ساختگی.

batch id در پروتکل جدید، ثابت در retry و scope آن source است؛ payload hash از JSON معتبر با کلیدهای object مرتب‌شده و ترتیب array حفظ‌شده تولید شود. همان batch id/hash همان رسید، hash متفاوت `BATCH_ID_REUSED`. این قانون receipt قبلی را معتبر می‌شناسد ولی auth/gate جاری را دور نمی‌زند. SFP batch ID ندارد: تشخیص اصلی در سطح نمونه است؛ برای lookup رسید، hash آرایهٔ canonical به ترتیب wire با channelIdentityId و profile هویتی ثابت استفاده شود. بستهٔ تغییرترتیب‌یافته می‌تواند رسید تازه ولی فقط duplicate بسازد. UUID تازهٔ هر HTTP retry هویت نمونه نیست.

## ۵. دریافت SFP و پاسخ قابل اتکا

پیشنهاد route مستقل adapter: `POST /ingest/adapters/sfp-http-count/v1`؛ آدرس نهایی در export اتصال صادر شود. در lab فقط loopback. احراز هویت باید با scheme/token واقعاً تنظیم‌شدهٔ این firmware تطبیق داشته باشد؛ فرض اجباری EdgeKey برای firmware موجود نکنیم. adapter verifier نسخه‌دار و معتبر از registry می‌گیرد و token را لاگ/بازنشر نمی‌کند. امنیت شبکهٔ نصب واقعی بخشی از تحویل بعدی است، نه ادعای اتصال عملیاتی امروز.

- Content-Type فرم-urlencoded؛ دقیقاً یک `node_id` و یک `data`؛ JSON داخل data آرایهٔ۱تا۷۰۰رکورد. فرم خام فعلی و فرم درصد-encoded معتبر پشتیبانی شوند؛ decoding فقط یک‌بار، duplicate field و JSON key تکراری رد شوند.
- هر رکورد دقیقاً `t` صحیح در دامنهٔ uint32 و `q` صحیح در دامنهٔ uint16؛ صفر q معتبر است. t نامعتبر تقویمی/ساعت مشکوک باید سیاست زمانی صریح داشته باشد؛ در این profile t=0 به‌عنوان epoch معتبر عملیاتی پذیرفته نشود. محدودیت زمان، خطای روشن بدهد و نه گردکردن/جابه‌جایی خاموش. `time/qty` alias خودکار نیستند. node_id در بازهٔ uint8 و فقط از mapping معتبر resolve شود.
- سقف پیشنهادی body برابر۲۵۶KiB، Content-Encoding فشرده در این profile رد، سقف runtime queue برابر۳۲ batch منتظر و حداکثر۲ batch هم‌زمان به‌ازای source؛ بیشتر از سقف پاسخ۴۲۹. این‌ها حدود اولیهٔ قابل تنظیم سرورند، نه benchmark ظرفیت. adapter به batch۷۰۰تایی یا محدودیت‌های جدید byte نباید ACK جزئی بدهد.
- هیچ backlog چندماهه‌ای فقط به‌علت پیش‌فرض۳۰روز بستهٔ قدیمی حذف نشود. retention خودکار خاموش است؛ محدودیت پذیرش زمان اگر تعریف شد باید در profile export و diagnostics باشد. زمان آینده/نامطمئن به زمان سرور تبدیل نمی‌شود.
- status HTTP و MQTT config adapterهای هم‌خانواده‌اند، نه count با fieldهای حدسی. status فاقد شناسه/زمانِ مبدأ نباید به production count یا event تاریخیِ دقیق تبدیل شود. MQTT موجود سفارشی JSON است؛ استاندارد Sparkplug و MQTT-countِ اجراشده ادعا نمی‌شود.

حالت پذیرش این profile `atomic_batch` است: prevalidate همهٔ رکوردها و duplicate/conflict داخل بسته؛ سپس resolve معتبر و transaction. تمام نمونه‌های جدید، receipt، ردیف‌های پذیرفته/duplicate و changeها در همان tenant commit ثبت شوند. یک conflict/reject → صفر sample تازه از آن بسته. نتیجهٔ شکست و جزئیات عیب‌یابی می‌تواند در تراکنش مستقل ثبت شود؛ نام حالت شکست `rejected_batch` باشد و با accepted اشتباه نشود.

تنها پاسخ موفق firmware: HTTP۲۰۰، Content-Type application/json و دقیقاً این۱۰بایت UTF-8، بدون newline/envelope:

```json
{"code":0}
```

پیشنهاد خطاهای adapter:۴۰۰ `INVALID_PAYLOAD`،۴۰۱ `AUTH_INVALID`،۴۰۳ `INGEST_DISABLED`،۴۰۹ `OBSERVATION_CONFLICT/REGISTRY_CHANGED/BATCH_ID_REUSED`،۴۱۳ `PAYLOAD_TOO_LARGE`،۴۲۹ `INGEST_BUSY`،۵۰۳ `STORAGE_UNAVAILABLE/SCHEMA_UNSUPPORTED/COMMIT_UNKNOWN`. خطای شکست هیچ پاسخ۲۰۰ و code0 ندارد. timeout با نتیجهٔ commit نامعلوم، موفقیت نیست؛ retry باید از ledger وضعیت واقعی را بازیابد. firmware فعلی ممکن است خودکار retry کند؛ تعارض باید در پنل قابل حل باشد تا صف برای همیشه بی‌دلیل مسدود نماند.

رسید داخلی شامل receiptId، batch identity/hash، source، profile، acceptanceMode، outcome، زمان commit، accepted/duplicate/conflict/rejected و row index صفرمبنا + sample reference/code است؛ نتیجهٔ ذخیره‌سازی به معنی مصرف موفق production نیست. خطای ثبت‌نشده در DB receipt پایدار معرفی نشود. payload خام کامل/credential ذخیرهٔ پیش‌فرض نیست؛ محتوای normalized مورد تعارض و hash و provenance کافی و محدودند.

## ۶. تراکنش، قفل و تغییرات قابل خواندن

۱. parse محدود بدون تغییر داده؛ دریافت tenant route با credential معتبر؛ اتصال مستقل INGEST به control/vault/tenant. توقف HTTP WEB نباید این مسیر را متوقف کند.

۲. روی control، اعتبار route و وضعیت مجاز با قفل مشترک کوتاه؛ روی tenant، gate/clock همان مرجع WEB با قفل نوشتن؛ metadata و source/credential revision و signal/mapping را تحت همین ترتیب دوباره بررسی کن. cache قبل تراکنش اجازهٔ commit نمی‌دهد. سپس receipt قبلی، identityهای درون batch و نمونه‌های قبلی، insertها و تغییرات بررسی/ثبت شوند. تمام writerها ترتیب یکسان داشته باشند؛ هیچ مسیر برعکس tenant→control قفل نگیرد.

۳. tenant commit، سپس آزادسازی control و پاسخ. اگر tenant commit شد ولی پاسخ/آزادسازی control خطا داد، اثر tenant برنمی‌گردد؛ retry بدون نمونهٔ تازه نتیجه را مشخص می‌کند. rollback control پس از commit tenant، rollback توزیع‌شده نیست.

۴. اصلاح registry، publish/bind/delete و correction از همان gate شرکت استفاده کنند. metadata lock اضافی در writer پس از clock گرفته نشود اگر مسیر core آن را قبل clock می‌گیرد؛ بستهٔ مرکزی باید مسیرهای production را هم در نمودار lock ترتیب دهد. حداکثر deadline پیشنهادی batch۱۵ثانیه؛ deadlock/timeout قابل retry با همان identity و بدون ACK موفق است. I/O broker/فایل/شبکه داخل lock ممنوع؛ درخواست SQL درایور باید timeout واقعی داشته باشد، نه فقط Promise timeout.

۵. `telemetry_changes.sequence` قدیمی یک PK منفرد است: اگر چند change در یک batch لازم است، برای **هر ردیف** sequence جدا از clock قفل‌شده رزرو و clock به آخرین مقدار منتقل شود؛ یک revision را برای چند PK استفاده نکنیم. همه در یک commit، بدون اتکا به ترتیب AUTO_INCREMENT. cursor API رشتهٔ integer است تا precision bigint از دست نرود.

۶. history پیشنهادی keyset با `(event_time_ms,sample_id)` و snapshot watermark؛ changes با `(sequence)` و page حداکثر۵۰۰؛ هیچ offset scan یا بازخوانی همهٔ شرکت‌ها برای هر تگ لازم نیست. late data ممکن است در صفحهٔ زمان قدیمی بیاید؛ changes دارای receipt/signal و بازهٔ event-time متأثر باشد تا reader آن بازه را invalidate کند. snapshot history باید revision مؤثر correction را ثابت کند؛ watermark ingest به‌تنهایی correction هم‌زمان را ثابت نمی‌کند. پیاده‌سازی دقیق snapshot/read و API query مالک برنامه است.

## ۷. حذف و چرخهٔ عمر

WEB impact دارای source/signal revision، consumer-set revision و زمان انقضا صادر کند. commit با همان مبنا و idempotency key، gate را قفل کند؛ حذف signal، انتخاب جدید و دریافت همان signal و bindingهای متأثر را در نقطهٔ commit قطع کند. حذف source همهٔ کانال‌هایش را می‌بندد. رکورد و هویت/کانال tombstone باقی می‌مانند؛ identifier یا channel mapping آزاد نمی‌شود. نمونه/تعریف/receipt/report گذشته DELETE نمی‌شوند.

عمل broker ACL/disconnect به‌صورت durable operation با lifecycle revision در همان tenant transaction درج و بیرون lock اجرا شود. دریافت حتی اگر disconnect هنوز انجام نشده، از gate بسته رد می‌شود. UI `logically_disabled` را از `network_disconnect_confirmed` جدا کند. replay receipt قدیمی پس از حذف، راه دریافت یا زنده‌کردن منبع نیست. birth یا پیام retained نیز gate را باز نمی‌کند.

تعلیق شرکت و rotation در control+tenant، چون XA فرض نشده، fail-closed و قابل retry باشند. موفقیت نهایی «تعلیق تأیید شد» پس از تثبیت gateهای tenant و control اعلام شود؛ حالت بینابینی pending/failed آشکار است. ترتیب دقیق commitها و reconciliation را core در بستهٔ مرکزی مشخص کند. تعویض binding ماشین فقط همان تخصیص را عوض می‌کند و source مشترک را غیرفعال نمی‌کند.

## ۸. CSV، preview و درخواست بازیابی

پیشنهاد ستون‌های نسخهٔ جدید template، جدا از فایل تنظیم اتصال:

```csv
signal_id,definition_revision,identity_kind,source_event_id,event_time,period_start,period_end,value
```

manifest جدا شامل template version، sourceId، channel identity mapping، signal/definition مجاز، type/unit/measurement، timezone rule و راهنما است؛ هیچ secret ندارد. شرکت و source از scope upload/manifest معتبر و نشست می‌آیند؛ سطر نمی‌تواند tenant را عوض کند. sample CSV جداگانه با دادهٔ ساختگی و توضیح غیرقابل اشتباه ارائه شود. template خالی فقط header دارد.

UTF-8 و BOM مجاز؛ comma و quoting CSV استاندارد، CRLF/LF؛ هیچ اجرای formula یا fetch URL در parser. زمان ISO8601 با Z/offset؛ epoch خام فقط با mapping/profile صریح. رشتهٔ value بر اساس type signal parse شود؛ null/empty برای count خطاست و صفر معتبر است. سقف پیشنهادی۱۰MiB،۵۰هزار سطر،۴KiB field؛ فایل بزرگ‌تر با خطای محدودیت رد شود، نه خواندن نامحدود RAM. CSV download برای spreadsheet رشتهٔ مخرب را به‌عنوان formula فعال صادر نکند؛ نمایش امن نباید مقدار ذخیره‌شده را بی‌خبر تغییر دهد.

upload در private با object ID غیرقابل انتخاب مسیر، SHA256/size و فایل immutable تثبیت شود. preview تمام سطرها، mapping و definition revisions، دادهٔ مبنای conflict، actor/scope و expiry را ثبت کند. پیشنهاد expiry۳۰دقیقه. خروجی شامل شمارش insert/duplicate/conflict/error و اثر correction است؛ تصمیم‌های قبول/اصلاح/رد سطر روشن باشند. default درخواست پس از رفع همهٔ خطاها/تصمیم‌ها ساخته می‌شود؛ subset با تأیید صریح تعداد سطرهای کنارگذاشته‌شده.

commit پیشنهادی فقط `{previewId,expectedPreviewRevision,idempotencyKey,decisions}` است؛ سطرهای جدید یا value دلخواه مرورگر پذیرفته نشوند. decisions فقط به row ID/hash مبنا و یکی از keep-existing / use-incoming برای conflict اشاره کنند. مقدار سوم دلخواه، preview تازه لازم دارد. درخواست append/correction و علت و actor ثبت شود. void عمل مجاز جدا با reason است؛ empty cell به معنی void نیست.

WEB immutable request را می‌سازد؛ INGEST تنها نویسندهٔ sample/correction و نتیجه است. auth، revision تعریف/نگاشت و **revision همان نمونهٔ مبنا** قبل اثر کنترل شوند. یک heartbeat یا sample نامرتبط نباید بی‌دلیل همهٔ preview را stale کند؛ revision مجموعهٔ consumer فقط در تصمیمی که اثر مصرف را بررسی می‌کند لازم است. data change مرتبط → `PREVIEW_STALE` و preview تازه؛ تصمیم دربارهٔ۷ روی۸ اعمال نشود.

بازیابی تاریخی source حذف‌شده، مسیر صریح دارای مجوز recovery و بازه/تعریف تاریخی است؛ live gate را باز نمی‌کند. publication شرط ذخیرهٔ داده نیست و recovery به معنی انتشار خودکار نیست. در source آزمایشی CSV نمی‌تواند LIVE بسازد.

## ۹. اجرای job، correction و ادامه پس از restart

دو موجودیت: درخواست ثابت WEB و اجرای متغیر INGEST. حالت اجرای پیشنهادی: queued → running → succeeded؛ running → retry_wait → running؛ یا needs_review / failed / cancelled. progress و counts از row ledger ساخته شوند. partial effects با پرچم `hasCommittedEffects` و لیست دقیق سطرها آشکار باشد؛ failed/cancelled به معنی برگشت اثرهای commit‌شده نیست.

پیشنهاد lease۳۰ثانیه، renew هر۱۰ثانیه با ساعت DB؛ claim همراه attempt/fence افزایشی. تمام تغییر اثر/progress/finish، lease معتبر و fence جاری را داخل همان transaction بررسی کنند. worker قدیمی پس از takeover حتی اگر زنده شد حق اثر/finish ندارد. همهٔ runningها هنگام startup reset نشوند. external I/O نیز outcome با attempt ثبت کند؛ fence دیتابیس به‌تنهایی اجرای فیزیکی تکراری روی تجهیز را خنثی نمی‌کند.

فایل ابتدا کامل validate/preview/approve می‌شود؛ اجرای effect در chunk حداکثر۲۰۰سطر و transaction کوتاه با idempotency روی `(requestId,rowId,decisionRevision)` است. این **اتمیک‌بودن کل فایل نیست**؛ UI تعداد commit‌شده/باقی‌مانده را نشان دهد. بعد restart از ledger ادامه یابد؛ crash قبل commit اثری ندارد، بعد commit سطر تکرار نمی‌شود. تغییر مجوز/revision مرتبط وسط کار → توقف needs_review با حفظ و نمایش اثرهای قبلی. تغییر تصمیم برای سطر commit‌شده، اصلاح تازه است نه اجرای دوبارهٔ همان job. این رفتار باید در API و راهنما قبل تأیید کاربر بیان شود.

correction/void append-only شامل sampleId، expectedEffectiveRevision، before/after canonical، reason، actor، request/row، زمان و revision است. reader با نمای مؤثر می‌خواند؛ raw و fingerprint اولیه دست‌نخورده‌اند. insert correction + افزایش revision مؤثر + row outcome/progress + change در یک commit و فقط با fence معتبر. claim/evidence و گزارش نهایی WEB خودکار بازنویسی نمی‌شوند؛ change اثر روی مصرف را به برنامه اطلاع می‌دهد. CSV موجود برای تغییر۷به۹ به‌تنهایی correction مجاز نیست؛ تأیید conflict لازم است.

external operation/command با idempotency ID، expected config/lifecycle revision، expiry و نتیجهٔ محدود ذخیره شود. MQTT فعلی retained response یا broker PUBACK تأیید اعمال تنظیمات نیست. پاسخ ذخیره NVS، requiresRestart، applied-confirmed و unknown جدا باشند. retry فرمان غیریدempotent بعد timeout خودکار انجام نشود مگر capability تجهیز آن را تضمین کند؛ خواندن state برای reconciliation انجام شود. جزئیات command wire در adapter هاب می‌مانند.

## ۱۰. تغییر مدل ذخیره‌سازی و grants لازم برای ادغام

این جدول delta منطقی نسبت به DDL قدیمی است، نه DDL آمادهٔ اعمال. نام نهایی، نوع/index، constraint و شمارهٔ migration را core یک‌بار منتشر می‌کند.

| موجودیت | تغییر لازم و مالک نوشتن |
|---|---|
| sources/signals/config/definitions | lifecycle و publication جدا؛ channel identity ثابت/tombstone؛ profile capability و mapping نسخه‌دار؛ WEB |
| samples | period_start صریح یا null، measurement/time/quality/provenance قابل بیان و identity پایدار؛ INSERT فقط INGEST |
| ingestions/receipt_rows/conflicts | acceptanceMode و outcome بسته، hash و نتیجهٔ ردیف‌ها؛ شکست تشخیصی مستقل از accepted ledger؛ INGEST |
| sample revisions/corrections | immutable before/after، expected effective revision، actor/reason/request، UNIQUE effect key؛ INGEST |
| effective head | CAS revision و pointer مؤثر بدون UPDATE raw؛ INGEST؛ reader فقط SELECT |
| recovery uploads/previews/requests | فایل خصوصی/hash، تصمیم و scope ثابت؛ WEB؛ INGEST فقط SELECT لازم |
| recovery execution/row effects | lease/fence/attempt، row idempotency و progress؛ INGEST |
| lifecycle/external operation requests | intent اتمیک WEB با حذف/config؛ INSERT WEB، execution/status محدود INGEST |
| runtime status | patch ستون‌های عملیاتی، بدون UPDATE تنظیمات؛ INGEST |
| changes/gate/component | ترتیب commit و schema compatibility، همان UoW؛ grants ستون/عمل مطابق نویسنده |

role مهاجرت از runtime جدا؛ WEB و INGEST نه DDL، نه DELETE تاریخچه و نه دسترسی آزاد business. INGEST به resources/users/production_reports/claims دسترسی لازم ندارد. WEB به sample/correction نوشتن مستقیم ندارد؛ درخواست می‌دهد. credentials کنترل فقط نمای route مجاز؛ credential tenant مجزا و vault مستقل از lifecycle WEB است. SQL/domain errors نگاشت محدود شوند. تفاوت NULL/UNIQUE، collation case-sensitivity signal key، precision و timestamp در migration manifest صریح باشند.

تغییر ساختار expand → runtime سازگار → contract؛ INGEST contract/schema ناشناخته را رد کند. new column nullable بدون سیاست معنا، سازگاری را اثبات نمی‌کند. old/new hash و بازه نباید با UPDATE خام دوباره تعبیر شوند؛ backfill با الگوریتم/نسخه و reconciliation مستقل، اگر لازم شد. هنوز migration دوموتوره یا تغییر MariaDB لازم نیست.

## ۱۱. آزمون پذیرش مشترک پیشنهادی

همهٔ موارد زیر **NOT RUN** هستند؛ این جدول مشخصات آزمون است، نه نتیجهٔ اجرا.

| ID | ورودی/اختلال | انتظار قابل مشاهده | مسئول شاهد |
|---|---|---|---|
| H01 | SFP یک sample t/q با q=7 و t غیرهم‌تراز | یک observed_delta، period=null، t*1000 بدون rounding، body دقیق code0 بعد commit | هاب + reader برنامه |
| H02 | همان بسته پس از قطع پاسخ commit‌شده | هیچ sample تازه؛ duplicate؛ response موفق پس از بررسی مجدد gate | هاب |
| H03 | timestamp ثابت، q جدید | conflict؛ هیچ sample تازهٔ بسته؛ non-200؛ مقدار اولیه ثابت | هر دو |
| H04 | دو سطر متعارض در یک بسته + سطر تازه | هیچ sample تازه حتی سطر سالم؛ diagnostic شکست | هاب |
| H05 | همان t/q و دو صفر با t متفاوت | اولی duplicate با محدودیت مستند؛ صفرها هر دو ثبت | هاب |
| H06 | rename/config/profile revision و replay | همان هویت، صفر نمونهٔ تازه؛ remap کانال قدیمی به signal تازه رد | مدیریت + هاب |
| H07 | correction۷→۹ سپس replay۷ | effective=9، raw=7، replay duplicate، هیچ برگشت correction | هر دو |
| H08 | حذف هم‌زمان ingest/binding | ترتیب commit مشخص؛ پس از تأیید gate هیچ sample/binding تازه؛ history باقی | هر دو |
| H09 | منبع مشترک دو ماشین و تعویض یک binding | منبع فعال برای مصرف دیگر؛ تاریخ تخصیص محفوظ | برنامه |
| H10 | WEB خاموش، INGEST و DB سالم | دریافت/رسید/registry/secret و broker کار کنند؛ پس از WEB-start همان داده خوانده شود | هر دو |
| H11 | DB قطع/commit مبهم/schema ناسازگار | هیچ ACK موفق کاذب؛ bounded queue؛ retry به یک اثر | هاب + adapter core |
| H12 | unauthorized tenant یا packet با companyId جعلی | هیچ خواندن/نوشتن tenant دیگر؛ خطای محدود | هر دو |
| H13 | CSV stale یا value دستکاری‌شدهٔ مرورگر | PREVIEW_STALE/INVALID_DECISION؛ هیچ overwrite | WEB + INGEST |
| H14 | crash قبل/بعد chunk، takeover و worker قدیمی | هر row یک effect؛ fence قدیمی رد؛ progress صحیح | هاب |
| H15 | revoke permission وسط job | توقف پیش از effect بعدی پس از cutpoint معتبر، اثرهای قبلی آشکار؛ بدون rollback نمایشی | core + هاب |
| H16 | observed_delta مرز شیفت و late arrival | زمان اصلی حفظ؛ aggregate بر مبنای مشاهده با پوشش unknown؛ finalization فقط policy برنامه | برنامه |
| H17 | ۷۰۰سطر SFP،۷۰۱سطر،۲۵۶KiB+ و صف پر | اولی در حد مجاز؛ اضافه‌ها خطای روشن، صفر ACK/اثر جزئی | هاب |
| H18 | CSV BOM/quote/zero/empty/عددبزرگ/offset | parse دقیق؛ zero≠empty؛ no precision loss؛ epoch نامشخص رد | هر دو |
| H19 | recovery منبع حذف‌شده با/بدون مجوز | live بسته؛ recovery فقط تاریخی و صریح؛ منبع زنده نشود | هر دو |
| H20 | چند change در یک batch و pagination late/correction | sequenceهای یکتا و commit-ordered؛ invalidation بازه درست؛ هیچ صفحهٔ ناسازگار پنهان | هر دو |
| H21 | SQL runtime کم‌مجوز | INGEST قادر به DDL/ویرایش registry/business نیست؛ WEB raw نمی‌نویسد | core |
| H22 | MQTT response retained/fragment/timeout | هیچ applied خیالی؛ پیام ناقص رد/diagnostic؛ command outcome صادقانه | هاب |

## ۱۲. اقلام موردنیاز از بستهٔ مرکزی و نتیجهٔ این تحویل

هنگام خواندن نخست فقط method4 تاریخی موجود بود. در ادامه، سشن برنامه پوشهٔ مرجع `D:/git/pouyeshgar-workshop/.local/worktrees/integrated-telemetry-v1/docs/integration/telemetry-execution-v2/` را برای نامزد `2.0.0-rc.1` ایجاد کرد. چهار فایل اولیهٔ README، ADAPTER-PORTS، TRANSACTIONS و SECURITY-RUNTIME خوانده شدند؛ نتیجهٔ جزئی در بخش۱۳ است. این مسیر تنها بستهٔ مرجع است و این فایل فقط تحویل برای ادغام است. تأیید نهایی هنوز صادر نمی‌شود؛ در snapshot بررسی‌شده schemaها، API، DDL، CSV/job، manifest و نمونه‌های نهایی هنوز ارائه نشده بودند. نبود فایل حین نگارش، ایراد نهایی بسته معرفی نمی‌شود.

تصمیم فنی پیشنهادی که نیازمند تطبیق دو سشن است: representation عدد دقیق، نام‌های envelope، سقف‌های عملیاتی، chunk/lease، مدل head correction و snapshot paging. این‌ها سؤال محصول تازه نیستند. اتمیک‌نبودن کل CSV و progress جزئی باید به‌روشنی در بستهٔ نهایی و UI تصریح شود؛ پنهان‌کردن آن اختلاف اجرایی واقعی خواهد بود.

پس از دریافت بستهٔ مرکزی، هاب schema/examples/vectors و grant/transaction را با این تعهدها مقابله می‌کند و نتیجه را تأیید یا با ایراد مشخص اعلام می‌کند. هیچ ادعای build، آزمون دیتابیس، اتصال firmware، benchmark یا آمادگی production از این تحویل حاصل نمی‌شود.

## ۱۳. بازبینی اولیهٔ نامزد مرکزی در حال نگارش

این بررسی جزئی است و approval روی کل بسته نیست. SHA256 فایل‌های خوانده‌شده:

```text
ADAPTER-PORTS.fa.md  82553F3C1664339E0990C86430EDA21C260C7E1ED94B7BB52BAB5DBADF96A495
TRANSACTIONS.fa.md   916FBE18E05F034E688D1285D6414DE8FAF4744F306037CD5F5D162D5043255F
```

**هم‌راستایی تأییدشده در متن:** استقلال WEB/INGEST، observed_delta بدون بازهٔ ساختگی، immutable mapping، raw/correction جدا، atomic live batch، permit مشترک برای لغو اختیار recovery، chunkهای قابل ادامه و fence، unknown برای command غیرتکرارپذیر و عدم تأیید business در هاب.

**تطبیق با انتخاب‌های مرکزی:** برای جلوگیری از چند قرارداد، حدود عددی signed64 و decimal(38,9)، chunk حداکثر۱۰۰، فایل۵MiB/۱۰هزارسطر، deadline۵ثانیه و limits مرکزی را به‌عنوان انتخاب نامزد می‌پذیرم؛ اعداد متفاوت بخش‌های قبلی این تحویل پیشنهاد اولیه بودند و پس از ادغام مرجع نیستند. count مصرف production همچنان محدودیت دقیق مستقل دارد. ظرفیت واقعی و دسترسی کم‌مجوز موتور هنوز آزموده نشده‌اند. سقف SFP۷۰۰سطر و پاسخ دقیق آن ثابت‌اند. معنای canonicalization با انتخاب نامزد v2 باید از همان schema/algorithm مرجع بیاید، نه hash پیشنهادی v1 بخش۴ این تحویل.

**H-R01 — اصلاح لازم در fingerprint محتوا:** در ADAPTER-PORTS فرمول `originalContentHash` فقط identityHash/value/definitionSemanticKey/unit دارد. برای sender_event، identity فقط event ID است؛ همان event ID و value با timestamp یا period تازه می‌تواند duplicate شود و اختلاف زمانی پنهان بماند. پیشنهاد: content fingerprint علاوه بر فیلدهای فعلی، eventTimeMs و periodStartMs/periodEndMs صریح (null در صورت نبود) را شامل کند. identity ثابت بماند؛ تغییر زمان برای همان event ID conflict است. همین قاعده در schema، نمونه و vector اضافه شود. quality/provenance متغیرِ دریافت با هویت مقدار مخلوط نشود.

**H-R02 — شرط اعتبار interval identity:** نامزد identity بازه را `[domainId,interval,startMs,endMs]` گرفته است. این تنها وقتی بدون دوباره‌شماری معتبر است که طول و هم‌پوشانی بازه در تعریف ثابت و قبل از hash کنترل شوند؛ برای دو end متفاوت در یک start نباید دو interval پذیرفته شود. پیشنهاد تحویل هاب: identity با start ثابت و end در content؛ یا اگر مدل مرکزی start/end را حفظ می‌کند، constraint/validator صریحِ بازه و vector متفاوت‌بودن end را اضافه کند. این تکمیل قرارداد داده است، نه تصمیم جدید محصول.

**H-R03 — مرز پذیرش طراحی با اثبات اجرایی:** TRANSACTIONS آزمون MariaDB و user محدود را شرط اثبات قفل view می‌داند؛ درست است، ولی مجوز فعلی فقط تدوین قرارداد است. approval طراحی نباید به‌عنوان PASS آن آزمون ثبت شود. بسته می‌تواند با شرط اجرای آزمون isolated پس از دستور شروع تصویب فنی شود؛ پیش از پذیرش runtime هیچ تضمین قفل یا benchmark تأیید نشده است. در صورت انتخاب stored procedure به‌جای view، قبل ساخت writer قرارداد/grants بازنگری و hash تازه شود.

**H-R04 — دقت نوشتن مرز حذف:** لحظهٔ commit نقطهٔ ترتیب منطقی قطع است؛ timestamp ذخیره‌شدهٔ cut داخل transaction انتخاب می‌شود و لزوماً زمان فیزیکی پایان commit نیست. بسته باید این دو مفهوم را جدا بنویسد تا binding/read policy از ادعای ساعت دقیق commit استفاده نکند. این نکتهٔ نگارشی/اجرایی است، نه مانع اصل gate مشترک.

وضعیت این چهار مورد: پیشنهاد اصلاح برای ناشر؛ هنوز پاسخ/اصلاح مرکزی مشاهده نشده است. هیچ سؤال محصول تازه‌ای از این بازبینی نتیجه نمی‌شود.

## ۱۴. ممیزی کامل snapshot نامزد مرکزی 2.0.0-rc.1

این بخش جایگزین وضعیت بازِ H-R01 تا H-R04 در snapshot اولیه است: هر چهار اصلاح در نامزد کامل ادغام و در متن و بردارهای مربوط مشاهده شدند؛ از نظر طراحی بسته‌اند. تمام۲۱فایل manifest خوانده/ساختاری بررسی شدند؛ SQL فقط متن بود و اجرا نشد. schema/API به‌صورت داده خوانده و انواع/بدنه/مرزهای آن با سند تطبیق داده شدند؛ ادعای اجرای validator مستقل JSON Schema یا تست HTTP نمی‌شود.

**مرجع دقیق بررسی:** SHA256 بایت‌های manifest برابر:

```text
4eb749e260e994d8df919840dd0d6f4699f8d9393ffb5e5e02150586c5665568
```

بررسی مستقل در این سشن: digest نرمال‌شدهٔ هر۲۱فایل با manifest برابر بود؛ هر۷golden vector هویت و content با محاسبهٔ مستقل SHA256/canonical JSON تطبیق داشت. این بررسی داده/مستندات است؛ نه runtime هاب، firmware، SQL، DB، lock/grant یا benchmark. فایل‌های مرکزی در حین ممیزی تغییر نکردند.

### نتیجهٔ فنی

**NEEDS REVISION — تأیید نهایی روی این hash صادر نمی‌شود.** معماری و تصمیم‌های محصول تأییدشده‌اند؛ موارد زیر اختلاف اجرایی قابل رفع در همین بسته هستند. نیازی به سؤال تازه از مالک یا بازکردن تصمیم دیتابیس/معماری نیست. runtime gates مثل view locking، grants و ظرفیت هنوز NOT RUN باقی می‌مانند و پس از اجازهٔ اجرا روی fixture مستقل اثبات می‌شوند.

### H-R05 — blocker: سقف بدنهٔ commit بازیابی با ظرفیت job سازگار نیست

مسیرها: `SECURITY-RUNTIME.fa.md` بخش limits؛ `domain.schema.json#/$defs/RecoveryCommit`؛ `openapi.json` عملیات commitRecovery؛ آزمون T34.

مدیریت عمومی فقط۶۴KiB است؛ تنها upload استثناست. RecoveryCommit تا۱۰هزار تصمیم می‌پذیرد. یک نمونهٔ صرفاً حافظه‌ای با۱۰هزار تصمیم replace، reason کوتاه «Test correction» و revision1، به۸۸۹۰۶۹بایت رسید؛ حدود۱۳٫۶برابر سقف. بنابراین فایل در حدود مجاز می‌تواند preview شود ولی کاربر نتواند تصمیم‌های آن را commit کند.

اصلاح پیشنهادی: سقف مستقل و صریح برای commitRecovery تعیین شود؛ پیشنهاد اولیه۸MiB به‌همراه x-body-limit-bytes در OpenAPI و کنترل byte قبل parse است، با تصریح اینکه سقف تعداد و سقف byte مستقل‌اند. اگر نگه‌داشتن سقف۶۴KiB الزام است، API ثبت/صفحه‌بندی تصمیم‌های ثابت و commit با reference لازم دارد؛ این شکل در schema فعلی وجود ندارد. راهکار انتخاب‌شده در تست۱۰هزار تصمیم و خطای۴۱۳ پوشش یابد. DDL فقط در راهکار staging ممکن است تغییر کند؛ firmware اثری ندارد.

### H-R06 — blocker: predicate بازیابی lease باید با state واقعی و زمان retry یکسان شود

مسیرها: `TRANSACTIONS.fa.md` بخش lease؛ `domain.schema.json#/$defs/Job`؛ `API-SEMANTICS.fa.md` job projection؛ آزمون T20/T02.

متن claim «queued یا leased با lease_until<=dbNow» است، درحالی‌که state اعلام‌شدهٔ job برابر running است و leased نه در schema و نه در mapping داخلی تعریف نشده است. next_at_ms نیز در predicate claim صریح نیست. دو پیاده‌ساز می‌توانند یکی running بنویسد و دیگری فقط leased را reclaim کند، یا retry backoff را نادیده بگیرند.

اصلاح پیشنهادی recovery: `(state='queued' AND next_at_ms<=dbNow) OR (state='running' AND lease_until_ms<=dbNow)`؛ سپس تحت clock، fence++، state=running و owner/lease تازه. تمام حالت‌های terminal، pending_authorization، cancel و needs_review قابل claim نیستند. وضعیت داخلی execution عملیات خارجی و projection آن به externalState نیز دقیقاً فهرست شود؛ اگر leased نام داخلی انتخاب می‌شود، mapping و predicate هر دو صریح شوند. صرف timestamp یا default lease=NULL مجوز claim حالت terminal نیست. DDL جدید لزوماً لازم نیست؛ متن/state machine و vectors باید یکسان شوند.

### H-R07 — blocker قرارداد چندمنبعی: config چند profile باید representation مرجع داشته باشد

مسیرها: CreateSource.adapterProfiles تا۱۶profile؛ SetConfig/SourceConfig تک profile؛ GET/PUT `/sources/{id}/config`؛ جدول config append-only؛ آزمون T01/T12.

CreateSource چند profile می‌پذیرد ولی GET config هیچ profile selector ندارد و SourceConfig تنها یک profileId/publicConfig برمی‌گرداند. معلوم نیست PUT پروفایلB، A را حذف می‌کند، merge می‌کند یا current_revision فقط آخرین profile است. RegistryRead و export باید بتوانند HTTP و MQTT و profileهای هم‌زمان را از snapshot واحد بازسازی کنند؛ hidden merge پیاده‌ساز قرارداد نیست.

پیشنهاد: یک source-config snapshot نسخه‌دار با entries آرایهٔ profileId/version/publicConfig/secretRefهای خصوصی، یا endpoint و projection صریح per-profile با source revision سراسری تعریف شود. scope secret reference و CAS روی همان snapshot روشن بماند. پروفایل مرکب SFP در بخش۱۵ HTTP و MQTT فعلی را در یک entry پوشش می‌دهد، اما API عمومیِ مجاز به۱۶profile همچنان باید رفتار معین داشته باشد. این تغییر generic config/API است، نه دخالت برنامه در parser یا تصمیم محصول جدید.

### H-R08 — blocker حقیقت منشأ: delivery نامعلوم در firmware موجود قابل بیان نیست

مسیرها: `domain.schema.json#/$defs/Provenance`؛ ADAPTER-PORTS؛ آزمون T03/T16/T29.

delivery اجباری و فقط live/replay/recovery/manual_correction است. SFP t/q هیچ replay flag، boot ID یا شناسهٔ نوع ارسال ندارد؛ همان قالب برای نمونهٔ جاری و آرشیو آفلاین استفاده می‌شود. قدیمی‌بودن timestamp، با clock نامطمئن، اثبات replay نیست. آداپتر نمی‌تواند در همهٔ موارد یکی از live/replay را با قطعیت انتخاب کند.

اصلاح کمینه: افزودن `unknown` به delivery و استفادهٔ آن برای SFP فعلی؛ CSV مجاز همچنان recovery است. late metadata از نوع delivery جدا بماند. گزینهٔ دیگر، delivery=sender و replayStatus مستقل است ولی برای این تحویل enum unknown تغییر کوچک‌تری است. quality clock و sourceMode مستقل می‌مانند. در SQL metadata_json جا دارد و تغییر فیزیکی جدید لازم نیست. شکل پیشنهادی adapter بخش۱۵ همین unknown را می‌خواهد و تا اصلاح enum، نمونهٔ normalized آن نباید به‌دروغ live/replay معرفی شود.

### H-R09 — تکمیل لازم: جدول mapping immutable در برابر config revision تازه

مسیرها: storage-additions.sql، telemetry_transport_mappings با UNIQUE(source_id,adapter_profile,transport_alias)؛ grants append-only؛ SET config و T12.

config_revision و adapter_version روی ردیف immutable هستند. با config تازه برای alias همان signal، INSERT ردیف نسخه‌دار دوم unique را نقض می‌کند و UPDATE هم مجاز نیست. پیشنهاد روشن: این جدول فقط اتصال هویتی اولیه/immutable را نگه دارد؛ ردیف موجود با همان domain دوباره استفاده شود و profile/config جاری از snapshot configs انتخاب شود. در این حالت config_revision آن، creation revision است و مرجع current نیست. اگر تاریخچهٔ خود mapping لازم است، head ثابت alias جدا از نسخه‌های append-only طراحی شود و binding alias→domain هرگز تغییر نکند. تغییر منبع تجاری در برنامه ربطی به این مسئله ندارد.

### H-R10 — تکمیل مدل خواندن و دریافت وضعیت؛ هم‌راستا با بازبینی خود سشن برنامه

مسیرها: Sample/Aggregate در domain؛ storage runtime/status/head و grants؛ port TelemetryRead؛ آزمون T07/T15/T25/T30/T32.

- Aggregate.sum فعلی Value غیرnullable است. نبود هیچ نمونهٔ مؤثر باید sum=null با coverage/کیفیت و sampleCount روشن داشته باشد؛ آن را صفر نسازیم. وجود نمونه‌های صفر معتبر می‌تواند sum=0 بدهد. sum دارای type فقط وقتی وجود داده و precision معتبر است؛ overflow سیاست خطای صریح لازم دارد.
- SampleView فعلی receiptId، correctionId و مرجع اثر/هش مؤثر را نمی‌دهد؛ effectiveRevision هست ولی کافی نیست که مصرف‌کننده تصویر کامل مبنای گزارش را بدون حدس نگه دارد. receiptId اصلی، correction reference و effective hash/تعریف تاریخی باید در projection قرارداد مصرف مشخص باشند. originalContentHash همان hash مقدار اولیه بماند.
- دادهٔ status فعلی SFP متن بدون زمان مبدأ و ID رخداد است؛ مدل runtime_status قدیمی فقط last_contact/last_error دارد. اگر status به‌صورت signal.state ذخیره می‌شود، flag زمانِ دریافت و محدودیت dedup باید مشخص باشد؛ اگر observation عملیاتی است، reported_state/schema/read endpoint و grant آن لازم است. «دریافت status پشتیبانی می‌شود» بدون مسیر ذخیره/مشاهده کافی نیست. outcome خصوصی command نیز به result_json محدود و redacted با projection قابل خواندن نیاز دارد.
- ترتیب قفل credential route باید در نمودار company gate → route credential → permit → tenant clock صریح باشد؛ فقط اعتبارسنجی قبل قفل کافی نیست. این نکته در پیام بازبینی سشن برنامه نیز علامت خورده است و با یک اصلاح مشترک بسته می‌شود.

### H-R11 — تکمیل grant semantics و پوشش migration

grants.json هم‌زمان update=false و updateColumns=[receipt_json] دارد. تعریف کنید update=false یعنی «UPDATE کل‌جدول ممنوع»، updateColumns مجوز مثبتِ فقط ستون‌های فهرست است؛ provisioner نباید آن را منع همهٔ UPDATE یا اجازهٔ کل‌جدول تفسیر کند. ستون‌های اجرایی نیز همین قاعده را داشته باشند. جدول خلاصهٔ STORAGE برای operations از logicalstate UPDATE صحبت می‌کند ولی grants.json update=false دارد؛ state اولیه و ownership بعدی یکسان نوشته شوند.

STORAGE M4 برای هر signal قدیمی profile minute/identity interval می‌سازد، ولی M5 دیگر scalarهای قدیمی را نیز قابل مهاجرت می‌داند. دامنهٔ interval فقط برای legacy exact interval باشد؛ gauge/state/cumulative با هویت مناسب واقعیِ baseline و journal خودشان، یا در صورت ابهام STOP صریح. این مسیر باید همراه preserve original hashes/IDs و collision check در T22 پوشش یابد. این بررسی فقط متن است؛ هیچ backfill یا DDL اجرا نشده است.

## ۱۵. تحویل دقیق profile SFP برای ادغام مرکزی

فایل محلی مکمل `docs/SFP-ADAPTER-PROFILE.proposal.json` بخشی از همین تحویل است؛ بسته یا profile نصب‌شدهٔ دوم نیست. ناشر مرکزی آن را با قرارداد اصلاح‌شده ادغام کند و مرجع نهایی داخل بسته باشد. بخش profile دارای configSchema و commandSchemas واقعیِ JSON Schema پیشنهادی است. root فایل proposal شامل privateSecretSchema، decoder، command mapping، runtime invariants و error mapping است و مستقیماً پاسخ AdapterProfiles نیست؛ فقط object profile به shape آن نزدیک است. capabilities طراحی با capabilities نصب‌شده/آزموده‌شده اشتباه نشوند.

profile مرکب `sfp.legacy-v1@1.0.0` هر دو transport فعلی را با mapping immutable و credential مستقل در یک config پوشش می‌دهد. محدودیت source فعلی uint8 node، uint32 t، uint16 q، t/q form،۷۰۰سطر، پاسخ دقیق۱۰بایتی code0 و unknown-period حفظ شده‌اند. count HTTP و MQTT کنترل‌اند؛ MQTT count یا Sparkplug استاندارد ادعا نمی‌شود. success فقط پس از ثبت/duplicate همهٔ سطرها و commit است. routeهای پیشنهادی در export تنظیم صادر می‌شوند؛ API WEB parser آن‌ها را پیاده نمی‌کند.

نام‌های command از Config.ino مستقیماً دوباره بررسی شدند: GiveState، GiveIdentify، VerifySettings، SaveSettings و Restart. command wire شامل command/data/sequenceId است. GiveState و GiveIdentify seqId دارند؛ VerifySettings در مسیر خوانده‌شده Settings_CreateJson را می‌فرستد و seqId تضمین‌شده ندارد، بنابراین retained/unmatched settings پاسخ قطعی یک درخواست تازه نیست. SaveOK ذخیره/readback را تأیید می‌کند؛ requiresRestart و اعمال سخت‌افزاری جدا می‌مانند. Restarting اثبات reboot کامل نیست و retry کور restart/save نداریم.

schema settings واقعی از metadata معتبر دستگاه استخراج می‌شود و editability/type/range/dependency و secret کنترل جدا دارند؛ فهرست نام دلخواه از مرورگر اجازهٔ write ایجاد نمی‌کند. پیام کامل command ابتدا از نظر اندازه بررسی می‌شود؛ محدودیت fragment firmware همچنان نقص شناخته‌شده و نیازمند آزمون است، بدون تغییر firmware در این مرحله. پاسخ Settings ممکن است secret داشته باشد؛ قبل هر observation عمومی، audit یا log حتماً redact و نگهداری خصوصی فقط در vault انجام شود.

فایل تنظیم قابل تحویل به تیم فنی، checklist و مقادیر معتبر برای UI/تنظیم فعلی است. firmware موجود الزاماً generic JSON import ندارد؛ دانلود فایل نباید «اعمال شد» نمایش داده شود. binary/source و ظرفیت بافر روی سخت‌افزار هنوز تطبیق/آزمون نشده‌اند.

### وضعیت تحویل و گام بعد

HUB-C01 و SFP-01 برای ادغام/رفع H-R05..11 آماده‌اند. فایل مرکزی تغییر نکرده است. هاب پس از snapshot اصلاح‌شده، schema/profile/receipt و موارد متناظر را روی hash تازه بازبینی می‌کند؛ اگر بسته شد، می‌تواند approval طراحی با runtime gates NOT RUN بدهد. اکنون مجوز شروع کد توصیه نمی‌شود؛ مانع، همین اصلاح‌های مشخص قرارداد است و نه اختلاف مفهومی یا تصمیم تازهٔ مالک.

## ۱۶. پایان بازبینی نامزد rc.2

تاریخ: ۲۰۲۶-۱۰-۱۹. این بخش پس از ادامهٔ همان مأموریت ناتمام ثبت شد. مرجع محصول و تقسیم کار تغییر نکرده‌اند. snapshot مرکزی در ابتدا و پایان بررسی با hash زیر شناسایی شد:

```text
version: 2.0.0-rc.2
manifest SHA256: ff5a188e2dec7c979cc44aa8ebdae49f37008f4d1790dfeaa7c9bb32ff3ac360
files: 22
```

### موارد بسته‌شده

اصلاح‌های H-R05 تا H-R11 در متن/مدل مربوط مشاهده و از نظر طراحی پذیرفته شدند: سقف۸MiB برای commitRecovery، predicate دقیق queued/running و next_at، snapshot entries چندprofile، delivery=unknown، metadata اولیهٔ immutable mapping، null برای sum فاقد نمونه، مرجع receipt/correction/تعریف تاریخی در SampleView، runtime status و نتیجهٔ command، قفل route credential، معنای updateColumns و STOP برای migration مبهم. این پذیرش به معنی اجرای هیچ‌یک نیست.

هر۲۲digest محتوای نرمال‌شده با manifest تطبیق داشت. بررسی کامل rc.1 و موارد تغییرکردهٔ rc.2 مبنای این ممیزی است؛ golden vectors در این snapshot تغییر نکرده‌اند و صحت محاسبهٔ مستقل آن‌ها در نوبت قبلی ثبت شده است. ادعای اجرای دوبارهٔ validator یا SQL نمی‌شود. همهٔ گیت‌های runtime از جمله T01 تا T34 هنوز NOT RUN هستند.

**انتخاب status صرفاً به‌صورت RuntimeObservation را تأیید می‌کنم:** برای این firmware timestamp و event ID تاریخی اختراع نشود، statusSignalId=null بماند، last_sample جلو نرود و گزارش production از آن sample فرضی نسازد. قالب decoder تکمیلی در بخش۱۷ است؛ با همین انتخاب مرکزی سازگار است.

### بررسی افزودهٔ conflict case/resolution

اصل ledger جدید صحیح است و پذیرفته می‌شود: کلید case برابر sampleId/incomingContentHash است؛ keep/replace/void با اختیار و CAS و actor ثبت می‌شود؛ retry همان hash حل‌شده فقط duplicate تصمیم پایدار با code روشن است و head را دوباره تغییر نمی‌دهد. resolved_* به معنی برابرشدن مقدار فرستنده با مقدار مؤثر نیست؛ به معنی تصمیم آگاهانهٔ ذخیره‌شده دربارهٔ همان اختلاف است. hash تازهٔ دیده‌نشده همچنان conflict است و حذف یا لغو دسترسی با این ledger دور زده نمی‌شود.

دو مورد زیر برای سازگاری همین رفتار با ذخیره‌سازی/آزمون باید صریح شوند؛ معماری یا تصمیم محصول را تغییر نمی‌دهند.

### H-R12 — blocker دقیق: رسید شکست نباید کلید دریافت موفق را برای همیشه اشغال کند

مسیرها: TRANSACTIONS بخش ingest و recovery؛ STORAGE بخش ingestions؛ baseline UNIQUE(source_id,batch_id)؛ profile decoder.batchId؛ آزمون‌های T04/T07/T29.

سناریو: نمونهٔ اولیه۷ است؛ بستهٔ SFP با۹ تعارض می‌خورد و diagnostic شکست ثبت می‌شود. کاربر keep/replace/void را پایدار می‌کند. firmware همان بدنه را retry می‌کند، پس batchId مشتق‌شده و payload hash همچنان ثابت‌اند. اکنون باید duplicate حل‌شده و پاسخ موفق بگیرد. اگر diagnostic شکست همان کلید batch را گرفته باشد، lookup رسید قبلی شکست را برمی‌گرداند یا UNIQUE مانع receipt موفق تازه می‌شود؛ UPDATE همان receipt نیز با immutableبودن سابقهٔ شکست ناسازگار است.

عبارت فعلی «diagnostic مستقل» جهت درست را می‌دهد، ولی namespace و precedence lookup را مشخص نمی‌کند. **اصلاح پیشنهادی قطعی بدون جدول جدید:**

1. فضای batch_id عملیاتی موفق را از diagnostic شکست جدا تعریف کنید. پیشنهاد محدود: همهٔ شناسه‌های ورودی به یک success-ledger key با پیشوند `ok:` و SHA256 از شناسهٔ قراردادی/namespace منتقل شوند؛ diagnostic با `diag:` و UUID مستقل ثبت شود. payload_hash محتوای معتبر همچنان برای همان success-ledger key مقایسه شود؛ collision/تفاوت hash خطای صریح است. الگوریتم namespace در یک فایل مرجع باشد و legacy receiptها با نسخهٔ خود خوانده شوند.
2. فقط receipt موفقِ commit‌شده cache نهایی پذیرش است. پس از receipt شکست، retry با auth/gate و case/resolution فعلی دوباره ارزیابی شود؛ شکست قبلی موفقیت نمی‌سازد و مانع موفقیت بعدی نیست.
3. diagnostic قبلی immutable بماند. موفقیت بعد از resolution receipt تازه می‌سازد و به case/resolution ارجاع می‌دهد؛ raw، head و diagnostic قبلی بازنویسی نمی‌شوند.

ناشر می‌تواند namespace هم‌ارز دیگری انتخاب کند، ولی shape و الگوریتم دقیق باید در همان بسته واحد باشد. test vector لازم: reject۹ → keep۷ → retry۹ → code0؛ همچنین replace۹ و void؛ پس از آن retry مکرر هیچ effect تازه نداشته باشد. این افزودن، آزمون پذیرش آینده است و فعلاً اجرا نشده است.

### H-R13 — blocker کوچک: تعارض داخلی بسته با alias حل‌شده تقدم روشن داشته باشد

مسیرها: TRANSACTIONS ingest بند۴؛ ADAPTER-PORTS؛ ACCEPTANCE.T14 و T29.

T14 فعلی به‌طور مطلق می‌گوید دو value متفاوت برای یک identity کل بسته را رد می‌کنند. ledger جدید اجازه می‌دهد originalHash و hash اختلافِ حل‌شده هر دو برای همان observation پاسخ duplicate بگیرند. اگر firmware بسته‌ای شامل هر دو بفرستد، prevalidation مطلقِ T14 می‌تواند قبل lookup resolution همیشه آن را رد کند؛ تصمیم کاربر صف را آزاد نمی‌کند.

اصلاح پیشنهادی: parse/type و جمع‌آوری گروه‌های identity قبل transaction انجام شود؛ تصمیم semantic conflict بعد از lookup پایدار original/case/resolution و تحت gate گرفته شود. اگر همهٔ hashهای گروه، original یا alias حل‌شدهٔ همان نمونه‌اند، همه duplicate و بدون effect تازه‌اند؛ حتی اگر valueهای wire متفاوت باشند. هر hash جدیدِ حل‌نشده یا گروه متناقضی که هنوز نمونهٔ مرجع ندارد، کل بسته را بدون sample تازه رد کند. T14 به «تعارض حل‌نشده داخل بسته» محدود و یک vector مجزا برای دو hash مجاز اضافه شود. این استثنا فقط از ledger پایدار می‌آید، نه از ترتیب سطرها یا انتخاب اولین مقدار.

### تکمیل خوانایی preview؛ شرط اجرای تصمیم آگاهانه

PreviewRow در schema فعلی incomingValue/existingValue دارد. content hash اکنون زمان و بازه را نیز پوشش می‌دهد، پس ممکن است valueها برابر باشند ولی اختلاف زمانی وجود داشته باشد. renderer باید تفاوت را از snapshot ثابت نشان دهد؛ برای این حالت تنها نمایش۷درمقابل۷ کافی نیست. پیشنهاد تکمیل projection با incoming/existing eventTime و period، caseId/incomingContentHash و differenceReasons است. هویت و hash تصمیم از preview سرور می‌آیند، نه از جایگزینی آن‌ها توسط مرورگر. این تکمیل با مفهوم preview دارای fingerprint سازگار است و parser خاص تجهیز وارد business نمی‌کند.

### نتیجه روی این snapshot

وضعیت هاب: **NEEDS REVISION؛ H-R05..11 CLOSED، H-R12/H-R13 OPEN.** اصل مدل جدید resolution و مسیر status پذیرفته‌اند. برای امضای فنی یک hash مشخص، این دو قاعده و decoder status بخش۱۷ در مرجع مرکزی ادغام شوند؛ سپس همان delta و manifest تازه قابل بازبینی‌اند. approval کلی یا امضای سشن برنامه به‌جای آن ساخته نشده است. این گزارش فقط محلی است و فایل approval کنار بستهٔ اصلی نیز در این سشن تغییر نمی‌کند.

## ۱۷. مکمل دقیق decoder HTTP status برای SFP-01

شواهد مستقیم: `internet.ino:216–223` فرم را با اتصال رشته می‌سازد؛ سطر۲۱۸ هر پیام را به شکل `{"s":"<text>"}` می‌گذارد. سطرهای۲۶۱تا۲۶۷ پاسخ۲۰۰ و substring code0 را می‌خوانند و سپس کل buffer status را خالی می‌کنند. `settings.h:317` ظرفیت این buffer را۵پیام تعیین کرده است. این بررسی source است؛ binary و سخت‌افزار اجرا نشده‌اند.

نمونهٔ کاملاً ساختگی wire:

```text
Content-Type: application/x-www-form-urlencoded
Authorization: <configured scheme> <private token>

node_id=1&data=[{"s":"Network connected"},{"s":"Queue retry pending"}]
```

پیشنهاد ادغام زیر در decoder پروفایل مرکزی؛ مقادیر این ضمیمه پیشنهادی‌اند تا در فایل مرجع بسته ادغام شوند:

```json
{
  "statusContentType": "application/x-www-form-urlencoded",
  "statusFormKeys": ["node_id", "data"],
  "statusRowKeys": ["s"],
  "maxStatusRows": 5,
  "maxStatusBodyBytes": 65536,
  "maxStatusTextUtf8Bytes": 8192,
  "statusCompressedBody": false,
  "statusAcceptanceMode": "atomic_runtime_snapshot",
  "statusIdentity": "sender_identity_unavailable",
  "statusSuccessStatus": 200,
  "statusSuccessBodyUtf8": "{\"code\":0}",
  "statusStorage": "RuntimeObservation.reportedState.httpStatusMessages",
  "statusEventTime": null,
  "statusTimeBasis": "received"
}
```

قواعد parser و دوام:

1. auth و source/node mapping و current profile/gate همان قواعد دریافت را رعایت کنند. node نامعلوم شرکت/تگ نمی‌سازد؛ status credential معتبر source حذف‌شده را زنده نمی‌کند.
2. برای فرم خامِ همین firmware، prefix قطعی `node_id=<decimal>&data=` را بخوانید و **تمام دنبالهٔ JSON را خام** parse کنید. این firmware percent-encoding انجام نمی‌دهد؛ استفادهٔ کور از URLSearchParams برای متن خام، `+` را به space و `&` داخل متن را به field تازه تبدیل می‌کند. در این مسیر raw، درصد و plus بخشی از متن‌اند، نه دستور decode. JSON باید تمام دنباله را مصرف کند؛ پس field اضافی بعد آرایه یا JSON key تکراری رد است.
3. فرم استاندارد percent-encoded نیز می‌تواند مسیر مجزای مشخص داشته باشد: فقط یک node_id و data، یک‌بار decode، سپس JSON کامل. raw/encoded با شکل دادهٔ آغازین مشخص شوند؛ fallback چندمرحله‌ای decode یا اصلاح حدسی متن مجاز نیست. decoder count هم از همین تفکیک raw/encoded استفاده کند؛ نام فیلد count همچنان t/q است.
4. data آرایهٔ صفر تا۵object با دقیقاً یک key رشته‌ای s است. متن خالی مجاز؛ بیش از۵، نوع غلط، NUL، JSON خراب یا حد byte → خطای صریح بدون code0. آرایهٔ خالی فقط contact معتبر را جلو می‌برد و snapshot قبلی پیام‌ها را پاک نمی‌کند. کنترل‌کاراکترهای مجاز JSON در UI/log به‌شکل امن render شوند؛ هیچ HTML یا command اجرا نشود.
5. پس از validation کامل و redaction، همهٔ پیام‌های همین آرایه به ترتیب دریافت در یک reportedState محدود ذخیره شوند، همراه receivedAt سرور، eventTime=null و timeBasis=received. پیام‌های این آرایه نباید فقط به آخرین s تقلیل یابند و بقیه در همان دریافت گم شوند. این ردیف آخرین snapshot عملیاتی است؛ نگهداری تاریخچهٔ همهٔ statusها یا exactly-once تاریخی ادعا نمی‌شود. payload/credential خام وارد log/audit عمومی نشود.
6. patch snapshot و last_contact و version/change لازم در tenant transaction با gate معتبر commit شود؛ بعد پاسخ۲۰۰ با بدنهٔ دقیق۱۰بایتی code0 صادر شود. خطای ذخیره یا commit مبهم، ACK موفق ندارد. retry ممکن است همان snapshot را دوباره تحویل دهد؛ به‌علت نبود sender ID/زمان، dedup قطعی یا تعداد رخدادهای مستقل از آن نتیجه نگیریم. status، last_sample شمارش و reportedConfigRevision/applied را جلو نمی‌برد.

**محدودیت واقعی firmware:** JSON وضعیت با escape استاندارد ساخته نمی‌شود. اگر متن s شامل quote/backslash/newline خام باشد ممکن است JSON خراب تولید شود. هاب نباید با حدس آن را اصلاح یا موفقیت جعلی صادر کند. متن سالم با +، &، درصد و Unicode باید حفظ شود؛ متن JSON خراب رد و محدودیت در diagnostics نمایان شود. بدون تغییر firmware نمی‌توان پذیرش همهٔ متن‌های دلخواه را تضمین کرد. همین تفکیک، سازگاری با پیام معتبر موجود است و نه وعدهٔ اصلاح firmware از سمت سرور.

بردارهای تکمیلی T29 برای مرحلهٔ اجرای مجاز: دو status سالم و ترتیب حفظ‌شده؛ متن خام `A+B & 50%` بدون تغییر؛ نمونهٔ فرم استاندارد با `%2B/%26`؛ آرایهٔ خالی بدون پاک‌کردن snapshot؛ نوع/JSON خراب و پیام ششم با non-success؛ قطع DB بدون code0؛ replay status بدون افزایش فرضی رخداد؛ late status بدون عقب‌بردن last_sample. در این مرحله فقط مشخصات‌اند و NOT RUN باقی می‌مانند.

## ۱۸. بازبینی delta نامزد rc.3

تاریخ: ۲۰۲۶-۱۰-۱۹. مرجع بررسی:

```text
version: 2.0.0-rc.3
manifest SHA256: 2d09356656a8fce8ee299e89f6499c4732f2f509d609648a57791ea9c3719c07
files: 23
```

### رفع موارد قبلی تأیید شد

- H-R12 بسته شد: success-ledger با کلید `ok:` و namespace ثابت، diagnostic با `diag:` و شناسهٔ مستقل، cache موفق فقط بعد از auth/gate، و ارزیابی تازهٔ original/case/resolution بعد شکست تعریف شده‌اند. رسید موفق تازه پس از تصمیم پایدار، diagnostic قبلی را بازنویسی نمی‌کند. هر دو بردار success-key افزوده‌شده با محاسبهٔ مستقل SHA256/canonical JSON تطبیق داشتند.
- H-R13 بسته شد: تقدم lookup تحت تراکنش بر conflict معنایی گروه روشن است؛ original و alias حل‌شده می‌توانند در یک گروه هر دو duplicate باشند؛ hash ناشناخته یا تناقض بدون original همچنان کل بسته را رد می‌کند. T14/T29 و سناریوهای receipt-resolution متناظرند.
- تکمیل PreviewRow پذیرفته شد: زمان/بازه، unit/semanticKey هر دو طرف، case/hash و differenceReasons از snapshot سرور بیان می‌شوند؛ دیگر اختلاف زمانی با value مساوی از کاربر پنهان نمی‌ماند.
- بخش۱۷ status در decoder پروفایل مرکزی مشاهده و پذیرفته شد: raw و percent-encoded مجزا، حفظ +/&/%، آرایهٔ۰تا۵، empty بدون پاک‌کردن پیام‌ها، RuntimeObservation بدون sample ساختگی، عدم جلو بردن last_sample/applied و code0 پس از commit. محدودیت JSON بدون escaping در firmware مستند است و firmware تغییر نمی‌کند.

تمام۲۳digest محتوای نرمال‌شده با manifest تطبیق داشتند؛ هیچ فایل مرکزی تغییر نکرد. بررسی ساختاری/محاسبهٔ hash، تست runtime یا firmware نیست. DDL/grants در rc.3 نسبت به rc.2 تغییر معنایی تازه‌ای نداشتند؛ گیت‌های اجرایی همچنان NOT RUN هستند.

### H-R14 — تنها مانع باقی‌مانده: receiptNamespace در schema context نیست

path: `domain.schema.json#/$defs/VerifiedAdapterContext` در برابر `ADAPTER-PORTS.fa.md` بخش «فضای نام رسید».

متن، `VerifiedAdapterContext.receiptNamespace` را لازم و ثابت می‌داند و الگوریتم success-key از آن استفاده می‌کند. ولی schema فعلی VerifiedAdapterContext این property را ندارد و additionalProperties=false است؛ پس context مطابق متن در schema رد می‌شود. profile.decoder.receiptNamespace وجود دارد، اما جای فیلدِ لازم در context قراردادی را نمی‌گیرد. هاب نباید برای عبور از validation آن را پنهان/حذف کند یا namespace را از payload حدس بزند.

اصلاح کمینهٔ پیشنهادی، بدون تغییر API عمومی، DDL یا firmware:

```json
{
  "receiptNamespace": {
    "type": "string",
    "minLength": 1,
    "maxLength": 160
  }
}
```

این property به properties و نام آن به required همان definition افزوده شود. مقدار از profile معتبر سمت هاب می‌آید؛ case-sensitive و opaque است، بدون trim/NFC یا وابستگی به config/نسخهٔ parser و payload دستگاه. یک context ساختگی با receiptNamespace معتبر باید بپذیرد و context فاقد آن باید رد شود؛ همچنان فیلد اضافی ناشناخته رد شود. سپس manifest دوباره تولید و hash جدید برای امضا منتشر شود.

### نتیجهٔ محدود به این hash

**NEEDS SCHEMA ERRATUM — H-R01..13 CLOSED؛ فقط H-R14 OPEN.** در این delta مانع دیگری شناسایی نشد. اصل طراحی دریافت/رسید/تکرارگیری/حل تعارض/status تأیید است؛ امضای کل snapshot تا رفع این ناسازگاری shape ثبت نمی‌شود. اصلاح محصول یا سؤال مالک لازم نیست. پس از همان اصلاح کمینه، بازبینی delta schema/manifest برای صدور `approved-with-runtime-gates-not-run` کافی است؛ اجرای آزمون DB/firmware/بار به مرحلهٔ مجاز پیاده‌سازی تعلق دارد.

این نتیجه در گزارش محلی هاب ثبت شده و approval ledger یا فایل مرکزی ویرایش نشده‌اند. کد، دیتابیس، سرویس و firmware تغییر یا اجرا نشدند.

## ۱۹. تأیید نهایی طراحی هاب روی rc.4

تاریخ: **۲۰۲۶-۱۰-۱۹** — بازبین: **سشن هاب Pouyeshgar Data Hub**.

```text
status: approved-with-runtime-gates-not-run
package: pouyeshgar.telemetry-execution
version: 2.0.0-rc.4
productReferenceVersion: 1.1.1
manifest SHA256: e5e1dfe4c5b0d6cf97882b0acdd7f8ecb32eb18fcdbc76d331622ff71a5d250d
manifest files: 24
open identified design blockers: 0
runtime acceptance: NOT RUN
implementation authorization: NOT GRANTED BY THIS REVIEW
```

### مبنای تأیید

H-R14 رفع شد: `VerifiedAdapterContext.receiptNamespace` در schema رشتهٔ الزامی با minLength=1 و maxLength=160 است؛ additionalProperties=false حفظ شده و context نمونه هیچ فیلد اجباری گمشده یا فیلد اضافی ندارد. نمونهٔ جدید مطابق shape تعریف‌شده است. گزارش مرکزی VALIDATION نیز positive و چهار حالت منفی همین اصلاح را ثبت کرده است؛ آن اجرای AJV متعلق به سشن برنامه است، نه ادعای اجرای مستقل AJV در هاب.

hash manifest مستقلاً با مقدار اعلام‌شده برابر بود و digest نرمال‌شدهٔ هر۲۴فایل بررسی و بدون اختلاف بود. این delta در ادامهٔ ممیزی rc.1، rc.2 و rc.3 پذیرفته شد؛ شماره‌های H-R01 تا H-R14 از نظر طراحی بسته‌اند. receipt namespace/diagnostic، تقدم resolution در dedup، حفظ raw/head، status decoder و preview آگاهانه از بازبینی rc.3 معتبرند. در این نوبت مانع طراحی دیگری شناسایی نشد.

تأیید شامل مسئولیت هاب در مرزهای normalized receive/write، profile SFP و HTTP/MQTT فعلی، receipt و dedup، atomic batch، correction/recovery و fencing، حذف و gate، دوام پس از restart و قراردادهای مشترک خواندن/ذخیره‌سازی/مجوز است. این تأیید مهندسی روی **همین snapshot** است؛ تغییر معنایی آینده بازبینی متناسب و hash تازه می‌خواهد. فقط تغییر نام نسخه به‌تنهایی تضمین سازگاری نیست.

فایل بیرونی `telemetry-execution-v2-approvals.json` فقط خوانده شد: سشن برنامه نیز webReview=design-approved را روی همین hash ثبت کرده و hubReview در زمان خواندن pending-final بود. این بخش شاهد مستقل تأیید هاب برای ثبت توسط ناشر همان ledger است؛ هاب فایل مرکزی یا ledger را ویرایش نمی‌کند.

### مرز این تأیید و اجرای بعدی

تمام آزمون‌های اجرایی، از جمله MariaDB view/lock/grant، migration/backfill، رقابت delete/ingest و recovery، HTTP/MQTT و binary واقعی firmware، قطع/وصل و بار/مصرف منابع، هنوز **NOT RUN** هستند. بررسی فایل، مثال یا hash جای آن‌ها نیست. B02/B07 و T01 تا T34 طبق بسته در مرحلهٔ مجاز پیاده‌سازی و fixture مستقل باید شواهد واقعی بگیرند. خرابی اثبات اجرایی که تغییر قرارداد می‌خواهد باید با اصلاح نسخه حل شود، نه نادیده‌گرفتن گیت.

بسته از منظر هاب آمادهٔ دریافت **دستور جداگانهٔ مالک برای شروع پیاده‌سازی** است؛ این گزارش خودش مجوز کدنویسی، migration، اتصال، deploy، تغییر firmware یا دست‌زدن به محیط برنامهٔ اصلی نیست. محدودیت‌های AGENTS و محل مجاز کار هر سشن حفظ می‌شوند. هیچ قابلیت نصب‌شده، تضمین صنعتی یا آمادگی production از این امضا نتیجه نمی‌شود.

در این مرحله فقط این گزارش محلی تکمیل شد. کد، DB، سرویس، محیط اجرایی، firmware و snapshot مرکزی تغییر نکردند. پیشنهادهای تاریخی HUB-C01 و SFP-01 پس از ادغام، مرجع اجرایی موازی نیستند؛ مرجع واحد همان بستهٔ مرکزی با hash بالا است.
