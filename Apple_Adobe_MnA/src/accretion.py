import pandas as pd

def accretion_dilution(acquirer, proforma) -> pd.DataFrame:
    standalone_eps = acquirer.forecast["Net Income"]/acquirer.info["sharesOutstanding"]
    proforma_eps = proforma["EPS"]
    accretion_perc = (proforma_eps-standalone_eps)/standalone_eps * 100
    return pd.DataFrame({
        "Standalone EPS": standalone_eps,
        "Pro Forma EPS": proforma_eps,
        "Accretion/Dilution %": accretion_perc
    })
