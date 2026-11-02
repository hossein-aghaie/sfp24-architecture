# CODEX HANDOFF — Pouyeshgar Smart Factory Pilot
Version: 2026-10-13 · Status: approved direction for implementation, detailed business rules pending.
Working branch: `feat/smart-factory-pilot-next`; keep `main` unchanged.
Primary company/pilot: «پویشگر» / Pouyeshgar. SFP24 is distinct product/provider technology branding, NOT the pilot factory's name. Build configurable company branding and use a verified company logo asset if supplied; never fabricate a logo claiming it is official.

## Product goal
Build a coherent, BEAUTIFUL, genuinely interactive web application around the EXISTING REAL-workshop 3D scene. The UX should feel like a screenshot from an implemented industrial application, not an AI concept poster. Clean modern blue/navy/neutral palette; industrial white or slate scene, subtle lighting/shadows, controlled attention colors for operational state; accurate Persian typography and correct RTL. Responsive for desktop, display, and tablet. Avoid decorative gauges unrelated to current operating data.

Original project: Vue 3 / TypeScript / Vite / Three.js, existing scene and reporting range utilities. The repository currently has NO operational backend/MariaDB/IoT connection/authentication; do not pretend otherwise.
Target stack (if implementing backend): Node.js LTS + Fastify + TypeScript; MariaDB/InnoDB; IoT adapters HTTP Edge Box-compatible when actual firmware contract available, optional MQTT; Docker Compose behind an existing Nginx AFTER approval. Do not replace the current client or assume live hardware.

## Core UX: three switchable monitoring presentations, same data/filter/state
1. **Immersive (EasyV-inspired)**: the working, interactive Three.js workshop uses MOST of the viewport, 3D objects are selected via raycast; concise DOM overlay tags on applicable machines and optional bottom strip for key metrics/critical events. Floating show/hide controls for chosen information layers. Suitable TV/Kiosk, but TV is a PRESENTATION MODE for any view (no menus/edit controls), not a fourth data view.
2. **Explore (3dverse-inspired)**: same 3D scene + collapsible slide-out contextual panel for selected device, process group, line, operation or alert. Sidebar can switch information layer; click an equipment model highlights it, shows a summary, preserves period & selection on drill-down. Avoid permanent dense panels that obscure 3D.
3. **Analytics (Advantech-inspired)**: 2D accessible cards, time-series trends, downtime Pareto, tables and comparisons, all based on exact same selected scope, metric definitions, and range. Mobile/tablet-friendly; do not assume 3D is available on every screen.
4. **Device/Line Detail is a separate deep-dive workspace** linked from the three presentations, NOT one of the three presentation modes. Follow the owner's previous one-machine/continuous-line OEE reference in spirit: OEE, Availability, Performance, Quality, production counters/rates, quality/scrap, state timeline, stops with causes, maintenance and improvement, operator/shift when permitted. Different lines and equipment may expose different applicable metrics.

## Navigation and screens (every visible nav action must work)
App shell: compact RTL-aware top bar with «پویشگر» brand + possible SFP24 attribution, factory/current scope selector, report period, current/previous navigation, connection/staleness indicator, alerts, language FA/EN, user/menu, and presentation selector. Right-side primary navigation in Persian (mirrored for English) with:
- پایش / Monitoring (Immersive, Explore, Analytics, equipment detail)
- تولید و عملیات / Production & Operations
- توقفات و رویدادها / Downtime & Events
- کیفیت / Quality
- تعمیرات و نگهداری / Maintenance
- برنامهٔ تولید / Planning
- افراد و تیم‌ها / People & Teams
- گزارش‌ها و بهبود / Reports & Improvement
- مالی / Financial (permission-gated, not fake financial data)
- تنظیمات / Settings, with defined subpages below
Navigation should represent real modules; if a full business workflow cannot be built, use a truthful functioning read-only page rather than a dead control.

Settings:
- organization/factory identity & branding, physical hierarchy (buildings/halls/areas) independent of operational hierarchy;
- facility layout/editor (preserve existing operations & versioned JSON);
- equipment catalog, create/update, identifiers/types/capabilities, optional GLB visual asset, assignment/relocation history;
- Edge nodes, device mapping and signal channel mapping, ingestion health with field validation and event timestamps;
- operations/lines/OP/product definitions independently configurable (OP meaning cannot be globally hardcoded; multiple operating models);
- operators, supervisors, teams and their scopes; avoid sensitive data in sample;
- shift calendar: multiple shifts incl. overnight, weekends/holidays and date-specific exceptions (current one-shift settings are only a prototype);
- KPI definitions and aggregation policy editor (formulas, units, applicable scopes, period, source, validation, versioning);
- dashboard display preferences: 3 standard layouts with controlled configuration, selected KPIs, layer visibility, label density, default view, saved presets;
- users, roles, permissions, data access scopes (RBAC); server-side authority required for real usage.
A future freeform Grafana-style Dashboard Studio is OUT OF SCOPE for v1, but reuse widget components.

## Critical semantics
- Hall is PHYSICAL, NOT the fundamental KPI owner. Do not label 'Hall OEE' without validated, explicitly defined equipment/process aggregation scope. Equipment/line/process/product/team analytics may span buildings or halls.
- OP may mean an operation/route step in one factory and a product or a defined reporting entity in another. Store distinct business entities and configurable assignments rather than collapsing them into one code.
- OEE = Availability × Performance × Quality only when denominators & production reference are valid. Weighted executive scores/custom product weights must be named as custom KPI, not deceptively OEE. Do not compute OEE from a simple average across unrelated machines.
- Data source kinds: PLC/Edge, ERP, manual form, imported record. Include quality/provenance, event_time, received_time, device status and stale/unknown handling. Online Edge node is NOT proof a machine is producing.
- Event alerts: active/cleared/acknowledged, severity, timestamp and owning equipment/operation; distinguish true critical events from missing data.
- Optional overview: one primary analysis layer (e.g. OEE/production/maintenance/quality/people/finance) and few additional alerts/critical overlays simultaneously; user can toggle secondary overlays. Incident selection focuses the model or opens details.
- Access: permissions on module, metric/layer, entity scope and action (view/analyze/configure/ack/export). Server-side authorization when backend exists. Everyone's available view types are not tied to role.
- Financial data only if explicitly connected/entered; leave an informative no-data state otherwise.

## Real pilot workshop scene: preserve asset arrangement
Existing `src/model.ts` defines hall-01 with ~16 pieces of equipment: three CNC lathes (Hami, Hyundai WIA SE220LA, NEWAY NL161H), Cincinnati/Arrow mill, custom broach, 10 bench/pillar drills, a manual lathe. The physical layout has lathes and mill on left from entrance, row of drills on right, end machines and partial mezzanine, materials in center, some adjacent area; hall-02 exists but is unmapped. Keep identities/locations stable. The 3D code models are coarse primitives now. Improve geometry/materials intelligently, preserving actual spatial orientation, camera controls and performance; integrate GLB only if lawful optimized assets available. Never substitute the imaginary gigantic factory screenshot for the actual layout. Do not infer exact manufacturer dimensions from photos.

## Baseline source architecture
`src/App.vue`: UI shell & report controls. `src/SceneView.vue`: rendering, OrbitControls, TransformControls, raycast, DOM labels; `src/visuals/equipment-models.ts`: type-based visual models; `src/model.ts`: layout identity/geometry and test cases; `src/reporting.ts`: Persian/Gregorian reporting periods. Need separate reusable components / domain stores/services as app grows; preserve backward compatibility with layout import/export and current localStorage data. Avoid giant monolithic App.vue.
No direct data ingestion inside Three.js render code; scene consumes validated operational state.

## Implementation priorities; deliver one real, coherent pilot rather than fake completeness
P0: maintain baseline features; complete blue branded app shell + accurate FA/EN switching; fully interactive Immersive, Explore, Analytics, machine Detail, functional main navigation and settings routes; usable responsive layout, keyboard access, configurable layers/overlays/presets; credible 3D material upgrades; meaningful demo records explicitly labeled demo; tests and browser screenshots.
P1: backend foundations + durable data for pilot: Fastify, MariaDB schema/migrations/seed, auth/RBAC, factory/equipment/operator/shift CRUD, configurable KPI definitions, validated sample ingest API/event store and simulation/fixture adapter (not falsely connected to live device); API errors and stale indicators correctly rendered; tests. Respect missing Edge firmware contract and local deployment constraints.
P2: advanced real IoT/ERP and production/CMMS/finance workflows only with schemas and inputs confirmed by owner. Do NOT claim these operate before integration tests against real systems. Document blockers explicitly.
The owner wants a holistic release, not piecemeal UI snippets. Commit integrated code and tests; if scope exceeds available run time, complete & validate coherent P0 first and clearly report next steps, never show P1/P2 as shipped.

## Acceptance checklist
- `pnpm install --frozen-lockfile`, `pnpm test`, `pnpm build` green; browser QA and captured REAL browser screenshot for at least 1366×768, 1920×1080 and tablet; compare screenshot layout to reference intent, do not paste concept-image as UI.
- All three monitoring modes selectable, actual scene interaction functional, same selection/period shared; machine Detail navigation works.
- Existing JSON layout editor and camera zoom work; switching view doesn't reset or delete equipment.
- Persian text accurate RTL, English LTR, no garbled characters/overflow.
- Period labels/calculations and data status valid; no invented live KPIs or undefined hall OEE.
- Visible menus either work or clearly indicate unconfigured/no data without dead buttons.
- Data source, alert, and role permissions visibly distinguish authorized from unauthorized; API-side access if implemented.
- Existing tests pass, add tests for aggregate semantics, scopes, settings and UI where possible; document missing browser/DB facilities honestly.
- README: commands and local deployment guide for Codex on owner's Windows machine, without overwriting or altering existing ERP/SFP deployments; CHANGELOG and concise QA evidence.
- Work in a feature branch, provide PR/diff, commit hashes and detailed remaining blockers; NEVER merge to main or deploy to Raspberry Pi without owner approval.

## Reference
Read the repository docs listed in AGENTS.md. Prior AI concept images are only broad visual inspiration and do NOT represent actual shop geometry or business numbers; owner can attach example screenshots to the Codex task. Prefer screenshots from the owner and runnable UI to stylized AI images.
