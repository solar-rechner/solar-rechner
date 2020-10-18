import pandas as pd

def calculation(strom, pv, bat, stromkosten, zins, laufzeit):
    invest_pv =  1190.00
    invest_bat =  1306.51
    invest_ac =  3585.00

    df = pd.read_csv("data/pv_data.csv", sep=';')

    eigenverbrauch = df["Eigenverbrauch (%)"][(df["Stromverbrauch"] == strom) & (df["PV-Leistung"] == pv) & (df["Batterie"] == bat)].values[0]
    autarkie = df["Autarkie"][(df["Stromverbrauch"] == strom) & (df["PV-Leistung"] == pv) & (df["Batterie"] == bat)].values[0]

    kosten_reststrom = (strom * (1.00-autarkie) * stromkosten) / 12.00
    einspeiseverguetung = strom * autarkie / eigenverbrauch * (1.00 - eigenverbrauch) * 0.0864 / 12.00

    kosten_pv = invest_pv * pv + invest_bat * bat + invest_ac
    finanzierung = (kosten_pv / (laufzeit*12.00)) + (kosten_pv * (zins/12.00))

    stromkosten_ohne = strom * stromkosten / 12
    stromkosten_mit = kosten_reststrom + finanzierung - einspeiseverguetung

    return stromkosten_ohne, stromkosten_mit, eigenverbrauch, autarkie, kosten_reststrom, einspeiseverguetung, kosten_pv, finanzierung