# 🚗 EV Ladekurven Vergleich

Ein interaktives Tool zum Vergleich der Ladeperformance verschiedener Elektrofahrzeuge (EVs). Mit dieser App lassen sich Ladekurven (Leistung über SoC) und Ladezeiten (SoC über Zeit) direkt gegenüberstellen.

## 🌟 Features
- **Leistungs-Vergleich:** Vergleiche die Ladeleistung (kW) basierend auf dem Ladestand (SoC %).
- **Zeit-Analyse:** Visualisiere, wie lange ein Fahrzeug lädt, um einen bestimmten SoC zu erreichen.
- **Interaktivität:** Wähle mehrere Fahrzeuge aus der Datenbank aus, um die Linien direkt übereinander zu legen.
- **Einfache Datenpflege:** Neue Fahrzeuge können unkompliziert über eine CSV-Datei hinzugefügt werden.

## 🚀 Live Demo
Die App ist live unter folgender URL erreichbar:
https://ev-chargingcurves-comparison.streamlit.app/

## 🛠️ Installation & Daten
Die App basiert auf **Python** und **Streamlit**.

### Datenstruktur
Die Daten werden in der Datei `ladekurven.csv` gepflegt. Die Struktur sieht wie folgt aus:
- `Modell`: Name des Fahrzeugs (und Batterievariante).
- `SoC`: Ladestand in Prozent (0-100).
- `Leistung`: Ladeleistung in kW.
- `Zeit_Minuten`: Verstrichene Zeit seit Ladestart.

### Lokal ausführen
Falls du die App lokal testen möchtest:
1. Repository klonen.
2. Abhängigkeiten installieren: `pip install -r requirements.txt`.
3. Starten mit: `streamlit run app.py`.

## 📈 Datenquellen
Die Ladekurven basieren zu Beginn auf öffentlich zugänglichen Testdaten (z.B. P3 Charging Index, Fastned, Herstellerangaben). 
*Hinweis: Die Werte dienen dem Vergleich und können je nach Außentemperatur und Säulentyp variieren.*

## ✍️ Mitmachen: Neue Fahrzeugdaten hinzufügen

Du hast Ladedaten für ein neues Elektroauto oder eine andere Batterievariante? Du kannst helfen, die Datenbank zu erweitern!

### So kannst du Daten beisteuern:
1. **Per Pull Request (für GitHub-Nutzer):**
   - Öffne die Datei `ladekurven.csv`.
   - Füge deine Daten am Ende hinzu (bitte das Semikolon `;` als Trenner nutzen).
   - Erstelle einen Pull Request.
2. **Per Issue:**
   - Erstelle ein neues [Issue](https://github.com/xtec1774/ev-chargingcurves/issues) und poste dort die Werte für Modell, SoC, Leistung und Zeit. Ich pflege sie dann ein.

### Das benötigte Format:
Damit die Kurven korrekt angezeigt werden, benötigen wir idealerweise Werte in 5% oder 10% Schritten.
Beispiel:
`Modell;SoC;Leistung;Zeit_Minuten`
`Mein Auto;10;150;0`
`Mein Auto;20;140;4`
...
