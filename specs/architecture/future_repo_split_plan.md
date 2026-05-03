
# Multi-Repo Consumption Model

This document supersedes earlier repo-split planning language. The repo split is now an active consumption model: Aeostara is the platform-agnostic base design, and platform implementations live downstream.

## Model

- ASH Pattern System remains upstream semantic authority.
- Aeostara binds ASH into a JSON configuration healing base design.
- Windows, Mac, and iOS repositories consume Aeostara through version pins and conformance reports.

## No Active Platform Branch Dependency

Aeostara base-design completion does not require platform branches or native source files. Branch/profile artifacts may be kept only as downstream templates or historical references. Active base CI validates base design artifacts, not platform implementations.

## Downstream Consumption Flow

1. Platform repo pins an Aeostara version.
2. Platform repo maps contracts and interfaces to native modules.
3. Platform repo runs Aeostara fixture vectors.
4. Platform repo records module mapping, verification report, diagnostics report, materialization boundary report, deviation log, and acceptance judgment.
