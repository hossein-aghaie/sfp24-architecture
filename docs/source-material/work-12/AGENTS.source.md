# Repository agent guidance — Pouyeshgar Smart Factory pilot

You are modifying the REAL Vue 3 + TypeScript + Three.js app in this repository, not building a static mockup.
Before coding, read `docs/CODEX-SMART-FACTORY-HANDOFF.md`, `README.md`, `docs/dashboard-layers.md`, `docs/DECISIONS.md`, `docs/hall-01-layout.md`, and review `src/App.vue`, `src/SceneView.vue`, `src/model.ts`, `src/reporting.ts`, `src/i18n.ts`.

## Non-negotiables
- Current owner-authorized product branch: `codex/03-production-recording` in `D:/git/pouyeshgar-workshop`. Stage 02 is frozen at `stage/02-structure-and-ui-foundation` (`7d31e30`); continue existing production services rather than rewrite them. Phase 2 presentation is `demo/phase2` in a separate checkout; older checkpoints are preserved under `archive/2026-10-19/*` tags. Never modify `main` or `next`, merge into the demo branch, or deploy automatically.
- Preserve existing layout geometry, the real workshop equipment identities and positions, selection/raycasting, layout JSON import/export, date range calculations, and tests.
- The hall is a PHYSICAL LOCATION, not an intrinsic OEE entity. Lines, equipment, operations, products, teams and organizational scopes can cross locations. Never silently use average OEE of machines as 'hall OEE'.
- Distinguish equipment state, data-connection freshness, alarm severity, and metric period. Never make invented numbers look like live machine data. Demo mode must be explicitly labeled.
- Permission filtering must be enforced server-side once an API exists; hiding front-end controls is not RBAC.
- Provide RTL Persian and LTR English with accurate labels, no AI-generated text baked into UI screenshots.
- Do not use static screenshots as the 3D viewer; reuse the working Three.js scene.
- Do not move existing on-device or server environments, configure live network services, or deploy to the owner's local Raspberry Pi without explicit approval.
- No secrets or identifiable employee data committed. Paths/caches on owner's Windows device belong under D:\\git\\pouyeshgar-workshop.
- Deliver working flows, not decorative links. If an external integration depends on missing firmware/ERP specifications, expose a truthful 'not configured' state and provide a tested adapter contract.
- Run available test, typecheck/build, and browser/screenshot QA where available; report evidence and remaining gaps accurately.

## Documentation precedence (2026-10-14 approved consolidation)
When available, start at `docs/START-HERE.md`, then `docs/PRODUCT-BLUEPRINT.md` (complete product vision), `docs/CURRENT-STATE.md` (shipped/tested), `docs/ARCHITECTURE.md`, `docs/UI-UX-SPEC.md`, `docs/DECISIONS.md` and `docs/RUNBOOK.md`. Historical Phase 1/2 handoff, research and progress documents remain source records, not independent current instructions. Confirm branch/HEAD and owner decisions before new work. The documentation-only fast-forward has been completed; future changes require the owner's review. Do not merge historical documentation branches or overwrite operational code.

## Owner-authorized monorepo migration — 2026-10-19
Current migration branch: `codex/telemetry-monorepo`, derived from reviewed `codex/integrated-telemetry-v1`. Owner authorized structural consolidation before rc.4 implementation. WEB remains src/ and server/. INGEST source and existing lab receiver tests live in services/ingest; its current server is a preserved SQLite lab receiver, not the rc.4 production runtime. Legacy Vue panel and independent simulator live in labs/data-hub. The sole approved contract snapshot is packages/telemetry-contract/contract, byte-preserved with its signed manifest. Financial/trial, runtime DB migration and rc.4 business changes are outside this structural step. Do not change root/main or the original hub repository or its private data. Coordinate shared package edits through one author; later sessions use separate worktrees. No automatic service startup/deployment.

## Owner-authorized workspace cleanup — 2026-10-19
The product now runs from the primary repository root, not .local/worktrees. Retired worktrees were removed only after Git/checkpoint and ignored-private-data backup. D:/git/pouyeshgar-demo-phase2 and D:/git/pouyeshgar-industrial-platform are presentation demos; no rc.4 development there. Do not restore archived branches as active work without owner direction. See docs/START-HERE.md for authoritative current docs; archives are historical evidence. Simulator may later be an external Windows program; preserving the lab simulator is not a requirement to embed it in WEB.


## Owner-authorized numbered checkpoints — 2026-10-28
Stage 01 is frozen at tag `stage/01-data-hub-foundation`, commit `3156ff7`, on `codex/telemetry-monorepo`. Stage 02 continued in the same primary checkout on `codex/02-structure-audit`; the owner subsequently authorized stage 03 on `codex/03-production-recording` from `7d31e30` (2026-10-29). These stage numbers start a new checkpoint sequence; they do not renumber the historical Phase 2 demo or imply a production release. Do not rename/delete old branches or tags, rewrite history, update main/demo, start services or deploy. At branch creation only the checkpoint and audit branch were registered. Current work follows the owner-approved 2026-10-28 cleanup; Graphify is a separate experiment in D:/git/graphiify. Audit work must establish code-to-API/storage/permission/test dependencies and current document authority before proposing removals. Do not treat an unreferenced file or old test as safe to delete without evidence. Private runtime data and local reference screenshots are outside Git and require separate backup.


## Owner-approved stage 02 cleanup — 2026-10-28
The owner authorized documentation consolidation with full historical preservation, removal of proven unused code and obsolete test databases/caches. Keep the active control database, current tenant/account credentials and physical layout identities; disposable historical QA schemas may be removed only after actual target/reference/live-connection verification. Retain a private recovery snapshot and report exact actions. No startup/deployment or changes to main/demo. CompanyFiles is the sole active file layout after verified transfer of current legacy assets; do not reintroduce fallback readers. Preserve applied migration history and the signed contract. Product direction from the latest conversation is in PRODUCT-BLUEPRINT's 2026-10-28 section, not just chat memory. Treat archived daily narratives as source records and current docs as authority.
