# ممیزی لینک‌های اسناد

> **Status:** Static Markdown relative-link check · **Source:** b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f · **Date:** 2026-11-02

## پوشش

**۹۴ از ۹۴ فایل Markdown** در docs و راهنماهای ریشه، با خواندن محتوا و تطبیق مقصد لینک‌های عادی نسبیِ Markdown با tree بررسی شدند. **۳۲ فایل دیگر** بیشتر JSON، HTML، Python و اسکریپت‌اند؛ برای آن‌ها آزمون لینک HTML/وابستگی اجرا نشد. در اسناد جاریِ اصلی مقصد نسبی گمشده پیدا نشد. شش anchor پرتکرار به بخش‌های PRODUCT-BLUEPRINT نیز با عنوان مقصد تطبیق داده شدند.

**۴۰ ارجاع نسبی به مقصد گمشده پیدا شد:** ۳۴ مورد در snapshotهای تاریخ‌دار جابه‌جا‌شده در `docs/archive/state-2026-10-19/` و `state-2026-10-28/`؛ ۶ مورد تصویر خصوصی `.local/qa/phase2/*.png` در گزارش تحویل فاز ۲، که داخل Git نیستند.

| شاهد | مسئله |
|---|---|
| [Archive Architecture:133](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/archive/state-2026-10-28/ARCHITECTURE.md#L133) | `../packages/telemetry-contract/README.md` در مکان جدید نسبی نیست |
| [Archive Current State:257](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/archive/state-2026-10-28/CURRENT-STATE.md#L257) | `product-notes/DATA-POINTS-AND-CONSUMERS.fa.md` نسبت به محل اصلی نوشته شده |
| [Archive Decisions:35](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/archive/state-2026-10-28/DECISIONS.md#L35) | `TENANCY-IDENTITY-DESIGN.md` کنار نسخه آرشیوی نیست |
| [Archive Start:5](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/archive/state-2026-10-19/START-HERE.md#L5) | اشاره به مسیر سابق package telemetry |
| [Phase2 Delivery:86–88](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/archive/deliveries/PHASE2-DELIVERY.md#L86-L88) | ۶ تصویر QA خصوصی در Git وجود ندارند |

[archive manifest](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/docs/archive/state-2026-10-28/manifest.json) می‌گوید لینک‌ها باید با مکان **اصلی** تفسیر شوند و snapshotها hash-محافظت‌شده‌اند. بنابراین این خطاها **نقص ناوبری تاریخچه** هستند، نه الزاماً خطای اسناد اجرایی جاری. مسیر امن: فهرست resolver خارج از snapshot و ثبت وضعیت unavailable برای تصاویر خصوصی. متن‌های تاریخی را صرفاً برای ظاهر شدن لینک دستکاری نکنید.

**محدودیت فنی:** پیوندهای بیرونی اینترنتی، لینک‌های HTML، ارجاعات صرفاً متنی یا code span، تمام heading anchorها و runtime از این check نتیجه نمی‌شوند.
