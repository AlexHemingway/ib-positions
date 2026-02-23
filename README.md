## 📊 ib-positions

**ib-positions** is a lightweight, async-first Python client for retrieving and structuring portfolio positions from Interactive Brokers (IB Gateway / TWS).

Designed for:

* Quant research pipelines
* Portfolio monitoring systems
* Risk and exposure analysis
* Live or batch position snapshots
* Downstream alpha modeling workflows

Built with modern Python tooling:

* `uv` for dependency management
* `asyncio`-native client
* `pydantic` data validation
* `pytest` + CI integration
* `src/` layout for production-grade packaging

---

## 🚀 Features

* Async IB connection handling
* Structured position models
* Pandas-ready output
* Type-safe models (Pydantic v2)
* CI-tested and coverage-enabled
* Clean modular architecture

---

## 🏗 Project Structure

```
ib-positions/
│
├── src/
│   └── ib_positions/
│       ├── client.py        # IB connection + data fetch logic
│       ├── models.py        # Typed position models
│       ├── main.py          # Example entrypoint
│       └── __init__.py
│
├── tests/
├── pyproject.toml
├── uv.lock
└── README.md
```

This project follows the **`src/` layout**, preventing import leakage and ensuring packaging correctness.

---

## 🔧 Installation

This project uses **uv** for dependency management.

Install dependencies:

```bash
uv sync --extra dev
```

Run tests:

```bash
uv run pytest
```

Run with coverage:

```bash
uv run pytest --cov=ib_positions --cov-report=term-missing
```

---

## 🔌 Running with IB Gateway

1. Start **IB Gateway** or **TWS**
2. Enable:

   * API access
   * Socket port (default 7497 for paper)
3. Ensure:

   * `localhost`
   * Correct client ID
   * Paper/live mode alignment

Run:

```bash
uv run python -m ib_positions.main
```

---

## 🧪 Testing Philosophy

* Unit tests isolate client logic
* Async test support via `pytest-asyncio`
* Coverage reporting enabled
* CI pipeline validates every push

Goal: reproducible, production-safe research infra.

---

## 📈 Design Goals

This package is intended to be:

* A foundation for real trading infrastructure
* Composable into risk pipelines
* Suitable for systematic portfolio construction
* Extendable toward:

  * Greeks
  * PnL attribution
  * Factor exposure mapping
  * Real-time risk monitoring

---

## 🧠 Roadmap

Planned improvements:

* Position → factor exposure mapping
* Portfolio-level aggregation utilities
* Risk metric computation (VaR, ES)
* Real-time streaming support
* IB execution wrapper
* Structured logging
* Metrics export (Prometheus-compatible)
