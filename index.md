<!DOCTYPE html>
<html lang="de" dir="ltr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Solarstrom Rechner</title>
        <link rel='stylesheet' type="text/css" href="{{ url_for('static', filename='css/index.css') }}">
        <link href='https://fonts.googleapis.com/css?family=Titillium Web' rel='stylesheet'>
    </head>

    <body>
        <div>
            <h2>Angaben zur Photovoltaikanlage</h2>
        </div>

        <form method="post" action=".">
            <div class="container">
                <div class="child">
                    <p class="eingabe">1) Jährlicher Stromverbrauch:</p>
                    <p class="beschreibung">Gebe einen Verbrauch zwischen 2000 und 10000 kWh ein.<br>Verwende 100 kWh Schritte.</p>
                    <input name="strom" id="field" placeholder="3000"/>
                </div>

                <div class="child">
                    <p class="eingabe">2) Installierte Leistung Photovoltaikanlage:</p>
                    <p class="beschreibung">Gebe eine installierte Leistung zwischen 1,0 und 19,9 kWp ein.<br>Verwende 0,1 kWp Schritte.</p>
                    <input name="pv" id="field" placeholder="7,1"/>
                </div>

                <div class="child">
                    <p class="eingabe">3) Kapazität Batteriespeicher:</p>
                    <p class="beschreibung">Gebe eine verfügbare Kapazität zwischen 0,0 und 19,5 kWh ein.<br>Verwende 0,5 kWh Schritte.</p>
                    <input name="bat"  id="field" placeholder="6,5"/>
                </div>

                <div class="child">
                    <p class="eingabe">4) Stromkosten:</p>
                    <p class="beschreibung">Gebe die monatlichen Stromkosten pro kWh in € an<br>Für 0,33 €/kWh verwende 0,33</p>
                    <input name="stromkosten"  id="field" placeholder="0,33"/>
                </div>

                <div class="child">
                    <p class="eingabe">5) Zinsen:</p>
                    <p class="beschreibung">Gebe die jährlichen Zinsen der Finanzierung an. KFW-Konditionen können <a href="https://www.kfw.de/inlandsfoerderung/Unternehmen/Energie-Umwelt/Förderprodukte/Erneuerbare-Energien-Standard-(270)/">hier</a> nachgelesen werden.<br>Für einen Zins von 1.03% verwende 1,03</p>
                    <input name="zins"  id="field" placeholder="1,03"/>
                </div>

                <div class="child">
                    <p class="eingabe">6) Laufzeit:</p>
                    <p class="beschreibung">Gebe die Laufzeit der Finanzierung in Jahren an. KFW-Konditionen können <a href="https://www.kfw.de/inlandsfoerderung/Unternehmen/Energie-Umwelt/Förderprodukte/Erneuerbare-Energien-Standard-(270)/">hier</a> nachgelesen werden.<br>Für eine Laufzeit von 10 Jahren verwende 10</p>
                    <input name="laufzeit"  id="field" placeholder="10"/>
                </div>
            </div>
            <p><input type="submit" class="button" value="Berechnen" /></p>
        </form>
    </body>
</html>