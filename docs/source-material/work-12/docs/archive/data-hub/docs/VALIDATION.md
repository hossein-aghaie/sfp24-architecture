# Local validation — 2026-10-18 (Asia/Tehran)

Release: 0.1.0, Node.js **24.19.0**, Fastify **5.12.5**, Vue **3.5.43**, Vite **7.3.7**, Aedes **0.51.3**, mqtt.js **5.14.1**, ExcelJS **4.4.0**, MariaDB connector **3.5.4**. Exact dependencies/integrities: pnpm-lock.yaml. Application tests cover source revision d7b51a86b524e63cb1685c8e9537851291657e63. Subsequent delivery changes add the runbook and strengthen only the Windows lifecycle scripts; no application code was changed in that follow-up.

Delivery follow-up, 2026-10-18: `Stop.cmd` → `Start.cmd` passed with HTTP health=ok, 50 simulator devices and collection stopped. A second `Start.cmd` correctly refused occupied port5220 without stopping any process. Both PowerShell scripts passed syntax parsing. The private repository target is `hossein-aghaie/pouyeshgar-industrial-platform`; the pushed commit is reported separately after remote SHA verification. No production deployment is performed.

Help-guide follow-up, 2026-10-18: frontend type check and production build passed. Existing Edge/Playwright verified the ten-node map, keyboard selection and storage explanation, current-versus-proposed company ownership, zero versus missing sample, four delivery/consumption milestones, English/Persian RTL, and contained horizontal map scrolling at390px. Browser page-error list and all POST/PATCH/DELETE requests after login were both empty: using the guide did not create records or send samples. English/Persian screenshots were visually inspected. The guide is loaded on demand and introduces no dependency, backend endpoint, company synchronization or original-application connection. Local evidence: private/logs/help-check.json; target ownership decision: ADR-001-COMPANY-OWNERSHIP.md.

Browser-history fix, 2026-10-18: type check/build and six existing-Edge regression scenarios passed (`node tests/navigation.mjs`): menu Back/Forward, no duplicate active-menu entry, guide tab history, selected node restoration after related-page navigation and reload, Persian RTL history, and direct links/invalid paths/manual hash changes. No page errors. The new navigation is client-only; backend and simulator code are unchanged. Evidence: private/logs/navigation-check.json.

## Evidence matrix

| Item | Status | Evidence / limit |
| --- | --- | --- |
| Frontend and backend type check + production build | PASS | vue-tsc --noEmit; tsc -p tsconfig.server.json; vite build |
| Integration suite | PASS, 9/9 | node --test via tsx; final local log private/logs/tests-final.log |
| Zero, duplicate, conflict and timestamp semantics | PASS | zero stored; replay with changed transport ID deduplicated; conflicting value preserved; invalid time rejected |
| Transaction failure | PASS | injected SQLite receipt-insert failure rolls back samples and receipts |
| Company isolation | PASS | company-scoped lists; forbidden cross-company device edit/key rotation/command/user creation |
| Outbox restart / fairness | PASS | reopened SQL database recovers interrupted sending; disabled destination cannot starve another |
| MQTT | PASS | actual loopback MQTT QoS1 publication, persisted sample before publish completion, command ACK, cross-device subscription refusal |
| CSV / XLSX | PASS | quoted CSV, zero vs empty, XLSX values, formula refusal |
| API polling | PASS, lab fixture | local source commits and advances cursor; replay deduplicates |
| Desktop browser workflow | PASS | owner login, eight pages, company filtering, create/edit/disable device, source wizard, file preview/import; existing Edge + Playwright |
| Language / responsive UI | PASS | English, Persian RTL, 390px mobile navigation; screenshots inspected; page error list empty |
| Independent simulator | PASS | separate process, 50 synthetic agents, 25 MQTT +25 HTTP, no shared database module |
| Real end-to-end local chain | PASS | ingestion → persistence → local receiver committed receipt; HTTP/MQTT command success; pause/resume; network outage/recovery; replay deduplication |
| Windows startup / stop | PASS | local scripts refuse occupied ports, hidden processes; stop verifies PID command path; data preserved |
| MariaDB connector end-to-end | UNVERIFIED | connector implemented, original DB blocked; no dedicated lab DB installed or accessed |
| Original Pouyeshgar receiving contract | DOCUMENTED ONLY | body adapter based on supplied handoff; no original API, DB or app contacted |
| Real physical devices / commands | UNVERIFIED | all command execution was simulated; physical machine control is absent |
| Linux deployment | UNVERIFIED | source uses Node cross-platform APIs; only Windows tested, no WSL changes |
| Production security / HA / sustained capacity / commercial packaging | UNVERIFIED | no public exposure, TLS/HA/retention testing or commercial legal clearance |

Browser tests initially created two empty acceptance devices. They were removed by the narrowly scoped fixture-cleanup script after checking they had no telemetry, command or source history; all 50 sample devices and all telemetry remain. An API fixture remains disabled and labelled as a local sample. There are no fabricated successful receipts for preloaded devices.

## Resource observations

Method: Windows Get-Process WorkingSet64, per-process cumulative CPU seconds, samples every 60 seconds. Hub and simulator are separate processes. Host reports 16 logical processors. Browser/build tools, OS cache and any unrelated existing applications are excluded. Working set is not private committed memory or total system RAM. These short runs are observations, not a capacity guarantee or a controlled before/after benchmark.

Second run: 50 agents, two signals per batch, preferred transports split evenly HTTP/MQTT, one batch every five seconds with logical-minute timestamps. One Atlas destination uses the local receiver; no external receiver. Intended generated rate is roughly 1,200 signal values/minute; do not confuse this accelerated test with a physical one-minute interval. Raw minute samples are retained privately and summarized in RESOURCE-SAMPLES.json.

| Sample | Hub MiB | Simulator MiB | Sum MiB | Combined CPU, % of 16-processor host over preceding minute |
| --- | ---: | ---: | ---: | ---: |
| Idle start | 79.2 | 75.5 | 154.7 | — |
| Idle, minute 1 | 80.5 | 76.4 | 156.9 | ~0.008% |
| Load, minute 1 | 101.7 | 122.9 | 224.6 | ~1.58% |
| Load, minute 2 | 122.4 | 144.3 | 266.7 | ~1.45% |

CPU calculation: delta of both processes' CPU seconds / elapsed seconds /16 ×100. First loaded minute uses about25% of one logical processor in total, rather than25% of the whole host. The measured rise in working set means a longer soak test is still needed; two minutes does not prove a memory ceiling or lack of a leak. Simulator memory is not required when running the hub with real agents elsewhere.

Startup is recorded separately in private/logs/startup-memory.json using the OS process peak working set over approximately the first30 seconds after readiness, with simulated collection stopped. Startup values are copied to RESOURCE-SAMPLES.json once that monitor finishes.

No Docker/WSL component is used by this implementation: **introduced Docker/WSL overhead is zero**. Pre-existing distributions/services were not altered or included in this attribution.

Logical file lengths after development installation: node_modules about158.5 MiB; private/ about217.8 MiB, mostly the isolated pnpm store/cache plus lab data/logs/screenshots. These are not physical allocated bytes; hard links may overlap. Root source/build size is additional. Exact download bytes were not captured and remain UNVERIFIED. No database server, container engine or system runtime was newly installed for this hub.

## Operational limits

Single hub process, isolated SQLite, no retention deletion/HA, local HTTP and MQTT without public TLS. Backups must preserve the database and master key securely. The generic receiver must confirm the matching stable event ID after commit. HTTP200, MQTT QoS1 and a UI status alone do not prove final production report consumption. Commercial packaging still has dependency provenance/licensing work recorded in LICENSING.md.
