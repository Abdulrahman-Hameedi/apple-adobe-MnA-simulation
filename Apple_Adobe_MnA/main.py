from src.data_loader import load_financials, save_financials
from src.company import Company
from src.forecasting import forecast_company 
from src.valuation import dcf_valuation, computeWacc
from src.deal import structure_deal
from src.synergies import compute_synergies
from src.proforma import build_proforma
from src.accretion import accretion_dilution
from src.monte_carlo import monte_carlo, probability_metrics
from models.assumptions import base_case, bull_case, bear_case
from src.sensitivity import wacc_vs_terminal_growth, premium_vs_synergy
from src.irr import compute_irr
from src.synergy_decomposition import synergy_npv_decomposition
from src.credit_ratios import compute_credit_ratios
import matplotlib.pyplot as plt


# 1. load the data
apple_data = load_financials("AAPL")
adobe_data = load_financials("ADBE")
save_financials("AAPL", apple_data)
save_financials("ADBE", adobe_data)

apple = Company("Apple", "AAPL", apple_data)
adobe = Company("Adobe", "ADBE", adobe_data)

# 2. Standalone Valuations
apple.forecast = forecast_company(apple, years=5)
adobe.forecast = forecast_company(adobe, years=5)

# Run Valuations
apple_dcf = dcf_valuation(apple)
adobe_dcf = dcf_valuation(adobe)
print("\n=====================================")
print("        Standalone Valuations        ")
print("=====================================")
print(f"Apple — Intrinsic Value/Share: ${apple_dcf['Intrinsic Value Per Share']:.2f} | WACC: {apple_dcf['WACC']:.2%}")
print(f"Adobe — Intrinsic Value/Share: ${adobe_dcf['Intrinsic Value Per Share']:.2f} | WACC: {adobe_dcf['WACC']:.2%}")

# 3. Scenario Analysis 
print("\n=====================================")
print("           SCENARIO ANALYSIS         ")
print("=====================================")
for scenario_name, assumptions in [("Base", base_case), ("Bull", bull_case), ("Bear", bear_case)]:
    deal = structure_deal(apple, adobe, assumptions)
    synergies = compute_synergies(adobe, years=5, assumptions=assumptions)
    proforma = build_proforma(apple, adobe, deal, synergies)
    acc_dil = accretion_dilution(apple, proforma)
    print(f"\n-- {scenario_name} Case --")
    print(f"  Purchase Price:    ${deal['Purchase Price']/1e9:.2f}B")
    print(f"  Goodwill:          ${deal['Goodwill']/1e9:.2f}B")
    print(f"  Year 5 Accretion:  {acc_dil['Accretion/Dilution %'].iloc[-1]:.2f}%")

# 4. Monte Carlo
print("\n=====================================")
print("           Monte Carlo Simulation    ")
print("=====================================")
deal = structure_deal(apple, adobe, base_case)
mc_results = monte_carlo(apple, adobe, deal, base_case)
print(f"\nMonte Carlo:\n{mc_results.describe()}")


plt.figure(figsize=(10,5))
plt.hist(mc_results["Year 5 Accretion %"], bins=50, color="steelblue", edgecolor="white")
plt.axvline(mc_results["Year 5 Accretion %"].mean(), color="red", linestyle="--", label=f'Mean: {mc_results["Year 5 Accretion %"].mean():.2f}%')
plt.axvline(0, color="black", linestyle='-', linewidth=1.5, label="Break-even (0%)")
plt.title("Monte Carlo: Year 5 Accretion/Dilution Distribution (Apple acquires Adobe)")
plt.xlabel("Accretion/Dilution %")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.show()

# 5. IRR
print("\n=====================================")
print("             IRR Analysis            ")
print("=====================================")

irr = compute_irr(adobe, deal, synergies, base_case)
apple_wacc = computeWacc(apple)
print(f"  IRR:     {irr:.2%}")
print(f"  WACC:    {apple_wacc:.2%}")
print(f"  Spread:  {irr-apple_wacc:.2%}")

# 6. Model Comparison 5-year vs 10-year
print("\n=====================================")
print("             Model Comparison        ")
print("=====================================")
for yr in [5, 10]:
    print(f"\n__{yr}-Year Analysis__")
    apple.forecast = forecast_company(apple, years = yr)
    adobe.forecast = forecast_company(adobe, years=yr)
    deal_ = structure_deal(apple, adobe, base_case)
    synergies_ = compute_synergies(adobe, years = yr, assumptions=base_case)
    proforma_ = build_proforma(apple, adobe, deal_, synergies_)
    acc_dil_ = accretion_dilution(apple, proforma_)
    print(f"  Year {yr} Accretion: {acc_dil_['Accretion/Dilution %'].iloc[-1]:.2f}%")
    synergy_npv_decomposition(apple, adobe, deal_, synergies_, base_case, years = yr)

# 7. Sensitivity
apple.forecast = forecast_company(apple, years = 5)
adobe.forecast = forecast_company(adobe, years = 5)
wacc_vs_terminal_growth(apple, base_case)
premium_vs_synergy(apple, adobe, base_case)

# 8. Credit Ratio Analysis
print("\n=====================================")
print("           Credit Ratio Analysis   ")
print("=====================================")
ratios = compute_credit_ratios(apple, adobe, deal, proforma)
for k,v in ratios.items():
    print(f"  {k:<30} {v:.2f}x")

# 9. Probability Metrics
print("\n=====================================")
print("       Probability Metrics           ")
print("=====================================")
probs = probability_metrics(mc_results, apple_wacc)
for k, v in probs.items():
    print(f"  {k:<25} {v:.1%}")
