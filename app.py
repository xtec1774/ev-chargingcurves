import streamlit as st
import pandas as pd
import plotly.express as px

# Seite konfigurieren
st.set_page_config(page_title="EV Ladekurven Vergleich", layout="wide", page_icon="🚗")

# Styling: Titel und Einleitung
st.title("🚗 EV Ladekurven & Ladezeit Vergleich")
st.write("Vergleiche die reale Ladeperformance verschiedener Elektroautos basierend auf Testdaten.")

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
    # 2. Fahrzeugauswahl direkt auf der Hauptseite
    modelle = sorted(df['Modell'].unique())
    auswahl = st.multiselect(
        "Fahrzeuge auswählen und vergleichen:", 
        modelle, 
        default=modelle[:2] if len(modelle) > 1 else modelle
    )

    st.markdown("---") # Trennlinie für bessere Optik

    if auswahl:
        gefilterte_daten = df[df['Modell'].isin(auswahl)]

        # Layout: Zwei Spalten für die Charts
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
            fig_power.update_layout(hovermode="x unified")
            st.plotly_chart(fig_power, use_container_width=True)

        with col2:
            st.subheader("Ladezeit (Minuten)")
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
            fig_time.update_layout(hovermode="x unified")
            st.plotly_chart(fig_time, use_container_width=True)
            
        st.info("💡 **Tipp:** Klicke auf die Namen in der Legende, um einzelne Fahrzeuge auszublenden. Bewege die Maus über die Kurven für exakte Werte.")
    else:
        st.warning("☝️ Bitte wähle oben mindestens ein Fahrzeug aus, um den Vergleich zu starten.")

# "Mitmachen"-Bereich
st.info("📢 **Daten beisteuern?** Besuche das [GitHub Repository](https://github.com/xtec1774/ev-chargingcurves), um neue Ladekurven einzureichen!")
