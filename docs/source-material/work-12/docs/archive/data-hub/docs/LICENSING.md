# Dependency licensing evidence

No upstream IoT platform source is included. This project's own source has no public open-source license assigned; the owner can choose its distribution policy separately. A zero-cost dependency is not an unconditional grant to redistribute it without notices.

The exact installed package metadata (including build/test tooling) is inventoried in [DEPENDENCIES.json](DEPENDENCIES.json). Versions are pinned in the lockfile. Vue, Fastify, Aedes, ExcelJS, mqtt.js and Lucide declare MIT in their installed metadata. Keep applicable copyright/license notices. Bundled Vue and Lucide notices are retained in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

Items requiring specific attention before commercial packaging:

- **mariadb 3.5.4:** LGPL-2.1-or-later, confirmed by the installed package/license and the [official connector repository](https://github.com/mariadb-corporation/mariadb-connector-nodejs). It is an optional dynamically loaded polling driver, not the hub database server. Do not strip its license or represent it as MIT. Packaging obligations depend on how the library is distributed/modified. MariaDB's [licensing FAQ](https://mariadb.com/docs/general-resources/community/community/faq/licensing-questions/licensing-faq) discusses connector distribution and distinguishes it from distributing the server; this does not replace reviewing the actual license.
- **jszip 3.10.2:** installed metadata offers MIT OR GPL-3.0-or-later. Record the selected MIT option and retain its notices if distributing it.
- **buffers 0.1.1:** installed tarball has no license field/file. A different maintained repository contains MIT/X11 metadata, but the original repository/commit could not be verified during this run. This inventory therefore leaves the exact installed artifact's permission **UNVERIFIED**. Resolve provenance or replace its dependency path before commercial redistribution. Local technical tests are not a legal clearance.

No AGPL platform is installed in this version. This document inventories evidence; it does not promise blanket commercial compatibility of every possible future bundle.
