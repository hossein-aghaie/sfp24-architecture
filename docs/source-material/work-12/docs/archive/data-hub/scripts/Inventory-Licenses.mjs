/** Inventory installed package metadata; this is evidence, not a legal opinion. */
import { readdirSync, readFileSync, existsSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
const packages = new Map();
const root = 'node_modules/.pnpm';
function collect(path) {
  const json = join(path, 'package.json');
  if (!existsSync(json)) return;
  try {
    const pkg = JSON.parse(readFileSync(json, 'utf8'));
    if (!pkg.name || !pkg.version) return;
    packages.set(pkg.name + '@' + pkg.version, {
      name: pkg.name,
      version: pkg.version,
      license: pkg.license || pkg.licenses || 'UNSPECIFIED',
      repository: typeof pkg.repository === 'object' ? pkg.repository.url : pkg.repository,
    });
  } catch {}
}
for (const entry of readdirSync(root)) {
  const dir = join(root, entry, 'node_modules');
  if (!existsSync(dir)) continue;
  for (const name of readdirSync(dir)) {
    if (name.startsWith('@')) {
      for (const scoped of readdirSync(join(dir, name))) collect(join(dir, name, scoped));
    } else collect(join(dir, name));
  }
}
const rows = [...packages.values()].sort((a, b) => a.name.localeCompare(b.name));
writeFileSync(
  'docs/DEPENDENCIES.json',
  JSON.stringify(
    {
      note: 'Installed package metadata including development tooling. Verify notices and obligations before distributing binaries.',
      packages: rows,
    },
    null,
    2,
  ),
);
const notices = [
  '# Bundled frontend notices\n\nRetain these notices when distributing generated frontend assets. Full dependency metadata: DEPENDENCIES.json.\n',
];
for (const name of [
  'vue',
  '@vue/runtime-core',
  '@vue/runtime-dom',
  '@vue/reactivity',
  '@vue/shared',
  'lucide-vue-next',
]) {
  let dir = join('node_modules', name);
  if (!existsSync(dir)) {
    for (const entry of readdirSync(root)) {
      const candidate = join(root, entry, 'node_modules', name);
      if (existsSync(join(candidate, 'package.json'))) {
        dir = candidate;
        break;
      }
    }
  }
  for (const file of ['LICENSE', 'LICENSE.txt', 'LICENSE.md'])
    if (existsSync(join(dir, file))) {
      notices.push(
        '\n## ' + name + '\n\n```text\n' + readFileSync(join(dir, file), 'utf8') + '\n```\n',
      );
      break;
    }
}
writeFileSync('docs/THIRD-PARTY-NOTICES.md', notices.join(''));
console.log(
  JSON.stringify({
    packages: rows.length,
    licenses: [
      ...new Set(
        rows.map((p) => (typeof p.license === 'string' ? p.license : JSON.stringify(p.license))),
      ),
    ],
  }),
);
