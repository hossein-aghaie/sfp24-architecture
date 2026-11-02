# Company administration usability — work log

Branch: `feat/phase3-company-accounts`. Baseline before this change: `474950e`.

Owner requested a simpler owner/company administration workflow without email or weaker security. Existing Phase 2 operational data and workshop code are outside this change.

## Implemented and locally validated

- Add/edit company modal: name, active-account capacity, licensed modules; optional generated sign-in code and default initial administrator username.
- Queue-based automatic database preparation. A separate privileged local worker uses the existing provisioner; the HTTP runtime retains no DDL privilege or provisioner credentials.
- User creation/edit/disable with existing role templates. No email prerequisite. One-time expiring sign-in card lets the recipient choose a personal password before receiving an application session.
- Own password change with current-password verification. Company-scoped administrator resets; provider support requires password reconfirmation, reason, typed company code and a session/company-bound 10-minute authorization. Administrator targets require password reconfirmation and company confirmation again.
- Reset codes are hashed, single-use and expire; reset initiation and password completion revoke old sessions. Active users awaiting reset still consume capacity. Sensitive actions are audited without passwords or codes.
- Control migration 2 is additive; migration 1 and existing tenant geometry/data are unchanged. No billing, email delivery, MFA or arbitrary custom-role editor added.

## Evidence

- Default suite: 33 passed, 1 real-MariaDB test skipped as expected without opt-in.
- Final explicit isolated-local MariaDB suite: **50 passed, 0 failed, 0 skipped**, including worker provisioning, two-company isolation, capacity concurrency, support scope, stronger admin reset, temporary-code first login, replay/expiry, self-password change, session revocation, pending-user recovery and original-admin recovery after role changes.
- Local integration guard verifies the exact approved private config, loopback port 3317 and `.local/phase3/data` before creating random fixture databases. It never points at the owner's existing company database.
- Production typecheck/build passed. Two connected browser-QA rounds passed create/edit company, worker provisioning, admin/operator activation, viewer restriction, own password change, company-user reset and provider administrator recovery.
- Reviewed actual screenshots and corrected low-height dialog clipping, typography, mobile action placement and tables. Repeated RTL/LTR desktop and mobile captures passed horizontal-overflow checks with zero browser JavaScript errors. Artifacts are ignored under `.local/qa/phase3-usability`. No current GitHub CI result is implied.

## Local rollout completed

1. Private pre-migration backup verified; migration 2 applied and replayed successfully.
2. Private local launcher starts the separate worker alongside only its owned services. Fixed its UTC timestamp parsing guard; unrelated services were not restarted.
3. Browser fixtures are explicitly fictional separate companies. The owner's pre-existing test company and its administrator password were not edited by QA.
4. User guide and developer/security seams are documented in `COMPANY-ADMIN-QUICKSTART.md` and canonical entry documents.

Remaining limits: existing role templates only (no custom permission editor), no MFA/email/SSO/provider recovery UI or audit-view UI, no production-hardening/load/restore certification, and no tenant operational migration from Phase 2.

## Follow-up: reversible company deactivation

Owner requested deactivation now and manual cleanup of test companies later. Added migration 3 (`suspended` flag, independent from lifecycle), provider-only password-confirmed suspend/resume endpoint and FA/EN confirmation dialog/buttons. Suspended companies cannot log in, activate a code, use tenant storage or retain company sessions/provider support grants. User rows, passwords, entitlements, capacity, storage and onboarding status remain intact; resume requires fresh login. No deletion, DROP or cleanup performed. Added real-MariaDB coverage for permissions, wrong password, suspension during onboarding/provisioning, code blocking, tenant denial, other-company isolation, retained data and non-revival of sessions. **51 tests pass, zero skips.** Connected browser QA passed suspend → open-session rejection → resume → fresh company login, along with the full prior create/edit/password workflow. The test harness respects the existing authentication throttle; server limits were not weakened.

No merge, deployment, stash operation or new branch is authorized by this usability task. Local private launchers and test artifacts remain ignored under `.local/phase3`.

## Separate login entries

Owner requested separate entry links instead of owner/company tabs. Added `/owner/login`, `/company/login`, and `/company/<code>/login` with the company code prefilled/read-only. Owner company rows can copy the dedicated link; new sign-in cards use it. Legacy entry/activation URLs remain compatible, and fragments are still removed on load. No backend authentication or permission boundary was weakened. Route unit tests plus existing real-MariaDB tests pass **52/52**, zero skipped; typecheck/build pass. Connected browser acceptance passed against a disposable real Fastify/MariaDB test-provider/control database, avoiding the owner's personal password. Final read-only browser checks also passed on the normal laptop service for owner/company login forms, the dedicated company code, Persian mobile layout and legacy redirect. Screenshots were visually reviewed; no production service or existing account credential was changed. Production hosting/SPA fallback is not deployed or validated.

## Login presentation refinement

Owner rejected the explanatory company-account slogan and technical database status on the customer login. Replaced them with «نبض تولید، در یک نگاه» / “Your production. In focus.” and a short supporting line. Added `LoginEmblem.vue`, a decorative industrial mark with CSS 3D stacked planes and a tiny inline vector icon, not an official brand-logo replacement. No new dependency, raster background, model asset or WebGL canvas; transform-only slow motion stops under `prefers-reduced-motion`. Login footer is concise; unconfigured service state remains actionable. Owner/company routes, account forms and backend behavior are unchanged. Build/typecheck and credential-free Chromium checks passed for FA/EN desktop, Persian mobile, legacy redirect, no horizontal overflow, reduced motion and desktop viewport fit. Actual screenshots were reviewed under ignored `.local/qa/phase3-usability`. This visual-only change does not claim a new real-MariaDB acceptance run.
