# Phase 3A progress checkpoint — 2026-10-14

## Final synchronization and CI evidence

Owner lifted the synchronization hold and authorized normal Push. Same-branch merge `9b1a3a6` preserved Remote `0a2fe68` plus all local implementation commits, with no conflicts or history rewriting. Local 33-pass test run and TypeScript/build succeeded. Real disposable MariaDB 11.4 CI [38596701887](https://github.com/hossein-aghaie/pouyeshgar-workshop/actions/runs/38596701887) completed successfully: **42 tests passed, zero failed, zero skipped, build passed**. Standard CI [38596701728](https://github.com/hossein-aghaie/pouyeshgar-workshop/actions/runs/38596701728) also passed. No laptop DB/server changes, deployments, main/pilot/next merges, stash mutations or Force Push. Earlier hold/unverified notes below are historical checkpoints, superseded by this evidence. Connected laptop browser onboarding and production/backup/load readiness remain untested.

Owner requested implementation on existing `feat/phase3-company-accounts`, per-company MariaDB, provider/company identity and modular monolith boundaries. No agent delegation, deployment, main/next or historical stash mutations performed.

## Preserved state

- Local pilot branch has `4bad5f8` (double-click server tools); not overwritten or applied wholesale.
- Existing untracked `docs/design/reference/README.md` remains untracked; images, secrets and QA artifacts remain ignored.
- Old stash `codex-pilot-before-review` retained unchanged.
- `docs/DECISIONS.md` vs historical `docs/decisions.md` collided on Windows. Historical contents copied exactly from Git into `docs/decisions-legacy.md`; canonical upper-case document preserved. `.local/phase3-safety/DECISIONS-working-before-sync.md` also holds the colliding historical working copy.

## Implemented

Two commits initially `b381fcc` and `b3ef3e6`: normalized control/tenant schemas; migrations; safe CLI/bootstrap/provisioner; separate runtime DB grants; per-company invitations/sessions/roles/capacity/modules; bilingual separate `/?accounts=1`; no operational data migration. Subsequent local changes improve accessible forms, scope boundaries, formatting, documentation and migration-version verification.

## Verification so far

- Local suite: original 26 + 4 new tests passed (30 pass, zero fail); opt-in real MariaDB suite skipped locally by design.
- TypeScript + Vite build succeeded before final formatting/UI tweaks; rerun pending/active.
- Actual API port 5185 without config rejects company login with `mariadb_not_configured`. No local MariaDB instance/service on 3306/3307 found in read-only checks; no installation or DB mutations attempted.
- `scripts/phase3-ui-qa.mjs`: actual Not Configured UI plus explicitly mocked provider create/edit, company invite, storage-button path; FA/EN screenshots, 1366/1920/800/390 widths, no horizontal overflow and no browser errors. Fixture screenshots are not connected MariaDB evidence. Visual review corrected checkbox layout, accessible select labels and RTL capacity ratio.

## Remote synchronization checkpoint

Remote advanced with owner document `0a2fe68` while coding. First normal push was rejected; no Force Push used. Its modular-monolith addendum matches implementation and must be preserved. Rebase stopped on the pre-existing case-colliding documents; rebase was safely aborted. Automatic approval rejected overwriting the document and rejected persistent assume-unchanged flags; neither was performed. Current branch is intact (ahead two / behind one before later commits). Asked owner asynchronously for permission to merge that remote documentation commit into **this same Phase 3 branch** and push; do not infer approval from elapsed time. Main/pilot/next must not be merged or changed.

## Additional verified checks

- Full Phase 2 browser QA passed again: desktop viewport, label collisions, Explore/Detail sizes, raycast/selection, hover/zoom/pan/drag/reset/legend, period queries, layers/2D map, industrial modules, configuration replay, QC and maintenance persistence. Separate offline/retry browser QA passed.
- Final formatted code/UI build passed. Phase 3 UI fixture QA repeated successfully after visual/accessibility fixes. Real MariaDB CI still requires push after remote reconciliation.
- Provider invitation reissue is restricted to the designated first-admin identity; it cannot reissue invitations for arbitrary invited employees. Tenant metadata carries an actually stored schema version and mismatches fail closed.

## Latest owner instruction — synchronization on hold

Owner explicitly requested: **no Merge, Rebase or Push for now**. Continue local implementation/tests and preserve commits. Canonical `DECISIONS.md` stays; the original historical text is now `docs/archive/DECISIONS-EARLY-PILOT.md`, moved via Git with original content/hash and all prior commits retained. No sync action may be inferred from previous push authorization. Before eventual sync, report current divergence, backups, archive integrity and a reviewed plan; wait for authorization. No Force Push, deletion of changes, cross-branch merge or stash manipulation.

Additional local tests now check case-insensitive tracked path collisions, exact archived Git content after checkout line-ending normalization, invalid migration plans before DB access, and denial of unsafe tenant-storage contexts before any connection. All executable MariaDB tests remain opt-in CI-only and unrun locally.

Final local verification for this increment: **33 pass, zero fail, one real-MariaDB suite intentionally skipped; TypeScript + complete build passed**. No Merge, Rebase, Push, installation, stash manipulation or deployment performed. Current known Remote remains `0a2fe68`; report divergence against that fetched ref, not as a freshly queried GitHub state.

## Next required work (subject to latest owner hold)

Finish local QA/build, commit current work, reconcile Remote only with the requested authorization or demonstrably safe approved method; push, run dedicated disposable MariaDB CI and fix any failures. Record actual CI link/counts in delivery docs; no claim of real DB validation before CI success. No local DB environment should be created without owner confirmation. Once CI passes, final brief report with actual tested vs untested scope.
