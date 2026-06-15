# railway-skipped-builds-repro

Minimal, deterministic repro of the `SKIPPED_BUILDS` cross-environment image-bleed bug.

The build cache is keyed on `serviceId + treeSha + buildConfigHash` (no `environmentId`).
A build-time value (`MARKER`) is baked into the image. When two environments of the
same service deploy the **same git tree** with the **same build config**, the second
deploy reuses the first environment's cached image — including its baked-in `MARKER`.

## How it fires

1. Both environments track `main` and set a per-environment `MARKER` build variable.
2. `SKIPPED_BUILDS` is enabled on the service (admin-only flag).
3. The **donor** environment deploys first → real build → bakes its `MARKER` → seeds the cache row.
4. The **victim** environment deploys the same commit → cache hit → build skipped → it serves the donor's image.

## What you see

In the victim environment's logs:

```
BOOT baked=baked_marker=<DONOR>  runtime=MARKER=<VICTIM>
```

`baked` (build time, bled across envs) disagrees with `runtime` (correct per env). That gap is the bug.
