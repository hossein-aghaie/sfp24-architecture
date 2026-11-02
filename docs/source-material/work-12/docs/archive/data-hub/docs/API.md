# Local API contracts

Base URL: `http://127.0.0.1:5220`. Management routes use the login session; device routes use `Authorization: EdgeKey <device-key>`. Never put credentials in a URL.

## Device telemetry

`POST /api/v1/ingest`

```json
{
  "device_id": "atlas-edge-01",
  "samples": [
    { "signal": "processed_count", "value": 0, "time": "2026-10-18T10:00:00Z" },
    {
      "signal": "temperature",
      "value": 25.4,
      "time": "2026-10-18T10:00:00Z",
      "event_id": "optional-stable-source-id"
    }
  ]
}
```

The optional `device_id` must match the key. Company/tenant fields in the body confer no authority. Signal must exist on the device. Minute delta requires a nonnegative integer and a minute boundary. Timestamps require Z or explicit offset. Maximum 2,000 samples/request; JSON body 16 MB. HTTP returns a receipt after commit with `id`, `accepted`, `duplicate`, `conflict`, `rejected`, per-row reasons, `receivedAt`. A 200 response may contain rejected rows: inspect the receipt.

Minute identity: company+device+signal+normalized UTC minute, even if source event ID changes. Gauge/state/cumulative identity: company+device+signal+(source event ID or normalized timestamp). Equal content is duplicate, different content at the same identity is conflict and never overwrites an old value.

MQTT 3.1.1: `mqtt://127.0.0.1:5221`, username device ID, password device key, QoS1. Publish the same payload to `devices/{id}/telemetry`; subscribe only to `devices/{id}/commands`; publish command results to `devices/{id}/acks`. Other-device topics, retained publications and payloads above 256 KB are refused. PUBACK follows the ingestion transaction; invalid/conflicting publications are rejected and may disconnect the sender. Use HTTP receipts/management history to diagnose individual rows. A configured disabled HTTP/MQTT source blocks that receiving path; otherwise authenticated registered devices can ingest without an extra source record.

## Commands

HTTP agent polls `GET /api/v1/device/commands`, executes each command ID once, and posts `POST /api/v1/device/ack`:

```json
{
  "command_id": "<id>",
  "status": "succeeded",
  "result": { "simulated": true, "intervalSeconds": 5 }
}
```

Status `received` means acknowledged, not executed; terminal statuses are `succeeded` or `failed`. HTTP polling returns registry fields `id`, `method`, `params`, `expiresAt`. MQTT command envelope is `command_id`, `method`, `params`, `expires_at`; results use the same ACK shape above. Agents must reject expired commands. Maximum result JSON is 8 KB; sensitive key names are redacted.

## Deliver to another application

Generic webhook envelope:

```json
{
  "schema_version": 1,
  "event_id": "<stable-hub-event-id>",
  "company_id": "atlas",
  "device_id": "atlas-edge-01",
  "signal": "processed_count",
  "value": 0,
  "unit": "pcs",
  "measurement": "minute_delta",
  "event_time": "2026-10-18T10:00:00.000Z",
  "received_at": "<UTC-ingestion-time>"
}
```

The receiver owns binding hub company/device IDs to its company/resource IDs. These independent sample IDs do not automatically match original application UUIDs. Commit before replying 2xx with `{"accepted":true,"event_id":"<same-id>"}`. The `Idempotency-Key` header is the same event ID. A timeout can occur after receiver commit; duplicates are expected on retry. Receiver deduplication remains mandatory. Eight attempts with exponential backoff capped at 60 seconds, then manual retry. Disabled destinations retain their pending rows without blocking others.

Optional `pouyeshgar-count` format is based only on the supplied programmer handoff:

```json
{
  "schema_version": 1,
  "node_id": "<explicit-connection-node>",
  "samples": [{ "time": "2026-10-18T10:00:00.000Z", "qty": 0 }]
}
```

It requires one selected device and node ID and routes only `processed_count/minute_delta`. Expected receipt has `rawEventId` and accepted/duplicate/conflict/rejected counts. Conflicts require review. The application consumer must still bind resources and prevent duplicate production claims. **Actual original-app integration, EdgeKey configuration, entitlement checks and final production consumption are unverified and have not been called.** Other signals must use a separately agreed generic receiving contract.

## Management

- `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/bootstrap?company=<id|all>`.
- `POST /api/{companies|devices|sources|destinations|users}` and `PATCH /api/{kind}/{id}`. No hard-delete endpoint: disable devices/connections or suspend a company. Company edits are owner-only; users cannot create an owner through these routes.
- `POST /api/devices/{id}/rotate-key`: key shown once, old key invalidated and MQTT clients disconnected.
- `GET /api/events?company=&device=&before=&from=&to=&limit=100` (max 500/page); `GET /api/receipts/{id}`.
- `POST /api/import/preview` `{name,base64}`: CSV/XLSX first sheet, headers unique, no formulas, max10 MB/2,000 rows. `POST /api/import/commit` `{deviceId,sourceId?,rows,mapping:{timeField,valueField,signal,valueType}}`. Empty numeric cells remain missing, not zero.
- `POST /api/sources/{id}/run`: enabled API/database source. Cursor advances only after commit without rejected/conflicting rows.
- `POST /api/commands` `{deviceId,method,params}`; `POST /api/commands/{id}/cancel`.
- `POST /api/deliveries/{id}/retry`, `POST /api/destinations/{id}/backfill` (latest 2,000 eligible events, duplicates ignored).

Bootstrap returns up to 300 recent events, 200 deliveries, 100 receipts/audit rows and 200 commands; it is not a full export. The event table has cursor pagination and exports only its currently loaded/filtered rows. Connected count is **active MQTT sessions**, while HTTP devices expose last contact separately. A received HTTP sample does not establish a persistent connection.
