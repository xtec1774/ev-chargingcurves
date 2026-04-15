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
