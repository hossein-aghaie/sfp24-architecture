# فناوری‌های استفاده‌شده در SFP24

**پاسخ کوتاه برای ارائه:** رابط با Vue 3 و TypeScript، نمایش سه‌بعدی با Three.js، نمودار با ECharts، بک‌اند با Node.js و Fastify و ذخیره‌سازی جاری با MariaDB ساخته شده است. پروژه یک monorepo با فرایندهای WEB و INGEST جداست؛ موتور عمومی نصب افزونه هنوز ساخته نشده است.

مبنای این جدول: خواندن کد `pouyeshgar-workshop @ b3f203b`، نه ادعای آزمون تازهٔ استقرار. نسخه‌های زیر نسخه/بازهٔ اعلام‌شدهٔ پروژه‌اند؛ فهرست کامل حل‌شده در lockfile همان نسخه است.

| لایه | فناوری و نسخهٔ اعلام‌شده | استفاده |
|---|---|---|
| رابط | Vue 3.5.43 + TypeScript 5.9.3 | فرم‌ها، پنل شرکت، میزساز و state رابط |
| سه‌بعدی | Three.js با بازهٔ ^0.180.0 | صحنهٔ واقعی تجهیزات، انتخاب و نمای مکانی |
| نمودار | ECharts با بازهٔ ^6.1.0 | نمودار و تحلیل نمایشی |
| Build | Vite 7.3.7 + vue-tsc 3.3.13 | توسعه، build و بررسی نوع Vue |
| اجرای بک‌اند | Node.js 24.x طبق engines محصول | API، worker و دریافت HTTP |
| HTTP API | Fastify 5.12.5 | خدمات حساب‌ها و عملیات و دریافت |
| دیتابیس اصلی | MariaDB | دیتابیس کنترل + دیتابیس مستقل هر tenant |
| درایور DB | mariadb 3.5.4 | درایور Node؛ این عدد نسخهٔ خود سرور MariaDB نیست |
| زمان و تقویم | Luxon 3.7.2 و jalaali-js 1.2.8 | بازه‌ها، منطقهٔ زمانی و نمایش تقویم |
| فایل صفحه‌گسترده | ExcelJS 4.4.0 | ابزارهای import/export موجود |
| آیکون | lucide-vue-next 0.468.0 | آیکون‌های رابط |
| مدیریت بسته | pnpm 11.25.0 و workspace catalog | هماهنگی بسته‌های monorepo |
| آزمون | node:test / tsx، vue-tsc، تست MariaDB و QA مرورگر | شواهد هر اجرا جدا گزارش می‌شود |
| CI | GitHub Actions | workflowهای build/test؛ وجود CI به معنی استقرار خودکار نیست |

## دیتابیس و دریافت داده

MariaDB پایگاه دادهٔ جاری محصول است. نسخهٔ محیط لپ‌تاپ گزارش‌شده 11.4.10 است؛ نسخهٔ هر سرور دیگر باید در همان محیط بررسی شود. raw و مقدار معتبر هاب در دیتابیس همان tenant ذخیره می‌شوند؛ یک دیتابیس مشترک برای تمام شرکت‌ها نیست. [معماری و مالکیت داده](core/ARCHITECTURE.fa.md).

دریافت HTTP جاری در `services/ingest/edgebox` و `http-channels` است. کتابخانه‌های MQTT/Aedes و کد receiver آزمایشگاهی در monorepo وجود دارند؛ این موضوع **پذیرش عملیاتی عمومی تمام پروتکل‌ها** را ثابت نمی‌کند. SQLite متعلق به نمونه/لابراتوار تاریخی است و DB عملیاتی جاری محصول معرفی نمی‌شود.

## محیط اجرا و موارد آینده

| مورد | وضعیت |
|---|---|
| توسعه و پایلوت محلی Windows | محیط موجود با launcher محلی |
| Raspberry Pi 5 با RAM هشت گیگابایت | هدف اعلام‌شده؛ استقرار/کارایی نسخهٔ فعلی روی Pi در این صفحه تأیید نمی‌شود |
| AI Provider، RAG و Embedding | طرح مشترک؛ سرویس عملیاتی متصل نداریم |
| Vector DB یا PostgreSQL | وابستگی اجباری یا جایگزین خودکار DB جاری نیستند |
| شبیه‌ساز مستقل HTTP | ابزار Node.js جدا از WEB/DB؛ v1 و v2 |

برای ارائه به مشتری، «امکان آینده» را به‌عنوان فناوری نصب‌شده معرفی نکنید. [وضعیت محصول](STATUS.fa.md) · [طرح AI مشترک](core/KNOWLEDGE-AI.fa.md).

## شواهد قابل بررسی

- [package.json کد مبنا](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/package.json)
- [catalog نسخه‌ها](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/pnpm-workspace.yaml)
- [lockfile](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/pnpm-lock.yaml)
- [کاتالوگ INGEST](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/services/ingest/package.json)
- [CI حساب‌ها](https://github.com/hossein-aghaie/pouyeshgar-workshop/blob/b3f203bc74fe9ef92f6d0ef290fee44fb6a1932f/.github/workflows/company-accounts.yml)

[بازگشت به صفحهٔ اول](../README.md)
