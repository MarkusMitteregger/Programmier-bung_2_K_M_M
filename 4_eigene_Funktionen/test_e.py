import test_m as tm 
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Funktion zur Konvertierung von Sekunden in mm:ss Format
def seconds_to_mmss(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

# Datei-Pfad
file_path = ("data/activities/activity.csv")	
# Leistungsdaten laden
df = pd.read_csv(file_path)

# Berechnet die Powercurve
powercurve = tm.calc_powercurve(df)

# Zeitfenster in mm:ss Format konvertieren
powercurve['Time_Window_mmss'] = powercurve['Time_Window'].apply(seconds_to_mmss)

# Definieren der gewünschten Zeitpunkte in Sekunden
desired_times = [1, 30, 60, 100, 300, 600, 1200]

# Zeitpunkte in mm:ss Format konvertieren
xticks_mmss = [seconds_to_mmss(t) for t in desired_times]

# Filter powercurve für Marker-Daten
marker_data = powercurve[powercurve['Time_Window'].isin(desired_times)]

st.subheader('Powercurve')

# Zeitreihenplot erstellen
fig = px.line(powercurve, x='Time_Window_mmss', y='Power', title='Evaluation PowerCurve')

# Hinzufügen von Markern zu den spezifischen Zeitpunkten
fig.add_trace(go.Scatter(
    x=marker_data['Time_Window_mmss'],
    y=marker_data['Power'],
    mode='markers',
    marker=dict(color='red', size=8),
    name='Specific values'
))

# Setze die x-Achse auf die gewünschten Zeitpunkte
fig.update_xaxes(title_text='Duration [mm:ss]', tickvals=xticks_mmss)
fig.update_yaxes(title_text='Powercurve [W]')

# Aktualisiere die Layout-Einstellungen für die x-Achse
fig.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=xticks_mmss,
        #ticktext=xticks_mmss,
        tickangle=-45  # Winkel der x-Achsen-Beschriftungen, um Überlappung zu vermeiden
    )
)

st.plotly_chart(fig)
