# ADR-002: Extract Platform Realizations into Independent Repositories

## Status

Authorized

## Date

2026-06-22

## Context

The agnostic Aeostara repository contained permanent Windows, macOS, and iOS implementation branches. The product authority model requires the agnostic base design and downstream native realizations to be separate products.

## Decision

Create `flynn33/Aeostara-Windows`, with `platform/windows` imported to destination `main` without history rewrite.

Create `flynn33/Aeostara-Mac-iOS`, with an implementation-free coordination `main` and exact-history `platform/macos` and `platform/ios` branches.

After source and destination commit, tree, history, workflow, protection, base-pin, and rollback evidence passes twice, delete the three platform branches from `flynn33/aeostara`. Preserve exact source heads through annotated archive tags and verified Git bundles.

## Constraints

No platform branch merges into agnostic `main`. Apple implementation branches never merge into coordination `main` or each other. Imported history is not squashed, filtered, rebased, or force-rewritten. Destination repository creation does not declare platform runtimes shippable. Agnostic schemas, enums, ASH semantics, and lifecycle remain unchanged. Secret values are not exported or committed.

## Consequences

Agnostic `main` becomes a clean independent base-design product. Windows and Apple implementations receive independent lifecycle, governance, CI, release, wiki, and issue surfaces. Destination repositories pin an exact Aeostara base release. Source platform branches cease to be active products after verified cutover.

## Acceptance

This decision is complete only when repository-separation gates pass twice, source branches are deleted and reconstructable, destination protections and workflows pass, final base pins resolve to the released agnostic commit, and the final judgment is `CONFORMANT`.
