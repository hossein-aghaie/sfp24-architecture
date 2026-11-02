# Visual implementation contract — Pouyeshgar Smart Factory
Updated 2026-10-13. Companion to `AGENTS.md` and `docs/CODEX-SMART-FACTORY-HANDOFF.md`.

## Mandatory reference images: supplied by owner in the Codex conversation
These image files are not automatically transferred from an unrelated ChatGPT conversation. Ask the owner to attach or copy them into `docs/design/reference/` before starting pixel-oriented implementation:
1. **Current REAL app screenshot** with the physical Hall 01 Three.js scene, machine shapes and placement. This is the **source of truth for actual geometry**. Also use `docs/hall-01-layout.md`, `src/model.ts` and `src/visuals/equipment-models.ts`.
2. **Approved blue/dark immersive dashboard concept** previously generated in ChatGPT. This is only a **style, chrome and composition** reference: colors, header, right navigation, optional layer drawer, compact overlays and bottom analytics. Its giant photorealistic industrial plant, made-up hall OEE labels, equipment or numbers are NOT the real workshop and must NOT be copied into production.
3. **Three-view concept sheet** showing Immersive / Explore / Analytics. Reference for distinct information density and interactions across the same underlying scene/data; not for machine identities or fake metrics.
4. **Existing machine/line-detail SFP screen** (four OEE gauges, machine overview, timeline, production rate and downtime). Use as functional inspiration for separate Device/Line Detail, NOT as a fixed formula or assumed line setup.
5. **Official company logos/assets** for Pouyeshgar (pilot factory) and SFP24 (platform/provider). Do not synthesize official logo files from a drawing; preserve aspect ratio and contrast. If absent, use text logo and configurable image URL/asset reference, and mark awaiting verified branding.

If any of these are missing, DO NOT claim pixel-accurate matching. Implement the layout architecture first and list the missing reference.

## Common shell — DESKTOP
- RTL Persian default; English LTR via real translated strings, locale, number/date format and mirrored navigation where appropriate.
- Compact header with Pouyeshgar pilot identity, optional SFP24 powered-by, scope selector, report date/time, data freshness, alarms, user and language controls.
- Fixed/collapsible right-hand app navigation in Persian; leave stage dominant, avoid unused huge masthead or repeated navigation bars.
- Factory selection and ANALYSIS SCOPE selector distinct from physical hall selector. Hall is a physical filter, not KPI ownership.
- `Demo data / دادهٔ نمونه` badge when sample mode active; unknown metrics show `—` with reason, not made-up values. Never display a fabricated real-time data acquisition.

## Monitoring modes, SAME selected entities / period / sources
### A — IMMERSIVE
The existing Three.js view fills most of remaining viewport (aim for dominant 65-80% of monitor workspace, responsive). Minimal floating overlays: selected equipment ID, state and ONE applicable key metric; global issue count and alert rail or slim dock. Right slide-out for layer toggles and overlay density, hidden/collapsible on TV. Optional small lower strip for genuine selected metrics and actionable alerts. No permanent unrelated pie charts or imaginary halls. Use current layout, real 16 items and current room details. Preserve orbit/zoom/top camera/raycast and visual asset identity.
### B — EXPLORE
Same Three.js instance and physical scene in a 55-70% content split + contextual drawer for selected entity. Drawer shows equipment name/model, operational state separate from connection state, current selection's KPI cards with provenance, recent stops/events and a working 'full detail' navigation. Layers are independent from the scene and can be toggled; charts only if justified by available selected data.
### C — ANALYTICS
2D overview with a constrained KPI strip, meaningful trends, Pareto, alerts and tables. Selectable scope can be equipment, operation, process/line, product, team or cross-physical selection, not always halls. On small screens stack tables/cards gracefully.
### Deep dive (not fourth presentation mode)
Full equipment / line workspace with OEE, availability/performance/quality if applicable, current production vs plan, quality, production-rate history, machine state timeline, stoppages, operator & maintenance tabs, source and definition metadata, and navigation back retaining filters.
### Presentation mode
TV/kiosk FULL SCREEN may wrap Immersive, Explore or Analytics. Presets store chosen layer/metric/card visibility and density. No freeform Drag-and-Drop Studio in v1.

## Visual quality and semantic rules
- Palette proposal: near navy #081A2D, panels #0D2944, blue accent #1E91FF, cyan highlights #57C8F8, quiet borders #25445F, readable text #EAF4FF. Use off-white floor/3D surfaces when it improves contrast. Theme tokens, not hard-coded scattered hexes.
- State semantics: running should not be confused with connected. Alarms visually salient: danger red, caution amber. Offline/no-data gray or outlined. A planned stop is not automatically a fault. Distinguish severity also with icon/text (accessible).
- Improve actual coded machine models: more identifiable CNC door/panel/windows/materials, realistic PBR-like roughness/metalness/shadows, optional licensed GLB, throttled/paced renderer, no dozens of phantom machines or corridors.
- Text remains browser DOM with native fonts for correct Persian spelling and accessible content. Screenshots are NOT backgrounds. Breakpoints for 1920x1080, 1366x768, ~800px and ~390px; on smaller devices use Analytics as easy default but never hide other permitted modes.
- Every control should either work or have explicitly marked not-configured/coming-later behavior; avoid misleading interactivity.

## Expected evidence
1. Commit updated real source files to the feature branch (do not just return images).
2. Run tests, `pnpm build`, and where environment supports, functional Playwright browser QA.
3. Screenshots from REAL rendered app for 1920x1080 and 1366x768 for EACH of A/B/C and detail. Compare side-by-side with attached concept/style image and actual workshop screenshot. Iterate at least one review pass on visible layout/text issues.
4. Add a factual feature matrix: fully working/demo-readonly/backend-incomplete/hardware-not-connected, and clear instructions to run on owner's Windows computer.
5. Do not describe a completed backend, full RBAC, shift planner or hardware integration unless code and tests prove it; implement truthful, coherent pilot and prioritize feature depth without fake data.
