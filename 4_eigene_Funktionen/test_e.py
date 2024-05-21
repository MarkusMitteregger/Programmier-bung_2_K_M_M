from test_m import calc_powercurve, best_effort
import pandas as pd
import streamlit as st
import plotly.express as px

file_path = "C:\\Users\\elisa\\Desktop\\MCI\\MGST_SS_2324(2)\\Programmierübung II\\Programmieren3\\Programmieruebung_2_K_M_M\\data\\activities\\activity.csv"
    
# Leistungsdaten laden
df = pd.read_csv(file_path)

powercurve=calc_powercurve(df)
be1=best_effort(df,1)
be5=best_effort(df,5)
be30=best_effort(df,30)
be60=best_effort(df,60)
be300=best_effort(df,300)
be1200=best_effort(df,1200)



st.subheader('Powercurve')
# Zeitreihenplot erstellen
fig = px.line(powercurve, x='Time_Window', y='Power', title='Auswertung PowerCurve')

fig.update_xaxes(title_text='Dauer [mm:ss]')
fig.update_yaxes(title_text='Powercurve [W]')

st.plotly_chart(fig)





