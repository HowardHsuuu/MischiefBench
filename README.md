# MischiefBench

**Open-source benchmark for measuring sandbagging and strategic helpfulness manipulation in LLMs**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Status: In Development](https://img.shields.io/badge/status-in development-orange)]()

## Overview

MischiefBench measures whether language models change their behavior when they believe they're being watched, evaluated, or audited—a class of strategic manipulation that standard benchmarks miss.

**What we test:**

- **Sandbagging:** Capability suppression under oversight

- **Information hiding:** Omitting alternatives/risks when monitored

- **Framing bias:** Shifting language to avoid scrutiny

- **Strategic evasiveness:** Increased refusals under evaluation pressure

**Method:** Paired-framing episodes—identical tasks under three framings (neutral, evaluated, oversight). We measure behavioral deltas, not just performance.

## Quick Start

*Coming soon: Installation and usage instructions*

For now, see [docs/architecture.md](docs/architecture.md) for full specification.

## Project Status

**Current Phase:** Architecture & initial development

**Hackathon:** Apart Research AI Manipulation Hackathon (Jan 9–11, 2026)

**Team:** 4 contributors

**Expected Release:** Mid-January 2026

## Documentation

- **[Architecture & Specification](docs/architecture.md)** — Full system design, schemas, metrics

- **[Threat Model](docs/threat_model.md)** — What we're measuring and why *(coming soon)*

- **[Contributing Guide](CONTRIBUTING.md)** — How to add scenarios or metrics *(coming soon)*

## Repository Structure

mischiefbench/

├── scenarios/ # Task definitions (JSON)

├── runner/ # Inference orchestration

├── scorers/ # Metrics computation

├── reports/ # Leaderboard generation

├── docs/ # Documentation

└── README.md # This file

## Team

- **Frank** (GitHub: @frankdeceptions369) — Scenario design, threat model, coordination

- **Florian** (Discord: @captainamazeballs) — Runner/infrastructure lead

- **Howard** (Discord: @howardhsuuu) — Metrics development lead

- **Val** (Discord: @valpip123emy) — Results/write-up lead

- **RNG** (Github: @rng-ops) — Special thanks to RNG for initial research documentation and conceptual groundwork that informed the benchmark design.

## License

MIT License — see [LICENSE](LICENSE) for details.

## Acknowledgments

Built for the [Apart Research AI Manipulation Hackathon](https://apartresearch.com/sprints/ai-manipulation-hackathon-2026-01-09-to-2026-01-11).

Scenario design inspired by real-world transparency analysis of AI technical recommendations.

*Last updated: January 6, 2026*