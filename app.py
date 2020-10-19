from flask import Flask, request, render_template
import pandas as pd
from math import ceil
import pandas as pd
import numpy as np
import json       
import pathlib
import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

tabelleEigenverbrauch = json.loads(pathlib.Path( "./data/eigenverbrauch.json").read_text())
tabelleAutarkie = json.loads(pathlib.Path( "./data/autarkie.json").read_text())

#Hilfsfunktion zum Berechnen des Verhältnisses PV/Last
def SetRatioPV(last, pv):
    ratio_pv = (pv/last*1000)
    return ratio_pv
           
#Hilfsfunktion zum Berechnen des Verhältnisses Bat/Last
def SetRatioBat(last, bat):
    ratio_bat = (bat/last*1000)
    return ratio_bat
              
#Funktion zum Interpolieren aus Matrix
def SucheWertAusMatrix(table, x, y):
                       
    #x-Index suchen
    xi = ceil(x/0.0625)+1                                            
    #y-Index suchen
    yi = ceil(y/0.0625)+1                      
                       
    obenLinks = table[yi-1][xi-1]
    obenRechts = table[yi-1][xi]
    untenLinks = table[yi][xi-1]
    untenRechts = table[yi][xi]
                       
    xInterpoliertOben = obenLinks + (x-table[0][xi-1])*(obenRechts-obenLinks)/(table[0][xi]-table[0][xi-1])
    xInterpoliertUnten = untenLinks + (x-table[0][xi-1])*(untenRechts-untenLinks)/(table[0][xi]-table[0][xi-1])
    if(yi>1):
        interpoliert = xInterpoliertOben + (y-table[yi-1][0]) * (xInterpoliertUnten-xInterpoliertOben)/(table[yi][0]-table[yi-1][0])
        return interpoliert
                        
    return xInterpoliertUnten
           
#Funktion zum Ermitteln des Eigenverbrauchsanteils
def GetEigenverbrauch(ratio_pv, ratio_bat):
    eigen = SucheWertAusMatrix(tabelleEigenverbrauch, ratio_pv, ratio_bat)
    return eigen
           
#Funktion zum Ermitteln des Autarkiegrades
def GetAutarkie(ratio_pv, ratio_bat):
    autark = SucheWertAusMatrix(tabelleAutarkie, ratio_pv, ratio_bat)
    return autark
           
#Funktion zum Ermitteln des Direktsanteils vom Eigenverbrauch
def GetDirektverbrauchEigen(ratio_pv):
    dir_eigen = SucheWertAusMatrix(tabelleEigenverbrauch, ratio_pv, 0)
    return dir_eigen
           
#Funktion zum Ermitteln des Direktsanteils vom Autarkiegrad
def GetDirektverbrauchAutarkie(ratio_pv):
    dir_autarkie = SucheWertAusMatrix(tabelleAutarkie, ratio_pv, 0)
    return dir_autarkie

def calculation(strom, pv, bat, stromkosten, zins, laufzeit, eigenverbrauch, autarkie):
    invest_pv =  1190.00
    invest_bat =  1306.51
    invest_ac =  3585.00

    kosten_reststrom = (strom * (1.00-autarkie) * stromkosten) / 12.00
    einspeiseverguetung = strom * autarkie / eigenverbrauch * (1.00 - eigenverbrauch) * 0.0864 / 12.00

    kosten_pv = invest_pv * pv + invest_bat * bat + invest_ac
    finanzierung = (kosten_pv / (laufzeit*12.00)) + (kosten_pv * (zins/12.00))

    stromkosten_ohne = strom * stromkosten / 12
    stromkosten_mit = kosten_reststrom + finanzierung - einspeiseverguetung

    return stromkosten_ohne, stromkosten_mit, eigenverbrauch, autarkie, kosten_reststrom, einspeiseverguetung, kosten_pv, finanzierung

@app.route('/', methods=["GET", "POST"])
def pv_calculation():

    if request.method == "POST":
        strom = request.form["strom"].replace(",",".")
        pv = request.form["pv"].replace(",",".")
        bat = request.form["bat"].replace(",",".")
        stromkosten = request.form["stromkosten"].replace(",",".")
        zins = request.form["zins"].replace(",",".")
        laufzeit = request.form["laufzeit"].replace(",",".")

        strom = float(strom)
        pv = float(pv)
        bat = float(bat)
        stromkosten = float(stromkosten)
        zins = float(zins)/100
        laufzeit = float(laufzeit)

        #Berechnung Eigenverbrauch & Autarkie
        ratio_pv = SetRatioPV(strom, pv)
        ratio_bat = SetRatioBat(strom, bat)
        eigenverbrauch = GetEigenverbrauch(ratio_pv, ratio_bat)
        autarkie = GetAutarkie(ratio_pv, ratio_bat)

        stromkosten_ohne, stromkosten_mit, eigenverbrauch, autarkie, kosten_reststrom, einspeiseverguetung, kosten_pv, finanzierung = calculation(strom, pv, bat, stromkosten, zins, laufzeit, eigenverbrauch, autarkie)
        return render_template("result.html").format(stromkosten_o=stromkosten_ohne, stromkosten_m=stromkosten_mit)

    return render_template("index.html")

if __name__ == "__main__": 
        app.run() 