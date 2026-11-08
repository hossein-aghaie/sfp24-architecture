# مطالعهٔ الگوهای توسعه‌پذیری ماژول، نصب، ارتباط و محیط‌های کاری در SFP24

> **وضعیت سند:** تحقیق و جمع‌بندی شواهد؛ نه ADR، نه قرارداد مصوب و نه مجوز پیاده‌سازی  
> **تاریخ بررسی منابع بیرونی:** ۲۰۲۶-۱۱-۰۸  
> **دامنه:** معماری ماژول‌ها، بسته‌بندی و چرخهٔ عمر، فناوری Backend/Frontend، ارتباط بین‌ماژولی، داشبوردها و میزهای کار  
> **روش:** مطالعهٔ مستندات رسمی سازندگان + تطبیق با اسناد معماری SFP24 و نمونهٔ کد مشخص‌شده در این سند؛ بدون نصب و آزمون عملی محصولات بیرونی
>
> **راهنمای بصری:** نمودارها با Mermaid نوشته شده‌اند تا GitHub آن‌ها را رندر کند و متنشان قابل ویرایش بماند. پیوندهای رسمی نیز به صفحات مستندات دارای تصویر و جزئیات همان نسخه می‌رسند.

## فهرست مطالب

- [۱. خلاصهٔ اجرایی](#۱-خلاصهٔ-اجرایی)
- [۲. واژه‌ها را از هم جدا کنیم](#۲-واژهها-را-از-هم-جدا-کنیم)
- [۳. چهار الگوی فنی متفاوت](#۳-چهار-الگوی-فنی-متفاوت)
- [۴. نمونه‌های بررسی‌شده و چیزی که واقعاً از آن‌ها می‌آموزیم](#۴-نمونههای-بررسیشده-و-چیزی-که-واقعاً-از-آنها-میآموزیم)
- [۵. آیا فناوری همهٔ ماژول‌ها باید یکی باشد؟](#۵-آیا-فناوری-همهٔ-ماژولها-باید-یکی-باشد)
- [۶. ثبت، نصب، فعال‌سازی و حذف ماژول دقیقاً چه هستند؟](#۶-ثبت-نصب-فعالسازی-و-حذف-ماژول-دقیقاً-چه-هستند)
- [۷. ارتباط بین ماژول‌ها](#۷-ارتباط-بین-ماژولها)
- [۸. داشبوردها، میزکارها و اتصال آن‌ها به ماژول‌ها](#۸-داشبوردها-میزکارها-و-اتصال-آنها-به-ماژولها)
- [۹. نقش Developer Admin و Company Admin](#۹-نقش-developer-admin-و-company-admin)
- [۱۰. خاموش‌کردن، ارتقا و بازنشستگی ماژول](#۱۰-خاموشکردن-ارتقا-و-بازنشستگی-ماژول)
- [۱۱. تطبیق با وضعیت واقعی SFP24](#۱۱-تطبیق-با-وضعیت-واقعی-sfp24)
- [۱۲. پیشنهاد مرحله‌بندی‌شده برای SFP24](#section-stage-plan)
- [۱۳. پرسش‌هایی که هنوز تصمیم می‌خواهند](#۱۳-پرسشهایی-که-هنوز-تصمیم-میخواهند)
- [۱۴. روش تحقیق و محدودیت شواهد](#۱۴-روش-تحقیق-و-محدودیت-شواهد)
- [۱۵. منابع](#۱۵-منابع)

---

## ۱. خلاصهٔ اجرایی

### نتیجه در یک نگاه

برای SFP24 لازم نیست همه‌چیز را از ابتدا اختراع کنیم؛ اما نباید معماری یک محصول دیگر را هم عیناً کپی کنیم. چهار نمونه، چهار مسئلهٔ متفاوت را خوب نشان می‌دهند:

| نمونه | مسئله‌ای که برای ما روشن می‌کند | الگویی که ارزش مطالعه دارد |
|---|---|---|
| Ignition | افزونهٔ واقعی چگونه داخل یک پلتفرم بارگذاری و مدیریت می‌شود؟ | بستهٔ ماژول، Manifest، سازگاری نسخه و محدودهٔ اجرا |
| Odoo | قابلیت‌های کسب‌وکاری چگونه به ماژول‌های وابسته و مستقل تقسیم می‌شوند؟ | Manifest، وابستگی، داده، دسترسی و ماژول واسط |
| Siemens Industrial Edge | برنامه‌ای با فناوری و Runtime مستقل چگونه منتشر و مستقر می‌شود؟ | Image، Container، بستهٔ استقرار و مدیریت نسخه |
| ThingsBoard | داشبورد چگونه از Widgetهای قابل استفادهٔ مجدد ساخته می‌شود؟ | Widget، Bundle، Alias، Context و چیدمان |

**پیشنهاد این تحقیق، نه تصمیم مصوب:** مرحلهٔ نخست SFP24 به‌صورت یک Modular Monolith مورد اعتماد باقی بماند؛ ماژول‌ها در Build مشترک حضور داشته باشند، قراردادهای روشن داشته باشند و برای هر شرکت جداگانه فعال یا غیرفعال شوند. بعد از آزمودن این مدل با چند ماژول واقعی، فقط سرویس‌هایی را مستقل کنیم که نیاز فنی مستند دارند.

در نتیجه:

- ماژول در نسخهٔ اول نباید به معنی «هر کسی یک فایل JavaScript بارگذاری کند» باشد.
- ثبت ماژول با نصب بسته، فعال‌سازی برای شرکت و دادن مجوز به شخص یکی نیست.
- Backend و Frontend ماژول مجبور نیستند یک زبان داشته باشند؛ ولی اتصال به Host باید قرارداد و Runtime سازگار داشته باشد.
- داشبورد نباید مالک منطق تخصصی ماژول شود؛ ماژول قابلیت و Widget را عرضه می‌کند و Host آن را در میز یا داشبورد مناسب قرار می‌دهد.
- ارتباط ماژول‌ها باید از Port/API یا Event نسخه‌دار عبور کند، نه از خواندن و نوشتن مستقیم جدول‌های یکدیگر.

### تصویر کلی معماری پیشنهادی

نمودار زیر یک **مدل هدف پیشنهادی** است؛ توصیف Runtime فعلی نیست.

~~~mermaid
flowchart TB
    subgraph CORE["Core / Host"]
      ID["هویت، شرکت، Tenant و Scope"]
      SEC["مجوز، Entitlement و سیاست دسترسی"]
      REG["Module Registry و بررسی سازگاری"]
      UI["UI Host و Workspace Runtime"]
      MSG["Port / Event / Task Infrastructure"]
    end

    subgraph MODS["Domain Modules"]
      PR["Production"]
      MT["Maintenance"]
      QL["Quality"]
      TR["Training"]
      OE["OEE"]
    end

    subgraph UX["سطوح تجربه"]
      WB["Workbench / میزکار"]
      DB["Dashboard / داشبورد"]
      PF["Entity Profile / پروفایل"]
      PG["Full Page / صفحه تخصصی"]
      V3["3D Context / نمای سه‌بعدی"]
    end

    REG --> PR
    REG --> MT
    REG --> QL
    REG --> TR
    REG --> OE
    SEC --> REG
    ID --> SEC
    PR --> MSG
    MT --> MSG
    QL --> MSG
    TR --> MSG
    OE --> MSG
    UI --> WB
    UI --> DB
    UI --> PF
    UI --> PG
    UI --> V3
    MODS --> UI
~~~

در این مدل، Core صاحب هویت، امنیت و میزبان رابط است؛ ماژول صاحب منطق و دادهٔ تخصصی خودش است؛ و میزکار محل ترکیب قابلیت‌ها برای کاربر است.

---

## ۲. واژه‌ها را از هم جدا کنیم

بخش زیادی از ابهام «ماژول را به هسته اضافه کنیم» از قاطی‌کردن چند مفهوم جدا به وجود می‌آید.

| اصطلاح | معنی ساده | مثال |
|---|---|---|
| Source Code | کد قابل ویرایش برنامه‌نویس | فایل‌های TypeScript، Vue یا Python |
| Build Artifact / Package | خروجی ساخته‌شده و آمادهٔ استقرار | فایل .modl، بستهٔ برنامه یا Imageهای Container |
| Manifest | شناسنامه و قرارداد اعلامی ماژول | شناسه، نسخه، وابستگی، سازگاری و قابلیت‌ها |
| Registry | فهرست ماژول‌های شناخته‌شده و نقاط اتصال آن‌ها | Host می‌داند ماژول چه قابلیت‌هایی عرضه می‌کند |
| Register | معرفی/ثبت ماژول در رجیستری Host | ثبت Descriptor و Contribution |
| Install | آماده‌کردن ماژول در محیط اجرا و منابع لازم | نصب بسته، آماده‌سازی Schema و تنظیمات |
| Deploy | انتشار نسخه روی محیط مشخص | استقرار نسخه روی سرور یا Edge Device |
| Entitlement | حق استفادهٔ یک شرکت از ماژول | شرکت مجاز به استفاده از Maintenance است |
| Enable | فعال‌کردن قابلیت برای یک شرکت | Maintenance در شرکت فعال شود |
| Permission | اجازهٔ یک شخص برای انجام عملیات | تکنسین اجازهٔ ثبت نتیجهٔ تعمیر داشته باشد |
| UI Contribution | قابلیتی که ماژول برای رابط Host عرضه می‌کند | فرم، Widget، صفحه یا بخش پروفایل |
| Unregister | خارج‌کردن تعریف ماژول از رجیستری | Host دیگر آن نسخه را برای استفاده عرضه نکند |
| Retire | بازنشسته‌کردن نسخه یا ماژول | انتشار جدید متوقف شود، اما سوابق حفظ شوند |

### یک مثال ساده

فرض کن ماژول تعمیرات را ساخته‌ایم:

1. برنامه‌نویس کد تعمیرات را در مخزن Git می‌نویسد.
2. Build، کد و منابع لازم را برای Runtime آماده می‌کند.
3. Manifest می‌گوید این ماژول چیست، چه نسخه‌ای دارد و چه قابلیت‌هایی عرضه می‌کند.
4. Registry ماژول را می‌شناسد و نقاط اتصالش را اعتبارسنجی می‌کند.
5. نسخهٔ ماژول روی محیط محصول Deploy می‌شود.
6. شرکت مجوز استفاده از آن را دارد و ماژول برای شرکت Enable می‌شود.
7. مدیر شرکت مجوزهای لازم را به تکنسین‌ها می‌دهد.
8. Host فرم و Widgetهای مجاز را در میزکار مناسب نمایش می‌دهد.

**نکته:** ثبت نام ماژول در Registry به‌تنهایی کد آن را نصب نمی‌کند، جدول‌های دیتابیس را نمی‌سازد، UI را اجرا نمی‌کند و مجوز کاربر صادر نمی‌کند.

---

## ۳. چهار الگوی فنی متفاوت

ماژولار بودن فقط یک شکل اجرایی ندارد. باید نوع استقلال را انتخاب کنیم.

### الگوی A — افزونهٔ داخل همان Runtime (In-process Plugin)

کد ماژول داخل محیط اجرای پلتفرم بارگذاری می‌شود و مستقیماً از APIهای Host استفاده می‌کند.

~~~mermaid
flowchart TB
    H["Host Runtime"]
    R["Module Registry"]
    A["Module A"]
    B["Module B"]
    C["Module C"]
    H --> R
    R --> A
    R --> B
    R --> C
    A --> H
    B --> H
    C --> H
~~~

**مزیت‌ها**
- ارتباط سریع و مستقیم با سرویس‌های Host.
- هزینهٔ کمتر برای فراخوانی بین فرایندها.
- امکان ارائهٔ قابلیت‌های عمیق در رابط و سرویس‌های پلتفرم.

**هزینه‌ها و ریسک‌ها**
- وابستگی به Runtime و API نسخهٔ Host.
- خطای یک افزونه می‌تواند روی فرایند Host اثر بگذارد.
- ایزوله‌کردن نسخه‌های متفاوت در یک فرایند دشوارتر است.
- اعتماد و امضای کد اهمیت زیادی پیدا می‌کند.

**نمونهٔ مرجع:** Ignition.

### الگوی B — ماژول کسب‌وکاری در Modular Monolith

ماژول‌ها مرز دامنه‌ای و کد مشخص دارند، اما در یک برنامه و Build مشترک منتشر می‌شوند.

~~~mermaid
flowchart TB
    BUILD["یک Build و یک نسخهٔ Host"]
    subgraph APP["یک برنامهٔ اجرایی"]
      CORE["Core Services"]
      P["Production Domain"]
      M["Maintenance Domain"]
      Q["Quality Domain"]
      UI["Shared UI Host"]
    end
    BUILD --> APP
    CORE <--> P
    CORE <--> M
    CORE <--> Q
    P --> UI
    M --> UI
    Q --> UI
~~~

**مزیت‌ها**
- توسعه و انتشار ساده‌تر در دورهٔ بلوغ اولیه.
- مرز مسئولیت ماژول‌ها می‌تواند مستقل بماند.
- تراکنش و تست یکپارچه ساده‌تر از چند سرویس مستقل است.

**محدودیت‌ها**
- Build و انتشار معمولاً مشترک‌اند.
- استقلال Runtime و نسخهٔ هر ماژول محدود است.
- جدایی کد به‌تنهایی امنیت یا جدایی داده را تضمین نمی‌کند.

**این الگو با معماری مستندشدهٔ فعلی SFP24 نزدیک است.** [معماری موجود](../core/ARCHITECTURE.fa.md) برنامه را Modular Monolith توصیف می‌کند و تصریح می‌کند Plugin Engine عمومی نداریم.

### الگوی C — سرویس مستقل (Out-of-process Service)

ماژول در فرایند و احتمالاً Container جداگانه اجرا می‌شود و از API یا Event با Host ارتباط می‌گیرد.

~~~mermaid
flowchart LR
    HOST["SFP24 Host"]
    API["API / Event Contract"]
    SVC["Maintenance Service"]
    DB["Maintenance Storage"]
    HOST <--> API
    API <--> SVC
    SVC --> DB
~~~

**مزیت‌ها**
- امکان انتخاب فناوری مستقل.
- امکان مقیاس‌دهی و استقرار جداگانه.
- خرابی یا ارتقای سرویس می‌تواند تا حدی از Host جدا شود.

**هزینه‌ها**
- شبکه، احراز هویت سرویس‌به‌سرویس و مدیریت خطا.
- سازگاری نسخهٔ پیام‌ها و API.
- پایش، استقرار، پشتیبان‌گیری و عملیات بیشتر.
- تراکنش بین چند سرویس ساده و اتمیک نیست.

**نمونهٔ مرجع:** برنامه‌های مستقل Industrial Edge.

### الگوی D — رابط مستقل یا Microfrontend

رابط ماژول در بسته یا برنامهٔ جداگانه ساخته می‌شود و در Host نمایش داده می‌شود.

راه‌های فنی ممکن شامل Web Components، iframe یا سامانه‌های Microfrontend هستند. هرکدام هزینهٔ خاص خود را دارند؛ انتخاب هیچ‌کدام در این تحقیق تصویب نشده است.

**نکته:** مستقل‌بودن Frontend لزوماً به معنی مستقل‌بودن Backend نیست و برعکس.

### مقایسهٔ چهار الگو

| معیار | In-process Plugin | Modular Monolith | سرویس مستقل | Microfrontend |
|---|---|---|---|---|
| جدایی Runtime | کم | کم | زیاد | فقط رابط |
| آزادی فناوری Backend | محدود | محدود/متناسب با Host | زیاد | مستقل از Backend |
| آزادی فناوری Frontend | تابع Host | تابع Host | مستقل از Backend | زیادتر |
| انتشار مستقل | وابسته به Host | معمولاً خیر | بله | معمولاً بله |
| پیچیدگی عملیات | متوسط | کم تا متوسط | زیاد | متوسط تا زیاد |
| ایزولاسیون خرابی | محدود | محدود | بهتر، نه مطلق | محدود به رابط |
| تناسب با مرحلهٔ اول SFP24 | نیازمند SDK و امنیت | **بیشترین تناسب** | فقط برای نیاز مشخص | فعلاً زودهنگام |

---

## ۴. نمونه‌های بررسی‌شده و چیزی که واقعاً از آن‌ها می‌آموزیم

این چهار محصول از نظر بازار و کاربرد هم‌رده نیستند. مقایسهٔ زیر، مقایسهٔ **الگوی فنی مستندشده** است، نه رتبه‌بندی کیفیت یا هزینه.

### ۴.۱. Ignition — افزونهٔ واقعی داخل پلتفرم

**مستندات بررسی‌شده:** Ignition 8.3 User Manual و Ignition SDK Programmer's Guide.

در Ignition، ماژول‌ها قابلیت‌های پلتفرم را گسترش می‌دهند. ماژول می‌تواند بخش‌هایی برای Gateway، Designer و Client داشته باشد. این محدوده‌ها نقش‌های اجرایی متفاوتی دارند.

طبق راهنمای SDK نسخهٔ 8.1، فایل .modl یک بستهٔ ZIP است که کد کامپایل‌شدهٔ JAR و فایل Manifest/Descriptor را در بر می‌گیرد. راهنمای 8.3 نصب و مدیریت ماژول را از Gateway توضیح می‌دهد. چون راهنمای ساختی که بررسی شد متعلق به SDK 8.1 است، جزئیات بسته‌بندی آن را نباید بدون تطبیق با SDK نسخهٔ 8.3 به‌عنوان مشخصات قطعی نسخهٔ جدید تلقی کرد.

**چیزی که از آن یاد می‌گیریم:**
- ماژول باید شناسه، نسخه و شناسنامهٔ معتبر داشته باشد.
- نقاط اجرای ماژول باید معلوم باشند.
- سازگاری با نسخهٔ Host مهم است.
- نصب، ارتقا، Enable، Disable و Uninstall عملیات مجزا هستند.
- نصب یا حذف در محیط عملیاتی ممکن است به Restart یا پنجرهٔ نگهداری نیاز داشته باشد.
- امضا و اصالت ماژول بخشی از مدل اعتماد است.

**چیزی که نباید کورکورانه کپی کنیم:** زبان Java، ساختار Gateway یا الزام به بارگذاری همهٔ ماژول‌ها در یک فرایند.

منابع رسمی: [Ignition Platform](https://docs.inductiveautomation.com/docs/8.3/platform) · [Modules Overview](https://docs.inductiveautomation.com/docs/8.3/getting-started/modules-overview) · [Install / Upgrade / Disable / Uninstall](https://www.docs.inductiveautomation.com/docs/8.3/getting-started/installing-and-upgrading/installing-or-upgrading-a-module) · [SDK: Anatomy of a Module](https://www.sdk-docs.inductiveautomation.com/docs/getting-started/anatomy-of-a-module/) · [SDK: Build a Module](https://www.sdk-docs.inductiveautomation.com/docs/getting-started/create-a-module/build-a-module/) · [SDK: Scopes, Hooks and Contexts](https://www.sdk-docs.inductiveautomation.com/docs/getting-started/anatomy-of-a-module/scopes-hooks-contexts/).

### ۴.۲. Odoo — ماژول کسب‌وکاری، وابستگی و ماژول واسط

**مستندات بررسی‌شده:** Odoo 19.0.

در Odoo یک ماژول معمولاً یک بسته/پوشهٔ نرم‌افزاری است که می‌تواند شامل این موارد باشد:

- مدل‌های Python و منطق Backend
- فایل‌های XML یا CSV برای داده، View، Menu و تنظیمات
- تعریف دسترسی‌ها و Record Ruleها
- Controllerها
- فایل‌های JavaScript، CSS و تصاویر رابط
- Manifest برای معرفی ماژول و وابستگی‌ها

فایل __manifest__.py اطلاعاتی مثل نام، نسخه، وابستگی‌ها، فایل‌های داده، Assetها و Hookهای نصب/حذف را اعلام می‌کند. این ساختار نشان می‌دهد که «ماژول» الزاماً یک فایل باینری واحد نیست؛ ممکن است یک بستهٔ کد و منابع باشد که پلتفرم آن را می‌شناسد و نصب می‌کند.

#### نمونهٔ ارزشمند: ماژول واسط

در مستندات رسمی Odoo، sale_crm نمونه‌ای از یک ماژول Link است که به دو ماژول sale و crm وابسته است و می‌تواند با فعال‌شدن وابستگی‌هایش نصب شود.

~~~mermaid
flowchart LR
    SALE["Sales"]
    CRM["CRM"]
    LINK["sale_crm Integration Module"]
    SALE --> LINK
    CRM --> LINK
    LINK --> RESULT["هماهنگی CRM و سفارش فروش"]
~~~

این الگو برای SFP24 مفید است: Production و Maintenance می‌توانند مستقل بمانند و یک Integration Module مسئول اتصال گردش خاص بین آن‌ها شود.

#### هشدار مهم دربارهٔ Uninstall

راهنمای Odoo هشدار می‌دهد حذف یک App می‌تواند رکوردهای دیتابیس آن را حذف کند و حتی به دلیل وابستگی‌ها، چند ماژول را با هم از نصب خارج کند. این رفتار برای سوابق تولید، تعمیرات، کیفیت و شواهد ممیزی SFP24 نباید بدون سیاست روشن حفظ داده کپی شود.

**چیزی که از آن یاد می‌گیریم:**
- Manifest و Dependency باید صریح باشند.
- ماژول واسط می‌تواند وابستگی بین دو دامنه را مدیریت کند.
- داده، UI و مجوز می‌توانند بخشی از بستهٔ ماژول باشند.
- حذف ماژول ممکن است اثر آبشاری داشته باشد؛ باید قبل از اجرا اثر آن معلوم شود.

منابع رسمی: [Module Manifests](https://www.odoo.com/documentation/19.0/developer/reference/backend/module.html) · [Building a Module](https://www.odoo.com/documentation/19.0/developer/tutorials/backend.html) · [Data Files](https://www.odoo.com/documentation/19.0/developer/reference/backend/data.html) · [Install, Upgrade and Uninstall Apps](https://www.odoo.com/documentation/19.0/applications/general/apps_modules.html).

### ۴.۳. Siemens Industrial Edge — برنامهٔ مستقل و بستهٔ استقرار

**مستندات بررسی‌شده:** Industrial Edge Platform v26.09.

در این الگو، برنامهٔ Edge می‌تواند چند Container داشته باشد. بستهٔ نمونهٔ Siemens شامل فایل‌های Docker Compose و پوشه‌های سرویس است. در مثال رسمی، سرویس تحلیل داده با Python و Dockerfile ساخته می‌شود. Imageها ساخته می‌شوند و App Publisher بستهٔ برنامه را برای Industrial Edge Management آماده و ارسال می‌کند.

~~~mermaid
flowchart TB
    SRC["Source Code"]
    BUILD["Build هر Container"]
    IMG["Container Images"]
    COMPOSE["docker-compose.yml"]
    PUB["Industrial Edge App Publisher"]
    IEM["Industrial Edge Management"]
    DEV["Edge Device"]
    SRC --> BUILD
    BUILD --> IMG
    IMG --> PUB
    COMPOSE --> PUB
    PUB --> IEM
    IEM --> DEV
~~~

این مدل «افزونه‌ای که درون Host بارگذاری می‌شود» نیست؛ برنامه یا سرویس مستقلی است که روی محیط Edge مستقر می‌شود.

**چیزی که از آن یاد می‌گیریم:**
- کد، Image و بستهٔ استقرار مفاهیم جدا هستند.
- یک برنامه می‌تواند چند سرویس با فناوری‌های متفاوت داشته باشد.
- انتشار و استقرار باید نسخه‌دار و قابل کنترل باشد.
- ابزار Publisher و Management بخشی از چرخهٔ عمر هستند.

**کاربرد احتمالی برای SFP24:** سرویس‌های Edge، دریافت داده، پردازش صنعتی، تحلیل سنگین یا AI؛ نه الزاماً تمام ماژول‌های کسب‌وکاری.

منابع رسمی: [Description of the First Industrial Edge App — v26.09](https://docs.industrial-operations-x.siemens.cloud/r/en-us/v26.09/industrial-edge-platform-operation-develop-an-application/developer-guide/handson-exercise/description-of-the-hands-on-application/description-of-your-first-industrial-edge-app) · [Mission of the App Publisher](https://docs.industrial-operations-x.siemens.cloud/r/en-us/v26.06/industrial-edge-platform-operation-setup-operate-utilize/security/industrial-edge-components-security-measures/industrial-edge-app-publisher-security/mission-of-the-industrial-edge-app-publisher-and-impact-on-exposed-services) · [Upload an App with App Publisher — v26.09](https://docs.industrial-operations-x.siemens.cloud/r/en-us/v26.09/industrial-edge-platform-operation-develop-an-application/developer-guide/handson-exercise/upload-the-app-with-ie-app-publisher-to-ie-management).

### ۴.۴. ThingsBoard — Widgetهای قابل استفادهٔ مجدد و داشبورد ترکیبی

**مستندات بررسی‌شده:** ThingsBoard Community Edition documentation.

در ThingsBoard، داشبورد از Widgetها ساخته می‌شود. Widget می‌تواند نمودار، مقدار لحظه‌ای، جدول هشدار، کنترل یا محتوای سفارشی باشد. Widgetها در Bundleها گروه‌بندی می‌شوند و برای استفاده در داشبوردهای مختلف قابل انتخاب‌اند.

نکتهٔ فنی مهم، Alias است: Widget به‌جای اینکه همیشه به یک دستگاه ثابت متصل باشد، می‌تواند از Alias یا Context داشبورد، موجودیت فعلی را دریافت کند. مثلاً کاربر از فهرست ماشین‌ها یک دستگاه را انتخاب می‌کند و Widgetهای صفحهٔ جزئیات به‌صورت پویا همان دستگاه را نمایش می‌دهند.

~~~mermaid
flowchart TB
    DASH["Dashboard"]
    ALIAS["Entity Alias / Context"]
    W1["Widget: Status"]
    W2["Widget: Trend"]
    W3["Widget: Alarms"]
    SELECT["کاربر تجهیز را انتخاب می‌کند"]
    SELECT --> ALIAS
    ALIAS --> W1
    ALIAS --> W2
    ALIAS --> W3
    W1 --> DASH
    W2 --> DASH
    W3 --> DASH
~~~

**چیزی که از آن یاد می‌گیریم:**
- Widget باید قابل استفاده در چند چیدمان باشد.
- چیدمان داشبورد از منطق دادهٔ Widget جدا باشد.
- Context انتخابی مثل تجهیز، سایت و بازهٔ زمانی باید به Widget برسد.
- داشبورد می‌تواند از چند ماژول محتوا بگیرد.
- Widget کنترلی و Widget نمایشی باید از نظر Permission و رفتار Backend تفکیک شوند.

این مدل برای داشبوردهای تله‌متری و پایش صنعتی مرجع مفیدی است؛ اما به‌تنهایی جایگزین معماری کامل میزهای عملیاتی، مدیریت کار و گردش تأیید SFP24 نیست.

منابع رسمی: [Widgets](https://thingsboard.io/docs/user-guide/widgets/) · [Dashboards](https://thingsboard.io/docs/user-guide/dashboards/) · [Aliases](https://thingsboard.io/docs/user-guide/aliases/) · [Data Visualization Building Blocks](https://thingsboard.io/docs/user-guide/data-visualization/).

### ۴.۵. نتیجهٔ تطبیق نمونه‌ها

| نیاز SFP24 | الگوی مرجع مناسب | برداشت قابل استفاده |
|---|---|---|
| معرفی نسخه و وابستگی | Ignition + Odoo | Manifest و سازگاری نسخه |
| ماژول واسط بین دو حوزه | Odoo | Integration Module |
| اجرای مستقل پردازش صنعتی | Siemens Industrial Edge | Container و بستهٔ استقرار |
| Widget و داشبورد قابل ترکیب | ThingsBoard | Widget مستقل + Context |
| دسترسی و امنیت | Odoo و قرارداد داخلی SFP24 | مجوز و Scope سمت سرور؛ نه صرفاً مخفی‌کردن UI |
| خاموش/حذف در محیط تولید | Ignition و Odoo | Lifecycle و اثر بر وابستگی و داده باید صریح باشد |

---

## ۵. آیا فناوری همهٔ ماژول‌ها باید یکی باشد؟

### پاسخ کوتاه

**خیر؛ اما نوع اتصال ماژول به Host تعیین می‌کند چقدر آزادی فناوری داریم.**

دو موضوع را از هم جدا کنیم:

1. فناوری Backend و Frontend حتی در یک برنامه هم لزوماً یکسان نیست.
2. فناوری یک ماژول با فناوری هسته هم لزوماً یکی نیست؛ ولی هرچه اتصال درون‌فرایندی‌تر باشد، محدودیت Runtime بیشتر می‌شود.

### سه وضعیت

| نوع ماژول | آزادی Backend | آزادی Frontend | شرط اصلی |
|---|---|---|---|
| ماژول داخل Modular Monolith | بهتر است با Runtime و زبان سرور Host سازگار باشد | بهتر است با UI Framework میزبان هماهنگ باشد | API و قرارداد مشترک |
| سرویس مستقل | زیاد؛ مثلاً TypeScript، Python یا Java | مستقل از Backend | API/Event، هویت، Tenant، نسخه و پایش |
| Microfrontend | Backend مستقل از UI | می‌تواند Framework دیگری داشته باشد | روش استاندارد Mount، Routing، Auth و امنیت |

### چرا یکسان‌بودن فناوری در مرحلهٔ اول مفید است؟

فرض کن هسته با Vue ساخته شده و یک ماژول با React نوشته شده است.

React component را نمی‌توان بدون Adapter یا معماری Microfrontend مستقیماً مانند یک Vue component در میزکار Mount کرد. راه‌حل وجود دارد، اما هزینه و پیچیدگی اضافه می‌کند.

همین موضوع در Backend هم هست: اگر ماژول در همان فرایند Node.js اجرا شود، استفاده از TypeScript/JavaScript طبیعی‌تر است؛ ولی اگر سرویس مستقل باشد، Python یا Java هم می‌تواند انتخاب شود.

### وضعیت فناوری SFP24

سند [فناوری‌های SFP24](../TECHNOLOGY.fa.md) و کد مبنای بررسی‌شده، این ترکیب را نشان می‌دهند:

| لایه | فناوری فعلی |
|---|---|
| Backend | Node.js و TypeScript |
| HTTP/API | Fastify |
| Frontend | Vue 3 و TypeScript |
| Build Frontend | Vite |
| سه‌بعدی | Three.js |
| نمودار | ECharts |
| Database | MariaDB |
| مدیریت بسته | pnpm workspace / monorepo |

در package.json کد بررسی‌شده، Node.js در بازهٔ 24.x تعریف شده است. نسخه‌های دقیق وابستگی‌ها باید از lockfile همان Commit خوانده شوند.

### پیشنهاد مرحلهٔ اول

- Backend ماژول‌های داخل برنامه: TypeScript و سازگار با Runtime هسته.
- Frontend ماژول‌های داخل میزکار: Vue و قرارداد UI هسته.
- ارتباط بین بخش‌ها: TypeScript Types و قراردادهای نسخه‌دار.
- سرویس مستقل: فقط وقتی نیاز واقعی وجود دارد؛ زبان آن می‌تواند متفاوت باشد.
- Microfrontend: فعلاً به‌عنوان گزینهٔ آینده نگه داشته شود، نه پیش‌نیاز هر ماژول.

**اصل مهم:** یکسان‌بودن فناوری را به‌عنوان راه کاهش هزینهٔ امروز انتخاب می‌کنیم، نه به‌عنوان قانون ابدی محصول. قراردادها باید امکان جداسازی انتخابی در آینده را حفظ کنند.

---

## ۶. ثبت، نصب، فعال‌سازی و حذف ماژول دقیقاً چه هستند؟

### ۶.۱. دو مدل بسته‌بندی را با هم اشتباه نگیریم

**مدل اول: ماژول داخل Build مشترک**

کد ماژول در مخزن محصول وجود دارد؛ Build آن را همراه Host آماده می‌کند؛ Descriptor و Componentهای مجاز در رجیستری کد تعریف می‌شوند. ممکن است برای شرکت A فعال باشد و برای شرکت B غیرفعال.

در این مدل، نصب بستهٔ جدید برای هر شرکت لزوماً وجود ندارد؛ چون کد از قبل در Deployment محصول حضور دارد.

**مدل دوم: بستهٔ مستقل قابل نصب**

ماژول به‌صورت Artifact جدا ساخته و منتشر می‌شود. Host آن را دریافت یا نصب می‌کند، سازگاری و امضا را می‌سنجد و سرویس یا Hookهایش را بارگذاری می‌کند.

این مدل به Package Manager، Trust Model، SDK، سازگاری نسخه و چرخهٔ عمر کامل نیاز دارد.

### مسیر مدل اول — مناسب مرحلهٔ نخست پیشنهادی

~~~mermaid
flowchart TD
    SRC["Source Code ماژول"]
    BUILD["Build مشترک محصول"]
    DESC["Descriptor و Contributionهای ثابت"]
    REG["Registry هنگام راه‌اندازی"]
    ENT["Entitlement شرکت"]
    READY["Readiness و تنظیمات"]
    PERM["Permission شخص"]
    UI["نمایش در میزکار/داشبورد"]

    SRC --> BUILD
    BUILD --> DESC
    DESC --> REG
    REG --> ENT
    ENT --> READY
    READY --> PERM
    PERM --> UI
~~~

### مسیر مدل دوم — هدف احتمالی آینده

~~~mermaid
flowchart TD
    SRC["Source Code"]
    BUILD["Build Artifact"]
    SIGN["Verify / Signature"]
    PUB["Package Registry"]
    DEP["Deploy روی Host"]
    REG["Register و بررسی Manifest"]
    PROV["Provision و Migration"]
    ENT["Entitlement شرکت"]
    ENABLE["Enable"]
    UI["UI Contributions"]

    SRC --> BUILD
    BUILD --> SIGN
    SIGN --> PUB
    PUB --> DEP
    DEP --> REG
    REG --> PROV
    PROV --> ENT
    ENT --> ENABLE
    ENABLE --> UI
~~~

این نمودار دوم **پیشنهاد آینده** است؛ موتور نصب بستهٔ مستقل در وضعیت فعلی SFP24 پیاده نشده است.

### ۶.۲. تفاوت Register، Install، Enable و Permission در یک مثال

| مرحله | سؤال | مسئول احتمالی |
|---|---|---|
| Build | کد به خروجی قابل اجرا تبدیل شده؟ | تیم توسعه |
| Publish | کدام Release معتبر منتشر شده؟ | مسئول انتشار محصول |
| Deploy | Release روی کدام محیط نصب شده؟ | Platform/DevOps |
| Register | Host می‌داند این ماژول چه قابلیت‌هایی دارد؟ | Host / Registry |
| Provision | Schema و تنظیمات لازم آماده‌اند؟ | Migration / Provisioning |
| Entitlement | شرکت حق استفاده دارد؟ | محصول/اشتراک |
| Enable | شرکت می‌خواهد و می‌تواند ماژول را فعال کند؟ | Company Admin طبق سیاست |
| Permission | این شخص چه کاری می‌تواند انجام دهد؟ | Access Administration |
| UI Contribution | قابلیت در کدام صفحه یا میز نمایش داده شود؟ | UI Host + Workspace Configuration |

### ۶.۳. Manifest چه چیزی را معرفی می‌کند؟

یک Manifest مناسب می‌تواند موارد زیر را اعلام کند:

| فیلد پیشنهادی | معنی |
|---|---|
| moduleKey | شناسهٔ پایدار ماژول |
| release | نسخهٔ انتشار |
| contractVersion | نسخهٔ قرارداد Host/Module |
| compatibleHost | بازهٔ نسخه‌های سازگار Host |
| requiredModules | وابستگی‌های اجباری |
| optionalModules | وابستگی‌های اختیاری |
| capabilities | قابلیت‌های ارائه‌شده |
| permissions | مجوزهای لازم/قابل تعریف |
| ports | ورودی و خروجی‌های ارتباطی |
| uiContributions | فرم، Widget، صفحه و بخش پروفایل |
| migrations | تغییرات دادهٔ متعلق به ماژول |
| health | روش سنجش آماده‌بودن |
| owner | مسئول نگهداری و پشتیبانی |

**Manifest فقط شناسنامه است.** اگر در آن بنویسیم ماژول تعمیرات جدول و Widget دارد، خود Manifest جدول و Widget را ایجاد نمی‌کند. کد اجرایی، Migration، اعتبارسنجی، کنترل مجوز و UI باید واقعاً وجود داشته باشند.

### ۶.۴. Dependency Graph

وابستگی‌ها باید قابل تحلیل باشند. اگر A به B وابسته است و B به A وابسته شود، چرخه ایجاد می‌شود و ترتیب نصب/ارتقا مبهم خواهد شد.

~~~mermaid
flowchart TD
    CORE["Core"]
    PROD["Production"]
    MAINT["Maintenance"]
    QUALITY["Quality"]
    LINK["Production-Maintenance Integration"]

    CORE --> PROD
    CORE --> MAINT
    CORE --> QUALITY
    PROD --> LINK
    MAINT --> LINK
~~~

در این مثال، ماژول واسط می‌تواند به هر دو ماژول وابسته باشد؛ اما Production و Maintenance مجبور نیستند مالک منطق یکدیگر شوند.

### ۶.۵. یک تفکیک ضروری: Release Lifecycle و Tenant Lifecycle

چرخهٔ عمر انتشار نرم‌افزار با چرخهٔ فعال‌بودن ماژول برای یک شرکت یکی نیست.

**چرخهٔ انتشار (Release):**

~~~mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Built
    Built --> Verified
    Verified --> Published
    Published --> Deployed
    Deployed --> Deprecated
    Deprecated --> Retired
~~~

**چرخهٔ شرکت (Tenant):**

~~~mermaid
stateDiagram-v2
    [*] --> NotEntitled
    NotEntitled --> Entitled
    Entitled --> Provisioning
    Provisioning --> Ready
    Ready --> Enabled
    Enabled --> Disabled
    Disabled --> Enabled
    Disabled --> Decommissioning
    Decommissioning --> Retained
    Retained --> [*]
~~~

این‌ها State Machine پیشنهادی برای روشن‌کردن مفاهیم‌اند؛ وضعیت‌ها و Transitionهای رسمی محصول هنوز تصویب نشده‌اند.

---

## ۷. ارتباط بین ماژول‌ها

ماژول مستقل نباید جزیرهٔ جدا باشد. اما یکپارچگی هم نباید با دسترسی مستقیم به دیتابیس دیگری ساخته شود.

سه الگوی اصلی وجود دارد:

### ۷.۱. Port / API — وقتی پاسخ فوری لازم است

مثال: Maintenance برای نمایش سابقهٔ تجهیز، از سرویس رسمی دادهٔ تجهیز یا سابقهٔ تعمیرات درخواست می‌کند.

~~~mermaid
sequenceDiagram
    participant M as Maintenance
    participant H as Core / API Host
    participant P as Production or Asset Service
    M->>H: Query Port + Actor + Tenant Context
    H->>H: Authorization / Scope Check
    H->>P: Validated Request
    P-->>H: Typed Response
    H-->>M: Result or Structured Error
~~~

نمونهٔ مناسب:
- دریافت اطلاعات تجهیز
- خواندن خلاصهٔ تولید
- بررسی وضعیت یک سفارش
- درخواست ثبت یک عملیات با کنترل مالکیت و مجوز

Port باید نوع ورودی و خروجی، مالک، مجوز لازم، خطا و نسخهٔ قرارداد داشته باشد.

### ۷.۲. Event — وقتی یک اتفاق رخ داده و چند بخش باید باخبر شوند

مثال: دستورکار تعمیرات تکمیل شده است.

~~~mermaid
flowchart LR
    M["Maintenance"]
    OUT["Outbox / Event Infrastructure"]
    P["Production"]
    I["Inventory"]
    D["Dashboard / Notifications"]

    M -->|"WorkOrderCompleted"| OUT
    OUT --> P
    OUT --> I
    OUT --> D
~~~

Event با Query فرق دارد:

- Query می‌پرسد: «وضعیت فعلی چیست؟»
- Command درخواست می‌کند: «این کار را انجام بده.»
- Event اعلام می‌کند: «این اتفاق رخ داده است.»

برای Eventها باید حداقل این موارد طراحی شوند:
- شناسهٔ یکتا و نسخهٔ Schema
- Tenant و منشأ رویداد
- زمان وقوع و زمان ثبت
- سیاست Retry و جلوگیری از پردازش تکراری
- ثبت شکست و Dead Letter
- ترتیب رویدادها در صورت نیاز
- رفتار هنگام غیرفعال‌شدن ماژول مصرف‌کننده

**این تحقیق وجود Event Bus عمومی و کامل در SFP24 را ادعا نمی‌کند.** مسئلهٔ Task/Event در [پرسش‌های باز هسته](../core/OPEN-QUESTIONS.md) هنوز باز است.

### ۷.۳. Integration Module — وقتی دو حوزه باید یک گردش مشترک داشته باشند

نمونه: ماژول واسط Production-Maintenance می‌تواند بعد از تکمیل تعمیر، وضعیت تجهیز را به گردش تولید وصل کند.

مزیت این الگو:
- Production مالک منطق تعمیرات نمی‌شود.
- Maintenance مالک منطق ثبت تولید نمی‌شود.
- قرارداد و قواعد هماهنگی در یک محل مشخص قرار می‌گیرد.
- اگر اتصال لازم نباشد، دو ماژول می‌توانند مستقل بمانند.

### ۷.۴. چه کاری نباید انجام دهیم؟

| کار پرریسک | جایگزین مناسب‌تر |
|---|---|
| خواندن مستقیم جدول‌های دامنهٔ ماژول دیگر | Query Port / API |
| نوشتن مستقیم در جدول ماژول دیگر | Action Port یا Command |
| کپی‌کردن Person یا Equipment در هر ماژول | ارجاع به هویت مشترک Core |
| ساخت مجوزهای موازی در هر ماژول | معرفی Permission توسط ماژول، مدیریت سیاست توسط Core |
| ارسال Event بدون نسخه و شناسه | Event Contract نسخه‌دار |
| وابستگی حلقوی بین ماژول‌ها | ماژول واسط یا قرارداد مشترک Core |

**اصل پیشنهادی:** هر ماژول مالک داده و قواعد دامنهٔ خودش باشد؛ Core هویت، Tenant، امنیت و زیرساخت ارتباطی مشترک را فراهم کند.

---

## ۸. داشبوردها، میزکارها و اتصال آن‌ها به ماژول‌ها

### ۸.۱. پنج مفهوم را یکی نکنیم

| مفهوم | معنی | نمونه |
|---|---|---|
| Workbench / میزکار | محیط کار متناسب با فرد یا گروه | میز اپراتور |
| Dashboard / داشبورد | چیدمان برای مشاهده و تحلیل | داشبورد تولید |
| Widget | جزء قابل استفادهٔ مجدد | نمودار توقف یا وضعیت دستگاه |
| Full-page Application | صفحهٔ کامل برای گردش پیچیده | مدیریت دستورکار تعمیر |
| Entity Profile Section | بخشی از صفحهٔ یک موجودیت | سابقهٔ تعمیرات تجهیز |
| 3D Overlay | محتوای مرتبط با موقعیت/تجهیز در صحنه | وضعیت ماشین در مدل سه‌بعدی |
| Inbox / Task View | نمایش کارهای ارجاع‌شده و نیازمند اقدام | کارتابل تعمیرکار |

این‌ها دسته‌های طراحی تجربه هستند، نه الزاماً انواع ثابت و مصوب Schema.

### ۸.۲. ماژول چه چیزی عرضه می‌کند و Host چه چیزی را کنترل می‌کند؟

**ماژول مالک:**
- Component و منطق نمایش تخصصی
- Query/Action Port موردنیاز
- Capability و Permission موردنیاز
- Contextهای قابل پشتیبانی
- عنوان، توضیح و نسخهٔ Contribution

**Host مالک:**
- چارچوب Mount و اجرای امن
- احراز هویت و Tenant Context
- کنترل Entitlement، Readiness، Permission و Scope
- مسیریابی و ناوبری
- ذخیرهٔ چیدمان میز/داشبورد
- خطا، Loading و رفتار ناسازگاری نسخه

**Company Admin یا Workspace Manager مالک:**
- انتخاب میز و داشبورد مورد استفاده
- ترکیب Widgetهای مجاز
- انتساب محیط به گروه یا افراد
- انتخاب زمینهٔ قابل مشاهده، در محدودهٔ مجاز

### ۸.۳. نمودار اتصال ماژول به داشبورد

~~~mermaid
flowchart TB
    subgraph MOD["Module"]
      META["Contribution Metadata"]
      COMP["Widget / Page Component"]
      PORT["Query / Action Port"]
      CAP["Capability + Permission"]
    end

    REG["Host Registry"]
    POLICY["Entitlement + Readiness + Scope + Permission"]
    EDITOR["Workbench / Dashboard Editor"]
    RUNTIME["UI Runtime"]
    API["Backend Authorization"]
    DATA["Domain Service / Data"]

    META --> REG
    CAP --> REG
    PORT --> API
    REG --> POLICY
    EDITOR --> RUNTIME
    POLICY --> RUNTIME
    COMP --> RUNTIME
    RUNTIME --> API
    API --> DATA
~~~

این نمودار یک قاعدهٔ مهم را نشان می‌دهد: **نمایش Widget و اجازهٔ اجرای عملیات دو موضوع مستقل‌اند.** حتی اگر Widget در داشبورد باشد، Backend باید Permission و Scope را دوباره بررسی کند.

### ۸.۴. نمونهٔ عملی: ماژول تعمیرات

| قابلیت تعمیرات | محل ارائهٔ احتمالی | مصرف‌کننده |
|---|---|---|
| اعلام خرابی | Widget یا فرم میز اپراتور | اپراتور |
| بررسی درخواست | صفحهٔ تخصصی یا Inbox | سرپرست تعمیرات |
| اجرای تعمیر | Full-page یا میز تعمیرکار | تکنسین |
| تأیید نتیجه | فرم/Action | بازبین |
| سابقهٔ تعمیرات | بخش پروفایل تجهیز | تکنسین و مدیر مجاز |
| روند خرابی | Dashboard Widget | مدیر |
| اعلان تغییر وضعیت | Notification | افراد مجاز |

یک ماژول می‌تواند چند Contribution داشته باشد و هر Contribution در چند محیط استفاده شود؛ لازم نیست برای هر میز، منطق تخصصی جداگانه نوشته شود.

### ۸.۵. Context و Alias

الگوی Alias در ThingsBoard برای SFP24 یک ایدهٔ مهم دارد: Widget به یک دستگاه ثابت قفل نشود.

بهتر است Widget بتواند Context بگیرد، مثلاً:
- تجهیز انتخاب‌شده
- سایت یا محدودهٔ مجاز
- بازهٔ زمانی
- سفارش یا دستورکار جاری
- شخص یا گروه کاری

در این صورت یک Widget «روند تولید» می‌تواند برای تجهیزات مختلف استفاده شود؛ اما Backend باید مجازبودن همان Context را بررسی کند.

این موضوع به معنی کپی‌کردن دقیق مدل Alias در ThingsBoard نیست؛ قرارداد Context در SFP24 باید با Tenant و Scope خودمان سازگار باشد.

### ۸.۶. آیا باید هر ماژول داشبورد خودش را داشته باشد؟

نه الزاماً.

سه شکل ممکن است:

1. **Widget مستقل:** ماژول فقط Widget عرضه می‌کند؛ مدیر آن را در داشبورد مشترک می‌گذارد.
2. **Dashboard Template:** ماژول یک چیدمان پیشنهادی عرضه می‌کند؛ شرکت آن را انتخاب و شخصی‌سازی می‌کند.
3. **Full-page Module:** ماژول صفحهٔ تخصصی خودش را دارد؛ Host فقط ناوبری و امنیت را مدیریت می‌کند.

این سه حالت می‌توانند کنار هم وجود داشته باشند. یک ماژول تحلیلی ممکن است Template داشبورد داشته باشد، در حالی که یک فرم پیچیدهٔ تعمیرات Full-page باشد.

### ۸.۷. پیشنهاد دسته‌بندی میزها

| نوع میز پیشنهادی | کاربر/هدف | محتوای نمونه |
|---|---|---|
| Operator Workbench | انجام عملیات سریع | ثبت تولید، اعلام خرابی، دستور کار جاری |
| Technician Workbench | اجرای کار تخصصی | دستورکار، چک‌لیست، سابقه تجهیز |
| Supervisor Workbench | هماهنگی و رسیدگی | کارتابل، موارد معطل، وضعیت تیم |
| Management Dashboard | تحلیل و تصمیم | KPI، روند، مقایسهٔ سایت‌ها |
| Quality Workbench | بازرسی و تصمیم کیفیت | نمونه‌برداری، نتایج، عدم انطباق |
| Contextual 3D Workspace | تعامل با مدل تجهیز | وضعیت، هشدار، سوابق و لایه‌های تخصصی |

این دسته‌بندی صرفاً پیشنهاد UX است. نباید به‌عنوان شش نوع ثابت و اجباری در Schema پیاده شود. یک فرد می‌تواند چند مسئولیت داشته باشد و به چند میز دسترسی پیدا کند.

---

## ۹. نقش Developer Admin و Company Admin

مدیریت عرضهٔ ماژول در سطح محصول با فعال‌سازی آن برای یک شرکت یکی نیست.

### تقسیم مسئولیت پیشنهادی

| نقش/محیط | مسئولیت | نمونهٔ عملیات |
|---|---|---|
| Product / Developer Admin | مدیریت تعریف و Release ماژول | ثبت نسخه، Manifest، وابستگی و سازگاری |
| Platform Operations | استقرار روی محیط‌ها | Deploy، Health، Rollout و Rollback |
| Company Admin | مدیریت استفادهٔ شرکت | انتخاب ماژول مجاز، تنظیمات و Enable/Disable |
| Access Admin | تخصیص دسترسی اشخاص | نقش، Permission و Scope |
| Workspace Manager | ترکیب تجربهٔ کاربری | ساخت میز و انتخاب Widgetهای مجاز |
| End User | استفاده از قابلیت | ثبت کار، مشاهدهٔ داشبورد و پاسخ به وظیفه |

### Developer Admin چه چیزهایی باید کنترل کند؟

**پیشنهاد برای آینده:**
- تعریف Module Family و Release
- بارگذاری یا انتشار Artifact مورد اعتماد
- بررسی Manifest و Dependency
- سازگاری با نسخهٔ Host و قراردادها
- وضعیت امضا و اصالت بسته
- انتشار، Deprecated و Retire
- گزارش Health و خطاهای بارگذاری

### Company Admin چه چیزهایی باید کنترل کند؟

**پیشنهاد برای آینده:**
- مشاهدهٔ ماژول‌های قابل خرید/فعال‌سازی
- بررسی پیش‌نیازهای راه‌اندازی
- Enable یا Disable طبق سیاست محصول
- تنظیمات اختصاصی شرکت
- تخصیص قابلیت‌ها و مجوزها
- انتخاب Widgetها و میزهای مناسب

**نکتهٔ امنیتی:** Company Admin نباید بتواند کد دلخواه را روی سرور محصول بارگذاری کند. فعال‌سازی قابلیت منتشرشده با نصب افزونهٔ ناشناس یکی نیست.

نام نهایی این محیط‌ها هنوز تصمیم محصول نیست؛ «Developer Admin» و «Company Admin» در این سند نام‌های توضیحی‌اند.

---

## ۱۰. خاموش‌کردن، ارتقا و بازنشستگی ماژول

### ۱۰.۱. Disable با Uninstall فرق دارد

| عملیات | معنی | اثر مورد انتظار |
|---|---|---|
| Disable | قابلیت برای شرکت متوقف شود | داده و سابقه حذف نشوند |
| Uninstall | اجزای نصب‌شدهٔ ماژول از محیط/شرکت برداشته شوند | نیازمند بررسی Migration و حفظ داده |
| Unregister | Host دیگر تعریف/نسخهٔ ماژول را برای استفاده عرضه نکند | نباید با وجود اجرای Worker یا درخواست باز تداخل داشته باشد |
| Retire | نسخه یا ماژول بازنشسته شود | سیاست پشتیبانی، مهاجرت و دسترسی تاریخی لازم است |
| Emergency Stop | اجرای خطرناک فوراً مهار شود | مسیر اضطراری با Disable عادی یکسان نیست |

این تفکیک برای داده‌های تولید، تعمیرات، کیفیت و آموزش اهمیت دارد. خاموش‌کردن ماژول نباید به‌طور پیش‌فرض سوابق آن را پاک کند.

### ۱۰.۲. قبل از حذف چه چیزهایی باید بررسی شوند؟

- ماژول‌های وابسته
- Widgetها و میزهایی که از آن استفاده می‌کنند
- Portها و Eventهای مصرف‌شده
- Workerهای فعال و صف‌های معوق
- تراکنش‌ها یا عملیات نیمه‌تمام
- Schema و Migrationهای اعمال‌شده
- سوابق و سیاست نگهداری/Export
- نسخهٔ قبلی و امکان Rollback
- اثر بر APIهای مصرف‌کننده

### ۱۰.۳. ارتقا در محیط عملیاتی

یک Update سادهٔ فایل کافی نیست. بسته به نوع ماژول، ممکن است نیاز باشد:
- نسخهٔ Host و Module تطبیق داده شوند.
- Migration داده اجرا شود.
- Workerها Drain یا متوقف شوند.
- Eventهای معوق با نسخهٔ جدید سازگار باشند.
- Rollback و Backup تعریف شوند.
- میزها و داشبوردهای قدیمی با Contributionهای نسخهٔ جدید سازگار بمانند.

مستندات Ignition نمونه‌ای از Restart موردنیاز در بعضی عملیات ماژول را نشان می‌دهند. Odoo نیز دربارهٔ اثر Uninstall بر داده و وابستگی‌ها هشدار می‌دهد. نتیجه برای SFP24 این نیست که همان رفتار را عیناً اجرا کنیم؛ نتیجه این است که Lifecycle باید از ابتدا صریح باشد.

---

## ۱۱. تطبیق با وضعیت واقعی SFP24

این بخش عمداً از پیشنهادهای بالا جدا شده است.

### ۱۱.۱. دو مبنای نسخه‌ای را با هم یکی نگیریم

- سندهای جاری STATUS.fa.md و TECHNOLOGY.fa.md در مخزن اسناد، کد pouyeshgar-workshop در Commit b3f203b را به‌عنوان مبنای وضعیت خود معرفی می‌کنند.
- بررسی دقیق رجیستری و UI Contribution در این مطالعه روی Snapshot کد pouyeshgar-workshop در Commit 55ad14d انجام شده است.

این دو SHA دو مبنای جدا هستند. این سند ادعا نمی‌کند که آن‌ها یک نسخه‌اند یا تمام وضعیت کد فعلی در هر دو یکسان است. یافته‌های جزئی رجیستری در ادامه فقط به Snapshot 55ad14d مربوط‌اند.

### ۱۱.۲. چه چیزهایی در کد 55ad14d واقعاً دیده می‌شود؟

| موضوع | شاهد کد | نتیجهٔ دقیق |
|---|---|---|
| Module Descriptor | server/platform/module-registry.ts | نوع ModuleDescriptor با Contract Version، Module Key، Release، Host Major و وابستگی‌ها تعریف شده است |
| Capability | همان فایل | قابلیت‌ها Permission، Entitlement، Availability و Port دارند |
| Dependency Check | همان فایل | وابستگی اجباری بررسی و چرخهٔ وابستگی رد می‌شود؛ کل چرخهٔ نصب و Dependency Resolution عمومی نیست |
| Port | همان فایل و server/operations/module-capabilities.ts | Portهای Query و Action در کد ثبت می‌شوند |
| UI Contribution | src/company/ui-contribution-contract.ts | انواع فرم، Widget، صفحه، Profile، Inbox، Notification و 3D Overlay تعریف شده‌اند |
| Component Registry | src/company/pilot-components.ts | Vue Componentها با Import ثابت و Map مجاز نگهداری می‌شوند |
| Contribution List | src/company/pilot-contributions.ts | Contributionهای پایلوت در کد تعریف شده‌اند |
| Desk Composition | src/company/desk-sections.ts | بخش‌های میز از Widgetها و Contributionهای موجود Resolve می‌شوند |
| Product Catalog | src/company/module-catalog.ts | فهرست محصول از وضعیت پیاده‌سازی واقعی جدا شده است؛ خود فایل صریحاً Product Catalog را معرفی می‌کند |

### ۱۱.۳. رجیستری فعلی چه می‌کند؟

در module-registry.ts، تابع createModuleRegistry Descriptorها، Portها، Contributionها و Componentهای مجاز را دریافت و اعتبارسنجی می‌کند. مواردی مثل شناسهٔ تکراری، Module ناشناخته، Contract Version نامعتبر، Host Major ناسازگار، وابستگی اجباری ناموجود، چرخهٔ وابستگی، Permission ناشناخته و Component ثبت‌نشده رد می‌شوند.

این یک **Registry ایستا و کد-محور** است؛ نه یک Package Manager که فایل ناشناس را از Developer Admin دریافت و در زمان اجرا بارگذاری کند.

در module-capabilities.ts، Descriptorهای Production و Maintenance در کد ساخته می‌شوند. Entitlement شرکت از جدول‌های موجود خوانده می‌شود. این جدایی مهم است: تعریف ماژول در کد و حق استفادهٔ شرکت از آن دو موضوع جدا هستند.

یک محدودیت دقیق در همین Snapshot: فیلد compatible در خروجی خواندن Capability به‌صورت ثابت true قرار می‌گیرد. بنابراین نباید آن را مدرک وجود ماتریس سازگاری Release به Release یا آزمون سازگاری واقعی هر Tenant تلقی کرد؛ بررسی compatibleHostMajor در Registry موضوع جداگانه‌ای است.

### ۱۱.۴. اتصال UI در Snapshot فعلی

در pilot-components.ts، کامپوننت‌های Vue با Importهای ثابت وارد و در یک Map ثبت شده‌اند. Registry فقط componentIdهایی را می‌پذیرد که در مجموعهٔ Componentهای مجاز وجود داشته باشند.

پس:
- Contribution Contract وجود دارد.
- Host می‌تواند Contribution را اعتبارسنجی کند.
- اتصال Component به کد واقعی وجود دارد.
- اما بارگذاری آزاد Component از بستهٔ مستقل در زمان اجرا از این شواهد نتیجه نمی‌شود.

### ۱۱.۵. وضعیت Workspace و Dashboard

سند [اتاق کاری، میز، داشبورد و محیط سه‌بعدی](../core/WORKSPACES.fa.md) تصریح می‌کند:
- ساخت و اختصاص میز نام‌دار وجود دارد.
- تعریف میز ذخیره و نسخه‌بندی می‌شود.
- یک میز می‌تواند به چند حساب و یک حساب به چند میز اختصاص یابد.
- انتخاب میز، مجوز یا خرید قابلیت ایجاد نمی‌کند.
- موتور عمومی Dashboard Builder و اتصال عملیاتی تمام کارت‌ها وجود ندارد.
- محتوای AssignedDesk در مبنای مستندشده هنوز Preview است.

بنابراین داشتن UI Contribution یا Desk Registry را نباید معادل موتور کامل داشبوردساز، Marketplace ماژول یا Plugin Runtime دانست.

### ۱۱.۶. چه چیزهایی هنوز ساخته‌شده محسوب نمی‌شوند؟

طبق [وضعیت محصول](../STATUS.fa.md)، [معماری موجود](../core/ARCHITECTURE.fa.md) و [قراردادهای پیش‌نویس](../contracts/README.md):

- SDK عمومی و کامل نصب ماژول ساخته نشده است.
- Plugin Engine برای بارگذاری آزاد بستهٔ مستقل وجود ندارد.
- قرارداد عمومی و نهایی Lifecycle هنوز تثبیت نشده است.
- موتور عمومی Event/Task برای تمام ماژول‌ها را نمی‌توان مفروض گرفت.
- Dashboard Builder عمومی و عملیاتی برای تمام Contributionها اثبات نشده است.
- مستقل‌بودن نسخهٔ هر ماژول برای هر Tenant قابلیت تأییدشده‌ای نیست.

### ۱۱.۷. اسناد داخلی مرتبط

| سند | نقش آن در این مطالعه |
|---|---|
| [معماری موجود](../core/ARCHITECTURE.fa.md) | مرز Runtime، WEB/INGEST، Modular Monolith و نبود Plugin Engine |
| [فناوری‌های SFP24](../TECHNOLOGY.fa.md) | مرجع فناوری و نسخه‌های اعلام‌شده |
| [Module & Capability Contract — Draft](../contracts/MODULE-CONTRACT-DRAFT.md) | پیش‌نویس Manifest، Ownership، Security، Ports و Lifecycle |
| [UI Contributions — Draft](../contracts/UI-CONTRIBUTIONS-DRAFT.md) | پیش‌نویس فرم، Widget، Profile، Inbox و Page |
| [Workspace](../core/WORKSPACES.fa.md) | وضعیت موجود میزها و پرسش‌های داشبورد |
| [Extensions](../core/EXTENSIONS.fa.md) | سازوکار موجود گسترش تعاریف؛ نه Plugin SDK |
| [Core Open Questions](../core/OPEN-QUESTIONS.md) | پرسش‌های باز Module، Dashboard، Event و Install |
| [تحقیق قبلی پلتفرم‌های عملیاتی](OPERATIONS-PLATFORMS.fa.md) | نمونه‌های Siemens Opcenter، Tulip، SAP Digital Manufacturing، AVEVA و RIGG |

### لینک شواهد کد

- [Module Registry در 55ad14d](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/55ad14d/server/platform/module-registry.ts)
- [Module Capabilities در 55ad14d](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/55ad14d/server/operations/module-capabilities.ts)
- [UI Contribution Contract در 55ad14d](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/55ad14d/src/company/ui-contribution-contract.ts)
- [Pilot Contributions در 55ad14d](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/55ad14d/src/company/pilot-contributions.ts)
- [Pilot Components در 55ad14d](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/55ad14d/src/company/pilot-components.ts)
- [Desk Sections در 55ad14d](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/55ad14d/src/company/desk-sections.ts)
- [Desk Studio Model در 55ad14d](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/55ad14d/src/company/desk-studio-model.ts)
- [Product Module Catalog در 55ad14d](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/55ad14d/src/company/module-catalog.ts)
- [Package Manifest در 55ad14d](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/55ad14d/package.json)

---

<a id="section-stage-plan"></a>

## ۱۲. پیشنهاد مرحله‌بندی‌شده برای SFP24

این بخش پیشنهاد معماری بر اساس شواهد بالاست؛ **تصمیم تأییدشده یا برنامهٔ اجرایی مصوب نیست.**

### مرحلهٔ اول — Modular Monolith مورد اعتماد

هدف: یک ماژول واقعی را از تعریف تا نمایش و کنترل دسترسی، با قرارداد روشن اجرا کنیم.

- Build مشترک و انتشار هماهنگ.
- TypeScript در Backend و Vue در Frontend ماژول‌های درون‌برنامه‌ای.
- Descriptor و Registry کد-محور.
- Dependency و Capability صریح.
- Portهای Query و Action.
- UI Contribution با Componentهای مورد اعتماد.
- Entitlement شرکت و Permission شخص جدا.
- حفظ داده هنگام Disable.
- ثبت نسخه و سازگاری قرارداد.

**چیزی که در این مرحله نمی‌سازیم:** آپلود کد دلخواه مشتری، Marketplace عمومی، Microfrontend اجباری، Microservice برای هر ماژول.

### مرحلهٔ دوم — Module SDK و Lifecycle رسمی

پس از آزمون مرحلهٔ اول با Production و یک ماژول دیگر:

- Manifest نسخه‌دار و Schema اعتبارسنجی‌شده.
- Compatibility Matrix.
- Dependency Resolver.
- قرارداد Migration و Rollback.
- Health و Readiness.
- چرخهٔ Publish/Deploy/Enable/Disable/Retire.
- قرارداد رسمی Port و Event.
- UI Contribution و Context Binding.
- Developer Admin برای Releaseهای مورد اعتماد.
- گزارش Audit و اثر هر تغییر.

این مرحله هنوز می‌تواند با Build مشترک اجرا شود؛ SDK به معنی نصب آزاد بسته نیست.

### مرحلهٔ سوم — جداسازی انتخابی سرویس‌ها

فقط اگر شواهد بار، مقیاس، جداسازی خرابی یا نیاز استقرار نشان دهد:

- Data Hub یا بخشی از آن
- پردازش و تحلیل سنگین
- Edge Runtime
- AI Worker یا Providerهای مستقل

برای هر جداسازی باید مالکیت داده، API/Event، احراز سرویس، بازیابی، Observability و هزینهٔ عملیاتی مشخص باشد.

### مرحلهٔ چهارم — بسته‌های مستقل و اکوسیستم توسعه‌دهندگان

این مرحله فقط در صورت نیاز واقعی محصول به توسعه‌دهندهٔ ثالث یا نصب مستقل مطرح می‌شود:

- Artifact Repository
- امضای بسته و Trust Policy
- Sandbox یا مرز امنیتی اجرای کد
- نصب/ارتقای کنترل‌شده
- سازگاری و سیاست پشتیبانی
- بررسی امنیتی و انتشار
- جداسازی نسخه‌ها در صورت نیاز

این مرحله از اکنون تصویب یا زمان‌بندی نشده است.

### جدول تصمیم پیشنهادی

| موضوع | جهت پیشنهادی فعلی | دلیل |
|---|---|---|
| مدل اجرای ماژول | Modular Monolith | کم‌کردن پیچیدگی در دورهٔ بلوغ |
| زبان Backend درون‌برنامه‌ای | TypeScript | سازگاری با Runtime فعلی |
| Frontend درون‌میزکار | Vue | سازگاری با Host فعلی |
| سرویس‌های مستقل | فناوری آزادتر | جداسازی واقعی از طریق قرارداد |
| نصب آزاد بسته | فعلاً نه | نیازمند Trust و Lifecycle کامل |
| Registry | کد-محور در مرحلهٔ اول | با واقعیت فعلی سازگارتر |
| ارتباط ماژول‌ها | Port/API؛ Event پس از قرارداد و آزمون | جداسازی مالکیت |
| Dashboard | Host-owned layout + Module-owned Widget | استفادهٔ مجدد و کنترل دسترسی |
| Data Ownership | مالکیت در ماژول | جلوگیری از وابستگی مستقیم |
| Disable | توقف استفاده، حفظ داده | محافظت از سوابق عملیاتی |

---

## ۱۳. پرسش‌هایی که هنوز تصمیم می‌خواهند

این تحقیق پاسخ فنی و گزینه‌ها را روشن می‌کند، اما تصمیم‌های زیر هنوز بازند:

| پرسش | چرا مهم است؟ | چه زمانی باید پاسخ داده شود؟ |
|---|---|---|
| آیا Release هر ماژول باید مستقل منتشر شود؟ | روی Build، تست و سازگاری اثر دارد | پیش از تثبیت SDK |
| آیا دو Tenant می‌توانند از دو Release متفاوت یک ماژول استفاده کنند؟ | به Isolation و Deployment وابسته است | پیش از طراحی Version Isolation |
| چه کسی می‌تواند Release منتشر کند؟ | Trust و امنیت زنجیرهٔ انتشار | پیش از Developer Admin |
| Uninstall چه اثری بر داده دارد؟ | حفظ سابقه و الزامات ممیزی | پیش از Lifecycle اجرایی |
| آیا Event Infrastructure مشترک لازم است؟ | هزینه و پیچیدگی عملیاتی | پس از سناریوهای واقعی چندماژولی |
| Dashboard مستقل لازم است یا Widget در Host کافی است؟ | روی UX و مالکیت چیدمان اثر دارد | پس از سناریوهای اپراتور/مدیر |
| چه کسی میزهای مشترک را منتشر و نسخه‌بندی می‌کند؟ | تغییر چیدمان روی کاربران اثر دارد | هنگام تکمیل Workspace |
| آیا Microfrontend ارزش پیچیدگی‌اش را دارد؟ | فناوری‌های متفاوت UI را ممکن می‌کند | فقط با نیاز واقعی توسعه‌دهندهٔ ثالث |
| سیاست توقف کارهای باز هنگام Disable چیست؟ | روی عملیات زنده اثر دارد | پیش از اجرای Lifecycle |

برای ثبت تصمیم از مسیر [Decision Records](../governance/DECISION-RECORDS.md) و برای تغییر مشترک از [Change Workflow](../governance/CHANGE-WORKFLOW.md) استفاده شود. این سند به‌تنهایی هیچ‌کدام از موارد بالا را تصویب نمی‌کند.

---

## ۱۴. روش تحقیق و محدودیت شواهد

### روش

1. مستندات رسمی سازندگان برای قابلیت‌های مورد بحث بررسی شد.
2. نسخهٔ محصول/مستند در جایی که مشخص بود ثبت شد.
3. یافته‌ها با اسناد جاری SFP24 تطبیق داده شد.
4. برای بررسی رجیستری و UI، Snapshot مشخص 55ad14d خوانده شد.
5. قابلیت‌های مشاهده‌شده از پیشنهادها و ایده‌های آینده جدا شدند.

### محدودیت‌ها

- محصولات بیرونی نصب یا در محیط عملیاتی آزمایش نشدند.
- کارایی، امنیت، هزینه، مقیاس‌پذیری و کیفیت تجربهٔ کاربر به‌صورت Benchmark مقایسه نشده‌اند.
- منابع رسمی، رفتار مستندشده را نشان می‌دهند؛ منبع فروشنده ممکن است محدودیت‌ها یا تجربهٔ واقعی مشتریان را کامل پوشش ندهد.
- مستندات SDK Ignition که ساختار .modl را توضیح می‌دهد متعلق به نسخهٔ 8.1 است؛ برای اجرای واقعی باید با SDK نسخهٔ 8.3 تطبیق داده شود.
- مستندات Odoo در این بررسی نسخهٔ 19.0 هستند.
- مستندات Industrial Edge در این بررسی v26.09 و صفحات تکمیلی v26.06 هستند.
- مستندات ThingsBoard از راهنمای Community Edition در تاریخ بررسی خوانده شده‌اند.
- Snapshot کد 55ad14d با SHA مبنای معرفی‌شده در STATUS/TECHNOLOGY یکسان فرض نشده است.
- هیچ تست Runtime، Build یا آزمون امنیتی برای این تحقیق اجرا نشده است.

### درجهٔ اتکای نتیجه‌ها

| نوع نتیجه | درجهٔ اتکا | توضیح |
|---|---|---|
| قابلیت‌های نوشته‌شده در مستندات رسمی | بالا برای همان نسخهٔ مستند | اثبات رفتار همهٔ نسخه‌ها یا استقرارها نیست |
| وجود ساختارهای Registry و Contribution در Snapshot کد | بالا برای همان Commit | اثبات وضعیت Commitهای دیگر نیست |
| نبود قابلیت در وضعیت جاری اسناد | مطابق مرجع وضعیت ثبت‌شده | باید هنگام تغییر مبنای کد دوباره بررسی شود |
| پیشنهاد معماری SFP24 | استنباط طراحی | نیازمند بررسی، چالش و تأیید صاحب محصول |
| Benchmark یا برتری قطعی یک محصول | بررسی نشده | از این تحقیق نتیجه نمی‌شود |

---

## ۱۵. منابع

### مستندات رسمی بیرونی

| موضوع | منبع |
|---|---|
| معماری و مدیریت Module در Ignition 8.3 | [Ignition Platform](https://docs.inductiveautomation.com/docs/8.3/platform) |
| نصب، ارتقا، Disable و Uninstall در Ignition 8.3 | [Installing or Upgrading a Module](https://www.docs.inductiveautomation.com/docs/8.3/getting-started/installing-and-upgrading/installing-or-upgrading-a-module) |
| ساختار .modl و JAR در SDK 8.1 | [Anatomy of a Module](https://www.sdk-docs.inductiveautomation.com/docs/getting-started/anatomy-of-a-module/) |
| ساخت بستهٔ .modl | [Build a Module](https://www.sdk-docs.inductiveautomation.com/docs/getting-started/create-a-module/build-a-module/) |
| Scopeها و Hookها | [Scopes, Hooks and Contexts](https://www.sdk-docs.inductiveautomation.com/docs/getting-started/anatomy-of-a-module/scopes-hooks-contexts/) |
| Manifest و Dependency در Odoo 19 | [Module Manifests](https://www.odoo.com/documentation/19.0/developer/reference/backend/module.html) |
| ترکیب یک ماژول Odoo | [Building a Module](https://www.odoo.com/documentation/19.0/developer/tutorials/backend.html) |
| فایل‌های دادهٔ Odoo | [Data Files](https://www.odoo.com/documentation/19.0/developer/reference/backend/data.html) |
| نصب و اثر حذف App در Odoo 19 | [Apps and Modules](https://www.odoo.com/documentation/19.0/applications/general/apps_modules.html) |
| بسته‌بندی برنامهٔ Industrial Edge | [First Industrial Edge App — v26.09](https://docs.industrial-operations-x.siemens.cloud/r/en-us/v26.09/industrial-edge-platform-operation-develop-an-application/developer-guide/handson-exercise/description-of-the-hands-on-application/description-of-your-first-industrial-edge-app) |
| نقش App Publisher | [App Publisher Security and Mission](https://docs.industrial-operations-x.siemens.cloud/r/en-us/v26.06/industrial-edge-platform-operation-setup-operate-utilize/security/industrial-edge-components-security-measures/industrial-edge-app-publisher-security/mission-of-the-industrial-edge-app-publisher-and-impact-on-exposed-services) |
| Widgetهای ThingsBoard | [Widgets](https://thingsboard.io/docs/user-guide/widgets/) |
| ساخت داشبورد ThingsBoard | [Dashboards](https://thingsboard.io/docs/user-guide/dashboards/) |
| Alias و Context داشبورد | [Aliases](https://thingsboard.io/docs/user-guide/aliases/) |

### اسناد و کد داخلی SFP24

- [تحقیق قبلی پلتفرم‌های عملیاتی](OPERATIONS-PLATFORMS.fa.md)
- [معماری موجود](../core/ARCHITECTURE.fa.md)
- [فناوری‌های SFP24](../TECHNOLOGY.fa.md)
- [وضعیت محصول](../STATUS.fa.md)
- [Module & Capability Contract — Draft](../contracts/MODULE-CONTRACT-DRAFT.md)
- [UI Contributions — Draft](../contracts/UI-CONTRIBUTIONS-DRAFT.md)
- [Workspace](../core/WORKSPACES.fa.md)
- [Extensions](../core/EXTENSIONS.fa.md)
- [Core Open Questions](../core/OPEN-QUESTIONS.md)
- [Documentation Policy](../governance/DOCUMENTATION-POLICY.md)
- [Change Workflow](../governance/CHANGE-WORKFLOW.md)

---

**نتیجهٔ نهایی تحقیق:** برای مرحلهٔ فعلی SFP24، ارزشمندترین مسیر این است که قرارداد ماژول، مالکیت داده، Portها، Permissionها و UI Contribution را کامل کنیم و یک ماژول واقعی را با این قرارداد آزمایش کنیم. نصب آزاد بسته، جداسازی Microservice و Microfrontend باید تصمیم‌های بعدی و مبتنی بر نیاز واقعی باشند؛ نه پیش‌نیاز شروع توسعهٔ ماژول‌ها.
