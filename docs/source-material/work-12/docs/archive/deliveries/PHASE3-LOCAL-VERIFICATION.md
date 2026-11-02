# Phase 3A local verification and safe Git handoff

Historical local handoff: the owner initially held synchronization, then explicitly authorized same-branch reconciliation and normal Push. That plan was executed as merge `9b1a3a6`, preserving both histories. [MariaDB CI](https://github.com/hossein-aghaie/pouyeshgar-workshop/actions/runs/38596701887) subsequently passed **42/42 tests, zero skipped, and build**. [Standard CI](https://github.com/hossein-aghaie/pouyeshgar-workshop/actions/runs/38596701728) also passed. The remaining sections record the local pre-push evidence and original plan, not a current hold or production-readiness claim.

## Document collision resolution

- Canonical: `docs/DECISIONS.md`.
- Historical: `docs/archive/DECISIONS-EARLY-PILOT.md`; original Git blob `0aa7d7a49abd1280fa6a36e61153be96ed1f0ad0`, identical to `395d0f8:docs/decisions.md`.
- Original lower-case path and previous commits remain in Git history; no rewriting/squashing/amending was used. The temporary `decisions-legacy.md` path has been renamed with `git mv`.
- Active links corrected; archive provenance/history commands in `docs/archive/README.md`.
- A regression test checks tracked filenames case-insensitively, canonical document identity and archived normalized Git content. CRLF checkout differences are not content changes.

## Local evidence

The test/build commands are `./scripts/dev.ps1 test` and `./scripts/dev.ps1 build`. Final local run for this increment: **34 tests total, 33 passed, zero failed, one deliberately skipped real-MariaDB suite**. All original 26 tests remain included. TypeScript checking and the complete Vite build passed.

Real browser QA already passed for the Phase 2 main modes, device selection, chart zoom/pan/drag/reset/legend, layers, period changes, QC and maintenance flows; offline/retry QA also passed. Phase 3 actual unconfigured mode and explicitly mocked UI forms passed with FA/EN and 1366/1920/800/390 widths. No claim of connected MariaDB browser onboarding is made. These screens are unchanged by the archive/test increment.

No local MariaDB service/listener was found on the checked ports. No database installation, Windows service change, Docker/WSL, ERP/hardware access or deployment was performed. New MariaDB integration suite and temporary CI service exist in committed source but cannot run until an authorized Push. Actual database isolation, transactional behavior and provisioning remain **unverified on a real engine** until that job passes.

## Proposed safe synchronization — do not execute without authorization

1. Keep all current commits and the ignored local safety backup; record exact HEAD and current Remote ref before any changes. Keep untracked reference files and historical stash untouched.
2. After owner approval, fetch and inspect any further Remote commits. Current known additional Remote commit is `0a2fe68` (owner's modular-monolith documentation addendum); its content has been reviewed and must be preserved.
3. Prefer one reviewed merge of that **same Phase 3 remote branch into this Phase 3 branch**, preserving both ancestries. Do not rebase across the historical case-colliding checkout, Force Push, or merge into pilot/main/next. If conflicts appear, stop to inspect both versions and preserve the canonical/archive split; never auto-select ours/theirs wholesale.
4. Re-run tests/build, check filenames and archive hash, inspect only intended source/docs in the push range, and confirm `.local`, credentials, DBs and QA outputs are excluded.
5. Only with the explicit final authorization, normal Push the Phase 3 branch. Wait for both CI workflows, including the disposable real MariaDB suite; investigate any failure and report exact tested/untested results. Do not claim Phase 3 production readiness from local fixture tests.

The merge in step 3 is a proposal only. No new Merge, Rebase, Push, branch, PR, tag, deployment or stash action is part of this local increment.
