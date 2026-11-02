# نقشه مفهومی SFP24

> **Status:** Proposed · **Owner:** Core · **Updated:** 2026-11-02

```mermaid
flowchart TB
 subgraph CORE["Platform Core / Shared Contracts"]
  A["Tenant / Person / Account"]
  B["Organization / Responsibility / Scope"]
  C["Entitlement / Permission"]
  D["Tag / Parameter / Typed Data"]
  E["Module & Capability Registry"]
  F["Profiles / Desks / Dashboards"]
  G["Versioned Ports / Events"]
 end
 subgraph MODULES["Domain Modules — examples"]
  P["Production"]
  T["Skill Gap / Training"]
  O["OEE"]
  M["Maintenance"]
  R["MRP"]
  L["Planning"]
 end
 E --> MODULES
 D --> MODULES
 MODULES <--> G
 MODULES --> F
 A --> B
 B --> C
 C --> F
```

**تفکیک حیاتی:** Person ≠ Account ≠ Position ≠ Responsibility ≠ Permission ≠ Qualification؛ Tag ≠ Parameter ≠ Business Record؛ Dashboard ≠ محاسبه رسمی KPI.

**آزمون فشار:** کارگاه بدون برنامه و بدون تگ، اضافه‌شدن EdgeBox، فرد چندمسئولیتی، شرکت چندسایتی، ماژول Skill Gap مستقل از Production، MRP با Forecast و Order، شرکت‌های مستقل با قرارداد تبادل.

این نمودار طراحی احتمالی است، **نه وضعیت ساخته‌شده**. [Open Questions](OPEN-QUESTIONS.md) · [Sources](../sources/README.md).
