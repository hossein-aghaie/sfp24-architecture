# SFP24 — مشخصات اجرایی پیشنهادی ۰۱: هسته، معرفی ماژول و قرارداد داده

> **Status:** Proposed executable specification v0.1 — **نه قرارداد مصوب، نه مجوز Codex برای تغییر کد**.  
> **Date:** ۲۰۲۶-۱۱-۰۵ · **Scope:** ثبت Production موجود و Maintenance سبک در Host فعلی؛ اتصال به میز و داشبورد، بدون ادعای ساخت ۴۴ ماژول.  
> **Source of truth:** [Module Contract](../../contracts/MODULE-CONTRACT-DRAFT.md)، [Domain Interaction Draft](../../contracts/DOMAIN-INTERACTION-CONTRACT-DRAFT.md)، [Data Contract](../../contracts/DATA-CONTRACT-DRAFT.md)، [UI Contributions](../../contracts/UI-CONTRIBUTIONS-DRAFT.md)، [هویت](../../core/IDENTITY-AND-ACCESS.fa.md)، [گسترش موجودیت](../../core/EXTENSIONS.fa.md)، [Workspace](../../core/WORKSPACES.fa.md).  
> **Code examined:** `hossein-aghaie/pouyeshgar-workshop`، `codex/04-core-workspaces-dashboard`، SHA `5c7ac617f95ee8b84cbd32d7fa8e7474a073ec97`؛ بررسی فایل‌ها انجام شده، **اجرای تازهٔ Runtime/تست واقعی انجام نشده**.  
> **Companion:** [گام‌های دقیق Codex](02-CODEX-WORK-PACKAGES.fa.md) · [آزمون‌های پذیرش و کارخانهٔ فرضی](03-DEMO-AND-ACCEPTANCE.fa.md).  
> همهٔ شناسه‌های نسخه/Schema جدید زیر **انتخاب‌های مهندسی پیشنهادیِ این بسته** هستند. Codex بعد از تصویب باید همان‌ها را اجرا کند و خودش معمار محصول نشود.

## ۱. معماری هدف با مرزهای قطعی

- **Host/Core:** Account، Person، Tenant/Scope، Role/Permission، Module Entitlement، Masterهای مشترک، اعتبارسنجی بین‌ماژولی، Audit و خدمات کوچک مشترک.
- **Trusted Module Registry:** شناسه/نسخهٔ ماژول، قابلیت، نیاز داده، readiness، portهای Query/Action/Event و UI Contributionهای ثبت‌شده در کد مورد اعتماد.
- **Domain:** Production مالک ProductionReport و WorkSession است؛ Maintenance مالک MaintenanceRequest، WorkOrder و TechnicalAction است. هیچ رکورد تخصصی را در یک جدول مبهم «همهٔ کارها» ذخیره نکنیم.
- **Experience Host:** Form، Profile، Desk، Dashboard، Inbox، Notification و 3D فقط دادهٔ معتبر می‌خوانند یا Action معتبر صدا می‌زنند. ساخت میز یا مخفی/نمایان‌کردن دکمه هیچ Permission تولید نمی‌کند.

**فهم دامنه:** Person ≠ Account ≠ Assignment ≠ Permission ≠ Qualification؛ Task ≠ WorkOrder؛ Comment ≠ Notification ≠ Task ≠ Approval؛ Tag/Parameter ≠ DomainRecord؛ License ≠ Readiness؛ Decision approved ≠ Validity at execution.

### ۱.۱. دادهٔ حداقلی شرکت

در آغاز ساخت Tenant فقط شرکت و مدیر معتبر و تنظیمات لازم لازم‌اند. Site، Resource، Part، Operation، Shift، سالن، چیدمان سه‌بعدی، برنامهٔ سالانه و سنسور **اجباری برای ساخت شرکت نیستند**. هر Capability در زمان استفاده، نیاز مشخص خود را اعلام می‌کند.

| Capability | لازم هنگام استفادهٔ معتبر | اختیاری |
|---|---|---|
| `production.record` | Actor/Permission، Site، Resource، زمان، نتیجهٔ دارای مبنای درست | برنامهٔ رسمی، Hub، OEE، شیفت و OP طبق قرارداد جاری |
| `maintenance.request` | Actor مجاز، Resource فعالِ همان Tenant، شرح، زمان ثبت | Sensor، Planning، عکس، PM، قطعات |
| `maintenance.work` | Request معتبر، انجام‌دهنده و شاهد نتیجه؛ قواعد مربوط به مخاطره | موجودی قطعه، Training، PTW (عدم وجودشان **کنترل ایمنی را حذف نمی‌کند**) |
| `maintenance.equipment_history` | ResourceRef و Permission خواندن | سه‌بعدی |
| `production.summary` | Entitlement/Permission + محدودهٔ مجاز | OEE |

از `requiredFor` موجود در `src/company/definition-catalog.ts` الگو بگیریم: لازم‌بودن داده برای Capability هرگز به معنی اجباری‌شدن آن برای ذخیرهٔ Person/Resource نیست.

## ۲. ثبت ماژول در کد مورد اعتماد

به جای اجرای کد/اسکریپت دلخواه مشتری، Descriptorهای TypeScript را در startup ثبت و اعتبارسنجی کنیم. Contract version نمونه `host.module.v1` است؛ Release ماژول مستقل از PolicyVersion/SchemaRevision باشد.

```ts
type CapabilityStatus = {
  key: string;
  licensed: boolean;
  enabled: boolean;
  compatible: boolean;
  ready: boolean;
  issues: Array<{
    code: string;
    scope: "company" | "site" | "resource" | "person";
    subjectId?: string;
    status: "missing" | "invalid" | "unavailable";
    resolution: "open_settings" | "contact_admin" | "retry";
  }>;
};
type ModuleDescriptor = {
  contractVersion: "host.module.v1";
  moduleKey: string;
  release: string;
  compatibleHostMajor: number;
  capabilities: string[];
  requiredModules: string[];
  optionalModules: string[];
  requiredPermissions: string[]; // معرفی، نه grant خودکار
  queryPortIds: string[];
  actionPortIds: string[];
  eventTypeIds: string[];
  uiContributionIds: string[];
  readinessResolverId: string; // فقط ID یک تابع Trusted Server
};
```

قواعد اعتبارسنجی Registry: تکرار `moduleKey`، Port نامعتبر، Permission ناشناس، Component ناشناس، Contribution بدون مالک، ناسازگاری Host Major و وابستگی سختِ حلقوی باید **startup fail** بدهند. از metadata مشتری، SQL، تابع JS یا import آزاد نسازیم.

### ۲.۱. ثبت دو ماژول

**Production موجود:** ماژول `production` اکنون `ready` است و `reports` بسته‌بندی وابستهٔ فعلی دارد. مسیرهای ثبت، شمارش، نسخه، اصلاح و گیت‌های مجوز کنونی را **حفظ** کنیم. تنها در Registry برای `production.record` و `production.history` و `production.summary` Adapterهای trusted و Query/Actionهای امن معرفی می‌کنیم؛ گزارش تازه از مسیر موجود `ProductionService` ثبت شود، نه یک ثبت موازی.

**Maintenance سبک:** در `src/company/module-catalog.ts` اکنون `maintenance` برابر `pilot_only` و در تعریف میز، ویجت `maintenance` آینده‌نگر است. ابتدا در حالت `pilot_only` برای آزمایش‌های داخلی ساخته شود. فقط بعد از گذر کامل آزمون، تأیید مالک و بررسی مجوزها، تغییرِ `readiness` به `ready` و نمایش برای خرید/فعال‌سازی در شرکت مجاز است. Capabilityهای این مرحله:
- `maintenance.request`: گزارش، مشاهده و بررسی خرابی؛
- `maintenance.triage`: درخواست توضیح، تصمیم مسئول و ارجاع گروهی؛
- `maintenance.work`: WorkOrder، ثبت اقدام و شاهد، تحویل و بستن؛
- `maintenance.equipment_history`: Query/Section مجازِ Resource.

PM زمان‌دار، Inventory، Costing، APM، کامل‌کردن PTW، کنترل CNC، Workflow Designer و OEE **در این مرحله اجرا نمی‌شوند**. نبود Production مانع درخواست خرابی دستی نشود.

### ۲.۱.۱. نمونهٔ Descriptor قابل پیاده‌سازی

ساختار زیر فقط IDهای registered trusted را معرفی می‌کند، **نه نام تابع JS ارسالی مشتری**. `requiredModules:[]` برای Maintenance به معنای عدم وابستگی اجباری آن به Production، OEE یا Training است:

```json
{
  "contractVersion": "host.module.v1",
  "moduleKey": "maintenance",
  "release": "0.1.0-pilot",
  "compatibleHostMajor": 1,
  "capabilities": [
    "maintenance.request",
    "maintenance.triage",
    "maintenance.work",
    "maintenance.equipment_history"
  ],
  "requiredModules": [],
  "optionalModules": ["production", "training", "inventory", "oee"],
  "requiredPermissions": [
    "maintenance.request.create", "maintenance.request.reply",
    "maintenance.request.cancel", "maintenance.request.view_own",
    "maintenance.request.view_scope", "maintenance.resolve_direct",
    "maintenance.triage", "maintenance.assign", "maintenance.perform",
    "maintenance.work.cancel", "maintenance.work.view",
    "maintenance.review_close", "maintenance.summary",
    "maintenance.policy.manage", "tasks.read_own", "tasks.claim",
    "tasks.decide", "notifications.read_own", "assignment.groups.manage"
  ],
  "queryPortIds": [
    "maintenance.request.list", "maintenance.request.get",
    "maintenance.work.get", "maintenance.resource.history", "maintenance.summary"
  ],
  "actionPortIds": [
    "maintenance.request.report", "maintenance.request.reply_info",
    "maintenance.request.cancel", "maintenance.request.triage",
    "maintenance.request.resolve_direct", "maintenance.work.assign",
    "maintenance.work.start", "maintenance.work.complete",
    "maintenance.work.review_close", "maintenance.work.reassign",
    "maintenance.work.cancel", "maintenance.policy.update"
  ],
  "eventTypeIds": [
    "maintenance.request_reported.v1",
    "maintenance.request_info_requested.v1",
    "maintenance.request_replied.v1",
    "maintenance.request_rejected.v1",
    "maintenance.request_cancelled.v1",
    "maintenance.request_resolved_direct.v1",
    "maintenance.work_created.v1",
    "maintenance.work_assigned.v1",
    "maintenance.work_reassigned.v1",
    "maintenance.work_started.v1",
    "maintenance.work_completed.v1",
    "maintenance.work_returned.v1",
    "maintenance.work_closed.v1",
    "maintenance.work_cancelled.v1"
  ],
  "uiContributionIds": ["maintenance.request.form", "maintenance.resource.history", "maintenance.inbox", "maintenance.summary.kpi"],
  "readinessResolverId": "maintenance.readiness.v1"
}
```

**محدودیت:** این نمونه فهرست کامل Permissionهای پایلوت را نشان می‌دهد؛ هر Action واقعی در Registry باید Handler مورد اعتماد و مجوز متناظر داشته باشد، و تفکیک Permission هر endpoint در [فایل ۰۲، بخش ۶](02-CODEX-WORK-PACKAGES.fa.md) مالک است. Permissionهای مشترک Task/Notification متعلق به Host هستند؛ ذکرشان در Manifest یعنی dependency/eligibility و **نه مالکیت داده یا grant خودکار**. Descriptor ناقص یا ناشناخته در Startup رد شود. در آغاز Runtime ماژول همچنان `pilot_only` است.

**Production Adapter:** شناسهٔ `production.record` به API موجود Production وصل شود، `production.history` به مسیر گزارش‌های موجود و `production.summary` به Query تجمیعی فعلی؛ هیچ `ProductionReport` دوم ساخته نشود و وابستگی Production به Maintenance اضافه نشود.

### ۲.۲. Readiness و پاسخ

Endpoint نامزد `GET /api/v1/company/module-capabilities` (یا مسیر سازگار موجود پس از بررسی Route Register) برای Actor مجاز، `ModuleDescriptor` عمومی و `CapabilityStatus` مجاز را می‌دهد؛ نباید فهرست Person/Resource محرمانه را در پیام خطای Readiness افشا کند. قابلیت خریداری‌شده ولی ناکافی به صورت `ready:false` با دلیل و مسیر تکمیل نشان داده می‌شود، نه اینکه بی‌سروصدا فعال شود.

Readiness در زمان نمایش UI تنها یک راهنماست؛ **در زمان اجرای Action دوباره** permission، entitlement، revision، scope و پیش‌شرط Domain بررسی شوند. اگر ma​intenance خاموش شد، عملیات تازه `403/409` مناسب بگیرد ولی خواندن سابقهٔ مجاز طبق Retention باید مسیر مستقل داشته باشد.

## ۳. سه شیوهٔ توسعهٔ اطلاعات

| روش | نمونه | قاعدهٔ مالکیت |
|---|---|---|
| `Master Field Extension` | مشخصهٔ مجاز و غیرمحرمانهٔ Resource | همان ID Resource؛ Definition trusted، Migration و Validator |
| `Module Domain Entity` | MaintenanceRequest، WorkOrder، TechnicalAction | جدول مستقل مالک ماژول و API اختصاصی |
| `Profile Section / Query` | سوابق تعمیر دستگاه، سابقهٔ صلاحیت فرد | داده کپی نمی‌شود؛ Query با Scope از صاحب دامنه |

**حقوق کارگر**، مدارک منابع انسانی و ارزیابی صلاحیت را به صورت فیلد آزاد در `people` نریزیم. حقوق متعلق به Payroll/Costing یا منبع بیرونی معتبر با محرمانگی و تاریخ اثر است. Training از `people.id` استفاده می‌کند ولی Assessment/Qualification تخصصی مستقل دارد.

در پایلوت فعلی هیچ Field Extension تازه‌ای بر `people` یا `resources` ضروری نیست؛ بنابراین `masterDefinitionExtensions` فعلی را **حفظ و بی‌دلیل تغییر ندهیم**. مسیر توسعهٔ موجود برای ماژول‌های آینده باید در تست Contract ثابت بماند.

## ۴. DomainRef / Action / Result

```ts
type DomainRefBase = {
  ownerModule: string;
  entityType: string;
  entityId: string;
  tenantId: string;         // از Server Context تطبیق داده شود
};
type DomainRef = DomainRefBase &
  ({referenceMode:"live"; revision?:never} |
   {referenceMode:"revision"; revision:number});
type ActionRequest<T> = {
  contractVersion: "domain.action.v1";
  requestId: string;           // UUID، ردیابی
  idempotencyKey: string;      // کلید ثابت در Retry
  correlationId?: string;
  subject?: DomainRef;         // برای تغییر رکورد موجود الزامی است
  contextRefs?: DomainRef[];   // برای create: Resource/Person/Parent موجود
  expectedRevision?: number;  // برای تغییر رکورد موجود
  input: T;
};
type ActionOutcome =
  | {status:"applied"; requestId:string; resultRef:DomainRef; resultRevision:number}
  | {status:"pending"; requestId:string; statusRef:DomainRef}
  | {status:"rejected"; requestId:string; code:string}
  | {status:"conflict"; requestId:string; code:string};
```

**قانون تفکیک Create و Update:** برای ساخت `MaintenanceRequest`، هنوز Request ID وجود ندارد؛ بنابراین `subject` نباید با شناسهٔ ساختگی مقداردهی شود. در action `maintenance.request.report`، `subject` حذف و `contextRefs` شامل Resource معتبرِ همان Tenant است؛ نتیجه `resultRef` به Request تازه اشاره می‌کند. در `triage/reply/resolve/assign` روی رکورد موجود، `subject` از نوع `revision` با `expectedRevision` معتبر الزامی است. برای `referenceMode:"revision"` وجود `revision` مثبت الزامی است؛ برای `live` ارسال revision رد شود. Resolver باید Parent/Context را با ACL بررسی کند. JSON ارسالی کلاینت برای Actor یا Tenant مرجع اعتبار نیست.

**مهم:** این مدل برای **TypeScript internal ports** و پاسخ‌های typed است؛ در این فاز Endpoint عمومی `/actions/execute` که arbitrary action اجرا کند نسازیم. هر ماژول HTTP مشخص دارد و به Server Actor متصل است. `tenantId`، `actorId`، Role و Permission از JSON مرورگر قابل اعتماد نیستند و با نشست تطبیق داده می‌شوند.

کلید Idempotency در محدودهٔ `tenant + actorUserId + actionKey + idempotencyKey` یکتاست؛ درخواست با همان کلید و Canonical Payload برابر باید همان نتیجهٔ پایدار را برگرداند، با Payload مختلف `409 key_payload_mismatch`. Receipt موفق، تغییر Domain و Outbox در **یک تراکنش Tenant DB** ثبت شوند. تا پایان دورهٔ نگهداری رکورد اثرگذار، کلید از بین نرود؛ سیاست کوتاه‌کردن عمر کلید نیازمند تصمیم/تست جداست.

`expectedRevision` برای انتقال وضعیت بررسی و تغییر با Lock/CAS اعمال شود؛ تعارض `409 stale_revision`. `unknown_to_caller` در قطع ارتباط یک **وضعیت مشاهدهٔ Client** است، نه نتیجهٔ پایدار Action؛ UI کلید قبلی را Retry/Status Inquiry کند، نه ساخت درخواست جدید.

خانوادهٔ خطاها: `permission_denied`، `module_not_licensed`، `module_not_implemented`، `module_not_ready`، `invalid_reference`، `subject_missing`، `stale_revision`، `key_payload_mismatch`، `prerequisite_invalid`، `invalid_transition`، `invalid_assignment`، `self_approval_forbidden`، `retryable_failure`. کدهای HTTP: `400` malformed، `401` unauthenticated، `403` unauthorized/licence، `404` invisible or missing، `409` conflict/state، `422` prerequisite، `503` unavailable. برای امنیت، 404 کاربر نامجاز نباید وجود رکورد را افشا کند.

### ۴.۱. مسیر داده و فرمان

- Source/Tag با event-time، received-time، quality و provenance وارد Hub می‌شوند؛ Parameter معنی شرکت/تجهیز را می‌دهد؛ Module با Port معتبر آن را مصرف می‌کند؛ Widget از Query مجاز می‌خواند. **قطع دیتا = صفر یا توقف قطعی دستگاه نیست.**
- ثبت دستیِ گزارش تولید یا درخواست خرابی، رکورد Domain است نه Tag مصنوعی.
- در این Pilot **هیچ درخواست خودکار از یک Tag خام** ساخته نمی‌شود؛ تشخیص خرابی و ضدتکرار الگوریتم اختصاصی در فاز بعد است.
- TAG.OUT، دریافت ACK و ارسال فرمان PLC نیز کاملاً خارج از فاز Pilot هستند؛ Desk یا Notification نباید کنترل ماشین را وانمود کند.

## ۵. نیاز به تضمین‌های زمانی و امنیتی

Timestampهای لازم را از هم تشخیص دهیم: `recordedAt` (ثبت سیستم)، `observedAt` (زمان گزارش/رخداد)، `effectiveAt` (اثر سیاست/وضعیت) و `createdAt`. APIهای پایلوت زمان UTC ISO8601 برگردانند؛ Site Timezone برای نمایش محلی استفاده شود. Domainهای حساس نمی‌توانند وضعیت «شرایط بیرونی نامعلوم» را `valid_now` فرض کنند.

Tenant DB تراکنش‌ها را نگه می‌دارد؛ Control DB مالک Accounts/Entitlements است. بین آن دو **اتمی‌بودن جهانی وعده داده نشود**؛ نزدیک لحظهٔ تغییر Domain، Entitlement و Permission بازبینی شود. جلوگیری از تعارض داخل Tenant DB با Lock/Revision است. Actionهای Maintenance هرگز به SQL جداول خصوصی Production دسترسی مستقیم نداشته باشند؛ از Query/Port معتبر یا ref قابل بررسی استفاده کنند.

## ۶. معیار پایان قرارداد ۰۱

اگر مصرف‌کننده‌ای بتواند تنها با دانستن `ModuleDescriptor`، `CapabilityStatus`، `DomainRef`، Action/Result و Queryهای typed از ماژول جدید استفاده کند، بدون دست‌زدن به جداول خصوصی یا ساخت هویت دوم، بخش Registry/DomainRef قرارداد هدف را پاسخ می‌دهد. **این شرط هنوز به معنای تست‌شدن نیست.**

نقطهٔ ورود برای بخش بعد: [قرارداد و مسیر اجرای Task، Notification و UI + بسته‌های Codex](02-CODEX-WORK-PACKAGES.fa.md)؛ آزمون‌های قابل اثبات در [فایل ۰۳](03-DEMO-AND-ACCEPTANCE.fa.md) هستند.
