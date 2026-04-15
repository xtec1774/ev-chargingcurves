import streamlit as st
import pandas as pd
import plotly.express as px

# Seite konfigurieren
st.set_page_config(page_title="EV Ladekurven Vergleich", layout="wide")

st.title("🚗 EV Ladekurven & Ladezeit Vergleich")
st.write("Wähle verschiedene Fahrzeuge aus, um ihre Leistung und Ladezeit zu vergleichen.")

# 1. Daten laden
@st.cache_data
def load_data():
    # Wir laden die Datei, die du gerade erstellt hast
df = pd.read_csv("ladekurven.csv", sep=";")
    return df

try:
    df = load_data()

    # 2. Fahrzeugauswahl
    modelle = df['Modell'].unique()
    auswahl = st.multiselect("Fahrzeuge hinzufügen:", modelle, default=modelle[0] if len(modelle) > 0 else None)

    if auswahl:
        gefilterte_daten = df[df['Modell'].isin(auswahl)]

        # Spalten für die zwei Charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Ladeleistung (kW)")
            fig_power = px.line(
                gefilterte_daten, 
                x="SoC", 
                y="Leistung", 
                color="Modell",
                markers=True,
                labels={"SoC": "Ladestand (%)", "Leistung": "Leistung (kW)"}
            )
            st.plotly_chart(fig_power, use_container_width=True)

        with col2:
            st.subheader("Ladezeit (Minuten)")
            fig_time = px.line(
                gefilterte_daten, 
                x="Zeit_Minuten", 
                y="SoC", 
                color="Modell",
                markers=True,
                labels={"Zeit_Minuten": "Zeit (Minuten)", "SoC": "Ladestand (%)"}
            )
            st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.info("Bitte wähle mindestens ein Fahrzeug aus der Liste aus.")

except FileNotFoundError:
    st.error("Datei 'ladekurven.csv' nicht gefunden. Bitte stelle sicher, dass sie im gleichen Ordner liegt.")
