# UI-UX SPEC — accepted direction and remaining validation

## نمایش دادهٔ موقت — ۲۰۲۶-۱۰-۲۸

آمادهٔ استفاده در حالت «نمایش بدون ثبت» آخرین مقدار نمایشی، زمان داده و زمان دریافت هر تگ را نشان دهد؛ تاریخچه با آن ادغام نشود. داده‌های دریافتی برای منبع انتخاب‌شده در این حالت، تب نمایشی مستقل با بازخوانی۵ثانیه‌ای، فیلتر تگ/نتیجه و صفحه‌بندی دارد. برچسب صریح موقت بودن و پاک‌شدن با restart گیرنده الزامی است. تست دریافت تعداد پیام‌ها را از تعداد مقادیر استخراج‌شده جدا نمایش دهد؛ کد و توضیح آلارم دو مقدار از یک پیام‌اند.


## جدول تگ — اصلاح جاری ۲۰۲۶-۱۰-۲۷

کد TAG.IN./TAG.OUT. با پیشوند قفل‌شده و نام قابل ویرایش، تک‌خطی باشد. اقدام ردیف سه‌نقطهٔ بدون کادر با منوی «ویرایش نام تگ / جزئیات فنی» است؛ منو جدول را گسترش ندهد و داخل overflow بریده نشود. دکمهٔ «ذخیره و اعمال» همان لحظه ثبت و اعمال می‌کند؛ Save قبلی پیش‌شرط نیست. بازخوانی دادهٔ ثبت‌شده «بررسی داده‌های دریافتی» نام دارد. این تصمیم بر نام‌گذاری قدیمی IN./OUT. و دکمه‌های ردیفی مقدم است.


## اصلاح جاری راه‌اندازی — ۲۰۲۶-۱۰-۲۷

کلید تست جدا وجود ندارد؛ همان کلید دستگاه استفاده می‌شود. شروع تستِ منبع عملیاتی با تأیید، توقف ثبت و پیش‌نمایش بدون تاریخچه است. Stop دریافت را بسته می‌گذارد تا حالت نهایی صریح اعمال شود. کد خوانای IN./OUT. جدا از UUID و کلید کانال، قابل ویرایش در مرحلهٔ تگ‌ها/آمادهٔ استفاده/فهرست تگ‌هاست؛ پیشوند جهت قفل و پسوند قابل ویرایش است. جدول اصلی نام، کد، مسیر مقدار، نوع/واحد، جهت و اقدام دارد؛ شناسه‌های داخلی زیر جزئیات فنی‌اند. نگاشت پارامتر کد/نام/منبع/جهت و جست‌وجو دارد. توضیح‌های تست فارسی ساده و مستقل از واژه‌های فنی پاسخ‌اند. این بخش بر شرح‌های قدیمی‌ترِ کلید تست یا سبزشدن صرفاً بر اساس نمونه مقدم است.


## بازخورد میدانی — عکس و نوع دستگاه، ۲۰۲۶-۱۰-۲۵

«ذخیرهٔ مشخصات» فقط۹px از فرم معرفی فاصله بگیرد. نوع منبع دستگاه/سامانه است، مستقل از پروتکل؛ گزینه‌ها با backend مشترک‌اند و OPC UA نباید به‌عنوان نوع سخت‌افزار ظاهر شود. انتخاب نوع، driver را فعال نکند. جدول کانال HTTP جهت «ورودی به هاب» نشان دهد؛ گزینهٔ نمایشی خروجیِ فاقد runtime اضافه نشود. عکس PNG شفاف روی پس‌زمینهٔ طبیعی فرم و بدون سفیدکردن فایل حفظ شود؛ بارگذاری/ذخیره و بازگشت بعد از رفرش باید واقعی باشد. image reference خصوصی از API مجاز بارگذاری شود؛ عکس در metadata/base64 روی دیسک یا public قرار نگیرد.


## راه‌اندازی منابع داده — ویزارد گرافیکی، ۲۰۲۶-۱۰-۲۵

نمای قبلی و نمای۲ برای مقایسه حفظ شوند. نمای۳ یک مسیر اجرایی باشد: دیاگرام کوتاه بالای فرم، معرفی/پروتکل/اتصال/پیام/تست/تگ/نتیجه. گرهٔ ساختار پیام بزرگ‌تر و پایان متمایز باشد؛ ردیف دیگری برای عنوان تکراری یا ابزارهای عمومی اضافه نشود. گره‌های طی‌شده قابل برگشت، مرحلهٔ بعد تابع اعتبار فرم و دریافت واقعی باشد. فهرست جانبی جمع‌شونده با جست‌وجو، مرحله و صفحه‌بندی برای ده‌ها مسیر؛ فرم اصلی متناسب با طول ورودی چندستونه شود. در موبایل دیاگرام اسکرول داخلی دارد و صفحه نباید افقی بیرون بزند.

در مسیر اصلی فقط HTTP عمومی تک‌آدرسه نمایش داده شود؛ قالب ثابت قدیمی انتخاب جداگانه نداشته باشد. منبع قدیمی با پیش‌نویس الگوی قابل ویرایش و هشدار تغییر URL باز شود؛ مهاجرت با ذخیرهٔ ساختار انجام شود. مسیر چندکاناله، کانال‌های متعدد و پیش‌نمایش استخراج با همان parser گیرنده دارد؛ پیش‌نمایش به سرور داده نمی‌فرستد. روشِ فاقد آداپتور فقط «پیش‌نویس» است و Next نباید اتصال موفق نشان دهد. ذخیرهٔ پیشرفت و وضعیت دریافت مستقل نمایش داده شوند؛ سبز نهایی یعنی نمونهٔ معتبر برای هر کانال ذخیره شده، نه اینکه دستگاه اکنون آنلاین است. اصلاح مسیرهای پیام بعد از دریافت، نسخهٔ تازه می‌سازد و دادهٔ قبلی را تغییر نمی‌دهد؛ نوع/واحد تگ موجود قفل است و معنای تازه کانال تازه می‌خواهد. جدول کانال‌ها، انتخاب/افزودن الگو و شرط/فیلتر صریح، چندستونه و بدون هدر اضافی باشد. ذخیرهٔ مشخصات و تعویض کلید با تأیید صریح در همان ویزارد باشند. کاربرد/فرمول پارامتر و کنترل خروجی به این ویزارد تحمیل نشوند. کاهش منوهای قدیمی پس از بازبینی مالک، گام بعدی است؛ هنوز حذف نشده‌اند.

## نمای کلی ۲ — مسیر شروع کار، ۲۰۲۶-۱۰-۲۴

آزمایش مستقل کنار نمای فعلی، بدون جایگزینی آن. بلوک‌های رنگی شماره‌دار با مسیر پیوسته و اقدام همان مرحله؛ معرفی منبع، روش ارتباط، مشخصات دریافت، آزمون پیام خام، تگ و استفاده در پارامتر. هر بلوک توضیح کوتاه، شاهد واقعی و دکمهٔ مرتبط دارد؛ انتخابش جزئیات را زیر مسیر باز می‌کند. هدر و دکمه‌های عمومی اضافه نباشند؛ فیلتر زمینه یک ردیف کوتاه بماند. روی دسکتاپ سه ستون با مسیر رفت‌وبرگشت؛ موبایل ترتیب یک‌ستونهٔ شماره‌دار. تعداد روش قابل انتخاب با تعداد منبع یا نوع ارتباط تعریف‌شده یکی نشود. وضعیت مراحل فقط بر پایهٔ شواهد catalog باشد؛ گام‌ها قفل اجباری ندارند چون دریافت خام بدون تگ ممکن است.

## راهنمای اصلی — بازبینی مالک ۲۰۲۶-۱۰-۲۴

منوی راهنما، صفحه‌ای تب‌بندی‌شده داخل فضای اصلی سایت است؛ پنجرهٔ modal یا عنوان «تصویر ارسالی» نداشته باشد. ناوبری سایدبار، URL و بازگشت مرورگر مانند صفحات دیگر حفظ شود. دو تصویر ارسالی مالک در تب‌های «ساختار اتوماسیون» و «راه‌اندازی برنامه» قرار می‌گیرند؛ تصویر تازه تولید نکنید. برای خوانایی، تصویر را به ارتفاع پنجره کوچک نکنید؛ عرض کافی، بزرگ‌نمایی، بازکردن اندازهٔ اصلی و ذخیره لازم است. تب آخر «آشنایی با هاب داده» تصویر نیست: جریان قابل انتخاب، توضیح مفهوم زیر نقشه، تفاوت تگ/پارامتر و لینک واقعی به صفحات مجاز دارد. اعداد، نرخ زنده، آنلاین‌بودن و DB مستقل فرضی نگذارید. تصویر مفهومی با وضعیت اجرا فرق دارد؛ توضیح فارسی/انگلیسیِ تب واقعی ملاک رفتار جاری است. فعلاً صفحات عملیاتی هاب از این تغییر راهنما مستقل می‌مانند.

## مرجع بصری مالک و راهنمای گرافیکی — ۲۰۲۶-۱۰-۲۴

نمونه‌های docs/design/data hub example جهت بصریِ سرمه‌ای، آیکون‌های واضح، فیروزه‌ای/بنفش/آبی/کهربایی و مرزهای برجسته را مشخص می‌کنند؛ محتوای فنی نمونه‌ها سند پیاده‌سازی نیست. در نمای کلی و راهنما، به‌جای کارت‌های متنی بلند، مسیر گرافیکی واقعی و قابل انتخاب نمایش داده شود؛ با انتخاب گره، زیر نمودار توضیح کوتاه و اقدام مرتبط بیاید. مرز هاب/مصرف‌کننده و معنای ذخیرهٔ فعلی روشن باشد. اعداد و وضعیت‌ها از catalog واقعی همان شرکت باشند. نقش نمودار فهم مسیر است، نه جایگزینی فهرست پرتراکم.

منوهای روزمره آشکار و با نام قابل فهم باشند: منابع اتصال، تگ‌ها، داده‌های دریافتی، تنظیمات اتصال، کنترل دریافت، راهنما. عبارت مبهم «درخواست‌های عامل» کنار گذاشته شد. کنترل دریافت به معنی کنترل خروجی دستگاه نیست. انتخاب دستگاه/منبع صریح باشد. کلیک نام منبع، جزئیات همان منبع را در کنار جدول باز کند؛ بستن پنل فهرست/صفحه‌بندی را حفظ کند. در اندازهٔ کوچک پنل بالای فهرست قرار گیرد و نمودار به چینش عمودی برسد؛ عنوان‌ها و مقدارها هم‌ردیف و تمام متن، واقعی و قابل انتخاب بماند.

## تصمیم مالک و اجرای هاب چندمنبعی — ۲۰۲۶-۱۰-۲۴

هاب به دستگاه یا یک اتصال خاص محدود نشود. فهرست‌های منبع، تگ و دریافت باید پیش‌فرض امکان دیدن مجموعه و فیلتر اختیاری داشته باشند؛ تغییر صفحه نباید بی‌درخواست اولین دستگاه را برای بررسی داده انتخاب کند. هر منبع فعلی یک مسیر/پروتکل است؛ گروه‌بندی چند مسیر زیر هویت دستگاه در آینده، با نمایش دروغین این قابلیت جایگزین نشود. اتصال کاربردی تگ به پارامتر/ماژول در فرم مصرف‌کننده می‌ماند؛ نگاشت کانال ورودی به تگ، کار هاب است.

سرمه‌ای/آبی حفظ و سبز یشمی ملایم برای نتیجهٔ معتبر/سابقهٔ دریافت به‌کار رود. پذیرش مجاز داده با آنلاین‌بودن دستگاه یکی نیست. هدر و آمار کوتاه، راهنمای شروع جمع‌شونده، اقدامات بعدی وابسته به وضعیت و جدول‌های فشرده با عنوان ثابت و صفحه‌بندی۲۵/۵۰/۱۰۰ لازم‌اند. در موبایل، جدول تشخیصی با عنوان ستون در محفظهٔ افقی بماند؛ تبدیل آن به کارتِ بدون عنوان ممنوع است. متن بلندِ مقدار فقط در جدول کوتاه شود و در جزئیاتِ پالایش‌شده قابل دیدن بماند.

پیام‌های ورودی و مقادیر تگ دو نمای مشخص‌اند: زمان فیلتر خام، زمان دریافت؛ زمان فیلتر مقادیر، زمان رخداد. صفر/خراب/نبود داده با یکدیگر ادغام نشوند. مشاهدهٔ مسیر، تگ‌ها و انواع تعریف‌شدهٔ پروتکل به معنی runtime پشتیبانی‌شده نیست؛ حدود واقعی پروفایل در راهنما/تنظیمات گفته شود.

## ۲۰۲۶-۱۰-۲۴ — تراکم کاری هاب

فضای دسکتاپ را با فرم تک‌ستونهٔ کشیده و فاصله‌های چندردیفی مصرف نکنید. فیلتر جست‌وجو و نمایش بایگانی در یک نوار؛ انتخاب منبع و مشخصات کوتاه هم‌ردیف؛ نام/وضعیت و نود/تگ در ستون‌های متناسب با طول داده قرار گیرند. کارت‌ها از ارتفاع کارت کناری کش نیایند. مشخصات فنی به‌صورت جفت عنوان/مقدار در همان ردیف و با جهت صحیح UUID/نشانی نمایش داده شود. استایل عمومی accounts برای fieldset و dl نباید این چینش را بشکند. فقط در عرض کم به یک ستون بروید؛ کنترل‌ها خوانا و قابل کلیک بمانند.

«تبدیل شمارش دریافتی به تگ» تنظیم فنی منبع است؛ با اتصال تگ به پارامتر در تعریف داده‌ها یکی نیست. در همان بخش این تفاوت نوشته شود؛ تنظیمات کم‌کاربرد عامل بازشدنی باشد. فرم تعریف تگ روی دسکتاپ دو ستون دارد و نوع اندازه‌گیریِ طولانی یک ردیف کامل می‌گیرد. QA با۱۰۰ منبع مصنوعی، فارسی/انگلیسی و موبایل انجام شود؛ ظرفیت نمایشی را با آزمون بار واقعی شبکه/DB اشتباه نگیرید.

**Accepted visual baseline:** Phase 2, `e19016d`, dark/navy Persian-first layout. This is a requirement summary, not license to reimplement/replace existing Vue or factory geometry.

## Four surfaces, three monitoring modes

Data Hub (2026-10-20): build and review the actual company application, not a parallel UX prototype. The hub owns source, channel/tag and connection preparation; Company Admin selects business use in machine settings. Display name accepts Persian/English and appears first in pickers; the technical channel key is separate, with inline rules and a preview. Keep provenance where it affects interpretation and unavailable capabilities explicit, without repetitive synthetic labels in operational menus. See [implemented workflow](guides/DATA-HUB-WORKFLOW.fa.md).
- **Immersive**: actual 16-equipment interactive Three.js stage dominates screen; compact HUD, contextual badges, alerts and real layer overlays; no fictional photorealistic factory.
- **Explore**: same model/data/period, selecting via raycast highlights equipment and opens contextual, closable panel; CTA never covers content.
- **Analytics**: meaningful production/OEE/downtime/equipment table; compact nonwasteful charts, no generic copy of Production on Quality.
- **Device/Line Detail**: dedicated drill-down, NOT a fourth monitoring mode. Shows state, provenance, OP/part/operator/shift if available; production, rates, downtime, valid A/P/Q and formula inspection; no invented machine/line OEE.

## Acceptance

Layout editor — owner revision 2026-10-23: keep one contextual tool panel. No selection exposes hall creation; selecting a hall exposes placement tools for that hall and its properties; selecting a resource exposes its properties. Background click clears selection. Hide empty contents and collapse populated contents. Sensors and machines follow the same location flow: the scene picker lists only same-hall or unassigned resources, and cross-hall scene transfers are blocked. Initial placement of an unassigned resource is committed together with the scene on Save layout. Later owner decision: location changes belong in resource definitions; allow without data, or require explicit responsibility acknowledgement when data exists. The server enforces this and atomically removes obsolete scene coordinates. Existing data and stored report locations remain unchanged; complete time-effective location history is not implemented. This supersedes the separate sensor-assignment button and simultaneous hall/resource creation sections.
- Desktop main Monitoring modes: 1366×768 and 1920×1080 without **document-level** vertical scroll; controls in compact header; never hide data with `overflow:hidden` as a shortcut. Internal scroll may be appropriate for long content if not trapping interactions.
- 3D equipment positions from `src/model.ts`, `src/visuals/equipment-models.ts`, `docs/hall-01-layout.md`; labels avoid collisions and adjust to selection/zoom.
- Layer Manager: 8 functional primary/secondary layers with legible legend and effects in 3D/2D/charts, governed by shared entity/time/source scope, not decorative toggles.
- Interactive charts: semantic time axis, units/ticks, tooltip, zoom/pan/drag/reset, legend, interval/drill-down and **visible no-data gaps**. KPI gauges reveal formulas, numerators and denominators.
- Show data freshness, simulator/manual/live provenance and unknown/zero distinction. Current instant status is not identical to selected historical period end.
- Persian RTL, English LTR; correct date, calendar and bidirectional panel positions. Existing dark theme approved; future light white/green must use owner-supplied reference and reusable design tokens.
- UI navigation should reflect enabled tenant module, data readiness and authorization separately; unconfigured modules cannot be passed off as working. Test account restrictions on API.
- Preserve layout editing, 2D/3D, wheel zoom, raycasting, scene asset integrity, selection, import/export JSON, kiosk modes, previous regressions.

## References and evidence
- Original owner visual assets, if present locally, `docs/design/reference` (NOT automatically all committed). Existing contracts: [UI-VISUAL-IMPLEMENTATION-CONTRACT.md](archive/research/UI-VISUAL-IMPLEMENTATION-CONTRACT.md) and [CODEX-SMART-FACTORY-HANDOFF.md](CODEX-SMART-FACTORY-HANDOFF.md).
- Current implementation review: [PHASE2-DELIVERY.md](archive/deliveries/PHASE2-DELIVERY.md), screenshot metadata `.local/qa/phase2/` accessible only on the owner's development PC. CI build/test cannot prove subjective fidelity.

## 2026-10-21 — Company definitions and workspace terminology

Current administration home: one continuous grid, no physical/production grouping or multi-catalog tab switcher. Each card has a distinct relevant icon, a short explanation, a count when meaningful and a direct same-name destination. Factory profile shows the configured name instead of a factory count; editing the profile cannot rename the sign-in account. Optional contact fields are explicitly marked. With one factory available, area/resource creation binds to it and displays its name without a redundant selector. Existing dependency-aware deletion of areas/resources remains.

Current workspace names: مدیریت سامانهٔ شرکت / میز کار / نمای جامع. Company Admin defaults to the first with three sidebar entries: تعاریف شرکت، کاربران و دسترسی‌ها، هاب داده. Roles do not dictate workspace names; additional workspaces still require explicit policy and action/module permissions. The earlier term “four surfaces” describes monitoring views and detail, not four workspaces. Future personal widgets belong within نمای جامع unless a genuinely separate workflow/access boundary warrants another workspace.

## 2026-10-21 — Readable tenant scale and compact definitions

Tenant scale tokens live in `src/company/tenant-shell.css`: body/menu/control text14px, input15px, control height42px and navigation row44px. These are product design choices, not claims of a universal WCAG minimum font size. Definitions cards use a36px icon beside the17px title,14px description and a wrapping count/action footer. Height follows content; never clip text to hit a fixed card height. The same tokens apply to the hub menu and tenant dialogs. Shared scene geometry and separate presentation demos are unchanged.

Entering Data Hub temporarily collapses the company menu to an accessible icon rail; the menu can be expanded, and leaving the hub restores its earlier state. Empty hub overview prioritizes the first-source action, hides zero-only statistics and retains the explanatory workflow below. No new source or device configuration is seeded by this layout change.

QA at1407×719 CSS px measured a185.3px example card,14px main/menu/button text,42px action and44px company navigation row. Existing10 workspace tests and build/typecheck passed. Actual product browser checks covered Persian/English,390px mobile, secondary settings navigation, hub collapse/expand/restore, visible empty-hub action and the source dialog. Real Chrome zoom200% was set through browser appearance settings in an isolated temporary QA profile (DPR2, CSS viewport691×310); factory and source-form controls remained reachable. This is a focused UI check, not a complete accessibility conformance audit. Evidence: `.local/qa/tenant-scale/`.

## 2026-10-21 — Factory identity and tenant status

Factory profile now includes a persisted optional logo using the shared image-field control/validator. Accepted PNG/JPEG payloads are bounded to256KB and2048×2048; remote URLs/SVG are rejected. Tenant migration12 adds nullable sites.logo_data_url. Small logos are stored as bounded data URIs in the existing tenant profile to remain available with its context; this is not a general asset repository. Larger/media-library needs require a dedicated asset API/store. Missing image fields preserve an existing logo; explicit null removes it. Existing CAS version and tenant scope checks apply, and image bytes are excluded from master audit details. Company logo saving/deletion, omission preservation, invalid input and foreign-tenant edits are covered by acceptance tests.

Tenant header shows factory name/workspace, page and user role with visible password/sign-out actions; saved logo is available in header and for future dashboards. The tenant footer is separate from demo report state and uses a13px font with actual company code, factory time zone and last successful master-context receipt timestamp. That timestamp is not equipment freshness or a network-health guarantee. Scene/demo reporting behavior is preserved in the separate non-tenant branch. The company sidebar no longer claims hardware/ERP is disconnected without checking it.

بازبینی نهایی پوستهٔ لوگو/هدر: مرورگر واقعی در۱۴۰۷×۷۱۹، فارسی/انگلیسی و۳۹۰px موبایل بدون overflow افقی و خطای API موفق بود؛ نوار پایین۱۳px و۴۱px ارتفاع اندازه‌گیری شد. پیش‌نمایش PNG وJPEG، حذف پیش‌نمایش و رد SVG بدون ذخیره در اطلاعات شرکت بررسی شدند؛ ذخیره/حذف واقعی و جداسازی شرکت‌ها در API ایزوله آزموده شدند. پیمایش کیبورد و دسترسی کنترل‌ها در زوم واقعی۲۰۰٪ Chrome نیز موفق بود (CSS691×310،DPR2)؛ این بررسی ادعای انطباق کامل دسترس‌پذیری نیست. شواهد `.local/qa/factory-branding/` و `.local/qa/tenant-scale/browser-200-result.json`.

## 2026-10-21 — Compact identity, no duplicate role

The later owner review supersedes the earlier always-visible role/workspace labels: tenant header now shows factory name/logo, current page and username only. Workspace chooser remains when more than one space is available. The tenant sidebar footer is removed entirely, including its duplicate account/role and collapse action; the header menu control remains functional. Demo sidebar behavior is preserved.

Factory sign-in code guidance is a short description under the full-name input, associated with aria-describedby; it is not a standalone callout. The name field precedes the optional logo editor. Header padding/minimum height and inherited heading margins were corrected without clipping labels. At1407×719 the measured header is60.5px, down from87.6px. Existing saved logo was verified unchanged across Persian/English and mobile navigation. Evidence: `.local/qa/compact-identity/`. Ten existing workspace tests and build/typecheck passed; no schema or business data changes.


## 2026-10-21 — Input catalog hierarchy and readable rows

Company definition cards follow factory profile, physical areas, resources, layout, then equipment inputs before production definitions. This is reading order rather than a mandatory linear wizard: layout and data assignment are separate uses of defined resources. The input page is a searchable, group-filtered six-column table independent of resource existence. A row opens the existing temporal signal-assignment flow; equipment/Hub are secondary related links. Current production consumption is distinguished from stored-only generic mappings. Sticky table headers and an internally scrollable region preserve row/column association on narrow screens; row/header fonts are explicitly14px to avoid inheriting the Phase2 scene table typography. Custom definition resource-kind checkboxes use one wrapping horizontal row with18px controls. No schema/runtime/permissions change was made by this UI revision.


## ویرایشگر چیدمان — ۲۰۲۶-۱۰-۲۱

بازطراحی بوم اجرا شد: صفحه در دسکتاپ از ارتفاع قابل استفادهٔ پوسته استفاده می‌کند؛ نوار ابزار ذخیره/انتخاب محل/نمای بالا و سه‌بعدی/نمای کامل/نام‌ها بالای بوم است. یک پنل جمع‌شونده دارای سه بخش سالن و تجهیزات، ویژگی‌ها، و فایل است. ویژگی‌ها در همان پنل اسکرول می‌شوند. جمع‌کردن پنل بوم را عریض‌تر می‌کند؛ منوی اصلی محصول با کنترل موجود خودش جمع می‌شود. در موبایل پنل و بوم زیر هم‌اند و اسکرول صفحه مجاز است.

در این ویرایشگر زوم با Ctrl یا Meta همراه چرخ ماوس و با کلیدهای +/− انجام می‌شود. چرخ معمولی در بوم preventDefault نمی‌شود؛ پنل کناری مستقلاً اسکرول دارد. سایر مصرف‌کننده‌های SceneView رفتار پیشین را نگه می‌دارند. انتخاب، TransformControls، مدل‌های موجود، شناسه‌ها، مختصات، JSON نسخه۱ و ذخیره با کنترل نسخه حفظ شده‌اند. برای بوم خالی راهنمای افزودن محل وجود دارد؛ نام شکل‌ها فارسی/انگلیسی است.

### پیشنهاد مسیر مدل و عکس — بررسی امکان اجرا، هنوز ساخته نشده

۱. مدل آمادهٔ مشتری: قابل اجراست. فرمت ورودی ترجیحی GLB/glTF؛ ابعاد واقعی در متر، جهت جلو، مبدأ کف و مقیاس یکنواخت باید بررسی و در پیش‌نمایش تأیید شوند. مطابقت اندازهٔ واقعی با bounding box مدل، جهت و سبک‌سازی برای نمایش چندین تجهیز لازم است. فایل CAD نیازمند تبدیل به مدل مناسب وب است. واحد glTF متر است: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#coordinate-system-and-units

۲. عکس‌ها و فایل مدل در پروفایل تجهیز: قابل اجراست. عکس‌های جلو/عقب/چپ/راست با عنوان و اندازهٔ واقعی مستقل از چیدمان ذخیره شوند تا در شناسنامه/نگهداری/تشخیص تجهیز هم قابل استفاده باشند. یک تب «رسانه و مدل» مناسب است؛ فایل مدل به داراییِ نسخه‌دار کتابخانه ارجاع دهد و در چیدمان انتخاب شود. عکس به‌تنهایی به معنی مدل سه‌بعدی نیست. هنوز endpoint/storage این قابلیت وجود ندارد؛ کنترل تزئینی اضافه نشده است.

۳. ساخت مدل از عکس: عملی است، اما پردازش جدا و تأیید انسانی می‌خواهد. موتور آمادهٔ photogrammetry مثل Meshroom/AliceVision می‌تواند در برنامه یا سرویس مجزا اجرا شود؛ نتیجه پس از سبک‌سازی، تصحیح اندازه و پیش‌نمایش وارد همان کتابخانه شود. چهار عکس برای آرشیو مفید است ولی تضمین بازسازی دقیق نیست؛ برای بازسازی، عکس‌های هم‌پوشان از زوایای متعدد لازم است و سطوح براق/شفاف دشوارند. راهنمای رسمی: https://meshroom-manual.readthedocs.io/en/latest/capturing/capturing.html . مدل مولد از چند عکس هم باید «تقریبی» تلقی و با ابعاد اندازه‌گیری‌شده اصلاح شود؛ نباید دقت مهندسی ادعا شود.

مسیر پیشنهادی توسعه: ابتدا رسانهٔ تجهیز و کتابخانهٔ مدل آماده، سپس آداپتور موتور تولید مدل. هر دارایی متعلق به شرکت، دارای نسخه، فرمت/حجم/هزینهٔ رندر بررسی‌شده و قابل بازگشت باشد. دارایی مدل از هویت تجهیز، آمار و نگاشت تگ جدا بماند. قالب‌های procedural فعلی و پنج Kind همچنان مسیر فعلی‌اند؛ JSON جانمایی، فایل مدل سه‌بعدی نیست. پشتیبانی از مدل آپلودی نیازمند طراحی سازگار schema و persistence و کنترل مالکیت سمت سرور است؛ در این تغییر اضافه نشده است.


### اصلاح بازخورد چیدمان — ۲۰۲۶-۱۰-۲۱

قواعد عمومی tenant کنترل‌ها را دوباره بزرگ کرده بودند؛ نوار ابزار و ورودی‌های این ویرایشگر اکنون با specificity صریح، ارتفاع۳۲px و عنوان محلِ تک‌ردیفی دارند. پنل از۳۰۰ به۲۶۰px باریک شده، تب نخست «جانمایی» و انتخاب قالب «مدل سه‌بعدی تجهیز» نام دارد. نام قالب همچنان به پنج مدل داخلی اشاره می‌کند، نه پشتیبانی از آپلود فایل مدل.

انتخاب JSON کنترل واقعی file input با عنوان روشن است. فایل سالم بلافاصله در صحنهٔ فقط‌خواندنی پیش‌نمایش می‌شود، نام فایل و تعداد محل/تجهیز نمایش داده می‌شود و بستن پیش‌نمایش به draft قبلی بازمی‌گردد. دکمهٔ ذخیره هنگام پیش‌نمایش غیرفعال و save guard دارد؛ برای فایل سازگار، پذیرش و سپس ذخیره دو اقدام جدا هستند. شناسه‌های خارج از شرکت فقط پیش‌نمایش می‌شوند و دلیل عدم امکان پذیرش در پنل فایل روشن است؛ تعاریف یا آمار شرکت از آن‌ها ساخته نمی‌شود. خطای JSON خراب کنار انتخاب فایل می‌آید. انتخاب دوبارهٔ همان فایل ممکن است. صحنهٔ ویرایشگر برچسب هندسی دارد و دادهٔ تولید نمایش نمی‌دهد.

فایل ارسالی مالک pouyeshgar-layout (1).json، با۲سالن و۱۶تجهیز، layout نسخه۱ فاز۲ است و مدل فایل سه‌بعدی نیست. مسیر پیشنهادی آپلود مدل همچنان تب رسانه و مدل در پروفایل تجهیز، و انتخاب آن در جانمایی است؛ در این برش چنین آپلودی ساخته نشده است. تبدیل/نگاشت شناسه‌های چیدمان خارجی به تعاریف شرکت نیز به اقدام صریح و جریان جدا نیاز دارد؛ فعلاً پیش‌نمایش و ورود فایل هم‌شناسه فراهم است.

نوار چیدمان در اصلاح بعدی با breadcrumb و بازگشت ادغام شد؛ همهٔ کنترل‌ها در دسکتاپ یک ردیف۳۴px دارند و نوار دوم حذف شده است. CompanyBreadcrumb یک slot اختیاری actions دارد؛ سایر صفحات بدون slot رفتار پیشین را حفظ می‌کنند.

### دیوار، در/پنجره و خوانایی ویژگی‌ها — ۲۰۲۶-۱۰-۲۳

دیوارهای صحنه عمومی‌اند: بریدگی، ورودی و اتاق نمونهٔ ثابت بر اساس شناسهٔ hall-01 رسم نمی‌شود. در کتابخانهٔ جانمایی، گروه‌های تجهیزات تولیدی، خط پیوسته، حسگر/ابزار اندازه‌گیری و در/پنجره در یک مسیر انتخاب می‌شوند. بازشو به دیوار انتخابی می‌چسبد و با کشیدن در نمای سه‌بعدی فقط در امتداد همان دیوار جابه‌جا می‌شود؛ فاصله و عرض عددی نیز قابل تنظیم است. بازشو در 2D و 3D نمایش دارد. محور جلو z=0، پشت z=depth، چپ x=0 و راست x=width است؛ فاصله در جلو/پشت از چپ و در کناره‌ها از جلو اندازه‌گیری می‌شود. عرض و فاصله برحسب مترند؛ ارتفاع دیوار و قاب‌ها برای دید داخل سالن شماتیک است، نه مدل معماری با ارتفاع واقعی.

Hall.wallOpenings یک افزونهٔ اختیاری به JSON چیدمان نسخه۱ است: id، kind=door/window، wall=front/back/left/right، offset و width. فایل‌های قبلی بدون آن معتبرند و بدون بازشوی فرضی نمایش داده می‌شوند. شناسهٔ تکراری، اندازهٔ نامعتبر، خروج از دیوار، هم‌پوشانی و بیش از۱۰۰ بازشو در هر محل رد می‌شود؛ کوچک‌کردن سالن هم نباید بازشو را بیرون دیوار ببرد. ذخیره در scene_layout دیتابیس همان شرکت، با مجوز سمت سرور، کنترل نسخه و audit موجود انجام می‌شود؛ migration دیتابیس یا تغییر قرارداد telemetry نیاز نبود.

فیلدهای ویژگی‌ها به ردیف‌های مستقل برچسب/عدد تبدیل شدند. ورودی عدد LTR، فونت۱۶px و حداقل عرض۱۰۴px دارد؛ قانون قدیمی کنترل‌های فشرده دیگر آن را کوچک نمی‌کند. پنل ابزار همچنان جمع می‌شود و اندازهٔ بوم حفظ شده است. حسگر یک نوع منبع مستقل است و به ماشین/خط/ایستگاه تبدیل نمی‌شود؛ انتخاب آن در گزارش و شمارش تولید ممنوع است. برای خط پیوسته یک مدل شماتیک نوار نقاله وجود دارد؛ سازندهٔ خط چندجزئی و مدل سه‌بعدی آپلودی شرکت هنوز ساخته نشده‌اند.

ساخت مدل از عکس همچنان پیشنهادِ مرحلهٔ بعد است: ابزار جدا برای بازسازی/پاک‌سازی/سبک‌سازی، تعیین مقیاس با اندازهٔ واقعی و سپس بارگذاری مدل از پروفایل تجهیز و انتخاب در چیدمان. بازسازی فوتوگرامتری محلی مانند COLMAP به سرویس AI نیاز ندارد؛ عکس‌های هم‌پوشان از زوایای متعدد لازم‌اند و چهار عکس ساده تضمین بازسازی نیست. راهنمای منابع: https://colmap.github.io/ و https://meshroom-manual.readthedocs.io/en/latest/capturing/capturing.html . این برش مولد مدل یا آپلود GLB را پیاده نکرده است.


## رابط ساختار پیام — بازبینی ۲۰۲۶-۱۰-۲۵
فرم قدیمی و انتخاب بین طراحی قدیم/جدید از مرحلهٔ ساختار پیام حذف شده است. رابط جدید همچنان UI-only و بدون اتصال به پارسر/ذخیره است؛ ذخیره و بعدی در این مرحله فعال نمی‌شوند.
انتخاب اصلی چهار گروه زمانی عمومی است: رویدادی، مقدار لحظه‌ای، بازهٔ ثابت و بازه با شروع/پایان صریح. کتابخانهٔ جداگانهٔ هشت قالب اختیاری در تب «قالب‌های آماده» بر اساس همین گروه‌ها فیلتر می‌شود؛ قالب‌ها فقط نقطهٔ شروع‌اند و همهٔ نام‌ها، فیلدها و گروه زمانی قابل تغییرند. کاربردهایی مثل دما یا آلارم، گروه اصلی نیستند.
راهنمای تعاملی پیام/رکورد/فیلد/کانال/نحوهٔ ارسال، هر مفهوم را در همان صفحه توضیح می‌دهد. هر فیلدِ مقدار یک کانال دارد؛ زمان، شناسهٔ رویداد و اطلاعات همراه جدا نمایش و شمارش می‌شوند. نحوهٔ ارسال از معنای زمانی مقدار جداست.
نمونهٔ آموزشی یک یا سه رکورد را با فیلدهای قابل انتخاب، مسیرهای تودرتوی نمایشی، رکورد مستقیم یا آرایه، و بدنهٔ JSON یا Form → JSON نمایش می‌دهد. این مولد نمونه، متن دستگاه را نمی‌خواند و پارسر دریافت نیست. تب «پیام خودم» فقط ورودی متن است و خطایاب ندارد. نمونه‌ها و شمارنده‌ها UI هستند و به‌عنوان دادهٔ زنده یا نتیجهٔ استخراج معرفی نمی‌شوند.
جدول ساختارها قابلیت انتخاب، ویرایش، کپی، حذف با تأیید و انتخاب فیلد دارد. هدرها، قالب‌ها و تنظیمات در فضای موجود چندستونه و هم‌ترازند؛ انتخاب اولیه فضای خالی و جدول خالی اضافه ندارد. پیام‌های یک‌مقداری و چندمقداری از روی تعداد کانال‌ها قابل تفکیک‌اند. قالب‌ها باعث ایجاد منطق پارس یا تفسیر تجاری مجزا نمی‌شوند.

باکس جداگانهٔ مفاهیم بالای فرم و برچسب‌های پیش‌طرح/عدم اتصال از نمایش فرم حذف شده‌اند؛ توضیح متناسب با انتخاب همچنان زیر نمونه دیده می‌شود. دکمهٔ افزودن فیلد ابتدا dialog کوچکِ توضیح/تأیید/انصراف باز می‌کند؛ انصراف یا Escape هیچ فیلدی ایجاد نمی‌کند. نمای متنی تکراری در حالت JSON حذف و فقط «بدنهٔ فرم ارسالی» برای نمایش بسته‌بندی Form باقی است. «پیام خودم» محل نگهداری متن مرجع همان ساختار است؛ خودکار پارس نمی‌شود. حذف نوشته‌های پیش‌طرح به معنی فعال‌شدن ذخیره یا پردازش نیست؛ اتصال runtime همچنان کار بعدی است.


## ذخیرهٔ ساختارهای پیام و نشست — ۲۰۲۶-۱۰-۲۵

ساختارهای تعاملی جدید اکنون در `messageStructures` پیش‌نویس خصوصی و رمزگذاری‌شدهٔ همان شرکت ذخیره می‌شوند؛ نام خالی هنگام ویرایش دوباره با نام قالب پر نمی‌شود. فیلدها، نمونهٔ شخصی و ساختارهای متعدد با برگشت مرحله و بازکردن مجدد حفظ می‌شوند. اعتبارسنجی ذخیره فقط ساختار و اندازهٔ سند را کنترل می‌کند و اجازهٔ پیش‌نویس ناقص را می‌دهد؛ این کار پارسر پیام ورودی یا اعمال schema اجرایی نیست. «ذخیره» در مرحلهٔ ساختار فعال است؛ «بعدی» پیش‌نویس را ذخیره و تست دریافت خام را باز می‌کند. عبور از دریافت به ساخت تگ برای این ساختارها تا اتصال پارسر بسته است و دلیل در همان صفحه نمایش داده می‌شود. پاسخ HTTP گیرنده هنوز تغییر نکرده است.

نشست ورود فعلی ۸ ساعت ثابت از زمان ورود اعتبار دارد و تمدید خودکار ندارد. فرانت دیگر هر 401 را logout نمی‌داند؛ تنها `authentication_required` برای توکن همان درخواست و همان نشست جاری، نشست را پاک می‌کند. خطای تأیید رمز یک عملیات، کلید دستگاه و پاسخ دیررس نشست قبلی نباید ورود فعلی را باطل کنند. علت قطعی خروج‌های گزارش‌شده بدون ثبت پاسخ شبکه مشخص نیست؛ این اصلاح یک مسیر خروج نامرتبط موجود در کد را برطرف می‌کند. مدت و قواعد ابطال سرور تغییر نکرده‌اند. برای بارگذاری اعتبارسنجی جدید پیش‌نویس، راه‌اندازی مجدد دستی WEB لازم است؛ هیچ سرویس واقعی توسط عامل راه‌اندازی نشد.


## اتصال پارسر ساختارها و HTTP 202 — ۲۰۲۶-۱۰-۲۵

توافق جدید مالک: سازگاری با قالب/دادهٔ قبلی الزام نیست. مرحلهٔ ساختار اکنون مستقیم به compiler/decoder مستقل `services/ingest/http-channels/structures.ts` وصل است؛ چهار گروه زمانی، JSON/Form، مسیرهای تو‌در‌تو/اندیسی/بدنه، نوع هر فیلد، چند مقدار و اطلاعات همراه، انتخاب ساختار و اشتراک آرایه با discriminator صریح پیاده‌اند. در آرایهٔ مشترکِ دارای فیلدهای متفاوت، حضور فیلدهای تعریف‌شده مسیر را تعیین می‌کند؛ هم‌پوشانی مبهم کانال‌ها در ذخیره رد می‌شود. «پیام خودم ← بررسی نمونه» همان decoder اجرایی را بدون شبکه و ذخیره اجرا می‌کند. Save/Next تعریف معتبر را روی منبع اعمال می‌کنند؛ دریافت → ساخت تگ → بازپردازش دادهٔ منتظر نگاشت → تأیید نهایی وصل است. نمونهٔ نامعتبر مانع ذخیرهٔ تعریف نیست؛ خود تعریف باید کامل و بدون ابهام باشد.

HTTP عمومی فقط پس از commit خام، 202 با بدنهٔ status=accepted برمی‌گرداند. خطاهای قبل از custody، Problem Details با statusهای401/403/413/415/429/503 و Retry-After برای429/503 دارند. شبیه‌ساز مستقل اکنون صرفاً202 را ACK می‌داند و form را URL-encode می‌کند؛ node در بدنهٔ مسیر عمومی لازم نیست. JSON یک‌بار در هر envelope خوانده می‌شود، مسیرها برای رکوردهای بسته پیش‌پردازش می‌شوند، lookup تگ Map است و اندازه/تعدادها محدودند؛ ادعای تست بار production وجود ندارد. بستهٔ خراب terminal done می‌شود، سطر خراب نمونه نمی‌شود، صفر/false حفظ می‌شوند، تکرار دوباره ذخیره نمی‌شود و تعارض نمونهٔ اول را تغییر نمی‌دهد. بازه و ارتباط رکورد/همراه‌ها در نمونه/رسید باقی‌اند. [قرارداد و روش تست](guides/DATA-HUB-WORKFLOW.fa.md).

تست:۱۲۳ تست root موفق، یک تست اختیاری skip؛ دو تست simulator موفق؛ build، check:edgebox و manifest قرارداد امضاشده موفق. QA با MariaDB ایزولهٔ موجود و schema/credentialهای تصادفی و حذف‌شونده: custody واقعی202، هفت مقدار شامل۵سالم/۲خراب، replay بعد از تگ، دو event در یک timestamp، بازه۶۰ثانیه و بازهٔ صریح۴۶ثانیه، duplicate/conflict، تشخیص JSON خراب/زمان آینده/کلید اشتباه، و503 هنگام نداشتن مجوز INSERT موفق. QA مرورگر ایزوله با UI واقعی: تعریف دو ساختار، تغییر مسیر و نوع، بررسی نمونه با parser واقعی، اعمال config، دریافت ترکیبی، ساخت هر دو تگ و تأیید نهایی موفق؛ APIهای مرورگر fixture بودند و دریافت/SQL جداگانه با adapter واقعی آزموده شد. WEB/INGEST/شبیه‌ساز واقعی راه‌اندازی یا دادهٔ شرکت پاک نشدند.
