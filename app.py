import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Seite konfigurieren
st.set_page_config(page_title="EV Ladekurven Vergleich", layout="wide", page_icon="🚗")

# Styling: Titel und Einleitung
st.title("🚗 EV Ladekurven & Ladezeit Vergleich")
st.write("Vergleiche Ladeperformance und reale Reichweitengewinne basierend auf Autobahn-Verbräuchen (ca. 120 km/h).")

# 1. Daten laden
@st.cache_data
def load_data():
    try:
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

        # --- ABSCHNITT: Schnellanalyse & Reichweite ---
        st.subheader("⚡ 15 Min. Reichweite & Goldstandard (10-80%)")
        
        metric_cols = st.columns(len(auswahl))
        
        for i, fahrzeug in enumerate(auswahl):
            auto_data = gefilterte_daten[gefilterte_daten['Modell'] == fahrzeug].sort_values("SoC")
            
            # Überprüfung ob alle notwendigen Spalten für dieses Modell befüllt sind (verhindert den ValueError)
            has_data = all(col in auto_data.columns for col in ['Kapazitaet_kWh', 'Verbrauch_kWh_100km'])
            
            zeit_10 = None
            row_10 = auto_data[auto_data['SoC'] == 10]
            if not row_10.empty:
                zeit_10 = row_10['Zeit_Minuten'].values[0]

            if zeit_10 is not None and has_data:
                try:
                    # Reichweite nach 15 Min
                    zeit_ziel = zeit_10 + 15
                    soc_nach_15 = np.interp(zeit_ziel, auto_data['Zeit_Minuten'], auto_data['SoC'])
                    soc_diff = soc_nach_15 - 10
                    
                    kap = auto_data['Kapazitaet_kWh'].iloc[0]
                    verb = auto_data['Verbrauch_kWh_100km'].iloc[0]
                    
                    # Nur rechnen, wenn Werte gültige Zahlen sind
                    if pd.notnull(kap) and pd.notnull(verb) and verb > 0:
                        geladene_kwh = (soc_diff / 100) * kap
                        nachgeladene_km = (geladene_kwh / verb) * 100
                        avg_pwr = auto_data[(auto_data['SoC'] >= 10) & (auto_data['SoC'] <= 80)]['Leistung'].mean()
                        
                        with metric_cols[i]:
                            st.metric(
                                label=fahrzeug, 
                                value=f"+ {int(round(nachgeladene_km))} km", 
                                delta=f"Ø {int(round(avg_pwr))} kW (10-80%)",
                                delta_color="normal"
                            )
                            
                            row_80 = auto_data[auto_data['SoC'] == 80]
                            if not row_80.empty:
                                dauer_80 = row_80['Zeit_Minuten'].values[0] - zeit_10
                                st.write(f"⏱️ 10-80%: **{int(round(dauer_80))} Min.**")
                                st.write(f"🔋 Akku: **{kap} kWh**")
                    else:
                        metric_cols[i].info(f"Daten unvollständig für {fahrzeug}")
                except:
                    metric_cols[i].error("Berechnungsfehler")
            else:
                metric_cols[i].warning(f"10% SoC Daten fehlen.")

        st.markdown("---")

        # --- DIAGRAMME ---
        col1, col2 = st.columns(2)

        chart_layout = dict(
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
            margin=dict(l=0, r=0, t=30, b=80),
            template="plotly_white"
        )

        with col1:
            st.subheader("Ladeleistung (kW)")
            fig_p = px.line(gefilterte_daten, x="SoC", y="Leistung", color="Modell", markers=True, line_shape='spline')
            fig_p.update_layout(chart_layout)
            st.plotly_chart(fig_p, use_container_width=True)

        with col2:
            st.subheader("Ladezeit (Minuten)")
            fig_t = px.line(gefilterte_daten, x="Zeit_Minuten", y="SoC", color="Modell", markers=True, line_shape='spline')
            fig_t.update_layout(chart_layout)
            st.plotly_chart(fig_t, use_container_width=True)
            
        st.info("💡 **Tipp:** Klicke auf die Namen in der Legende, um einzelne Fahrzeuge auszublenden.")
    else:
        st.warning("☝️ Bitte Fahrzeuge auswählen.")

# "Mitmachen"-Bereich
st.info("📢 **Daten beisteuern?** Besuche das [GitHub Repository](https://github.com/xtec1774/ev-chargingcurves)!")
