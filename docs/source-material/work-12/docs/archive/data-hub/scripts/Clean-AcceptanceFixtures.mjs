/** Remove only device records created by tests/browser.mjs, never user or seeded devices.
 * Run with the hub stopped. Refuse removal if any device acquired telemetry/history. */
import { Store } from '../dist-server/server/store.js';
const store = new Store();
try {
  const candidates = store
    .list('devices')
    .filter(
      (d) => d.name === 'Acceptance test device' || /^Acceptance test device \d{13}$/.test(d.name),
    );
  for (const d of candidates) {
    if (d.sample || d.tenantId !== 'atlas') throw new Error('Refusing an unexpected test device');
    const samples = store.db
      .prepare('SELECT count(*) AS n FROM samples WHERE device_id=?')
      .get(d.id);
    if (
      Number(samples.n) > 0 ||
      store.list('commands', d.tenantId).some((c) => c.deviceId === d.id) ||
      store.list('sources', d.tenantId).some((s) => s.deviceId === d.id)
    )
      throw new Error('Device has history; no fixture removed');
  }
  store.tx(() => {
    for (const d of candidates) {
      store.db
        .prepare("DELETE FROM entities WHERE kind='devices' AND id=? AND tenant='atlas'")
        .run(d.id);
      store.audit('atlas', 'acceptance-test', 'test.fixture_removed', d.id, d.name);
    }
  });
  console.log(
    `${candidates.length} empty browser-test devices removed; 50 seeded devices preserved.`,
  );
  for (const source of store
    .list('sources')
    .filter((s) => /^Acceptance API fixture \d{13}$/.test(s.name))) {
    if (source.enabled) throw new Error('Test API fixture unexpectedly enabled');
    store.put('sources', { ...source, name: 'Local API sample (disabled)', sample: true });
  }
} finally {
  store.close();
}
