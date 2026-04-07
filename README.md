# apple-adobe-MnA-simulation
A quantitative M&A analysis simulating a hypothetical acquisition of Adobe Inc. by Apple Inc., built entirely in Python using real financial data from Yahoo Finance.

## What This Project Does
- DCF valuation of both companies using computed WACC
- Full deal structuring (50% cash / 50% stock, goodwill, exchange ratio)
- 5-year pro forma financial statements
- Accretion/dilution analysis across base, bull, and bear scenarios
- Monte Carlo simulation (500 iters) with probability metrics
- Sensitivity heatmaps (WACC vs terminal growth, premium vs synergy realization)
- IRR analysis vs cost of capital
- Synergy NPV decomposition (5-year and 10-year)
- Credit ratio analysis (pre and post deal)

## Project Structure
mna_simulation/
├── src/
│   ├── data_loader.py
│   ├── company.py
│   ├── forecasting.py
│   ├── valuation.py
│   ├── deal.py
│   ├── synergies.py
│   ├── proforma.py
│   ├── accretion.py
│   ├── monte_carlo.py
│   ├── sensitivity.py
│   ├── irr.py
│   ├── synergy_decomposition.py
│   └── credit_ratios.py
├── models/
│   └── assumptions.py
├── main.py
└── requirements.txt

## Key Findings
- Deal is accretive in 100% of Monte Carlo simulations
- Base case Year 5 accretion: 5.56% | Year 10: 10.53%
- IRR: 13.94% vs WACC: 10.09% — spread of 3.85%
- Zero probability of dilution under any (simulated) scenario
- Post-deal Debt/EBITDA: 1.09x — within safe thresholds

## How to Run
pip install -r requirements.txt
python main.py

## Tech Stack
Python, pandas, numpy, yfinance, matplotlib, seaborn, numpy-financial

## Author
Abdulrahman Hameedi — BSc Applied Computer Science & AI
