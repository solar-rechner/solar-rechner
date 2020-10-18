from flask import Flask, request, render_template
from calculation import calculation

app = Flask(__name__)
app.config["DEBUG"] = True

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

        stromkosten_ohne, stromkosten_mit, eigenverbrauch, autarkie, kosten_reststrom, einspeiseverguetung, kosten_pv, finanzierung = calculation(strom, pv, bat, stromkosten, zins, laufzeit)
        return render_template("result.html").format(stromkosten_o=stromkosten_ohne, stromkosten_m=stromkosten_mit)

    return render_template("index.html")

if __name__ == "__main__":
    app.run()