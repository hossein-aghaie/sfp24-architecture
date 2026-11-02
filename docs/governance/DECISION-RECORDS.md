# Architecture Decision Records

قالب: `docs/decisions/ADR-XXXX-topic.md`. شماره یکتا؛ وضعیت Proposed/Approved/Rejected/Superseded.

هر سند: Context، Evidence همراه نسخه، Alternatives، Decision با تأیید، Reasons، Trade-offs، Rejected paths، Consequences، Revisit trigger، لینک Implementation/Tests.

اگر تصمیم تغییر کرد، **سابقه را پاک نکنید**. تصمیم قدیمی Superseded و با پیوند به جانشین ثبت شود. [فهرست ADR](../decisions/README.md).

## تصمیم تخصصی یک ماژول

قالب بالا دربارهٔ تصمیم مشترک هسته و کل محصول است. تصمیم فقط مربوط به یک ماژول در `docs/modules/<module>/decisions/<module>-NNNN-topic.md` ثبت می‌شود و از فهرست تصمیم‌های همان ماژول لینک می‌گیرد. فهرست‌های موجود مانند DECISIONS آموزش تغییر محل نمی‌دهند. شناسهٔ تصمیم حوزه‌ای با شناسهٔ ADR مشترک اشتباه نشود.

اگر اثر تصمیم از ماژول فراتر می‌رود، موضوع برای تصمیم مشترک ارجاع داده شود؛ تصمیم تخصصی به‌تنهایی قواعد هسته را تغییر نمی‌دهد. در هر دو حالت، لینک گفتگو، تحقیق، آزمون و دلیل رد گزینه‌ها ضروری است. [محل ثبت اسناد](DOCUMENTATION-POLICY.md) · [درخواست تغییر مشترک](CHANGE-WORKFLOW.md).
