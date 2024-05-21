import test_m as tm 
import pandas as pd
import streamlit as st
import plotly.express as px

# Funktion zur Konvertierung von Sekunden in mm:ss Format
def seconds_to_mmss(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

# Funktion zur Berechnung der x-Ticks (nur jede Minute)
def compute_xticks(seconds_range):
    ticks = []
    for seconds in seconds_range:
        if seconds % 60 == 0:
            ticks.append(seconds)
    return ticks

file_path = "C:\\Users\\elisa\\Desktop\\MCI\\MGST_SS_2324(2)\\Programmierübung II\\Programmieren3\\Programmieruebung_2_K_M_M\\data\\activities\\activity.csv"
    
# Leistungsdaten laden
df = pd.read_csv(file_path)

# Berechnet die Powercurve
powercurve = tm.calc_powercurve(df)

# Zeitfenster in mm:ss Format konvertieren
powercurve['Time_Window_mmss'] = powercurve['Time_Window'].apply(seconds_to_mmss)

st.subheader('Powercurve')
# Zeitreihenplot erstellen
fig = px.line(powercurve, x='Time_Window_mmss', y='Power', title='Auswertung PowerCurve', markers=True)

# Berechnung der x-Ticks (nur jede Minute)
max_seconds = powercurve['Time_Window'].max()
xticks_seconds = compute_xticks(range(max_seconds + 1))
xticks_mmss = [seconds_to_mmss(seconds) for seconds in xticks_seconds]

fig.update_xaxes(title_text='Dauer [mm:ss]', tickvals=xticks_seconds, ticktext=xticks_mmss)
fig.update_yaxes(title_text='Powercurve [W]')

st.plotly_chart(fig)
