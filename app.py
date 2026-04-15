import streamlit as st
import pandas as pd
import plotly.express as px

# Seite konfigurieren
st.set_page_config(page_title="EV Ladekurven Vergleich", layout="wide", page_icon="🚗")

# Styling: Titel und Einleitung
st.title("🚗 EV Ladekurven & Ladezeit Vergleich")
st.write("Vergleiche die reale Ladeperformance verschiedener Elektroautos basierend auf Testdaten. ACHTUNG: Daten sind Community-basiert ohne Garantie!")

# 1. Daten laden
@st.cache_data
def load_data():
    try:
        # Laden der CSV mit Semikolon-Trenner
        df = pd.read_csv("ladekurven.csv", sep=";")
        return df
    except Exception as e:
        st.error(f"Fehler beim Laden der ladekurven.csv: {e}")
        return None

df = load_data()

if df is not None:
    # 2. Fahrzeugauswahl
    modelle = sorted(df['Modell'].unique())
    auswahl = st.multiselect(
        "Fahrzeuge auswählen und vergleichen:", 
        modelle, 
        default=modelle[:2] if len(modelle) > 1 else modelle
    )

    st.markdown("---") 

    if auswahl:
        gefilterte_daten = df[df['Modell'].isin(auswahl)]

        # --- ABSCHNITT: Schnellanalyse 10-80% (Direkt unter der Auswahl) ---
        st.subheader("⏱️ Schnellanalyse: Der Goldstandard (10% auf 80%)")
        
        # Erstelle Spalten für die Metriken
        metric_cols = st.columns(len(auswahl))
        
        for i, fahrzeug in enumerate(auswahl):
            auto_data = gefilterte_daten[gefilterte_daten['Modell'] == fahrzeug]
            
            # Suche Werte für 10% und 80%
            row_10 = auto_data[auto_data['SoC'] == 10]
            row_80 = auto_data[auto_data['SoC'] == 80]
            
            if not row_10.empty and not row_80.empty:
                zeit_10 = row_10['Zeit_Minuten'].values[0]
                zeit_80 = row_80['Zeit_Minuten'].values[0]
                # Berechnung Durchschnittsleistung im Fenster 10-80
                leistung_avg = auto_data[(auto_data['SoC'] >= 10) & (auto_data['SoC'] <= 80)]['Leistung'].mean()
                
                dauer = zeit_80 - zeit_10
                metric_cols[i].metric(
                    label=fahrzeug, 
                    value=f"{int(round(dauer))} Min", 
                    delta=f"Ø {int(round(leistung_avg))} kW",
                    delta_color="normal"
                )
            else:
                metric_cols[i].info(f"ℹ️ {fahrzeug}: Daten für 10% oder 80% SoC fehlen in der CSV.")
        
        st.markdown("---")

        # --- ABSCHNITT: Diagramme ---
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Ladeleistung (kW)")
            fig_power = px.line(
                gefilterte_daten, 
                x="SoC", 
                y="Leistung", 
                color="Modell",
                markers=True,
                line_shape='spline',
                render_mode='svg',
                labels={"SoC": "Ladestand (%)", "Leistung": "Leistung (kW)"},
                template="plotly_white"
            )
            fig_power.update_layout(hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_power, use_container_width=True)

        with col2:
            st.subheader("Ladezeit ab 10% SoC (Minuten)")
            fig_time = px.line(
                gefilterte_daten, 
                x="Zeit_Minuten", 
                y="SoC", 
                color="Modell",
                markers=True,
                line_shape='spline',
                render_mode='svg',
                labels={"Zeit_Minuten": "Zeit (Minuten)", "SoC": "Ladestand (%)"},
                template="plotly_white"
            )
            fig_time.update_layout(hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_time, use_container_width=True)
            
        st.info("💡 **Tipp:** Klicke auf die Namen in der Legende, um einzelne Fahrzeuge auszublenden. Bewege die Maus über die Kurven für exakte Werte.")
    else:
        st.warning("☝️ Bitte wähle oben mindestens ein Fahrzeug aus, um den Vergleich zu starten.")

# "Mitmachen"-Bereich
st.info("📢 **Daten beisteuern?** Besuche das [GitHub Repository](https://github.com/xtec1774/ev-chargingcurves), um neue Ladekurven einzureichen!")
