# Phase 3B — operational company workflow checkpoint

Owner's pasted mission (2026-10-14) authorizes implementation on `feat/phase3-company-accounts`. Baseline HEAD `71e80a5`; five local commits preserved. Remote fetched; 5 ahead, 0 behind. No merge/stash/delete/deploy authorized. Pre-existing untracked `docs/design/reference/README.md` is not part of this work.

Read remote `docs/module-readiness-onboarding:docs/PHASE3B-MODULE-READINESS-ONBOARDING.md` without merging. Its proposal-only wording and open questions are superseded **only where the new owner mission explicitly decides**: independent per-user scoped permissions, multirow drafts/final reports, good output + final scrap, auditable correction, no mandatory approval, CSV first permitted. Other future-module suggestions remain proposals.

## Ordered execution

1. Verify/push the preserved Phase 3A baseline and inspect CI.
2. Add control permission registry/rules migration; templates preserved, direct rules override that permission's template, deny wins within matched scope. Preserve at least one active company-wide user manager independent of job/role title. Provider support remains metadata/user-only.
3. Add shared tenant master-data migrations/services: sites, optional physical areas, distinct equipment/line/station resources, parts, OPs, people with optional login link, shifts/calendar, scrap reasons. Soft disable and stable identifiers/snapshots preserve history.
4. Add readiness contract and production service/API: multiple rows, drafts, idempotency/version checks, personal attribution, timezone/overnight intervals, pending part names, consistent scrap-reason counts, finalization, correction requests and audited revisions. Tenant DB only; no simulator data, targets/OEE or attendance inference.
5. Integrate company navigation, setup, independent permissions editor, mobile production form and real filtered reports. Same authenticated workspace; retain account/password flows.
6. Run positive/negative real MariaDB tests, two-company isolation, scopes, last-manager/capacity, persistence/revisions, and connected browser/mobile QA. Apply tested migrations to approved local test environment after private backup; do not reset owner's password or migrate Phase 2 data.
7. Only after P0 passes: actual parts CSV preview/mapping/confirm/export, controlled real dashboard linkage, simple persisted widget preferences. Record P1 gaps honestly. P2 remains adapter contracts/documentation only.
8. Commit in small verified steps; normal push on same branch, inspect/wait for CI including real MariaDB. No completion claim for untested features.

## Implementation notes / decisions

- Permission catalog is code-extensible and seeded into central schema; no arbitrary user-supplied permission keys or provider privileges. Administrative user management is company-wide; operational actions can be scoped to site/area/resource. A rule for a permission overrides that permission's role template; removing all rules restores inheritance. Explicit denies take priority. Resource IDs are validated against the same tenant DB.
- Operational records use typed relational tables. Revision JSON is an audit snapshot, not the authoritative operational database. Good + final scrap is computed per row; cohorts stay separated by resource/part/OP/unit, never a finished-goods total across sequential operations.
- Manual intervals are declared work-report periods, not machine running time or attendance. No automatic hourly allocation of shift quantities. Daily reports use report date; timestamps carry site timezone/UTC and overnight dates explicitly.
- Master data and people/shift services are shared, not copies per module. No site, fake machine or simulation is automatically created for a new company.
- Production capture and own/detail reports depend on `production`; aggregate reporting depends on `reports`. Core setup/access does not require buying planning/quality/OEE. Capability availability, license, permission, prerequisites and data sufficiency remain separate.

## Current checkpoint

Baseline pushed at 71e80a5; GitHub Actions 38627374062 (standard) and 38627373958 (real MariaDB) both succeeded. Foundation committed at 86d340d. Production/master/access HTTP APIs and tenant migration 3 now implemented. Full isolated MariaDB suite: **63 passed, 0 skipped**, including two fresh operational companies, 120+3, drafts, multirow OP cohorts, auditable corrections, scoped permissions, multiple effective managers, capacity, persistence through fresh server/storage instances and license revocation. Fixed a duplicate SQL result-column alias found by those integration tests. UI integration is in progress; no P0 browser completion claim yet. The owner control/tenant databases have NOT yet been upgraded; existing running API/worker are preserved until the complete slice is verified.

## 2026-10-15 UI / local environment checkpoint

- Backend slice committed `b68359f`. Scoped policy is shared as a pure TypeScript function between server and UI; backend remains authoritative.
- New bounded Vue components under `src/company/`: navigation/readiness, shared master-data forms, scoped permission editor, multirow production editor, record/history/correction views and actual ECharts daily summary. Existing account/password/provider flows are reused.
- Connected browser P0 passed against a **separate disposable real MariaDB control/tenant fixture**, not mocked data: master data, scoped operator grants with viewer template, linked person, mobile 120+3=123 plus explicit-zero second row, draft/resume/final, correction request and manager 125+2=127 revision, real summary/filter change. Persian desktop/tablet/mobile screenshots have no document horizontal overflow. Additional shift/calendar/disable coverage and final screenshot pass are in progress.
- Existing account-browser regression passed: add/edit company, no-email activation, password change/reset, suspend/resume and provider support. Existing account owner password was not used/reset.
- Actual fixture API stop/restart plus fresh browser retained records/revisions. Chart QA passed exact hover values, interactive legend/series toggle, real wheel data zoom and reset across five stored report dates.
- Visual review found legacy form CSS stacking all report filters vertically and fieldset columns affecting mobile; corrected scoped CSS. Second density refinement puts chart beside summary cards on desktop. Browser tests also exposed an async detail-load race clearing correction text; fixed by showing the dialog only after all data load.
- One parallel local DB run hit the Portable instance's 32-connection cap. No service settings were changed. Stopped only the disposable QA API and reran suite sequentially: **63/63 passed, zero skips**. Added shared opening-pool protection and a concurrent-connection assertion; final rerun pending.
- Private logical backup of approved local control plus **five** existing tenant databases completed before additive migration. Control v4 / tenant v3 and least-privilege grants applied; approved API 5186/worker restarted, web 5176 and MariaDB 3317 retained. No Phase 2 transfer or credential reset. Final source refresh still needed after remaining fixes.
- P1 CSV import/export, persisted dashboard builder and controlled Phase 2 scene linkage are **not implemented**. P2 remains documentation-only; no hardware/ERP connection.

## First P1 adapter checkpoint — 2026-10-15 (supersedes CSV gap above)

Parts CSV v1 implemented: bounded UTF-8 parse (500 rows / 200 KB), template download, comma/semicolon/tab, code/name/unit mapping, row errors, preview with no catalog writes, actor-bound 30-minute batch, explicit atomic confirmation via shared MasterService, idempotent replay and formula-safe export. Tenant forward migration 4 adds `import_batches`; no account redesign. Real MariaDB suite **68/68 passed, zero skips**; browser template/upload/mapping/invalid+valid preview/confirm/replay/export/mobile flow passed. Build passed. Final full rerun pending after oversized-body error refinement. Private backup + v4 upgrade of approved owner-test tenants completed; API/worker refreshed. Remaining P1: persisted dashboard builder and controlled Phase 2 scene/data linkage, XLSX/other entity imports. P2 stays contracts only.

## Final local acceptance checkpoint

Final full regression including oversized request handling: **68/68 passed, zero skips**. Production build/typecheck passed. P0 + CSV browser scripts reran successfully with v4 tenant schemas, night shift, quick creation/soft disable and compact review/confirmation. Original Phase 2 three modes passed 1366×768 and 1920×1080 document overflow checks; actual canvas pointer raycasting selected another equipment and wheel changed the real camera rendering. This used a fresh **in-memory** Phase 2 API on 5188, closed after the test; the owner's stored pilot/simulator was not read or changed. The company summary now fits the first 1366×768 viewport; explicit Persian/1920 document-height assertions are in the final chart QA. Snapshot review led to collapsing CSV configuration after preview, keeping confirmation visible, and reducing legacy spacing; no dashboard content was hidden to mask overflow. Final normal push/CI wait remains before handoff.

## Git / CI acceptance

Four implementation commits normally pushed, ending at `17b4f24`; local/remote 0 ahead / 0 behind. GitHub [MariaDB CI 38639227439](https://github.com/hossein-aghaie/pouyeshgar-workshop/actions/runs/38639227439) and [standard CI 38639227577](https://github.com/hossein-aghaie/pouyeshgar-workshop/actions/runs/38639227577) both **completed successfully for that exact SHA**. Final Persian/1920 chart document-height assertions passed. Final documentation-only acceptance record follows this code commit; no further feature work was started. [PHASE3B-DELIVERY.md](PHASE3B-DELIVERY.md) is the concise Persian handoff and explicit remaining P1/P2 scope. Pre-existing untracked `docs/design/reference/README.md` remains untouched and unpushed; Stash retained. Approved manual-test services are running; disposable QA servers will be stopped before handoff.
