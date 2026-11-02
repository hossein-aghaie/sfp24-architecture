# Smart Factory / Industrial Operations Platform — Product Blueprint

**Date:** 2026-10-14
**Consolidated into Phase 2 documentation on 2026-10-14.** This is the authoritative forward-looking product vision, not a description of shipped functionality. Some historic status/branch notes in sections 13, 21 and 30 describe the moment they were first drafted; see `docs/CURRENT-STATE.md` for the actual verified delivery and `docs/START-HERE.md` for live branch guidance.
**Status:** Living product/architecture requirements; not a claim that features are implemented.
**Pilot customer/factory:** پویشگر (Pouyeshgar)

**CRITICAL OWNER CLARIFICATION — D-014 (2026-10-14):** One independently purchasing company = ONE licensed **company account / tenant**. A company account has its own enabled/purchased modules, a contracted number of user-login seats, first company administrator, roles, and potentially multiple physical sites/factories. An owner of three independent companies buys THREE independent accounts; never implement a tenant that owns multiple independently contracted company tenants. This explicitly supersedes ambiguous earlier Company/Tenant cardinality proposals in this document. See `docs/TENANCY-IDENTITY-DESIGN.md` v0.2 and `docs/DECISIONS.md` D-014. The deployment host (provider vs customer), physical DB isolation and precise seat billing are still open.
**Product/technology branding:** SFP24 is separate from Pouyeshgar.
**Code development branch at time of writing:** feat/smart-factory-pilot-next
**Documentation-only branch holding this proposal:** docs/platform-product-blueprint

> IMPORTANT FOR FUTURE CHATGPT / CODEX SESSIONS: Read this document together with AGENTS.md, docs/CODEX-SMART-FACTORY-HANDOFF.md, docs/archive/research/UI-VISUAL-IMPLEMENTATION-CONTRACT.md, docs/archive/DECISIONS-EARLY-PILOT.md and the ACTUAL current code. This document records the owner's product vision and open decisions, NOT a command to implement everything immediately. Do not invent business rules, silently change working code or treat mock data as production. Codex was still actively editing the development branch when this file was created; do not rewrite or merge in-flight work without inspection.

## جهت ادامه پس از هاب — بازبینی مالک، ۲۰۲۶-۱۰-۲۸

این بخش جمع‌بندی مرجع گفتگو برای ادامهٔ محصول است؛ توضیح تکمیلی ۲۰۲۶-۱۰-۲۹ در همین بخش آمده است. تأیید پاک‌سازی به معنی مجوز ساخت همهٔ قابلیت‌های آینده نیست. جزئیات زیر جای اصطلاحات مبهم «سیستم جامع» را می‌گیرند.

- **دامنهٔ مشتری:** ثبت واقعیِ کار از کارگاه یک‌دستگاه/یک‌نفر، بدون پلان/سفارش/شیفت ثابت، تا شرکت دارای چند کارخانه و برنامهٔ سفارش‌محور یا پیش‌بینی‌محور لازم است. پشتیبانی فعلیِ رابط یک کارخانه در هر شرکت را با هدف چندکارخانه‌ای اشتباه نگیریم؛ اجرای آن هدف توسعهٔ جدا می‌خواهد. سلسله‌مراتب فیزیکی، ساختار عملیات و اختیارات مستقل‌اند.
- **نخستین برش کاربردی:** «ثبت و گزارش تولید»؛ قطعه، OP، منبع کاری، شخص انجام‌دهنده، تاریخ/بازه، تعداد و ضایعات. مدت/علت توقف نیاز مطلوب همین جریان است، ولی فرم/منطق توقف و تأیید گزارش تا بررسی کد و توافق جزئیات، ساخته‌شده یا نهایی فرض نشوند. برنامهٔ تولید پیش‌نیاز ثبت نیست؛ اتصال اختیاری به کار/سفارش برنامه‌ریزی‌شده بعداً اضافه می‌شود. گزارش‌های پایهٔ همان قابلیت از ثبتش جدا و اجباری فروخته نشوند؛ بسته‌بندی نهایی تجاری هنوز تثبیت نشده است.
- **ماژولار و یکپارچه:** ماژول‌ها جدا قابل عرضه‌اند، ولی هویت‌ها و ارتباط کار/نتیجه مشترک‌اند. خرید چند ماژول به‌تنهایی یکپارچگی ایجاد نمی‌کند. ماژول نصب‌نشده نباید مرحلهٔ اجباری یا وابستگی پنهان به ثبت ساده تحمیل کند. ارتباط پایهٔ ماژول‌های داخلی موکول به خرید یک بستهٔ مبهم «یکپارچه‌سازی» نشود.
- **میز کار و کارتابل:** پیشنهاد معماریِ بعدی، کارتابل/ارجاع/اعلان/ثبت نتیجهٔ مشترک است؛ ماژول کار تخصصی را عرضه می‌کند و ادمین شرکت صفحات و محدودهٔ اختیار را تنظیم می‌کند. هر شخص کارتابل یا برنامهٔ مستقل کدنویسی‌شده نخواهد داشت. جابه‌جایی کارت‌ها مجوز ایجاد نمی‌کند. وظیفه، مسئول، موضوع، موعد اختیاری، وضعیت و سابقه لازم دارد. موتور گردش‌کار عمومی هنوز اجرا نشده است.
- **تعریف میزهای قابل استفادهٔ مجدد — تکمیل ۲۰۲۶-۱۰-۲۹:** شرکت بتواند چند میز با نام دلخواه از الگو یا خالی بسازد؛ هر میز شامل بخش‌های عرضه‌شدهٔ ماژول‌ها، ترتیب و محدودهٔ نمایش است. یک میز به چند فرد و یک فرد به چند میز با ورودی پیش‌فرض قابل انتساب باشد. الگوهای انجام کار/سرپرستی/تحلیل نقطهٔ شروع‌اند؛ ساده/یکپارچه دو حالت ثابت نرم‌افزار نیستند. کپی میز مستقل است، تغییر میز مشترک بر استفاده‌کنندگان همان میز اثر دارد. داشبورد برای مشاهده، کارتابل برای کار ارجاع‌شده و فرم تخصصی برای منطق ماژول است؛ این‌ها می‌توانند داخل میز قرار گیرند. منوی تنظیم واحد «میزهای کار و داشبوردها» و میان‌بر تعاریف به همان مقصد پیشنهاد شده‌اند؛ منوهای موازی اپراتورساز/داشبوردساز نسازیم. تنظیم میز خرید یا مجوز جدید ایجاد نکند و منبع دادهٔ دستگاه را تغییر ندهد. وضعیت اجرایی در CURRENT-STATE نگه‌داری می‌شود: تعریف و انتساب میز ذخیره می‌شوند؛ محتوای داخل میز فعلاً نمایشی است.
- **اشخاص و مجوزها:** انجام‌دهندهٔ کار با ثبت‌کنندهٔ گزارش یکی فرض نشود. ثبت برای خود/دیگری، خواندن خود/دیگران، اصلاح و بررسی/تأیید، اختیارات جدا با محدودهٔ شرکت/محل/تجهیز هستند؛ عنوان شغلی مجوز نیست. گردش پیشنهادی بررسی اختیاری است تا کارگاه یک‌نفره گرفتار تأیید تصنعی نشود. رفتار فعلی ارسال/اصلاح گزارش، تأیید چندمرحله‌ای نیست و در این پاک‌سازی تغییر نمی‌کند.
- **پارامتر و هاب:** هاب منبع/مسیر/تگ و نوع/زمان/کیفیت داده را می‌شناسد؛ تفسیر کاربردی، تبدیل و قواعد در پارامتر/مصرف‌کننده‌اند. پارامتر قابل استفادهٔ چند مصرف‌کننده است؛ کپی تاریخچه به‌ازای هر ویجت یا پارامتر نسازیم. ماژول ورودی موردنیاز و واحد/بازه/موضوع/رفتار دادهٔ ناقص را تعریف می‌کند. شمارش دستگاه بدون ارتباط به کار، قطعه و OP خودکار گزارش تولید نمی‌شود.
- **فرم توسعه‌پذیر:** تعریف ساختاریافتهٔ اطلاعات و نمایش مشترک، همراه منطق تخصصی در کد ماژول؛ هدف فرم‌ساز یا ERP همه‌منظوره نیست. اطلاعات ماژولی به موجودیت پایه اضافه می‌شوند، نه اینکه برای هر شرکت نسخهٔ متفاوتی از فرم اصلی بسازیم. [جزئیات و سؤال‌های باز](product-notes/DATA-POINTS-AND-CONSUMERS.fa.md) حفظ می‌شوند.
- **خروجی و ERP:** کنترل تجهیز، مسیر مستقل فرمان با اختیار ارسال/انقضا/شناسه و نتیجهٔ اجرا می‌خواهد؛ ACK انتقال با اجرای فیزیکی فرق دارد. اتصال ERP/انبار با آداپتور و قرارداد نسخه‌دار است؛ ساخت ERP یا اتصال آماده به همکاران سیستم ادعا نمی‌شود. خاموش/روشن‌کردن تجهیز از تگ ورودی خودکار مجاز نمی‌شود.
- **گسترش‌های واقعی آینده:** ارجاع برنامهٔ تولید، بازرسی و تعیین تکلیف کیفیت، درخواست/کار تعمیراتی، مهارت و آموزش/ارزیابی مجدد، و تحویل قطعات بین OPها. شمارش کم، به‌تنهایی شکاف مهارتی را اثبات نمی‌کند. این‌ها فهرست هدف‌اند، نه قابلیت‌های فعال.
- **وضعیت عرضه:** قابلیت ساخته‌نشده در کاتالوگ باید وضعیت روشن و فعال‌سازی ممنوع در سرور داشته باشد؛ این خواسته پس از audit کاتالوگ به تغییر اجرایی جدا تبدیل شود. پاک‌سازی فعلی به‌تنهایی مجوزها/خریدهای شرکت را بازتعریف نمی‌کند.

**نمونهٔ پذیرش برش آینده:** ثبت یک کار بدون پلان؛ ثبت توسط خود یا نمایندهٔ مجاز با هویت‌های جدا؛ مشاهده در محدودهٔ مجاز؛ گزارش صحیحِ سالم/ضایعات در همان قطعه/OP؛ دادهٔ دستی یا شمارش خودکار با منشأ روشن. سپس همان جریان با یک کار ارجاع‌شده آزمایش شود. داشبورد/ورک‌اسپیس مصرف‌کنندهٔ خروجی مجاز است، نه مرجع تغییر حساب تولید.

### تکمیل سناریوی کارگاه و مرزهای توسعه — ۲۰۲۶-۱۰-۲۹

این توضیح، تکمیل جهت بالاست؛ ماژول یا سند مستقل تازه و ادعای پیاده‌سازی نیست. ثبت/گزارش تولید یک ماژول کاربردی است؛ «production workflow» صرفاً نام پیشنهادی مرحلهٔ تکمیل همین جریان است، نه ماژول زیرساختی دیگری که قبل از آن باید خریده یا در مخزن جدا ساخته شود. مالکیت فعلی کد در ARCHITECTURE است؛ تغییر شاخهٔ Git مخزن جدید ایجاد نمی‌کند. مرحلهٔ۰۳ در codex/03-production-recording از checkpoint۰۲ شروع شده است؛ توسعه باید ابتدا کد و قراردادهای موجود را تطبیق دهد، نه اینکه ثبت/گزارش را دوباره از صفر بنویسد.

- **شیفت، حضور و کار واقعی:** تعداد شیفت‌ها در مدل و رابط به سه گزینه محدود نشود؛ شرکت بتواند شیفت‌های نام‌دار متنوع، هم‌پوشان، شبانه و انتساب تاریخ‌دار به فرد/گروه را تعریف کند. نبود سقف ثابت سه‌شیفتی به معنی حذف محدودیت‌های فنی حجم/نرخ نیست. ساعت برنامه‌ریزی‌شده، حضور واقعی، اضافه‌کاری و بازهٔ انجام کار مستقل‌اند. از نام شیفت یا برنامهٔ حضور، انجام کار روی دستگاه استنتاج نشود. ثبت ساده بدون شیفت اجباری باقی بماند؛ مثال‌های ساعت و نام افراد قاعدهٔ عمومی یا اطلاعات seed نیستند.
- **کار معمول و جابه‌جایی:** دستگاه/قطعه/OP معمول یا آخرین کار، پیشنهاد قابل تأیید/تغییر است، نه انتساب دائمی. ارتباط انجام‌دهنده، کار/OP، دستگاه یا محل کار و بازهٔ واقعی باید قابل ثبت باشد. تعویض دستگاه، تحویل به نفر دیگر یا کار دستی سوابق قبلی را بازنویسی نکند. تعیین انتساب می‌تواند دستی، پیشنهادی از RFID/دوربین یا ورودی سامانهٔ دیگر باشد؛ منبع، زمان، کیفیت و تأیید/تعارض باید روشن باشند. ادغام خودکار این منابع یا مرجع قطعیِ تشخیص چهره هنوز تعیین/پیاده نشده است.
- **بازکاری:** اصلاح قطعهٔ ردشده، تولید قطعهٔ نو یا ضایعات قطعی فرض نشود. کار اصلاحی باید در صورت وجود مرجع به کار/قطعه/تولید قبلی مرتبط شود؛ ثبت دوبارهٔ تعداد اصلاح‌شده، خروجی نو را دوباره نشمارد. روز هفته، رسیدن پالت به تعداد مشخص یا دستگاهِ مثال، گردش ثابت همهٔ مشتری‌ها نیست. تعیین تکلیف کیفیت و جزئیات ردیابی بچ/قطعه هنوز طراحی تخصصی لازم دارند.
- **ورودی‌های متنوع و فرم مشترک:** دادهٔ هر فیلد کاربردی ممکن است دستی، تگ/پارامتر، فایل یا سامانهٔ خارجی باشد. ماژول نیاز و معنای داده، شرکت نگاشت/تنظیم و مجوز، و آداپتور روش دریافت را تعیین می‌کنند. افزودن ورودی خودکار نباید فرم جداگانهٔ ثبت تولید برای هر پروتکل یا شرکت بسازد. منشأ، زمان رخداد و دریافت، کیفیت، سابقهٔ اصلاح و اولویت/تعارض منابع حفظ شوند؛ قاعدهٔ دقیق حل تعارض، مستقل از ظاهر فرم نیاز به تصویب دارد.
- **یادداشت و اقدام:** موضوع یادداشت/اعلام مشکل می‌تواند دستگاه، کار یا گزارش باشد؛ مخاطب عمومیِ مجاز، سرپرست، همکار بعدی یا تیم فنی از خود متن جداست. خواندن، پاسخ و رفع مشکل وضعیت‌های متفاوت‌اند. یادداشت یا اعلام خرابی پایه، وجود ماژول تعمیرات را ثابت نمی‌کند؛ بعداً می‌تواند مرجع درخواست تعمیر شود. جزئیات چرخهٔ اعلان و ارجاع هنوز عملیاتی نیستند.

**پایلوت دریافت، طبق شرح مالک در این گفتگو:** تراش machine1 برند New Way یک EdgeBox دارد؛ ورودی فعلی قابل استفاده، HTTP با تعداد افزایشی همان بازهٔ یک‌دقیقه‌ای است، نه شمارندهٔ تجمعی. مشاهدهٔ رلهٔ فک، شمارش دستگاه است و به‌تنهایی سالم/ضایعات، شخص یا OP را اثبات نمی‌کند. قرارداد payload، مرز timestamp، تکراری و دادهٔ عقب‌افتاده پیش از اتصال مصرف‌کننده با نمونهٔ واقعی/کد بررسی شود. شمارش بازه‌ای که تغییر کار/شخص داخلش رخ داده، بدون قاعدهٔ مصوب بین آن‌ها تقسیم نشود؛ ابهام باید آشکار باشد. دقت اعلامی سخت‌افزار، شاهد کالیبراسیون یا آزمون جدید نرم‌افزار نیست.

**سایر ورودی‌های آینده:** مالک مسیر فعلی DI6/پاور و تنظیمات/پایش MQTT را شرح داده است؛ مرجع این مرحله برای تعداد، HTTP است و اتصال جدید MQTT یا ارسال پاور از HTTP ادعا نمی‌شود. سیگنال پاور، ارتباط دستگاه، heartbeat و وضعیت استنتاج‌شدهٔ ماشین جدا بمانند؛ نویز DI6 یا قطع ارتباط به‌تنهایی خاموشی قطعی نیست. خواندن برنامهٔ CNC، OP، start/stop و feed/speed از کنترل، LAN یا RS-485، و دریافت SCADA اهداف قابل اتصال‌اند؛ سازگاری پروتکل/رجیسترها/دقت هنوز تأیید نشده و از شمارش فعلی استخراج نمی‌شوند. این شرح، الزام معماری نرم‌افزار قدیمی یا مجوز تغییر firmware/شبکه نیست.

**گام اجرایی بعد از نمونهٔ UI:** کد/API/ذخیره/مجوز/تست ثبت تولید موجود بررسی و کمبودها مشخص شوند؛ سپس یک مسیر واقعی شروع کار، انتساب زمانی، شمارش HTTP، ضایعات/توقف/بازکاری و گزارش مشترک اپراتور/سرپرست تکمیل شود. نمونهٔ نمایشی میز کار را تحویل backend یا مجوز ساخت همهٔ ماژول‌های آینده تلقی نکنید. تغییر schema در صورت نیاز با مهاجرت و آزمون مجازِ همان مرحله انجام می‌شود؛ انعطاف‌پذیری قولِ «هیچ تغییر دیتابیسی در آینده» نیست.

## 1. Confirmed product direction / تصمیم‌های قطعی

1. **پویشگر اولین سناریوی واقعی و کارخانهٔ پایلوت است، نه مرز قابلیت‌های نرم‌افزار.** محصول باید در نهایت برای سازمان‌ها و صنعت‌های متنوع قابل پیکربندی و فروش باشد.
2. دامنهٔ محصول، پایش صنعتی + مدیریت عملیات + اتصال داده + تحلیل و بهبود است. تنوع واقعی از کارگاه سفارش‌محور و ماشین‌کاری چندعملیاتی تا خطوط پیوسته، مونتاژ و بسته‌بندی وجود دارد.
3. **ورود داده یک طیف است:** دستی، نیمه‌خودکار، واردات فایل، اتصال نرم‌افزار دیگر، دستگاه/EdgeBox، SCADA، MQTT، HTTP POST، API، خواندن دیتابیس خارجی و ترکیب این روش‌ها. نباید همهٔ شرکت‌ها را مجبور به نصب EdgeBox یا ثبت دستی کرد.
4. دادهٔ نمونه/شبیه‌ساز باید آشکارا از دادهٔ سنجیده‌شده و واقعی جدا باشد. پایلوت باید سناریوهای واقعی‌نما داشته باشد ولی نباید عنوان «اندازه‌گیری واقعی» بگیرد.
5. در این مرحله نرخ‌های معمول دریافت حدوداً هر دقیقه‌اند؛ ممکن است برخی هشدارها سریع‌تر ارسال شوند. حجم و نرخ واقعی پیش از انتخاب زیرساخت تخصصی Time-Series باید اندازه‌گیری شود. ساخت یک سامانهٔ High-Frequency Historian در حال حاضر هدف نیست.
6. **Hall/Area ساختار فیزیکی است؛** Line/Cell/Operation/Product/Team/Equipment و دامنه‌های KPI از نظر منطقی مستقل‌اند و ممکن است چند سالن را پوشش دهند. OEE سالن را با میانگین سادهٔ OEE تجهیزات نسازید.
7. رابط فعلی Vue 3 + TypeScript + Three.js و چیدمان واقعی کارگاه باید حفظ شود؛ سه حالت Immersive، Explore، Analytics از داده و انتخاب مشترک استفاده می‌کنند. Device/Line Detail فضای تحلیل عمیق مستقل است. تم تیرهٔ فعلی حفظ و تم روشن سفید/سبز در آینده افزوده شود.
8. برای مشتری جدید فرآیند ساده و قابل‌فهم راه‌اندازی، پیکربندی و ورود اطلاعات لازم است؛ نباید برای اضافه‌کردن دستگاه، تغییر شیفت یا فرمول KPI به توسعه‌دهنده وابسته باشد.
9. دسترسی‌ها و داده‌ها باید برحسب شرکت/کارخانه/کاربر و مجوز تفکیک شوند؛ صرف پنهان‌کردن منوها امنیت نیست.
10. قبل از فرم‌سازی گسترده، مدل اطلاعات، گردش‌کار و قواعد کسب‌وکار باید با صاحب محصول بررسی و مرحله‌به‌مرحله تأیید شوند.

## 2. Product principles / اصول طراحی

- **Configurable core, optional modules:** ماژول‌های کاربردی قابل روشن/خاموش و شخصی‌سازی، اما قرارداد اطلاعات و امنیت مشترک.
- **Simple on day one, flexible later:** پیش‌فرض‌های مناسب برای کارخانهٔ ساده؛ تنظیمات پیشرفته در بخش تخصصی.
- **Operational truth:** هر عدد باید منبع، زمان رویداد، زمان دریافت، بازه، دامنهٔ محاسبه، واحد و کیفیت/اعتبار داده داشته باشد.
- **Traceability and auditability:** نسخهٔ تنظیمات مؤثر، ثبت‌کننده، اصلاحات، چرایی تغییر و تاریخچهٔ اجرا حفظ شود.
- **Event time ≠ ingest time ≠ reporting time.** تأخیر شبکه، دادهٔ آفلاین و بازپردازش نباید بی‌سروصدا آمار را خراب کنند.
- **No false completeness:** ماژول‌هایی که فقط demo/read-only هستند دقیقاً همین برچسب را نشان دهند.
- **Keep interfaces open:** API و event contracts برای اتصال ERP، Grafana، AI و نرم‌افزارهای دیگر.
- **Preserve real workshop geometry and previous tested workflows.** هر تغییر بصری یا مدل جدید نباید جانمایی و ویرایش/انتخاب کارگاه را خراب کند.

## 3. Multi-tenant organization and physical model

حداقل تفکیک‌های پیشنهادی (نیازمند تثبیت جزئیات):
- Tenant / customer organization: محدودهٔ داده و قرارداد مشتری نرم‌افزار.
- Company/legal entity، Plant/Site، Building/Hall، Area/Zone: سلسله‌مراتب فیزیکی/سازمانی، قابل تنظیم؛ برای همهٔ شرکت‌ها وجود همهٔ سطوح اجباری نباشد.
- Asset/Equipment، Work center/Cell، Line: دستگاه و گروه‌بندی عملیاتی، مستقل از محل فیزیکی.
- Operator/Person، Team، Role/Membership، Skill/Certification: افراد، صلاحیت، نقش و عضویت؛ ممکن است یک فرد چند نقش/کارخانه داشته باشد.
- Product/Part، BOM/Recipe where applicable، Operation/OP، Routing/Process graph، Job/Work order، Production plan.
- Quality inspection, downtime event, alarm, maintenance work order, shift calendar, measurement/signal and KPI definition.

**ساختار فیزیکی سالن، ساختار فرآیند تولید و ساختار اختیارات سه مفهوم جدا هستند.** یک خط می‌تواند چند دستگاه/سالن را دربر گیرد. جابه‌جایی فیزیکی تجهیز نباید سوابق تولید قبلی را تغییر دهد.

Multi-tenancy candidate patterns (shared DB with tenant keys, separate schema, dedicated DB) must be compared for on-premise versus future SaaS; DO NOT freeze a tenancy isolation strategy before deciding deployment, security and cost constraints.

## 4. Data capture spectrum and source contracts

### Capture modes
1. Manual: اپراتور/سرپرست مقدار تولید، توقف، شروع کار، کنترل کیفیت یا تعمیرات را ثبت می‌کند.
2. Assisted: بخشی از داده با دستگاه/حسگر می‌آید و بخشی توسط انسان تکمیل/تأیید می‌شود (مثلاً علت توقف).
3. Batch/import: CSV/Excel/file/API import، سیستم حضور و غیاب، خروجی ERP یا MES خارجی؛ validation، mapping و گزارش خطا لازم است.
4. Automated: EdgeBox/PLC/SCADA/MQTT/HTTP/OPC UA (پس از تأیید مشخصات واقعی)، دیتابیس صنعتی خارجی، webhooks.
5. Hybrid per equipment/event type: همان دستگاه می‌تواند شمارندهٔ خودکار و علت توقف/بازکاری دستی داشته باشد؛ precedence و reconciliation قابل تنظیم اما کنترل‌شده باشد.

### Common inbound event/envelope (conceptual; exact schema to be approved)
tenant_id, site_id, equipment_id/resource_id, source_type, source_id, event_id/idempotency_key, event_type, event_timestamp, received_timestamp, optional valid_from/valid_to, payload, unit, schema_version, mapping_version, quality_flag, simulator/demo flag.

Examples: production_count_delta or absolute_count with reset/wrap semantics; machine_state_transition; alarm_raised/alarm_cleared; operation_started/paused/completed; manual_downtime_reason; quality_inspection_result; maintenance_action.

- Maintain raw payload for investigation where appropriate and normalized validated records for reporting; protect secrets and retention.
- Use deduplication, idempotent ingestion, late/out-of-order handling, reconnect buffering, rate limits, data-quality checks and source health monitoring.
- Sampled status snapshots and actual state-transition events differ; derive durations only with specified rules and freshness/unknown handling.
- For minute-level samples MariaDB/InnoDB is a reasonable starting point. Benchmark real cardinality, indexes, partition/retention and queries; do not migrate to a Time-Series DB solely because the data has timestamps.
- Alarm events may use a faster event path when technically justified, independent from regular minute snapshots.
- Future read-only integration/exports for Grafana and external analytics via SQL views/read replicas or versioned metrics API with tenant/permission restrictions.

### Edge connectors
Adapter/connector registry with capability declaration, configuration schemas, identity, mapping of signal to domain semantics, connection status and simulator mode. Separate adapter specifics from business logic. Never assume SFP24 EdgeBox firmware registers or command meanings without real contracts. Do not interfere with running ERP/home automation/hardware environments without approval.

## 5. Equipment state: do not collapse distinct meanings

Model separately:
- Connectivity/Freshness: connected, delayed/stale, offline, unknown.
- Technical/physical: powered, ready, alarm/fault, maintenance lockout, unknown.
- Operational mode: producing, setup, idle/waiting, scheduled stop, unscheduled stop, manual work, unknown.
- Work assignment: has active job, no job, reserved, awaiting material/tool/person.
- Dispatch availability/eligibility: can new work be assigned given capacity, maintenance, skills, fixtures, locks and calendar.
- Alarm severity/acknowledgement: distinct from state and from availability.
- OEE Availability is a calculated KPI with defined planned-production-time rules; not the same as machine allocatability or network connectivity.

Each state needs evidence and effective period; do not infer "machine broken" from no samples, nor "no job" from stopped spindle alone. Show visible differences in 3D overlays/legend without an overload of labels. Configure semantics per equipment and allowed manual override with audit trail.

## 6. Two opposite factory examples using one operational core

### A. Pouyeshgar / flexible job-shop
- Customer orders and potentially diverse low-volume parts; each part can have its own versioned Routing/OP sequence (e.g. turning, drilling, milling, broaching, inspection).
- An operation may have multiple eligible machines, tools/fixtures and operators based on skill.
- Operators change machine assignments, potentially within a shift. Record time-bound actual assignments.
- Job-specific cycle time, setup time, quantity, yield, scrap/rework, hold, queue and subcontracted/external process when relevant.
- Can require serial, lot/batch, container or intermediary WIP tracking at configurable granularity.

### B. Fixed/continuous line (shampoo/juice, etc.)
- Multi-stage line (e.g. molder/former → filler → capper → labeler → packer) with throughput, buffers and bottlenecks.
- Line state, equipment state and downstream/upstream blocking/starvation are distinct.
- Recipe/product changeover, line scheduling, traceability lot/batch, quality sampling and downtime attribution to bottleneck.
- Configurable topology and data semantics, not an assumed universal fixed recipe or machine order.

### Unifying model
Process definition is a versioned graph of operations/resources with optional alternate routes, parallel stages, buffers, rework and subcontracting. Work execution instances link actual operators/equipment/time/quantity back to order/operation. Scheduling vs execution vs reporting are separate layers. **Do not model everything as a single fixed linear sequence or infer line OEE from an average of component OEE.**

## 7. Workforce, shifts, planning, quality and maintenance

**Shift/calendar:** one 12-hour shift, two 12-hour shifts, three 8-hour shifts, overnight cross-midnight, breaks, holidays, exceptions, seasonal rosters, site time zones. Distinguish standard schedule and actual attendance. Shift reporting must use event-time intervals and correct business-day boundaries. A badge/card-reader on LAN is a future connector, not an assumed installed integration.

**People:** identity and personnel profile, optional avatar, skill matrix, job qualifications, team membership, role, attendance data link, time-bounded allocation to equipment/operation, manual correction with audit. Do not commit real personal/biometric data or employee photos to demo seeds. Sample users should be clearly fictional.

**Planning:** demand/order → routing → jobs/operations → constraints (machine capacity, setup/changeover, material, tools, skilled operators, shift calendar, subcontracting, deadline) → proposals and confirmed plan. Separate capacity planning, dispatching, APS and MRP; identify required inventory/BOM/ERP data before enabling MRP. For constrained scheduling, deterministic rules or an optimization solver may precede AI; humans approve changes. For machine shop vs line, use suitable dispatch/line-planning strategies against same underlying entities.

**Quality:** inspection plan by part/operation/lot, checkpoints, measurements with tolerances and units, sampling plans, defects, scrap/rework/hold/disposition, genealogy traceability where needed. Define how quality events affect yield and OEE without silently interpreting every scrap as an OEE quantity.

**Maintenance / CMMS:** asset register (make/model/serial/commissioning/criticality), counters and calendar triggers for preventive maintenance, corrective request, fault, triage, assigned technician, work order, work carried out, downtime relationship, parts consumed, approvals and history. Manual/service providers possible. Clarify if predictive maintenance is appropriate with available data.

**Notifications & Andon:** role/scope-targeted alerts, acknowledgements, escalation, shifts, daily summaries, operator instructions and management reporting. Anti-spam, audit and source quality mandatory; future email/SMS/app integrations are optional.

## 8. KPI definitions, metrics engine and dashboards

A KPI definition must identify metric ID, semantic meaning, scope (asset, operation, product, team, line, site if valid), numerator/denominator, unit, filters, exclusion policy, planned time/calendar rules, thresholds/targets where configured, formula version, effective date, and source-quality requirements.

- Scope and period from UI must affect actual backend queries and calculation, not just labels.
- Time presets: current shift to now; selected shift; hour/hourly; today; yesterday; recent week; month; arbitrary interval. Time zones and midnight boundaries matter.
- Distinguish current live state from state-at-report-period-end, and snapshots from aggregated intervals.
- Charts: proper axes/units/ticks, tooltips, drill-down, zoom/pan/reset when meaningful, gaps as gaps rather than invented continuous slopes, series provenance. Gauges must expose formulas and inputs when clicked; never invent company-specific targets.
- Industrial OEE = Availability × Performance × Quality only under a well-defined measurement model. Weighted custom performance metrics must not be called standard OEE. Aggregation requires approved source time and production semantics; never average equipment OEE for a hall without a legitimate defined method.
- Layer manager for state, production, KPI, faults, quality, maintenance, people, freshness: visibility genuinely affects 3D and contextual data; one primary layer plus controlled overlays; legend and freshness status.

## 9. UX, data-entry and onboarding

User requirement: **main desktop dashboard information visible without document scroll** at 1366×768 and 1920×1080, compact unified controls, responsive panel sizing, no hidden CTAs or nested scroll traps. Three distinct views with same filters/selection; real equipment 3D stage retained.

Onboarding (provisional flow; approve before implementation):
1. Create tenant/company, sites, locale/time zone/currency and verified branding.
2. Configure halls/areas, assets, work centers and 3D model mappings/positions.
3. Establish calendars, shifts, holidays, breaks.
4. Invite users, choose scoped roles/permissions and staff/skills.
5. Define products/parts and process routes/OPs; optional BOM/recipes, inspection templates.
6. Define machine capabilities, event and data-source mappings, Edge/connectors or manual forms.
7. Define KPI definitions, planned-time policies, dashboards, alarms and notifications.
8. Import or enter initial orders/jobs; test with simulator or sample data; validate reports.
9. Activate live source only after connectivity and data-quality acceptance.

Each step should be resumable, validated, importable/exportable and permission-aware. Basic experience simple; expert settings available when needed. Define amendment history and effective-dated records so edits to an operator, shift or equipment capability do not rewrite historical production.

Theme system: existing dark navy industrial design; future light white/green based on owner-provided *original* artwork, optional customer branding/theme tokens. Consistent chart/state colors and contrast; do not conflate theme colors with operational severity. Persian RTL, English LTR, calendar choices.

## 10. Security, tenants, audit and deployment

- Multi-tenant separation at API/query and storage level; organization membership, site/equipment/process scope, action-level RBAC with possible future ABAC for approvals; deny-by-default.
- Authentication/session, account invites/reset/disable, operator/quality/maintenance/finance/plant manager permissions; service accounts and Edge credentials distinct from human accounts.
- Audit log: who changed what/when/why, before/after for critical configs and approvals; revision/effective dating.
- On-premise pilot and possible SaaS future; offline and local-first operation may matter. No promise of turnkey multi-tenancy/security until implemented and tested.
- API versioning, idempotency, migrations, backup/restore, retention, device provisioning, monitoring, error handling and integration logs.
- Avoid premature microservice sprawl: consider modular monolith (separable bounded contexts) with event/API interfaces. DB decision and per-tenant hosting to be revisited after measurable needs and threat modelling.

## 11. AI and open ecosystem (future, not mandatory in first pilot)

Useful AI applications: downtime root-cause hypothesis, anomaly/trend detection, quality drift, maintenance risk, operational shift reports, natural-language KPI explanations, improvement suggestions, what-if planning. Outputs must include confidence, evidence/provenance, relevant period, human approval and tenancy-bound permissions. Do not fabricate root causes from insufficient samples.

Optimization of scheduling may use OR-Tools/constraint solver or deterministic dispatch rules without a large language model. Do not place autonomous production control in an LLM.

Other services via documented APIs/connectors: ERP, finance, attendance, SCADA, MES, MRP/APS, Grafana, maintenance and messaging. Expose controlled metrics/stream contracts for internal or external Grafana. AI assistance is a service consumer, not the source of operational truth.

## 12. Standards to study, not compliance claims

Review relevant requirements only after exact product scope: ISO 9001 (quality/process traceability), ISO 22400 (manufacturing KPI definitions), IEC 62443 (industrial control system cybersecurity), and other standards as they become materially relevant. Map requirements to evidence and functions; never state ISO certification/compliance without formal assessment.

## 13. Actual implementation status at handoff

User-reported Codex progress for Phase 2: visually improved compact dark RTL UI, simulator demo labels, three monitoring views, detailed device screens, charts, layer manager, production/downtime/maintenance pages. Codex reported successful automated/browser QA and is still modifying code as of 2026-10-14. Earlier report said Fastify, server-side scoped authorization, local persistence, timed simulator, MariaDB adapter; **real MariaDB connection, live hardware, ERP integrations, and organizational RBAC were explicitly NOT claimed as fully proven**.

These are reports/screenshots, NOT independent verification of the latest branch, schema or end-to-end behavior. On next review: inspect actual HEAD/working tree, database migrations, API routes, auth enforcement, data lineage, simulator persistence, UX QA artifacts, and performance. **Do not interrupt the ongoing Codex run or push files to its active branch.**

## 14. Recommended design sequence (not a blanket implementation order)

**A — Review current deliverables:** collect Codex final report, commits, QA/screenshots, determine real vs stub/demo; preserve baseline.

**B — Freeze cross-cutting foundations:** tenant/organization boundaries, physical asset model vs operational group, time-zone/calendar, event envelope and source provenance, user permission vocabulary, versioning/migrations.

**C — Owner workshop for first operational slice:** agree manual/assisted/automated path for one Pouyeshgar CNC and one OP, one actual operator assignment, production event, stop reason, calculation and period filter; acceptance tests.

**D — Define foundation settings/onboarding:** company/site/hall/equipment/model mappings, shifts, people/skills, connector mapping and KPI metadata. Use real forms and validation, not decorative interfaces.

**E — Pilot end-to-end vertical slice:** define equipment + shift + operator + part + job/OP → ingest simulator/manual events via API → persist DB → query historical/shift reports → 3D overlay, charts and detail with drill-down. Then validate a second manufacturing scenario (fixed line) against model assumptions.

**F — Expand modules intentionally:** scheduling, quality, CMMS, alerts, Andon, external connectors, permissions and external APIs; AI/optimization after reliable data.

## 15. Open questions — ask owner when designing each module

1. Single-tenant on-premise vs centrally hosted multi-tenant SaaS, and whether hybrid installations need synchronization?
2. Minimum traceability granularity: quantity only, lot, serial, container/pallet, WIP operation movements?
3. Distinction between company, plant, subcontractor, customer and supplier in a service machining business?
4. Exact names/identity of assets, equipment/line memberships and capability templates across industries?
5. OP semantics in each business: process step, job, product, routing version, production weight? Never hard-code a universal assumption.
6. Source priority/manual corrections; count absolute vs delta, reset behavior, idle vs stopped, alarm lifecycle; EdgeBox firmware contract?
7. Planned vs actual shift/attendance; midnight/holidays/breaks; employee time clock API?
8. Material/BOM/order/inventory needed for realistic MRP, scheduling, service-vs-make-to-stock models?
9. Formula editor safety, permissions, effective dates, test fixtures; metrics query/retention patterns?
10. Defined OEE and breakdown policies per equipment/operation/line; quality/rework and manual inspection semantics?
11. Role matrix for operator, supervisor, quality, maintenance, finance, manager, tenant admin; dual approvals?
12. Deployment, backup, resilience, performance targets and service-level requirements?

**Operating rule:** advance through concrete owner-reviewed decisions; do not infer unprovided business rules from screenshots or seed data. New chat sessions must read this product blueprint plus the current code before issuing implementation prompts.


---

# 2026-10-14 ADDENDUM — Configurable modules, incomplete data, changing plans, and next-session operating guide
**Decision record:** This section formalizes the owner's later explicit requirements. Treat them as product requirements, not as features already implemented. It supplements the earlier cross-industry vision and is intended to be understandable when this chat is unavailable. Later validated decisions must supersede earlier assumptions explicitly and with a documented reason.

## 16. Critical requirement: a customer may only want ONE module / قابلیت‌های مستقل

**Confirmed owner scenario:** A company might buy/enable only OEE; or just machine counts, stoppages and daily operator reports. It might have no formal production plan, no quality records, no ERP, and no IoT hardware. The software MUST remain useful without forcing unwanted dependent modules or fake data.

Three independent axes MUST NOT be conflated:
1. **Tenant capabilities/modules**: what is licensed/enabled/configured (Monitoring, production entry, downtime, OEE/KPI, quality, maintenance/CMMS, planning, workforce, finance integrations, etc.).
2. **Data readiness/provenance**: what facts actually exist, source type (manual/import/IoT/API/simulator), freshness, validity and completeness for a metric; may vary by equipment and date.
3. **User authorization**: what the current user may read, enter, approve, edit, export or administer, scoped by tenant, site, equipment and role.

Optional fourth axis: **operational configuration maturity** — module is enabled but onboarding, sensor mappings, schedules, ideal cycle times, thresholds or formulas have not been completed.

UX/API requirements:
- A disabled module is absent from or explicitly disabled in ordinary navigation according to the tenant configuration; cannot be called anyway through API. Its historical data must not be deleted on deactivation.
- An enabled module with no data shows a clear empty state with its missing prerequisites and actionable entry/import/connect steps; never fabricate values or present a zero instead of unknown.
- A user without permission cannot gain access by URL/API, even if the module is enabled.
- A device can have automated count, manual stop-reason coding and imported quality checks simultaneously. **Capture method is per data type/source/device, not a universal company switch.**
- Navigation, forms, home dashboard, available charts, Layer Manager, table columns and report exports derive from module capability + data readiness + permission; a company with only basic production and stops sees a SIMPLE, relevant interface.
- Do not build one monolithic mandatory onboarding wizard that demands planning, BOM, QC, CMMS, OEE and connected sensors before the first operator can record production.
- Distinguish \`disabled\`, \`not configured\`, \`no data in selected period\`, \`source stale\`, \`access denied\`, \`not applicable\`, \`demo/simulator\` and \`valid zero\` in UI and APIs.
- An OEE-only company may still need supporting definitions/inputs (planned production time, ideal cycle/rate, good and total counts and time losses); these can be imported or manually entered **without enabling a comprehensive order planning or QC workflow**. If essential inputs missing, do not display calculated standard OEE.

Illustrative tenant modes (not hard-coded product editions):
| Customer need | Required minimum workflow | Explicitly optional |
|---|---|---|
| Machine counts + downtime only | register device, calendar/period, manual/import/IoT count and state/stop events, daily reports | work orders, quality, BOM, advanced planning, OEE |
| OEE only | equipment, planned-time rules, ideal cycle, good/total quantity and applicable downtime; source provenance | full quality inspection process, full ERP/MRP, detailed scheduling |
| Manual-only workshop | operators/supervisors record shift/day production and stops | EdgeBox, PLC, real-time telemetry |
| Flexible job shop | optional customer orders, part/OP/job, alternate machines, skill-based staffing, changing assignments | fixed production plan, permanent line topology |
| Fixed automated line | topology, product/recipe/batch as needed, line & equipment events and throughput | job-shop dispatch model |
| Full manufacturing suite | opt-in planning/QC/CMMS/analytics/integrations and shared audit | no fake data to fill missing features |

## 17. Unplanned / volatile production is a FIRST-CLASS workflow / تولید بدون برنامهٔ ثابت

**Owner example:** Pouyeshgar's customer-driven jobs frequently change daily/weekly due to demand, economic conditions and customer revisions. Some shops have no routinized scheduling process at all.

- Production event entry MUST work without a formal production order, a committed plan or an ERP connection. Show actual production, manual stoppage and shift/operator daily reports without inventing targets.
- Optional later refinement: \`unplanned activity\` → associate to a customer/order/part/OP/work center → optionally create or link a job/plan. Preserve original evidence, timestamps and amendment/audit trail.
- Separate: actual observed facts (machine, time, operator, quantity, state, stop reason) vs business attribution (part, OP, job, customer) vs plan/target, which may be missing or revised.
- Support ad-hoc jobs, day-of or week-of plans, standing/routine recipes, formal orders and advanced scheduling as distinct workflows. Operators can switch equipment and assignments as required; use time-bounded actual assignments.
- When plan is missing: display actual count and actual stops; **do not claim attainment %, schedule variance, plan delay, planned-vs-actual OEE inputs** without defined semantics. May show "No plan configured".
- Plan revisions must be versioned with effective times and reason/author. Historical reports should offer "plan as known then" vs "latest revised plan" where relevant, not silently rewrite past achievement.
- Tables must degrade gracefully: omit unavailable plan fields or show \`— / no plan\`, not a forest of invented \`0\` values. Dynamic columns and chart slots must avoid useless empty cards.
- For job-shop, routes/OPs can be alternative, parallel, outsourced, rework, quality gate or ad-hoc; lines can have fixed connections, buffers, bottlenecks and products. Both rely on common actual execution/event data but preserve distinct planning methods.

## 18. Capture and interoperability is a CONFIGURABLE PIPELINE, not one fixed API

**Confirmed use cases:** manual shift logs, mobile/tablet workstation entries, Excel/CSV imports, machine/EdgeBox/PLC/SCADA feeds, attendance readers with LAN, other ERP/finance systems, direct authorized database extracts/dumps, HTTP API, MQTT, and exposing the platform's own data back to partners, analytics or Grafana.

Conceptual pipeline:

\`\`\`text
Manual forms     Excel/CSV       Edge / PLC / SCADA       external API / DB / ERP
      \\               |                   |                       /
        → Connector / import job / schema mapping / validation / permissions
        → Source-tagged, idempotent normalized events / observations
        → Operational records and audit / corrections / quality flags
        → Scoped queries and metric engine (time, shift, scope, formula version)
        → Dashboards + tables + Excel/CSV exports + documented outbound APIs / Grafana
\`\`\`

Do not require all connectors for an initial release. Define a connector contract, implement one realistic vertical slice, then add adapters incrementally. A supplier's API structure is NOT presumed universal: per-adapter authentication, polling/webhook, schema mappings, rate limits, retries, deduplication, timestamp, tenant/equipment identity and error dashboards are needed.

Manual capture:
- Let operator/supervisor register by shift/day/equipment/OP (if known): completed counts, good/reject counts (when available), stop reason and times, notes; role-based approvals and correction history.
- A manual once-daily report is not live telemetry. Derive daily/historical metrics only to the actual available granularity; use honest freshness flags. May allow a foreman to enter data for many machines from one shift sheet.
- Partial input must be valid (e.g. count without part or plan), but clearly mark calculations unavailable until prerequisites arrive.

Excel/import/export:
- Each eligible domain (equipment, personnel, parts, OP/routes, schedules, operations, stops, quality etc.) should support import templates and export, **based on permissions**, with preview, column mapping, types/units/time zone validation, row-level error listing, dry run, repeat-import dedupe/upsert policy and reproducible import logs.
- Export bounded filtered datasets (scope, time, tenant, columns, encoding/locale) and async jobs if large. Avoid promising arbitrary database dumps for end users.
- Outside database connector: read-only least-privilege account, allowlist of sources, encrypted credentials, incremental cursor/high-water mark, mappings, safe query budget and reconciliation; full dump exchange only by explicit controlled migration procedure, not ongoing blind imports.
- Outbound: documented versioned read APIs, secure auth/scopes, pagination/filters, optional webhooks and analytics-friendly materialized views; Grafana inside/outside platform is a consumer, not the only possible presentation.

## 19. Source-aware state, availability and OEE contracts

These separate values must be modeled, queried, filtered and visualized distinctly:
- **Connectivity:** data source healthy/stale/offline/unknown; do not infer powered-off from disconnected.
- **Physical readiness:** powered / faulted / under maintenance / ready / unknown, grounded in evidence.
- **Operational activity:** producing / setup / idle due to no job / waiting material or operator / planned stop / unplanned stop / unknown.
- **Dispatch eligibility:** whether a *new task could be assigned now*, based on resource, calendar, maintenance, operator, tooling and capacity; not equivalent to physical ON state.
- **OEE Availability:** defined formula over classified planned time, not a raw live boolean.
- **Alarm lifecycle:** active/cleared/acknowledged, severity, timestamps and provenance; alarms may update faster than sampled counters.

If no current source data exists, show unknown/unobserved, not a fabricated green running state. Allow documented manual status reporting with its own author and timestamps. Any automatic inference (e.g. idle from stable counter) needs configurable duration, valid signal freshness and clear provenance.

## 20. Minimum UI/UX contract established by the owner in Phase 2

The actual pilot's dark blue RTL design and working Three.js scene are now valuable assets; preserve them. An optional light white/green theme and possible branded themes are planned, with owner-supplied reference artwork when available.

The decisive visual requirements and measurable tests established previously:
- **Desktop at 1366×768 and 1920×1080:** viewing primary Monitoring dashboards must NOT require vertical DOCUMENT scroll. Place scope, date/shift filters, selected view, alerts and primary metrics in compact control/header rows. Never hide actual content via crude \`overflow:hidden\`. Context panels/tables may have controlled accessible scrolling without covering CTAs.
- Immersive: existing real-workshop 3D geometry remains dominant; efficient camera framing, scalable non-colliding labels, opt-in layer overlays, compact alarms, kiosk suitability. Do NOT substitute a concept image of a fictional factory.
- Explore: same Three.js geometry/data and filters, raycast selection, strong highlight, contextual panel with essential information immediately visible; CTA never obscures the panel.
- Analytics: distinct analytical composition with useful charts/tables and true domain content; avoid generic copied production charts under Quality, wasteful oversized 2-item Pareto cards or giant empty chart containers.
- Device/Line Detail: contextual job/part/OP, operator, time range, state, freshness, production, OEE A/P/Q, valid formula trace, state/downtime timeline and device 3D. Formula explanations must be KPI-specific.
- Layer Manager: toggles genuinely affect 3D markers/labels/selection context and matching data views; primary layer and non-overloading secondary alerts, explanatory legend.
- Charts/Gauges: actual analytical components with semantic axis units/ticks, period labels, tooltip, meaningful zoom/pan/reset/drilldown, legend and source. Gap in data MUST NOT be connected as an invented smooth trend; show gaps as gaps. A gauge click exposes source data, numerator, denominator, definition/version and time period (when relevant).
- All KPI/card/chart/table outputs must share effective time range, shift-calendar logic and scope; presets include start-of-shift→now, hourly, today, yesterday, recent week, current month and arbitrary intervals; crossing midnight must work.
- English LTR/Farsi RTL genuine; date formatting appropriate to locale; fonts, hierarchy, contrast, spacing and responsive layouts intentionally designed.
- Browser visual QA with screenshots and interaction verification, regression tests for old scene, JSON import/export, raycasting, orbit/zoom, fullscreen, state storage.
- User's approval: Phase 2 UI became substantially satisfactory, so **avoid initiating a wholesale redesign** after Codex finishes. Final QA and targeted flaws only.
- Missing integrations/data must be honest Demo, no-data or not-configured states. UI aesthetics do not justify invented production data.

**Reference photographs** live in the Codex conversation / owner-supplied \`docs/design/reference\` when actually copied. Do not claim asset files are committed unless verified.

## 21. Next-session handoff — USE THIS IF THE ORIGINAL CHAT IS UNAVAILABLE

**Product in one sentence:** A saleable configurable industrial-operations and digital-twin platform, piloted first in a flexible CNC job-shop (Pouyeshgar), supporting manual → assisted → automated data capture, optional OEE/production/quality/CMMS/planning modules, time/shift-aware metrics and integration APIs, with a common audited operations model.

**What is approved:** Pouyeshgar first, not only; diverse factories; no forced modules or live hardware; no fixed schedule requirement; common normalized data contracts; transparent demo/measurement; user-scoped access; real workshop Three.js layout; compact quality visual design; separate physical vs operational scopes; possible light theme.

**What is proposed rather than decided:** exact tenant storage strategy, module licensing UX, final OEE exclusions, normalized event schema, manufacturing process graph details, job/lot/serial traceability levels, exact shift setup, operator skill constraints, scheduling engine, attendance adapter, hardware message contracts, dedicated time-series DB, AI features and ISO alignment. These require explicit owner decisions and should not be coded as arbitrary universal rules.

**Current work state:** Codex is still completing and testing Phase 2 on \`feat/smart-factory-pilot-next\`; this document is on **separate** \`docs/platform-product-blueprint\` branch to avoid conflicts. No unreviewed merge or deploy. \`main\`, \`next\`, earlier safety stash untouched. A recent Codex screenshot showed QA and ongoing modifications, not final acceptance.

**Before any new coding prompt:**
1. Read this full file, \`AGENTS.md\`, \`docs/CODEX-SMART-FACTORY-HANDOFF.md\`, \`docs/archive/research/UI-VISUAL-IMPLEMENTATION-CONTRACT.md\`, and latest Codex final report plus current Git status/commits. Distinguish documented **requirements** from proven **implementation**.
2. After Codex finishes, consolidate conflicting parallel docs with owner: one canonical Product Blueprint (this), one architecture/current-state reference, one UI acceptance/spec, one operations/runbook, decision log and module specs as necessary. Archive obsolete materials with traceable Git history; do not blindly delete.
3. Inspect actual backend/db (MariaDB adapter vs tested DB), security, simulator persistence, charts/query code, export adapters, auth, tests, QA screenshots; prove behavior rather than taking a green QA banner as universal readiness.
4. Owner and assistant then review data model and data-entry flows **one module at a time**, starting with organization/site/assets, a shift, person, one CNC operation, manual or simulated event, report, and available KPI. Validate this end-to-end before adding more generic forms.
5. For any idea, categorize: confirmed requirement, alternative/proposal, pending question, implemented/tested, or deferred. Keep a decision log with date and rationale.
6. Continue in same project with target active development branch *after verifying* what Codex committed; do not mistake documentation-only branch as development base, and do not apply old stash without inspection.

**Specific new-session comprehension check:** The platform MUST work for a customer with **no IoT device, no production plan, no QC module**, still allowing daily manual operator counts/stops and honest reports. Another customer can choose only OEE and supply the necessary inputs manually or via Excel/API. A continuous bottling line must be representable without forcing machine-shop jobs. A single company may mix source modes per machine/data type. Disabled module, absent data and denied permission are three different outcomes.

**Next owner interaction:** Wait for Codex's FINAL report; do not send it scope-expanding prompts while it runs. Then audit screenshots and code, reconcile docs, and agree data-entry/domain choices before implementing the next backend slice.


---

# 2026-10-14 EXTENDED DOMAIN CHAPTER — Demand modes, forecasting, scheduling, inventory, logistics and international models
**Status:** Detailed product/domain discussion, NOT a completed feature specification or evidence of implementation. Authored to preserve context across ChatGPT and Codex sessions. This chapter does not supersede approved UI, source honesty, module independence, tenant isolation or current workshop geometry. The owner explicitly requested full explanations and multiple realistic scenarios rather than a terse feature list.

## 22. Why this chapter exists / چرا این فصل اضافه شده است

**Owner's business goal:** Build a unified platform that starts small (one company only wants counts and downtime, supplied by an operator or EdgeBox) yet can ultimately support the operational needs and integrations of far larger, complex, multi-line manufacturers. Pouyeshgar is the first REAL pilot, not a hardcoded vertical. The software must offer coherent, optional capabilities rather than compelling small customers to adopt a complete ERP.

**New questions from the owner:** If a company plans from confirmed orders, how is that distinguished from producing against demand forecasts? What if it holds inventory, uses warehouses, moves materials internally, ships to customers or coordinates multiple locations? How do production scheduling, logistics and external ERP coexist? Can we map concepts to international manufacturing and supply-chain standards without inventing a unique closed architecture? Can a single platform span Pouyeshgar's changeable CNC shop and a food/beverage conglomerate?

**Principle:** Keep concept definitions, scenario examples, alternatives and decisions explicit; do not leap directly to database tables, UI forms or a premature megaproject. Record what is *observed*, *requested*, *proposed*, *undecided*, *not implemented* and *tested* separately.

## 23. Demand ≠ order ≠ forecast ≠ production plan ≠ actual production

**Do not flatten these distinct business concepts into one "production order" table.** They refer to different claims, times, commitments, and levels of uncertainty.

- **Customer order / Sales order (سفارش مشتری):** A specific contractual or commercially accepted demand. Includes customer, items, quantities, requested/committed due dates, change history, status; may originate in ERP or be entered manually. For subcontract/service manufacturing, customer may own raw materials and may request processing, not purchasing a finished product.
- **Forecast (پیش‌بینی تقاضا):** A non-binding estimate of expected demand, by product/family/site/customer and future buckets (day/week/month). Holds method/version, confidence or scenario, creation timestamp and author/source. Not equivalent to a confirmed sale.
- **Internal replenishment demand (نیاز تأمین موجودی):** Demand to replenish safety stock, minimum/maximum level or reorder point; may result from forecast/consumption policy even with no external customer order.
- **Manual/ad-hoc production request (درخواست فوری/موردی):** Work authorized by shop supervisor even when no formal order or forecasting module is used; owner explicitly requires this for fluctuating Pouyeshgar workloads.
- **Master production schedule (MPS / برنامهٔ اصلی تولید):** Management's time-phased decision of what finished or intermediate items should be available and when, reconciling multiple demand sources, capacity and constraints. It must be versioned; a forecast is an input, not a plan by itself.
- **Production/job/work order (دستور/کار اجرایی):** An authorization to make/process a specific quantity or perform an operation. Can be generated from MPS, from an order, or created manually. Actual operations must remain usable even if formal work orders are disabled.
- **Actual execution (اجرای واقعی):** Verifiable evidence: start/stop, machine, operators, quantity, rejects, serial/lot/container if applicable, timestamp, source. May diverge from every plan and still must be recorded accurately.

### Examples (illustrative, not committed business rules)

**Scenario A — Pouyeshgar / order-driven (Make-to-Order / MTO):**
An industrial customer asks for 120 shaft parts by next Wednesday. Workshop receives a request by phone, later an order; OP1 turning and OP2 drilling have several eligible machines; operator assignment changes mid-day. There may be no approved weekly plan. We must capture actual machine work immediately and optionally link it to the order once confirmed. A changed requested date produces a new order revision and scheduling proposal, not a silent overwrite of past execution. If this is a service job, track material ownership and the work performed without assuming the shop owns or sells the raw stock.

**Scenario B — Bottle/shampoo/juice manufacturer / forecast-driven stock (Make-to-Stock / MTS):**
A weekly demand forecast proposes 50,000 bottles, with 10,000 in salable inventory and 4,000 safety stock (illustrative numbers only). MPS proposes a quantity after accounting for demand, availability, confirmed orders and the chosen forecast-consumption policy. Replenishment may produce batches/line campaigns with recipe/packaging specifications. Actual shipped goods, inventory, receipts and forecast error become reportable once the respective modules or integrations exist. We must never automatically double-count the same customer sales orders *and* the forecast that already incorporates those orders.

**Scenario C — Mixed mode:**
Some SKUs are stocked to forecast; special branded labels are manufactured to confirmed orders; spare parts are replenished by min/max; urgent jobs are created manually; and a manufacturer may assemble final variants on receipt of an order (Assemble-to-Order / ATO). Different planning policies may coexist by product/site/time. The application must not have one global \`order-based=true/false\` flag.

**Scenario D — No planning module whatsoever:**
A small customer enters shift-end output and downtime on paper/Excel or by phone. No product master or forecast is mandatory. Dashboard shows actual count/downtime and source timestamps; unavailable planned-vs-actual/OEE components are labeled unavailable, not invented.

### Forecast consumption / avoid double counting

Forecast vs confirmed orders in the same buckets require an explicitly configurable **forecast-consumption or netting rule**; candidate practices include consuming forecast with accepted orders or retaining separate scenarios. Do not subtract arbitrary quantities without date/product/site mapping. Keep all original demand records and revisions; computed net demand is a derived view with an explained policy.

### Decisions still open

- For the initial pilot, is an ad-hoc job sufficient or should Pouyeshgar introduce a minimal work-order identifier? Which records can remain anonymous/unattributed?
- Is order commitment date distinct from requested date? Who authorizes changes? Which revision is visible in historical reports?
- How are forecast time buckets, scenario/version and forecast accuracy defined? Forecasting itself is a future optional service; a company may import third-party forecasts.
- For service operations, what documents distinguish customer-supplied raw materials, shop-owned purchased materials and outsourced jobs? This must be defined with the owner; do not copy rules from the separate ERP project without reading its approved domain docs.

## 24. Planning and scheduling are several separate services, not synonyms

**Demand planning / Forecasting:** estimates future market/customer demand and uncertainty. Algorithms could range from human entered forecasts and moving averages to statistical models or later AI; source, scenario and horizon must remain explicit.

**S&OP / Integrated Business Planning (IBP):** longer-horizon coordination of demand, production, procurement, capacity and financial objectives, usually at aggregate product-family/site level. Not mandatory for a small shop.

**MPS (Master Production Scheduling):** medium/short-horizon executable production quantities and dates at an appropriate product/line/site level, reconciled against demand and inventory policy.

**MRP (Material Requirements Planning / برنامه‌ریزی نیاز مواد):** time-phased explosion of planned quantities using valid BOM/recipe, lead times, inventory balances, reservations, scheduled receipts, scrap/yield and lot rules. Requires reliable material and inventory inputs; cannot be truthful when BOM and balances are unknown.

**MRP II / Capacity planning:** incorporates resource/material capacity and sometimes broader manufacturing planning. Do not present a pure MRP material explosion as proof that a feasible machine/operator schedule exists.

**Finite-capacity scheduling / APS (زمان‌بندی با ظرفیت محدود):** assign jobs/operations to eligible equipment and shifts, respecting skills, tooling, route precedence, setup/changeover, maintenance, due date, line availability and material constraints. This is different from mere due-date sorting.

**Dispatch / shop-floor control:** choose what job OP runs NEXT on a particular machine, based on current real constraints. Can work even in an unscheduled shop with dispatch heuristics.

**Execution / MES:** record what ACTUALLY happened, even when plans failed, were canceled or were never created.

**Rescheduling:** after a new urgent order, fault, staff absence, shortage or order revision, propose changes. Record baseline, reason, constraints, affected jobs and approval; don't rewrite historical plan vs actual reports. Avoid automatic reassignments that surprise operators.

### Two different scheduler logics, common kernel

**Flexible CNC/job shop:** jobs are routed through alternate machines; setup time/sequence, skills and fixtures matter. Possible priority choices (illustrative): earliest due date, least slack, shortest processing time, minimal setups, weighted tardiness. No one heuristic is always best.

**Packaging/bottling line:** synchronized equipment, product family/campaign, bottleneck, speed compatibility, sanitation/cleaning and changeovers, buffer capacity and recipe/quality holds matter. Line scheduling and resource eligibility are not represented faithfully by pretending each filler/labeler is an independent job-shop machine.

Keep **orders, plans, assignments and actual events separate**. Expose multiple levels of planning complexity as optional modules:
- L0: no plan — manual/IoT observations only.
- L1: target/shift quantity or simple daily work list, editable.
- L2: order-linked jobs/routes and assignments; rudimentary capacity overview.
- L3: MPS/material needs and stock-aware capacity planning, with versioned plans.
- L4: constraint-based multi-resource APS, scenario comparisons and replanning; human approval.
This is **an illustrative adoption ladder, not hardcoded subscription tiers**.

### Does scheduling require AI?

No. Deterministic rules, SQL-based priority queues and optimization/constraint-solving may produce auditable feasible plans; using an LLM to directly decide machine dispatch is neither necessary nor automatically safer/better. AI can explain options, forecast demand, suggest bottleneck investigations or prepare scenario summaries, with traceable assumptions and human approval. Validate performance against real shop scenarios.

## 25. Warehouse, inventory, materials and logistics require their own business semantics

A company can choose NONE, minimal stock reference, external ERP integration or integrated inventory/WMS capabilities. The core MES/monitoring must work without forcing warehouse setup.

### Model candidates (not final DB schema)
- Item/material/SKU and unit of measure, conversions and version; raw, intermediate/WIP, finished, spare, consumable, packaging, tool as distinct material roles where relevant.
- Product/part specification and effective-dated BOM/recipe; lot/batch/serial genealogy level selectable (not every piece needs serialization).
- Facility, warehouse, location/bin, work center buffers, vendor/customer/subcontractor locations.
- Stock movement / inventory transaction: receipt, issue to job, consumption, produced output, return, transfer, rework, scrap, adjustment and shipment. Event timestamp, source, approval and document link.
- Availability buckets: on-hand, reserved, allocated, quality hold/quarantined, blocked, in transit, expected and available-to-promise; do NOT treat all as interchangeable physical counts.
- Material ownership **vs** physical custody: customer-owned material at Pouyeshgar, shop-owned purchased stock, consignment, external subcontractor custody and customer returns may require separate tracking and permissions.
- In-process tracking: WIP quantity by OP, lot/container, source, destination, losses and rework; make granularity tenant/product-specific.
- Procurement request/PO, supplier lead times and open receipts where purchasing module enabled; otherwise import availability from ERP.
- Outbound logistics: shipment, packing units/cartons/pallets, carrier, dispatch, receipt/proof of delivery, returns/recalls when applicable; avoid promising transport-management features as part of basic monitoring.
- Materials planning should never consume ERP stock snapshots as if they were precise real-time balances when data freshness and correction rules are unknown.

### Story 1: Pouyeshgar service machining
Customer supplies 200 blanks for operation OP-A. They are *physically received* at Pouyeshgar but may remain legally customer-owned. Work happens in several batches; 160 proceed to OP-B, 10 are rejected/held, 30 remain as WIP (illustrative only). Shipment of 150 good parts need not imply 150 materials purchased by Pouyeshgar. Without an inventory module, preserve the minimum provenance and count events; with optional material tracking, reconcile ownership, custody, source lot, transformations, scrap and shipments. **Do not infer the specific scrap/weight settlement logic from a generic inventory model**; this is the separate ERP project's specialized domain and requires explicit integration/approval.

### Story 2: Juice bottling business
Concentrate, water, bottles, caps, labels and cartons have separate stocks, lots and supplier receipts. A batch/recipe consumes materials; the filling and packing line produces finished cases/pallets; QC may quarantine a lot. Shipment availability must reflect quality release and allocations; shelf life, traceability and recall capability may be essential. This scenario motivates item genealogy and logistics integration but does NOT make them mandatory for the simple CNC pilot.

### Story 3: Company with a separate ERP or warehouse application
ERP is system of record for purchase orders and stock. Smart Factory receives material-readiness and approved jobs via a versioned connector and reports actual quantities, WIP and downtime back. Avoid implementing a second conflicting financial inventory ledger. Support mapping, reconciliation and read-only mirroring, then define explicit responsibilities and sync direction for each entity.

### Inventory/logistics decisions to agree later
1. Which system owns item masters, stock balances, orders, purchasing and valuation for each customer?
2. Is inventory tracking merely counts at work centers or a full WMS/bin-level system?
3. Are ownership, custody and subcontracted materials required at MVP?
4. Granularity: aggregate quantity, lot/batch, serial, container, pallet? Regulatory and customer obligations differ.
5. How do material reservations, quality holds and released WIP affect APS and available-to-promise?
6. Should the platform perform purchasing and shipments, or only integrate with ERP/TMS/WMS?

**Do not build a comprehensive accounting-grade inventory or logistics system merely to make the pilot dashboard richer.** Build stable interfaces and add optional bounded modules only when validated.

## 26. Unifying processes without oversimplifying manufacturing

The reusable common layer should distinguish:
1. **Demand signal** (customer order / forecast / reorder / manual request).
2. **Planning proposal and approved plan** (MPS / order/job / schedule version; optional).
3. **Resource and process definition** (site, line, cell, equipment, people/skills, materials, recipe/BOM, route/OP graph, capabilities).
4. **Work execution instance** (job-operation or line/batch/run; may be unscheduled).
5. **Observation/event** (counts, machine state, stop, alarm, inspection, inventory movement, personnel assignment), with provenance, event time and correction/audit.
6. **Operational result** (good output, scrap, WIP, downtime, performance and delivery progress).
7. **Derived metrics and decisions** (KPI, forecast error, bottleneck, plans, recommendations) with source periods, definitions and access controls.

An OPTIONAL feature consumes shared data and contributes new semantics. Missing data is not a valid zero. An enabled planning module does not retroactively turn previous anonymous counted production into planned orders. A customer's configuration may mix manual stop codes, IoT counters, Excel BOM, ERP stock and an external scheduling algorithm in the same operational period.

### Architectural boundary proposal
- Core: tenant/security/audit, site/resources, time and sources, typed events, ID mapping, API and metric query primitives.
- Manufacturing operations: equipment/line modes, stops/alarms, manual jobs/OP, shift people assignments, traceability as needed.
- Planning domain: demand, forecast versions, order lifecycle, MPS, dispatch, constraint scheduler; no direct hardwired PLC control.
- Materials/stock domain: optional inventory/WIP/purchasing/logistics bounded module or connector with a declared system of record.
- Quality and CMMS: independently enabled and optionally enrich operation outcome and state.
- Analytics/AI layer: read governed snapshots/metrics; never act as authoritative source of facts.
This is a candidate modular-monolith decomposition to be validated against the actual implementation; do not force multiple network microservices prematurely.

## 27. Standards and international ecosystem — careful, source-grounded mapping

There is **no single international standard for building the complete app**. Standards provide complementary domain vocabulary, boundaries and interchange models, NOT an out-of-the-box user experience or a ready-to-code universal data model. Some are paywalled; inspect licenses, current editions and constraints before incorporating exact schemas.

| Reference | What it contributes | What it does NOT guarantee |
|---|---|---|
| **ISA-95 / IEC 62264** | Logical manufacturing operations vs enterprise planning/integration boundary; equipment/material/personnel/operations concepts and interfaces, applicable to discrete, batch and continuous industries | A complete custom ERP, shop dispatch scheduler, IoT firmware protocol or finished UI |
| **ISA-88 / IEC 61512** | Batch control, recipes, procedural models and equipment/physical model, especially food, beverage, chemical and pharmaceutical batch contexts | A mandatory recipe model for every CNC order or a universal serial-tracking solution |
| **ISO 22400** | Industry-neutral manufacturing KPI terminology and composition concepts | Automatic valid OEE without trustworthy input definitions, time policies and company data |
| **ASCM SCOR Digital Standard** | Common supply-chain process map: Orchestrate, Plan, Order, Source, Transform, Fulfill, Return; business performance/flows | A purchasable logistics module or one mandatory workflow for every small business |
| **GS1 EPCIS / CBV** | Event vocabulary and interoperable what/when/where/why traceability across partners and physical flows, where relevant | Requirement that every tenant use barcodes, GTINs, pallet serialization or EPCIS API |
| **MESA B2MML (based on ISA-95)** | Existing XML interface schemas that can inform business/manufacturing integration, possible external compatibility | That every internal entity must be stored as raw B2MML, or that a generic JSON conversion is automatically validated |
| **ISO 9001** | Quality/process records, traceability and process improvement perspectives when in scope | Certified compliance simply by shipping a software feature |
| **IEC 62443** | Security requirements and risk/control framework relevant to industrial system connectivity | Proof of cybersecurity merely because roles/login exist |

Primary official references (verify current editions during implementation):
- ISA-95: https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard
- ISA-88: https://www.isa.org/standards-and-publications/isa-standards/isa-88-standards
- ISO 22400: https://www.iso.org/standard/56847.html (validate accessible catalog URL/edition)
- ASCM SCOR DS: https://www.ascm.org/corporate-solutions/standards-tools/scor-ds/
- GS1 EPCIS: https://www.gs1.org/standards/epcis
- MESA B2MML: https://github.com/MESAInternational/B2MML-BatchML

**Mapping policy:** Each future module specification should have a \`Standards & vocabulary\` section listing applicable reference, exact standard/edition where reviewed, mapped concepts, departures and unresolved differences. Never claim standards-compliant, certified or vendor-compatible without conformance evidence. Commercial-scale adoption also requires tested tenant isolation, performance, failover, on-premise/edge reliability, cyber security, data retention, multisite governance, change control and support.

## 28. Concrete acceptance scenarios for future development (not yet tests)

The following are contract tests to WRITE and implement as modules mature; this does NOT claim they currently pass:

1. **Basic manual customer**: New tenant enables only Monitoring + manual production and stoppage entry. Adds three machines with no IoT, no quality/ERP/BOM/orders. Operator records a shift's units and 35-minute stop. Manager filters selected shift; report and Excel export show facts, actor, source and times. No irrelevant menu blocks onboarding.
2. **OEE-only customer**: Supplies planned production time, ideal cycle and good/total quantities manually or through import. Standard OEE yields transparent A/P/Q with traceable inputs; remove quality count, and the display becomes 'insufficient data', not a fabricated percentage.
3. **Pouyeshgar volatile order**: Work begins from phone request without formal plan. After an order arrives, supervisor links execution to new order version; customer changes due date; old realized counts and historical commitments remain queryable, no retroactive corruption.
4. **Mixed-source equipment**: IoT counter samples every minute, operator adds a coded stop reason later, QC sends Excel checks nightly, one PLC alarm arrives immediately. Time-window report reconciles sources and marks updates/delays; duplicates don't inflate counts.
5. **Forecast-driven packaging**: Forecast of bottles and confirmed orders in same week feed one demand reconciliation rule, no double count. MPS proposal considers usable inventory and safety stock; plan not silently assumed executable until BOM/material availability and line capacity validation.
6. **Multi-shift change**: Operator changes machine mid-shift; three 8-hour shifts cover midnight; actual attendance differs from roster. Each historical query uses relevant effective interval and time zone without attributing production to the wrong shift/person.
7. **Warehouse/QC hold**: Finished lot quarantined by QC cannot be counted as freely available for shipment; stock and plan reflect hold, with traceable override authorization when appropriate.
8. **Line vs job-shop**: Continuous line and flexible job-shop use distinct planning/control strategies but common event provenance, effective time, scoped reports and tenant-independent software.
9. **Permissions and tenants**: Disabled planning doesn't expose APIs or phantom schedule cards; unauthorised worker cannot call QC/admin; tenant A cannot read tenant B through reports, exports, websockets or integration credentials.
10. **Interoperability**: External inventory master via secured read-only connector, production output via permissioned API/Excel, Grafana consumer only sees approved tenant/site metrics with source and calculation version.

## 29. Scope discipline and delivery sequence (architectural vision ≠ current release)

The user wants one coherent environment, but **that does not mean building full ERP + APS + WMS + MES + SCADA + CMMS + AI simultaneously**. Doing so without deeply validated semantics would jeopardize accuracy and time-to-value.

Recommended order, subject to user approval:
1. Finish current Codex Phase-2 QA; preserve its tested interactive UI and 3D behavior. Evaluate final report, branch, migrations and tested DB reality.
2. Reconcile contradictory existing docs, separating historical decisions vs current contract; keep this product blueprint canonical but no unreviewed merge into the in-progress branch.
3. Establish minimal tenant/source/time/equipment/shift/permissions/event models; test one manual and one Edge Simulator data path for same machine.
4. Enter one realistic Pouyeshgar production case with changeable ad-hoc OP, operator assignment, manual stop cause, useful date-range report; make optional fields explicit.
5. Add configuration of module visibility/readiness and precise metric prerequisites before providing OEE claims.
6. Define and test orders vs forecast vs replenishment conceptually with miniature sample datasets, version and audit; **do not add a full APS yet**.
7. Decide whether materials and warehouses are an external ERP integration, an optional native ledger, or merely manual availability indicators. Build only the selected path.
8. Validate a fixed production-line scenario against chosen process model. Then extend scheduling, quality, CMMS, logistic/traceability and optional AI in well-defined milestones.

**Gates for implementation:**
- No irreversible schema design for order/forecast/inventory ownership before owner reviews example flows and exceptions.
- No silent assumptions about manufacturer-specific stock, legal ownership, cycle time, scrap, quality, forecast consumption or due-date policy.
- No fabricated "live" values where sources are manual or delayed.
- No new UI overhaul if the current result is substantially approved.
- Any next Codex prompt must cite this chapter and a specific validated vertical slice; don't issue a single large scope-expanding task while Codex is actively editing.

## 30. Plain-language recap for fresh ChatGPT/Codex sessions / خلاصهٔ فهم مسئله

**User's intended outcome, not a coding order:**

«می‌خواهیم از پویشگر شروع کنیم، ولی نرم‌افزار را محدود به کارگاه CNC نسازیم. یک مشتری شاید فقط تعداد تولید، توقفات و گزارش روزانهٔ کارگر را بخواهد؛ دیگری فقط OEE؛ دیگری برنامهٔ سفارش‌محور داشته باشد؛ و شرکت بزرگ‌تر براساس پیش‌بینی تقاضا، موجودی، مواد اولیه، ظرفیت خط، حمل‌ونقل و سفارش مشتری برنامه‌ریزی کند. داده ممکن است دستی، اکسل، API، EdgeBox، PLC یا مخلوطی از آنها باشد. ممکن است هیچ برنامهٔ تولید مصوبی وجود نداشته باشد و برنامهٔ کارگاه هر روز تغییر کند. نباید مشتری را مجبور به خرید و تعریف تمام ماژول‌ها کنیم. اطلاعات واقعی، فرضیات، پیش‌بینی، برنامه و خروجی اندازه‌گیری باید همیشه از هم جدا باشند. می‌خواهیم از اصطلاحات و چارچوب‌های جهانی مثل ISA-95، ISA-88، ISO 22400، SCOR و GS1 در جای درست الهام بگیریم و همهٔ این مسیرها را در محیطی یکپارچه و قابل رشد به هم متصل کنیم. اما الآن نمی‌خواهیم همهٔ ERP و لجستیک را یک‌جا بسازیم؛ باید اول مدل و گردش‌های واقعی را توافق کنیم و بعد هر بخش را با مثال، اعتبارسنجی و تست پیاده کنیم.»

**Key distinction:** Order-based vs forecast-based is an attribute of DEMAND and PLANNING policy; it must NOT constrain whether ACTUAL PRODUCTION can be recorded. Inventory and logistics can be external service connectors or native optional domains. Integration standards guide concepts; they do not magically solve all factory-specific semantics.

**Current reference:** این فایل در docs/PRODUCT-BLUEPRINT.md همین شاخه است؛ مسیر docs/platform-product-blueprint و دستور انتظار برای سشن‌های قدیمی، فقط سابقهٔ پیش از تجمیع بودند. برای کار تازه ابتدا START-HERE و بخش موضوعی مرتبط را بخوانید؛ وضعیت ساخته‌شده در CURRENT-STATE است.

**Current next step:** طبق جهت ۲۰۲۶-۱۰-۲۸، پاک‌سازی ساختار و سپس یک برش واقعی ثبت/گزارش تولید؛ ساخت تمام قابلیت‌های این چشم‌انداز یک‌جا مجاز نیست.
