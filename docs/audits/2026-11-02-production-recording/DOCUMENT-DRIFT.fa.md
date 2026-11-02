# اختلاف‌های اسناد و تقدم مرجع — شرح مستند

> **Status:** Observation + suggested remedy · **Source:** b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f · **Updated:** 2026-11-02

## ۱. شاخه اجرای جاری

[START-HERE](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/START-HERE.md#L1-L15) و [README](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/README.md#L1-L5) و [AGENTS](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/AGENTS.md#L6-L7) مرحله ۰۳ را جاری اعلام می‌کنند؛ [DEVELOPER-GUIDE خط ۷](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/DEVELOPER-GUIDE.md#L7) و [CURRENT-STATE خط ۷](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/CURRENT-STATE.md#L7) مرحله ۰۲ را جاری نوشته‌اند. تاریخچه مرحله ۰۲ حذف نشود؛ عبارت «شاخه جاری» در دو سند دوم باید به وضعیت تازه متصل شود.

## ۲. میز قابل ذخیره در مقابل فرم و داده عملیاتی

[CURRENT-STATE ۷۹–۸۵](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/CURRENT-STATE.md#L79-L85) مرحله Preview در RAM و بدون ذخیره را می‌گوید. [سطرهای ۱۵۰–۱۵۴](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/CURRENT-STATE.md#L150-L154) ذخیره/اختصاص میز با کنترل نسخه و migration را بیان می‌کنند؛ در عین حال اقدامات داخل میزها همچنان شبیه‌سازی هستند. [UI-UX-SPEC ۵۴–۶۰](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/UI-UX-SPEC.md#L54-L60) و [۷۰–۷۴](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/UI-UX-SPEC.md#L70-L74) همین تاریخچه را لایه‌لایه نگه داشته‌اند.

**چکیده دقیق مورد نیاز:** saved desk configuration = موجود طبق گزارش تحویل؛ real domain widgets/dashboard engine = ساخته‌شده فرض نشود. متن تاریخ‌دار گذشته به عنوان evidence بماند.

## ۳. سند امضاشده rc.4 و پرونده تأیید

[contract README](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/packages/telemetry-contract/contract/README.fa.md) و [REVIEW](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/packages/telemetry-contract/contract/REVIEW.fa.md) سابقه Draft دارند؛ [manifest](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/packages/telemetry-contract/contract/manifest.json) بخشی از snapshot immutable است. [approval sidecar](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/integration/telemetry-execution-v2-approvals.json) با manifest hash ثابت ثبت کرده:
- status: `design-approved-awaiting-owner-implementation-instruction`
- hubReview: `approved-with-runtime-gates-not-run`
- ownerImplementationAuthorization: `false`
- runtimeEvidence: `not-run-not-authorized`

این یعنی **تأیید طراحی ≠ permission to implement ≠ runtime acceptance**. [VALIDATION](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/packages/telemetry-contract/contract/VALIDATION.json) فقط structural checks را PASS و SQL/DB/HTTP/MQTT/runtime را Not run می‌داند. اصلاح باید در navigation/status note باشد، نه محتوای hash-محافظت‌شده.

## ۴. یک شرکت، یک Tenant، یک کارخانه اکنون؛ Multi-site آینده؟

[Tenancy design](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/TENANCY-IDENTITY-DESIGN.md) چند شرکت مستقل زیر یک Tenant را رد می‌کند. [DECISIONS ۴۶–۴۸](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/DECISIONS.md#L46-L48) چند سایت بالقوه درون یک Tenant را مجاز دانسته، اما [DECISIONS ۹۲–۹۶](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/DECISIONS.md#L92-L96) **مدل فعلی** را یک کارخانه برای هر شرکت می‌داند. [CURRENT-STATE:34](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/CURRENT-STATE.md#L34) چندکارخانه را اجرایی نمی‌داند. این تفاوت، لزوماً دو تصمیم هم‌زمان متناقض نیست؛ مرز Scope و قابلیت گسترش باید روشن شود، وگرنه ایجنت آینده ممکن است از مدل فعلی الزام دائمی نتیجه بگیرد.

## ۵. دیگر خطرهای تعبیر

- [CURRENT-STATE:18](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/CURRENT-STATE.md#L18) تکمیل‌نبودن اتصال عمومی پارامتر را می‌گوید؛ [۱۱۲–۱۲۲](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/CURRENT-STATE.md#L112-L122) یک اتصال محدود شمارش تولید را تحویل‌شده گزارش می‌کند. **محدود با عمومی یکسان نیست**؛ اصلاح خلاصه به جلوگیری از سوءبرداشت کمک می‌کند.
- [README:24](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/README.md#L24) درباره نبود دمو و [operator-preview.ts](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/src/operator-preview.ts) درباره پیش‌نمایش عمومیِ ساختگی حرف می‌زنند. بدون آزمون مرورگر نمی‌توان دسترس‌پذیری واقعی HTTP را نتیجه گرفت.
- [CodeX handoff](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/CODEX-SMART-FACTORY-HANDOFF.md) مسیر تاریخی است و باید با اولویت اسناد فعلی خوانده شود.
- [method4 older contract](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/integration/method4/README.fa.md) و قرارداد `2.0.0-rc.4` هر دو برای فهم تاریخچه ارزش دارند، ولی یکی مرجع executable قرارداد جاری دیگری نیست.

**مرز ممیزی:** صرفاً متن، Git tree، Git SHA و نمونه‌های قابل مشاهده کد خوانده شدند؛ هیچ تست صنعتی تازه صورت نگرفت.
