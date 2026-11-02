# ADR 001 — Company identity across the hub and the main application

Status: **target integration design, not an implemented synchronization feature**.

The current isolated hub is a local lab. Its owner can create test companies, technical device identities, sources and company-admin accounts. Those actions do not touch the original application. Its company IDs are independent from the original application's UUIDs.

For future integration, the recommended business source of truth is the original application: create the business company there first, then provision or link the hub's technical company registry by stable IDs. A same-name company in both interfaces is not a binding. Integration must explicitly map main-company ID ↔ hub-company ID, and hub device ↔ main-app machine/resource with validity rules. That mapping/provisioning is not implemented by the current Companies form.

The hub owns technical collection configuration and delivery history. The main application owns business company context, sites/resources, OP and formal production reporting. The generic event envelope currently contains company_id, device_id and signal, but no machine/resource ID or OP. The receiver must use an explicit binding; it must never infer resource/OP, machine state or good parts from a raw minute count.

Owner clarification: Dev Admin in the main app owns company lifecycle, operator entitlements, purchased modules and company-admin identity; Company Admin owns the factory/resources/operators/shifts there. The integration proposal is now expanded in [INTEGRATION-HANDOFF.fa.md](INTEGRATION-HANDOFF.fa.md). Binding must support **signal-to-resource**, with effective dates: an EdgeBox can carry multiple channels or machines, so a device-to-resource shorthand is not sufficient. The v2 structured events, provisioning, catalog change notifications and delegated authentication in that handoff are proposals, not implemented endpoints.

Current delivery is a push worker posting to an enabled destination API, not a shared database or a main-app database polling loop. Only synthetic local endpoints are allowed by default. A successful local test receiver does not establish original-app integration.

No original repository, original database, company, credentials, service or hardware was read or changed to implement this guide. The main-app context comes from the supplied programmer handoff. No integration API, migration or production connector is introduced by this ADR.

## User-facing guide

The Help & guide menu explains the available flow using interactive, keyboard-accessible boxes. Its dashed path is the proposed main-app boundary, not a live connection. The sample is synthetic and never sent; zero and missing examples explain validation without creating records. Guide content is in src/guide-content.ts; rendering/layout is in src/HelpGuide.vue, loaded only when opened. No diagram/image dependency or remote asset is required.
