# Industrial Data Hub — HTTP minute-count slice

## Historical first slice

The HTTP contract below remains valid. Its preview-only consumer and missing transport/UI statements describe the first slice and are superseded by [PRODUCTION-DATA-SOURCES.md](../../guides/PRODUCTION-DATA-SOURCES.md). Current browser acceptance is `scripts/data-sources-qa.mjs`; the old script name delegates to it.

This independent branch extends the existing Factory workspace. It does not replace the Phase 2 scene, company accounts, workspaces, manual production or reports. No existing owner database has been upgraded by the local browser fixture.

## Implemented boundary

`HTTP adapter → immutable parsed raw event → minute normalization → processed_count → time-effective resource assignment → Production input binding → read-only count preview`

`src/data-hub/contracts.ts` owns signal semantics. `server/data-hub/normalize.ts` validates transport data, independently of Production. `server/data-hub/service.ts` owns ingest, provenance, quality, assignment and consumer lookup. `server/data-hub/http.ts` is the versioned HTTP adapter. `src/data-hub/DataHubWorkspace.vue` is a page in the original Factory shell. All company records use the existing tenant storage resolver and standard migrations.

Only `processed_count` is operational. `final_scrap_count`, `machine_state` and `operator_activity` are future typed registry entries, not implemented receivers. Node identity is opaque and is not globally trusted. A company-specific hashed device key selects the connection and tenant; a body cannot select a database/company. Provider sessions are denied tenant Hub APIs.

## Packet contract v1

This is a new, explicitly documented test contract, **not a verified implementation of the real EdgeBox firmware**:

```json
{
  "schema_version": 1,
  "node_id": "neway-fictional",
  "samples": [
    { "time": "2026-10-15T09:00:00Z", "qty": 10 },
    { "t": "2026-10-15T09:01:00Z", "q": 0 },
    { "T": "2026-10-15T09:02:00Z", "Q": 23 }
  ]
}
```

- `POST /api/v1/data-hub/ingest/http`, `Authorization: EdgeKey <one-time connection credential>`; user Bearer sessions are not device keys.
- Timestamp is the **start** of a completed 60-second interval, with `Z` or explicit offset. Stored as UTC epoch milliseconds. No silent rounding, no ambiguous local strings, no cumulative-count interpretation. Every interval must have ended by server receipt time. Device clock synchronization is a deployment prerequisite; no future-clock correction is guessed.
- Each sample uses exactly one alias pair. Count is a nonnegative integer, maximum 1e9 pieces per minute. That maximum is an input safety bound, not a claimed machine capacity. At most 1440 samples / 256 kB per batch. Malformed batches are rejected atomically before raw inserts, with a specific error code; rejected bodies are not archived. There is no quarantine console in this slice.
- Counts mean **all processed pieces**, including good pieces and final scrap. They do not prove good output, runtime, operator, part or OP. Zero is a received zero, missing is no received interval. Neither proves a stopped or offline machine.
- Live-path backlog is configurable 1–30 days (default 7). `/http/replay` permits older data only for a connection explicitly created as `SIMULATOR`. It still rejects incomplete/future minutes. The UI always labels mode and separates event time from receipt time.
- Late means receipt more than 120 seconds after interval end; it remains valid if otherwise accepted. This is a transport diagnostic, not an OEE or downtime rule.
- Identical connection/signal/minute/count retries create receipts/raw history but only one canonical measurement. Conflicting counts append evidence, preserve the first count, mark the interval disputed and **exclude it from the valid total**. A later matching retry does not resolve a conflict. Conflict resolution is not implemented.
- Raw is the original parsed JSON value serialized server-side, with SHA-256 hash; it is not a byte-for-byte HTTP wire capture or signed/tamper-proof ledger. Authorization headers are never part of it. Runtime DB grants allow INSERT/SELECT only on event/measurement/conflict/receipt tables; DB administrators remain privileged.
- Range is `[from,to)`, minute-aligned, at most 7 days. UI inspection returns the first 1000 samples and 200 compressed gaps with actual totals/counts. The total covers the full requested range, not just the displayed sample subset. No retention deletion job yet; size/capacity planning is required before production.
- In-process IP/connection rate limits protect this single-instance pilot; no shared multi-instance limiter or production TLS termination is installed. Connections must use HTTPS before a real remote feed is enabled. No real device was contacted.

## Tables and migration

Forward migration 6 adds central `data_hub_keys` (only hashes and routing) and tenant `hub_connections`, `hub_assignments`, `hub_bindings`, `hub_raw_events`, `hub_measurements`, `hub_conflicts`, `hub_ingestion_receipts`. Prior migration SQL/checksums remain unchanged. Existing provisioning applies latest standard migrations and grants. Migrate a target installation only after reviewing backups and provisioning permissions; the web runtime cannot apply DDL.

Assignments have valid-from/to and retain prior resource identity. An initial assignment can cover previously unassigned historical data. A subsequent transfer starts no earlier than the next minute and latest received measurement end; it cannot rewrite prior mapping. A Production binding selects one processed-count source for a resource/range. Concurrent bindings are serialized by resource and overlapping active intervals are rejected. Disabling a connection/key/binding preserves history.

`data_hub.manage` and `data_hub.read` are company-wide permissions for shared data infrastructure, attached to the existing accounts core. No new commercial module/pricing policy is invented. Production consumption also requires its purchased/ready module plus the user's scoped `production.enter`; owning a role or a device key does not grant it. Existing explicitly restricted workspace policies may need the new page enabled by their company manager; the page is not forced into a user's policy.

Keys are random, shown/downloaded only at creation or rotation, hashed in the central database, never retrievable. Rotation revokes previous keys. Connection disable, company suspension and key rotation are coordinated with in-flight ingestion. Settings/key/binding actions use the existing audit facilities without secrets. There is no automatic key expiry in this first slice; managers rotate/revoke them explicitly.

## Manual check with fictional data

1. Use an **isolated upgraded test company**, then Factory → **منابع و اتصالات داده / Data sources & connections**. Define a resource with pieces (`pcs`) in Master data first.
2. Create HTTP connection, choose `SIMULATOR`, enter a fictional node ID and select that resource. Save the one-time key JSON privately, outside Git. Choose an assignment start before the test range.
3. In Connection/mapping settings create `processed_count → Production` binding. The Production module must be purchased/ready. Mapping/binding does not manufacture part or OP attribution.
4. From the repository root, use Node ≥22.12:

   ```powershell
   node scripts/send-hub-demo.mjs --key-file <private-downloaded-key.json> --node <fictional-node-id> --url http://127.0.0.1:5197
   ```

   This sender refuses non-loopback targets and uses the SIMULATOR-only replay route. It generates six completed minutes `[10,20,0,30,40,23]`, total **123**. Output shows the exact `[from,to)` to select in the panel. UI datetime fields are explicitly Gregorian/Tehran; API timestamps are UTC. To repeat an identical packet later, save a packet privately and use `--packet <packet.json>` instead of regenerating timestamps.
5. Select that exact six-minute range, inspect coverage/zero/receipt times and raw provenance. Enter **3 final scrap in the preview calculator**, giving **120 good**. **This does not save a production report.** Repeat identical timestamps/counts: total remains123. Omit a minute: gap appears; send it late: coverage becomes complete. Send a different count for an existing minute: conflict remains visible and the trustworthy total excludes it.

The `GET /api/v1/company/data-hub/production-count?resourceId=…&from=…&to=…` consumer lookup is operational and returns mapping/binding/measurement provenance plus `reportIntegration: preview_only`. The existing ProductionEditor remains MANUAL. No telemetry report evidence is persisted, intervals are not reserved across reports, and a final manual report is never silently recalculated from later telemetry. Automatic form attachment requires explicit part/OP/time attribution, durable evidence snapshots, interval reuse controls and correction semantics; those are intentionally deferred rather than delivering an unsafe half-integration. The `CountEvidence` TypeScript shape is a future contract, not a shipped persistence feature.

## Extension contracts; not shipped connectors

Future adapters should convert a source-specific envelope into a validated typed signal with authenticated connection, source event/receipt times, unit, interval/value semantics, quality, raw provenance and idempotency identity. They must not write Production rows directly or bypass assignment/licensing/scoped permission checks. Cumulative counters require their own reset/rollover adapter; never reinterpret them as minute deltas. MQTT, OPC UA, SCADA, RFID/operator activity, REST polling and external SQL remain unimplemented. A future mapping wizard may preview/validate vendor fields before saving an adapter configuration; arbitrary executable transformations and SQL are not permitted by this contract. No standards certification/compliance is claimed.

No Custom Dashboard tab, iframe or Grafana server was added. A future Grafana connector should call an authenticated, read-only, company-bound aggregate API via its server, with explicit allowlisted metrics/time ranges and audit, never expose tenant DB credentials, never rely on browser-supplied tenant IDs, and never make a public shared dashboard bypass company/user permissions. Company managers may later save permitted widget/query definitions; widget layout cannot grant data access. Keep the original Three.js scene and reporting source contracts independent of that renderer.
