# Compliance Rules

## Shipped Product Rules

1. **Native only** — shipped product must be a native compiled binary
2. **No Python** — shipped product must not depend on Python runtime
3. **No YAML** — shipped product must not include a YAML parser
4. **JSON-only v0.1** — all configuration files are JSON
5. **Code-agnostic specs** — shared behavior definitions on `main` remain code-agnostic; platform branches are native realization branches and may adopt platform-specific patterns
6. **Forsetti boundary compliance** — platform branches may integrate with their platform's Forsetti framework while observing boundary rules: no framework modification, no direct module-to-module communication, no direct OS communication, no module-owned UI, framework-mediated I/O only

## Repository Automation (Exempt)

Python and YAML are permitted in:
- GitHub Actions workflows (`.github/workflows/`)
- CI scripts (`ci/`)
- Repository automation scripts (`.github/scripts/`)

These are not part of the shipped product.

## Per-Platform Rules

### Windows (platform/windows)
- R001: Only MSVC, CMake, vcpkg, nlohmann/json, CppUnitTest, Windows SDK, WinUI 3
- R005: Interface-first design, all concrete types `final`, constructor DI
- /W4 /WX (warnings as errors)

### macOS (platform/macos)
- Native toolchain: Swift 5.9+, SwiftPM or Xcode-native
- Foundation-only shipped path (no C++, no Obj-C++, no CMake, no vcpkg)
- XCTest for testing

### iOS (platform/ios)
- Native toolchain: Swift 5.9+, SwiftUI, SwiftPM or Xcode-native
- Foundation-only shipped path (no C++, no Obj-C++, no CMake, no vcpkg)
- XCTest + XCUITest for testing
