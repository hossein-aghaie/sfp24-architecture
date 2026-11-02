# Operator count feedback — 2026-10-16

Owner field-test screenshot exposed a misleading form: a connected source had only 56 of 480 required minutes, yet its partial sum appeared in the report total. The server correctly refused missing count evidence, but its message suggested a mandatory fetch action. Scrap reason quantity 100 also disagreed with final scrap 5.

- Existing initial and selection-triggered count loading is retained; visible draft forms now poll every 15 seconds, with no overlapping poll and no required fetch button. Network failures retain an explicit retry action.
- Partial counts remain visible as provisional source information, never as the report's complete total. Complete evidence fills the total automatically; good output derives from count minus manually entered final scrap.
- Incomplete/error source states stop saving before a report request and explain the work-period requirement. Scrap reason mismatch is shown beside reasons and blocks final submission. Backend validation, source evidence, override permission/reason, and immutable finalized snapshots remain unchanged.
- No tenant settings, reports, passwords, source data, or running services were modified by this change.

Validation: Vue typecheck and Vite build passed; 9 focused domain/workspace/feedback tests passed. `scripts/production-feedback-qa.mjs` mounts the real Vue form with an explicitly fake API and exercises initial fetch, actual polling without a fetch click, incomplete count protection, good-output calculation, scrap mismatch, and submission. Screenshots and result are ignored under `.local/qa/production-feedback`. This is component browser QA, not a new real MariaDB report-submission test or full product regression. User's actual report remains unsubmitted by the agent.
