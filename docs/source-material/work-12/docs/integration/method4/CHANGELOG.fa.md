# تغییرات بستهٔ قرارداد

## 1.1.0 — ۲۰۲۶-۱۰-۱۸

تحویل اجرایی WEB و DDL دقیق A1، control migration8 / tenant migration10 / component schema1. قرارداد wire و storage پایه1.0.0 باقی است؛ نسخهٔ1.0.0 بستهٔ اسناد صرفاً طرح بود و schema اجرایی تحویل نداده بود. بستهٔ جدید باید با manifest جدید کامل کپی شود؛ hash قدیمی را نگه ندارید.

افزوده‌شده: STORAGE-CONTRACT، RUNBOOK، storage-v1.json و ابزار export/check. روشن‌شدن ترتیب قفل/تعلیق/rotation، vault و SQL user مستقل worker، reuse جدول evidence تولید، صف فرمان عامل، APIهای واقعی، محدودیت نسخهٔ اول و وضعیت B3. watcher تولید روی SQL پایدار است و registry long-poll دارد. receiver قدیمی از runtime پیش‌فرض WEB خارج و فقط برای آزمون regression نگهداری شده است.

## 1.0.0

طرح روش۴، سناریو، مسئولیت‌ها، نمونهٔ ساختگی پیام و رسید و manifest قابل‌بررسی با عادی‌سازی پایان‌خط؛ بدون پیاده‌سازی schema/worker جدید.
