# Workstream 11 — Skill Gap (independent ChatGPT Work track)

**Repository:** `hossein-aghaie/pouyeshgar-workshop`  
**Branch:** `work/11-skill-gap`  
**Source branch:** `codex/03-production-recording`  
**Source commit (branch point):** `5eb2b52cc57abc76c374271219b2a63d65399129`  
**Owner / intended environment:** independent ChatGPT Work session  
**Created:** 2026-10-30  
**Status (2026-10-31):** stage 3 authoring-intake preview committed and pushed as `f57e23ebe4e59c934e4c283bfa11f1fcffacb765`; isolated Cloud checkout, Node/pnpm build/typecheck and MariaDB-backed tests verified by Codex. **Not implemented:** operational LMS, Employee Onboarding, Activity/Competency/Assessment, Skill Gap calculation, connected AI, or persistent training backend. No merge into core or production deployment.

## Notice for Codex agents and other development sessions

This branch is **not** a Codex production-development stage, a continuation of the Codex session, or work produced by that session.

It was deliberately branched from the production-development commit above so the Skill Gap module can be explored and developed **in parallel, independently**. Shared commit ancestry does not imply shared task ownership.

- Codex should continue its assigned production work on its own branch.
- Do **not** switch to, modify, merge, cherry-pick, or treat `work/11-skill-gap` as an upstream continuation unless the project owner explicitly requests that action.
- Do **not** assume commits on this branch were authored or requested by the Codex production session.
- Shared-core changes, migrations, and eventual integration require explicit coordination and review.
- Seeing this branch when listing GitHub branches is informational only; it is not an instruction to act on it.

## Intended scope

Explore and, when separately authorized, implement a Competency & Skill Gap module using existing company/person identity and permission contracts. Its first iteration should avoid modifying the production-recording workflow.

This document marks ownership and branch provenance only. It does not create a Work environment, database, implementation, or authorization to change the production branch.

## Working with an unfinished host application — do not expand scope

Pouyeshgar Workshop is actively being developed by a **separate Codex session**. At this branch point, some dashboards, company onboarding cards, forms, registries and cross-module workflows may be partial, provisional or unfinished. These are **expected work-in-progress conditions**, not automatic defects attributed to Workstream 11 or invitations to finish the Codex session's tasks.

- Do not redesign, repair, complete or refactor unrelated dashboard, production, onboarding, telemetry, or other core features just because they appear incomplete.
- Do not infer that all product modules or all declared UI controls are functional. Compare claims against the actual implementation and the branch-point documents.
- Distinguish **non-blocking unfinished functionality** from a **genuine Skill Gap integration blocker**. Report blockers precisely; make the smallest explicitly authorized change needed, preferably confined to Workstream 11. A blocker must not be hidden or worked around using duplicate identities/data.
- Preserve and report pre-existing build/test failures as baseline issues if encountered; never describe failing tests as passing or dismiss a newly introduced regression as pre-existing without evidence.
- Do not touch either `codex/03-production-recording` or `main` or any real production company data.

## Architectural target: independent development, integrated module

This branch is independent **for development and testing**, not a separate product or an independently deployed microservice.

The intended target is the **current modular monolith**: the existing WEB frontend/backend, shared platform company identity/auth/permissions/module entitlements, and the existing MariaDB operational database **for each tenant company**. The account/control database remains separate; do not combine tenant databases across companies.

For the first Skill Gap implementation:

1. Reuse the existing company and `people.id` identities; do not build a second employee/person table or separate login mechanism.
2. Own the Skill Gap domain code, tables, migrations, validation, authorization and public service contracts in a clear internal module boundary. Prefer isolated domain folders and tables within the **existing per-company tenant database**.
3. Use existing authenticated server services, scoped actor/context and in-process TypeScript contracts for internal module-to-module queries. Avoid loopback HTTP, additional network services, separate databases, queues, duplicate caches and broad new cross-module API surfaces without a demonstrated operational need.
4. Respect ownership: other modules may consume a documented Skill Gap read/service contract, but must not write its domain tables directly; Skill Gap must not bypass core authorization/people services with unscoped cross-module SQL. A shared physical database does **not** imply uncontrolled data ownership.
5. Keep onboarding optional: companies using production without Skill Gap must not be required to supply skills, certificates or training information. A person may exist with only minimal base identity; capability-specific completeness/eligibility is enforced by the feature actually using it, not by saving every person.
6. Support historical records and safe deactivation: adding or disabling this module must not silently erase assessments. Check the existing people lifecycle and FK/deletion behavior before introducing a contract; never assume people can already be hard-deleted.
7. Make the module accessible through the current module catalog, permissions, workspace registry and company forms via the **smallest possible integration seams**. If the host lacks a needed extension point, document the exact missing seam and its minimal proposal; do not build an unapproved generic plugin engine or rewrite shared forms.
8. A dedicated Skill Gap page or person-profile section may be justified for multi-record assessments; it is not a license to fork the global profile/onboarding workflow.
9. Keep production-recording, dashboards, ingest contracts and telemetry code outside the implementation scope. Support future consumers through an explicitly scoped contract (for example, competency check by person and operation), not immediate speculative integrations.

## Integration / merge discipline

- Work on this branch and its isolated Work environment only. The source is a fixed historical commit, not a live mirror of Codex's evolving branch.
- Prefer additive changes in module-owned paths. Keep core/shared files changed to a **small, listed set of registrations or interfaces**; provide a per-file integration manifest for later review.
- Do not modify shared migration history destructively or assume a locally chosen schema number will remain unused in concurrent Codex work. Reconcile migration ordering/collisions before merge; never run unreviewed migrations on a real tenant.
- Tests must cover core identity reuse, entitlement/permission isolation, per-tenant data, absent skills, skill qualification/expiry, and non-interference with production. Report which checks were run and which were not.
- Before eventual merge, compare against the latest Codex branch and resolve contract/migration conflicts. No automatic merge or integration is authorized by this note.

## Status and handoff

The independent Codex Cloud environment validated git access and ran isolated checks on stage-3 code: Typecheck/Build passed, 167 ordinary tests passed (2 skips), and 231 tests with temporary MariaDB passed (1 Windows-only skip). The MariaDB instance was removed. GitHub received commit `f57e23e`; these are historical recorded results, not evidence of production deployment or completed operational training functionality. The core Codex session does not automatically read live Work 11 conversation state; integrate through committed artifacts and owner-coordinated review.

## Additional product boundary: company roles, delegated training and AI (2026-10-30)

**Authoritative product detail (Persian):** [docs/README.md](README.md), **sections 15–23** (AI, ownership/permissions, UI integration, employee onboarding, benchmark/standards, competency engine and acceptance gates). Read that section before modifying UI, permissions or workflows. The earlier training AI preview had an **incorrect temporary location and access gate; corrected in stage 3 (`f57e23e`)**.

**Three user domains, not three services/databases:**
- **Provider/Developer Admin** provisions a company, chooses licensed modules, account seat capacity and initial Company Admin. It is **not** the company's training-content administrator.
- **Company Admin** initializes purchased modules, manages people/accounts and grants feature permissions. The same person may also manage training, but this is not required.
- **Company members** act through feature permissions and scopes. Training manager, course approver, qualified assessor, supervisor and learner are **delegable functional responsibilities**, not mandatory organizational departments. Training management continues after initial setup; learners are not the only users.

**Important identity and entitlement constraints:**
- Distinguish **person record** from **login user**, business job title, assigned permissions and verified practical assessor qualification. An existing person without a login may still have training evidence. Do not equate account seat_limit with a limit on employee records.
- Any training screen/operation must be gated by the **purchased AND ready module** and **server-validated training-specific permission**; the navigation, direct URL and API must honor this.
- Do not use global users.manage as the permanent permission for training operations. Enable a qualified staff member to administer training without giving them global user administration. Restrict approval of machine qualification to appropriately authorized and qualified assessors.

**AI preview: historical mistake and current stage-3 correction:**
- **Historical (pre-stage-3):** TrainingAiIntake.vue was incorrectly registered as a global company definitions card under `users.manage`. **Current:** removed from definitions, relocated under the Training module; available only via training entitlement/readiness and `training.ai.author` through server-validated Workspace. Still local JSON-only; no actual AI/LMS.
- The correct home is **inside Training & Competency module setup/operations**, not the general company onboarding area or Provider Admin. Its setup function may be used by Company Admin, and later by training-content editors with scoped training.ai.author authority.
- Its purpose is to elicit tasks/OPs, equipment, documents/photos/videos, competencies, HSE and quality requirements and propose **training package/content and module-local setup**, subject to review. It must not change application code, global permissions, purchased entitlements, migrations or platform settings. No unapproved external AI transmission or automatic safety/qualification approvals.
- **Stage 3 completed:** global card removed, module entitlement/permission integration tested with delegated author and unlicensed denial; no training API exists yet. Any future training endpoint must enforce tenant/entitlement/permission independently. The general `workspaces.ts` `pageAvailability` change affects all company pages and requires core review before merge.

**Training operations and automation:**
- Include distinct onboarding/setup **and ongoing operations**: draft/review/publish courses, schedule/assign learning, assess practical competence, approve qualifications, follow expiry/renewal and produce audit evidence.
- Support manual, recommendation-only, and pre-approved rule-based/event-driven scheduling as product directions. Example "20 minutes per week" is company policy, not an ISO-prescribed duration.
- Maintenance downtime is **not** evidence that an operator is free. A later integration may suggest a learning window only after verified person/shift/work obligations are considered. The Training module must work without Maintenance, Planning, Production or dedicated HSE enabled; use explicit in-process contracts for future triggers and no cross-module table ownership leakage.

**Development-session sequencing (updated 2026-10-31):** Phase-0 environment validation and stage-3 integration work have been completed and recorded on Work 11. Stage 4 and Employee Onboarding remain **unapproved for code implementation**. The core Codex session owns concurrent core work and may have unpublished changes; preserve branch isolation and request explicit owner approval before integration. See product-notes section 18 for the detailed employee journey, safety boundary, 70–20–10, Buddy model, acceptance scenarios and unresolved decisions. Do not replace that product contract with this summary.

## 2026-10-31 specification audit and next coding gate

The canonical Persian product document has been expanded with **section 19**, current Odoo/industrial-training benchmarks and standards, and **section 20**, a behavior-level implementation contract for Activity -> Competency Requirement -> Person Assignment -> Evidence/Assessment -> Qualification -> explainable Gap, coverage, LMS lifecycle, delegated permissions, and phased acceptance. Section 18 contains the fully specified new-employee onboarding path. These sections are **design contracts, not built features or approved schema/API migrations**.

Critical current-code mismatch for the next phase: the preview's lone `training` workspace page currently requires `training.ai.author`. This must remain a narrowly scoped authoring-preview permission, **not** the authorization model for learners, Buddy, supervisors, technical assessors or company training managers. Define independent training pages/actions and server guards; do not grant everyone AI-authoring or global `users.manage` merely to access the module. Confirm the shared `pageAvailability` behavior with the current core developer before integration.

No Stage 4 implementation, new migration, merge or deployment is authorized by this documentation-only audit. See the canonical product document for precise decision points that must be reviewed by the owner.

## Cross-module AI and local RAG architecture — 2026-10-31

**Authoritative full product specification:** Persian product document section **22**. The owner decided on an optional shared knowledge/retrieval and AI-provider capability for all entitled modules, while the Training module owns its authoring assistant. Employee-facing AI is a cross-module personal knowledge assistant, not a Training-exclusive chatbot. **Offline-by-design:** course display, onboarding, quizzes, deterministic Skill Gap, records and keyword search must work with no LLM or cloud connection.

A separately authorized external ChatGPT/AI session may create a **portable, schema-validated content package** (lessons, exams, source references, onboarding material) from permitted files, but must **not** change application code, database schema, tenant data directly, permissions, or publish content. Import is draft/quarantine -> preview/map -> specialist review -> publish. The current `sfp24.training-authoring-intake` JSON is input metadata only, **not** the content package format.

RAG/embeddings should initially reuse per-tenant MariaDB plus CompanyFiles; no second vector database is a prerequisite. Evaluate MariaDB native VECTOR only after confirming target MariaDB version (stable in 11.8) and measured Raspberry Pi capacity; reliable keyword-search fallback is mandatory. Scope-filter retrieval before any local/cloud LLM receives source text. Keep core AI service ownership with the core team, not a broad Work 11 core refactor. Owner identified Raspberry Pi 5 (8 GB RAM) as the intended host. Do not select or install local AI models now: at implementation/deployment time, explicitly ask the owner to confirm current OS, storage, MariaDB version, load and authorization before making runtime or migration choices. No performance or deployment promise. **Documentation only; no Stage 4 code approval.**

## Learner account and industry policy decision — 2026-10-31

The product owner selected **personal, authenticated mobile learner access for every worker as the primary experience**, complemented by actual in-person OJT, Buddy/site induction, observed practical performance and separately authorized qualification decisions where applicable. Industry/tenant/site/activity policies must be configurable and versioned, separating invariant product security/evidence rules from company choice and authoritative legal/standard/customer requirements. **See Persian product specification section 23 in full**; do not infer a universal annual refresher, 80%-pass threshold, or mandatory practical signoff for every course.

**Hard identity blocker:** current `server/platform/accounts/service.ts` counts all active `company_users` against `seat_limit` under `active-humans-v1`. A new learner account does **not** escape that rule today. Do not silently bypass it by adding a learner role or an uncounted login path. Learner authentication, account category, commercial learner capacity and backward-compatible policy-version changes need a separate owner/core-team design and authorization before execution. Distinguish a Person with no login from a Learner with an authenticated personal login. Maintain an optional staff-verified in-person evidence path, not shared passwords or pretend self-certification.

The Work 11 release target remains integrated **Skill Gap + LMS + Employee Onboarding**, with staged implementation/testing and no new coding approval from this documentation change.
