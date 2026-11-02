# Architecture and extension guide

This is a new, independent implementation. StreamPipes was a visual reference; no StreamPipes, IoTSharp or OpenRemote code was copied. No original Pouyeshgar service, database, repository or device is used.

## Runtime

| Process                          | Responsibility                                                                  | Listener                                 |
| -------------------------------- | ------------------------------------------------------------------------------- | ---------------------------------------- |
| Hub, Node.js 24+                 | Fastify API, Vue static files, Aedes MQTT, SQLite, polling and delivery workers | HTTP 127.0.0.1:5220, MQTT 127.0.0.1:5221 |
| Simulator, separate Node process | 50 synthetic agents, its own persisted buffer and command execution ledger      | HTTP 127.0.0.1:5223                      |

No Docker, WSL, Java, .NET, Redis, NATS or external database server is needed for this lab. Aedes implements MQTT 3.1/3.1.1, not MQTT 5. The MQTT session store is in memory; application events, command intentions and delivery retries are in SQLite. We do not claim a durable MQTT session broker.

SQLite is an isolated local choice, not a proposed migration from MariaDB. One hub process owns the database. Run no second hub process against the same private/ directory. Production storage, retention, HA, TLS, quotas and deployment remain separate decisions; this lab is not a production readiness certificate.

## Boundaries

1. **Company and device registry:** owner sees all companies; company administrators see only their own. Device keys are random, stored as SHA-256 hashes and scoped to one device. Company identity comes from authenticated records, never from a telemetry body.
2. **Ingestion:** signal type, unit and measurement semantics are defined per device. HTTP, MQTT, file import, API polling and restricted MariaDB polling all use the same validation/transaction path.
3. **Persistence:** accepted samples, receipt and destination outbox entries commit in one transaction before acknowledgment. Zero is data. An absent value is not zero. Minute delta is not cumulative count, good parts, machine state, OP or production reporting.
4. **Delivery:** one durable entry per destination/event. Retried events retain the same ID. A receiver must deduplicate and acknowledge after its own commit. Receiving telemetry is distinct from delivering it and from consuming it as a production report.
5. **Commands:** `get_status`, `set_interval`, `pause_collection`, `resume_collection`. They affect a cooperating agent, never a physical machine. Durable queued/sent/acknowledged/succeeded/failed/expired/cancelled states remain distinct. Expiry is 120 seconds. MQTT retries up to four sends before expiry; HTTP agents poll pending intentions. Agents must persist command IDs/results and deduplicate execution.
6. **Simulator:** imports an exported credential profile and only speaks HTTP/MQTT. It never imports the hub database module. Simulated network outages retain queued batches in its own file. Each batch advances a logical minute; a five-second interval accelerates time and is not real minute production. Queue capacity is 500 batches per agent; collection pauses on a full queue rather than silently dropping data.

## Module map

| File                              | Change here when…                                                 |
| --------------------------------- | ----------------------------------------------------------------- |
| server/store.ts                   | storage, encryption, seeding or audit changes                     |
| server/domain.ts                  | signal validation, deduplication or ingestion transaction changes |
| server/management.ts              | company/device/source/destination/user schemas change             |
| server/connectors.ts              | file parsing, column mapping or polling changes                   |
| server/delivery.ts                | receiver format/acknowledgment or retry policy changes            |
| server/commands.ts                | supported command catalog or lifecycle changes                    |
| server/mqtt.ts                    | MQTT authentication/topics change                                 |
| server/app.ts                     | HTTP route/session boundaries change                              |
| server/index.ts                   | hub process lifecycle and worker scheduling change                |
| server/simulator.ts               | independent simulated agent behavior changes                      |
| src/App.vue                       | navigation, login or modal orchestration changes                  |
| src/Overview.vue / Records.vue    | operational views change                                          |
| src/Editor.vue / ImportWizard.vue | guided configuration/import changes                               |
| src/Simulator.vue                 | simulator interface changes                                       |
| src/i18n.ts / style.css           | translated interface text or layout changes                       |

The frontend emits user intentions; authorization is enforced again on the backend. Technical identifiers, raw payloads, imported values and upstream error text are not translated. English is the initial default, with saved Persian/RTL preference.

`src/navigation.ts` synchronizes the main page, guide tab and selected guide node with hash URLs and native browser history. It uses pushState for distinct navigation and restores popstate/hashchange; clicking the active item does not add another entry. Refresh and direct links restore the view after authentication. No new routing dependency is required. URL/history contains navigation identifiers only, never credentials, payloads or form drafts. It does not replay submissions when navigating Back or Forward.

## External connections are deliberately gated

Only the synthetic `/api/lab/source` and `/api/lab/receiver` are permitted by default. Other URLs need exact origin/path entries in `HUB_ENDPOINT_ALLOWLIST`; redirects are refused. Do not add the original application's endpoints without a separately reviewed integration step. Configuring a URL in the UI does not silently grant network permission.

MariaDB connector: localhost only, database name `pghub_lab_*`, explicit simple table/column identifiers, bound cursor parameter, read-only transaction, 200 rows/poll. It never runs DDL or arbitrary SQL. Use a dedicated least-privilege read-only account. No MariaDB server was installed; end-to-end database connectivity remains unverified. PostgreSQL is not implemented and a migration is not justified by these tests.

Source and destination secrets use AES-256-GCM with an ignored local master key. Do not lose the key or store it with public backups. Windows filesystem ACL hardening is a deployment task. Sessions are HttpOnly/SameSite=Strict, local same-origin only. This local HTTP lab has no public TLS or production identity provider.

## Follow-on work

Agree device provisioning, retention/archival, signal schema evolution, authentication policies, monitoring, backup/restore, Linux deployment and real agent contracts before production. SQLite data and raw receipt history currently grow until explicitly archived. A process memory snapshot does not measure the OS file cache or prove capacity. No exactly-once guarantee is made across a network.
