# تجمیع ساختاری WEB و INGEST — ۲۰۲۶-۱۰-۱۹

این مرحله با دستور صریح مالک، پیش از پیاده‌سازی قرارداد rc.4 انجام شد. تغییر منطق دریافت/تولید، migration دیتابیس، اتصال تجهیزات، تغییر firmware، merge به شاخهٔ اصلی و deployment جزو این مرحله نیست.

## شاخه و نقطه‌های بازگشت

- شاخهٔ جدید: `codex/telemetry-monorepo`.
- Worktree: `D:/git/pouyeshgar-workshop/.local/worktrees/telemetry-monorepo`.
- مبنای WEB: `6881af4f543c48af3ba3a60bcf8b78ed3a48ad41` در `codex/integrated-telemetry-v1`.
- checkpoint شامل تمام ۳۲ فایل کاری ثبت‌نشدهٔ همان سشن، از جمله UI و بستهٔ تأییدشده: `2dd5d45`؛ پیش از انتقال ساخته شد. فایل‌های اصلی آن worktree و تغییرات ثبت‌نشده‌اش دست‌نخورده‌اند.
- مبنای هاب: `b9c43c162bc5be826f568a41e580f8cac17214ea` در مخزن قبلی و شاخهٔ `main`؛ هیچ tracked change نداشت. شش گزارش ثبت‌نشده در `docs/archive/data-hub/reviews` حفظ شدند.
- واردکردن کامل تاریخچهٔ هاب با subtree بدون squash: `82dada9686c153deb382b67cccdd890c2d6cb11d`. commit مبنای هاب ancestor واقعی این شاخه است؛ فقط کپی فایل یا مخزن توکار نیست.
- برای مرور وضعیت قبل از تجمیع، از `2dd5d45` یک branch/worktree جدا بسازید؛ checkoutهای فعال را reset نکنید. هر دو مخزن قدیمی فعلاً باقی می‌مانند و هیچ کدام archive یا حذف نشدند.

## محل واحد هر بخش

| مسیر | مسئولیت واقعی اکنون |
|---|---|
| `src/` و `server/` | WEB فعلی، بدون جابه‌جایی یا تغییر منطق |
| `services/ingest/server/` | backend آزمایشگاهی هابِ قبلی، شامل دریافت و management قدیمی؛ هنوز پیاده‌سازی rc.4 نیست |
| `services/ingest/tests/hub.test.ts` | همان ۹ تست موقت SQLite/HTTP/MQTT |
| `labs/data-hub/src/` | پنل Vue مستقل قبلی؛ به WEB متصل یا در منوی آن نصب نشده |
| `labs/data-hub/server/simulator.ts` | شبیه‌ساز مستقل قبلی؛ از lifecycle WEB و INGEST مستقل |
| `packages/telemetry-contract/contract/` | تنها بستهٔ اجرایی مصوب، بدون تغییر محتوای آن |
| `docs/archive/data-hub/` | مستندات، launchers و lock/config قبلی برای سابقه؛ دستورالعمل فعال نیستند |

پنل قبلی از session و `/api`های قدیمی استفاده می‌کند. انتقال آن به UI اصلی یا حذف management از backend قدیمی نیازمند کار پیاده‌سازی بعدی است؛ در این انتقال وانمود نشده که API قدیمی rc.4 است. `createApp` قدیمی همچنان فقط با اجرای صریح آزمایشگاهی seed می‌کند؛ هیچ import یا startup از WEB به آن اضافه نشد.

## قرارداد و مرز دو فرایند

نسخه: `2.0.0-rc.4`؛ SHA256 دقیق manifest:

`e5e1dfe4c5b0d6cf97882b0acdd7f8ecb32eb18fcdbc76d331622ff71a5d250d`

هر ۲۴ artifact با digest قبلی مطابق است. مسیر قدیمی `docs/integration/telemetry-execution-v2` فقط redirect مستنداتی دارد. record تأیید هر دو سشن در `docs/integration/telemetry-execution-v2-approvals.json` با نقشهٔ انتقال مسیر حفظ شد. فایل‌های wrapper و validator پکیج بیرون snapshot امضاشده‌اند. بعضی اشاره‌های نسبی داخل متن frozen بازتاب محل تاریخی‌اند؛ README بیرونی پکیج، محل فعلی record و سند واحد محصول را مشخص می‌کند. آن‌ها مجوز ایجاد قرارداد کپی‌شدهٔ دوم نیستند.

WEB و INGEST دو lifecycle، دستور اجرا، خروجی build و credential محدود مستقل دارند. dependency به پکیج قرارداد صرفاً JSON/schema/location است، نه dependency به runtime دیگری. INGEST آینده برای هر packet به HTTP WEB وابسته نمی‌شود؛ دسترسی پایگاه داده از مسیرهای محدود مصوب و TenantDirectory می‌گذرد. Monorepo مجوز مشترکِ نامحدود دیتابیس نمی‌سازد. اجرای جدا روی دو سرور و مقیاس‌دهی جدا باید در پیاده‌سازی rc.4 حفظ و تست شود؛ این migration آن آزمون را انجام نداده است.

MariaDB فعلی حفظ شده؛ مرزهای persistence و قابلیت مهاجرت کامل به engine/topology دیگر طبق قرارداد تغییری نکرده‌اند. SQLite در کد قدیمی فقط lab است، انتخاب دیتابیس محصول نیست. مالی و trial ساخته نشده‌اند.

## وابستگی و محیط مشترک

Node توصیه‌شده و CI: `24.19.0`؛ ابزار بسته‌ها: `pnpm@11.25.0`. نسخهٔ Node در `.node-version` و `.nvmrc` ثبت شده؛ `packageManager` در manifest ریشه موجود است. نسخهٔ سیستم تغییر نکرد. تنظیم store/cache و رفتار اجرای script در خود pnpm-workspace.yaml ثبت شده است؛ فایل .npmrc فقط به این مرجع اشاره می‌کند چون pnpm 11 تنظیمات پروژه را از workspace می‌خواند.

یک `pnpm-workspace.yaml` و یک lockfile فعال ریشه داریم. catalog برای Vue، Fastify، MariaDB، ExcelJS، TypeScript، tsx، Vite، plugin-vue، vue-tsc، Node types، formatter و آیکون‌ها نسخهٔ exact مشترک دارد. نسخه‌های اصلی WEB موجود حفظ شدند؛ ابزارهای قدیمی پنل هاب با آن‌ها یکسان شدند. lockfile قدیمی هاب فقط در archive برای سابقه است.

```text
pnpm install --frozen-lockfile
pnpm test:all
pnpm build:all
```

فرمان‌های مجزا: `pnpm test` و `pnpm build` برای WEB؛ `pnpm test:ingest` و `pnpm build:ingest` برای دریافت؛ `pnpm contract:check` برای قرارداد؛ `pnpm build:hub-lab` برای پنل قدیمی.

`pnpm ingest:lab` فقط فرمان صریح اجرای آزمایشگاه قبلی است، نه راه‌اندازی rc.4. cwd آن `services/ingest` است؛ private و dist همان‌جا محلی و ignored می‌مانند. پنل با build جدا در `services/ingest/dist` خروجی می‌گیرد تا backend قدیمی بدون تغییر منطق فایل‌هایش را سرو کند. شبیه‌ساز از `pnpm simulate:hub-lab` با همان cwd آزمایشگاه، در خود فرایند راه‌انداز و بدون ساخت child اجرا می‌شود؛ SIGINT/SIGTERM مستقیماً به همان فرایند می‌رسند و توقف wrapper فرزند جدا باقی نمی‌گذارد. هیچ‌یک با install/build/test خودکار شروع نمی‌شوند. پورت‌های ثابت قدیمی ممکن است در اختیار نسخهٔ قبلی باشند؛ این فرمان‌ها در این مرحله روی آن پورت‌ها اجرا نشدند. launchers قدیمی archive شده‌اند و به‌عنوان فرمان فعال ارائه نمی‌شوند.

private، credential، فایل دیتابیس، node_modules و خروجی build قبلی وارد Git یا مخزن جدید نشدند. فقط بسته‌های عمومی dependency از cache نصب شدند. مسیر store/cache محلی هر worktree زیر `.local` است؛ از مسیر مطلق لپ‌تاپ در تنظیمات قابل commit استفاده نشده است.

## شواهد قبل و بعد

| بررسی | قبل | بعد |
|---|---|---|
| WEB default tests | ۷۴ موفق، ۱ skipped اختیاری، صفر fail | همان نتیجه |
| هاب default tests | ۹ موفق، صفر fail | همان ۹ موفق |
| WEB typecheck و build | موفق | موفق |
| backend هاب typecheck/compile | موفق در کپی ایزولهٔ مبنا | موفق |
| Vue هاب typecheck/build | موفق در کپی ایزولهٔ مبنا | موفق؛ هر ۹ فایل خروجی byte-identical |
| توقف شبیه‌ساز | راه‌انداز جدید موجود نبود | یک تست ساختگیِ بدون شبکه: cwd صحیح، PID برابر با launcher، پایان پس از SIGTERM |
| قرارداد | snapshot تأییدشده | ۲۴ digest، ۶۱ تعریف، ۳۷ operation، ۳۲۹ reference، ۸ مثال منفی و golden vectors موفق |
| مرورگر | این مرحله baseline تصویری تازه ادعا نمی‌کند | ورود WEB و ورود ساختگی پنل قدیمی موفق؛ pageerror صفر |

۲۲۱ فایل کد WEB (`src/server/tests/tools/scripts`) پس از نرمال‌سازی CRLF/LF بدون اختلاف‌اند. همهٔ ۶۰ فایل tracked هاب یا بدون تغییر حفظ/منتقل شده‌اند یا تنظیم build آن‌ها ثبت شده؛ تنها تغییر فایل پیکربندی Vite قدیمی، مسیر static output است. نقشه و hashها در `TELEMETRY-MONOREPO-SOURCE-MAP.json` قرار دارند. CSS/JS اصلی WEB بعد از نادیده‌گرفتن hash شناسه‌های scoped Vue و نام فایل CSS برابرند؛ اسم bundle متفاوت به‌تنهایی تغییر رفتار نیست.

QA مرورگر با Chromium موقت، پورت loopback تصادفی و SQLite ساختگی انجام شد؛ هیچ account یا شرکت جاری مصرف نشد. سرورها و مرورگر تست بسته و دیتابیس موقت پاک شد. تصاویر محلی در `.local/migration/browser` و logها در `.local/migration` هستند و commit نمی‌شوند. CI به Node/pnpm مشترک و تست/build workspace بروزرسانی شد، ولی اجرای remote CI هنوز انجام نشده است.

نصب frozen/offline پس از بازسازی فقط node_modules خود worktree با store محلی آن موفق شد؛ مسیر واقعی node_modules metadata هم به همین worktree اشاره می‌کند.

در کپی اولیهٔ cache، junction داخلی `projects` به اشتباه دنبال شد؛ پردازش همان کپی متوقف و فقط زیرپوشهٔ موقت تأییدشده پاک شد. package blobs و index عمومی کش جدا استفاده شدند. هیچ checkout یا سرویس قبلی از این روال پاک یا جابه‌جا نشد.

## تقسیم کار از این نقطه

هر سشن باید از همین branch/commit مشترک، worktree و branch خودش را بسازد. WEB مالک `src/`، `server/` و منطق business است؛ INGEST مالک `services/ingest/` و adapter/recovery execution است. پنل نهایی هاب در WEB طبق قرارداد اجرا می‌شود؛ `labs/data-hub` مرجع اجرای فعلی/سابقه است، نه پنل نهایی محصول. سشن هاب نباید دوباره از مخزن قدیمی به عنوان مبنای کدنویسی rc.4 ادامه بدهد.

قرارداد مشترک با یک نویسنده و بازبینی طرف مقابل تغییر کند؛ دو agent روی همان فایل/lockfile هم‌زمان ننویسند. افزودن dependency مشترک از catalog و یک تغییر lockfile هماهنگ انجام شود. این برنچ را دو سشن به‌طور هم‌زمان ویرایش نمی‌کنند.

گام بعدی، پیاده‌سازی و آزمون واقعی rc.4 پس از پایان بازبینی همین انتقال است. T01 تا T34، migration واقعی MariaDB، lock/grant/race، firmware، اتصال صنعتی، بار و scale هنوز NOT RUN هستند؛ ۹ تست قدیمی هاب جای آن‌ها را نمی‌گیرند. اسناد تغییر مکان داده‌اند، تصمیم‌های محصول باز نشده‌اند.

## نتیجهٔ بازبینی انتقال

سشن برنامه و سشن هاب انتقال ساختاری را تأیید کردند. implementation commit بررسی‌شده `e51f09653a9cbe5ba657ba1ae1fef27b8e5f6389` است؛ record دقیق در [TELEMETRY-MONOREPO-REVIEW.json](TELEMETRY-MONOREPO-REVIEW.json) قرار دارد. هاب فایل‌ها/مرزها و اصلاح wrapper را مستقلاً خواند؛ تست‌ها را دوباره اجرا نکرد و به‌دلیل محدودیت Git ادعای بررسی مستقل ancestry نمی‌کند. شواهد اجرای تست و ancestry متعلق به سشن برنامه‌اند. commit بعدی صرفاً همین ثبت ممیزی است و منطق runtime را عوض نمی‌کند.
