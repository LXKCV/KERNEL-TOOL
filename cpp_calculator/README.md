# ProCalcX (Qt6 / C++20)

Professional desktop calculator architecture with modular modes: basic, scientific, programmer, converter, notes, history, graph, and equation solver.

## Features included
- Modern Qt6 UI shell with sidebar navigation and dark theme
- Expression engine service with modular extension point
- Persistent settings/history/notes via JSON
- Scalable services/modules/plugin-ready folder layout
- Cross-platform build for Linux + Windows with CMake

## Build (Linux)
```bash
sudo apt install qt6-base-dev qt6-charts-dev nlohmann-json3-dev cmake g++
cmake -S . -B build
cmake --build build -j
./build/ProCalcX
```

## Build (Windows)
1. Install Qt6 (MSVC), CMake, and vcpkg/conan for `nlohmann_json`.
2. Configure from **x64 Native Tools Command Prompt**:
```powershell
cmake -S . -B build -DCMAKE_PREFIX_PATH="C:/Qt/6.x/msvc..."
cmake --build build --config Release
.\build\Release\ProCalcX.exe
```

## Architecture
- `src/app`: bootstrap and wiring
- `src/core`: parser/evaluator engine
- `src/services`: settings/history/notes persistence
- `src/modules`: mode-specific domain logic (extensible)
- `src/ui`: widgets/pages/main shell
- `themes/`: runtime QSS themes
- `assets/`: icons/sounds/animations
- `data/`: local persisted user files

## Planned extension points
- currency API provider plugin
- rich formula syntax highlighter + markdown notes editor
- mini graph visualizer via Qt Charts
- startup animation + sound FX manager
- equation solver and symbolic pipeline

