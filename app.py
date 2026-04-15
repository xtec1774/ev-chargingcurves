import streamlit as st
import pandas as pd
import plotly.express as px

# Seite konfigurieren (Breites Layout und Titel im Browser-Tab)
st.set_page_config(page_title="EV Ladekurven Vergleich", layout="wide", page_icon="🚗")

# Styling: Titel und Einleitung
st.title("🚗 EV Ladekurven & Ladezeit Vergleich")
st.write("Vergleiche die reale Ladeperformance verschiedener Elektroautos basierend auf Testdaten.")

# 1. Daten laden (mit automatischer Semikolon-Erkennung)
@st.cache_data
def load_data():
    try:
        # Wir nutzen sep=";", da deine Excel/CSV-Datei Semikolons verwendet
        df = pd.read_csv("ladekurven.csv", sep=";")
        return df
    except Exception as e:
        st.error(f"Fehler beim Laden der ladekurven.csv: {e}")
        return None

df = load_data()

if df is not None:
    # 2. Fahrzeugauswahl in der Seitenleiste (Sidebar)
    st.sidebar.header("Einstellungen")
    modelle = sorted(df['Modell'].unique())
    auswahl = st.sidebar.multiselect(
        "Fahrzeuge auswählen:", 
        modelle, 
        default=modelle[:2] if len(modelle) > 1 else modelle
    )

    if auswahl:
        gefilterte_daten = df[df['Modell'].isin(auswahl)]

        # Layout: Zwei Spalten für die Charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Ladeleistung")
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
            st.subheader("Ladezeit")
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
            
        st.info("💡 **Tipp:** Du kannst in der Legende auf ein Modell klicken, um es auszublenden, oder mit der Maus über die Linien fahren für Details.")
    else:
        st.warning("👈 Bitte wähle mindestens ein Fahrzeug in der Seitenleiste aus.")

st.sidebar.markdown("---")
st.sidebar.info("📢 **Daten beisteuern?**\nBesuche das [GitHub Repository](https://github.com/xtec1774/ev-chargingcurves), um neue Ladekurven einzureichen!")
