# Unified Phase 2 tenant shell — execution checkpoint

Owner-authorized branch: `feat/unify-phase2-tenant-shell`, from `f629caa`. Phase 2/pilot/main/next and old stash are preserved. Pre-existing untracked `docs/design/` is not staged.

## Implemented and locally accepted

- Company sign-in now mounts the actual `App.vue`, not the parallel CompanyWorkspace home. Original sidebar, monitoring modes, Three.js, camera/selection and layers remain the product shell. Owner administration stays separate.
- Shared company forms (master data, users, multirow capture, records/corrections, CSV) are embedded in existing menu sections. Identity and manual/company provenance appear in the header.
- Company mode bypasses pilot LocalStorage layout and all simulator/pilot metric endpoints. Empty companies receive no 16-machine seed or simulator counts.
- Additive tenant migration 5 stores a versioned scene document in the company's own DB. Stable visual IDs equal operational resource IDs; authenticated context filters the scene. Whole-document edits need company-wide master management; tenant-reference checks, optimistic locking and audit apply.
- Layout UI reuses SceneView/TransformControls, explicit area/resource/model placement, dimensions, JSON export and validated import preview. Generic dimensions/shapes are explicitly provisional, not measurements.
- Original Analytics/Explore/Device components accept company-content slots. Manual summaries retain resource/part/OP/unit cohorts; unavailable OEE/runtime/telemetry stay unknown. Existing ECharts daily chart is reused.
- Daily presets query report dates. Hour/custom/shift filters include whole contained report intervals, never prorate manual counts. Shared filters reach report views too.

## Evidence so far

- Final typecheck/production build passed. Full real MariaDB suite passed **70/70, zero skips** after stopping the disposable QA API; isolated company scene/version/foreign ID/filter tests and overnight/calendar unit coverage pass.
- Original Phase 2 browser regression PASSED: three modes ×1366/1920, real canvas raycasting and camera zoom. Evidence remains `.local/qa/phase3b/pilot-regression`.
- Unified real MariaDB browser QA PASSED in `scripts/tenant-shell-qa.mjs`; images `.local/qa/unified-shell`. Actual UI entered 120 good +3 scrap. Six desktop monitoring screenshots, device, layers, FA/EN/tablet/mobile, re-login persistence, date filters, five-day tooltip/legend/zoom/reset, limited operator and second-company isolation passed with no JS errors or simulator calls. Corrected reactive cloning, form scroll sizing, crowded toolbar, chart overlap/height, mobile identity and detail camera framing.
- First full DB suite hit the independent portable instance's 32-connection limit because the disposable UI fixture was concurrently running. This is not a passing run. Stop ONLY the disposable fixture API (exec session 8192, stdin `stop`), then rerun sequentially. Do not alter the database connection limit or stop owner services.
- Existing approved Portable control +five tenant databases privately backed up and tenant v5 applied. Only tracked test API/worker refreshed; DB/web/live services/data/passwords/stash untouched. QA API5187 stopped after testing.

## Final handoff checks

1. Backend `76fd29f`, UI `d5ecdbd`, QA/docs `584b1ae`, mobile follow-up `12b70e5` committed and normally pushed. Both Actions passed on code acceptance `12b70e54e55e56ce4d6582844c082fee6b386ae3`: [UI/build](https://github.com/hossein-aghaie/pouyeshgar-workshop/actions/runs/38683048884), [real MariaDB](https://github.com/hossein-aghaie/pouyeshgar-workshop/actions/runs/38683049230). This final documentation checkpoint follows that code acceptance; no merge/force push/deploy.
2. Visual comparison `.local/qa/unified-shell/comparison.html`; actual screenshots remain ignored. Delivery facts and limitations are in `UNIFIED-SHELL-DELIVERY.md`.
3. Final mobile QA also asserts header action bounds; all browser cases passed again. The five approved existing tenant DBs were rechecked read-only at v5, company login returned HTTP200, and test API health is configured. Local/remote were synchronized after normal push; only pre-existing untracked `docs/design/` remains. Do not claim personal owner credentials or industrial production deployment were tested. New companies intentionally start empty; the 16-machine pilot remains in the labelled Demo.

Private credentials/DBs/backups/screenshots remain ignored under `.local`. QA fixture was started fresh on loopback 5187 (not owner API5186). No owner password is used.
