# قراردادها — موجود در برابر پیشنهادی

## قراردادهای وابسته به نسخهٔ فعلی کد

| موضوع | مرجع و حدود اعتبار |
|---|---|
| حساب، هویت و scope | [مرجع هویت](../core/IDENTITY-AND-ACCESS.fa.md)؛ جزئیات رفتار به کد b3f203b متصل است |
| تگ، پارامتر و مصرف تولید | [مرجع داده](../core/DATA-AND-PARAMETERS.fa.md) و [راهنمای تولید](../operations/guides/PRODUCTION-DATA-SOURCES.md) |
| snapshot امضاشدهٔ تله‌متری | [تله‌متری و مرز Runtime](TELEMETRY.fa.md)؛ بایت مرجع فقط در package مخزن کد |
| registry فیلد/صفحه داخل کد | [گسترش تعاریف](../core/EXTENSIONS.fa.md)؛ SDK نصب عمومی نیست |

## Draftهای آینده

- [Module & Capability](MODULE-CONTRACT-DRAFT.md)
- [Data Contract](DATA-CONTRACT-DRAFT.md)
- [UI Contributions](UI-CONTRIBUTIONS-DRAFT.md)

این Draftها SDK/API مصوب عمومی نیستند و قرارداد موجود را بی‌صدا supersede نمی‌کنند. قبل از تثبیت، Production و حداقل یک مصرف‌کنندهٔ مستقل دیگر باید سنجیده شوند؛ تغییر ناسازگار نسخه، اثر migration و آزمون لازم دارد.
