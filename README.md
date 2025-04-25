# Bank Nifty Trading System 🏦📈

A configurable algorithmic trading system focused on Bank Nifty futures, supporting High-Risk and Low-Risk strategies. Features include backtesting, forward simulation (virtual trading), stress testing, and reporting.

## 🚀 Features
- Supertrend-based strategies (with VIX adaptive logic)
- Margin & leverage simulation with risk management
- Backtesting engine with benchmark comparison (NIFTYBEES)
- Forward simulation for virtual trading
- Automated reporting & interactive visualizations
- CI/CD integration for continuous testing
- Scalable architecture for multi-asset trading (Phase 2 Ready)

## 📂 Project Structure
```plaintext
/trading-system/
  ├── backtrader/       # Strategy logic
  ├── data/             # Data fetching & preprocessing
  ├── reports/          # Reports & visualizations
  ├── scripts/          # Run backtests & simulations
  ├── config/           # YAML configs
  ├── tests/            # Unit & integration tests
