import pandas as pd
import streamlit as st
import plotly.express as px

# Funktion zur Zoneneinteilung basierend auf der Herzfrequenz und der maximalen Herzfrequenz
def get_heart_rate_zone(heart_rate, max_hr):
    if heart_rate < 0.6 * max_hr:
        return 'Zone1'
    elif heart_rate < 0.7 * max_hr:
        return 'Zone2'
    elif heart_rate < 0.8 * max_hr:
        return 'Zone3'
    elif heart_rate < 0.9 * max_hr:
        return 'Zone4'
    else:
        return 'Zone5'

# Funktion zur Analyse der Herzfrequenz
def analyze_heart_rate(df, max_hr):
    # Herzfrequenz-Zone für jede Zeile berechnen
    df['HeartRateZone'] = df['HeartRate'].apply(lambda x: get_heart_rate_zone(x, max_hr))

    # Zeit in den Herzfrequenzzonen berechnen
    time_in_zones = df.groupby('HeartRateZone')['Duration'].sum()

    # Dauer in mm:ss formatieren
    time_in_zones = time_in_zones.apply(lambda x: '{:02}:{:02}'.format(int(x) // 60, int(x) % 60))

    return time_in_zones

# Funktion zur Analyse der Leistung
def analyze_performance(df):
    # Durchschnittliche Leistung in den Herzfrequenzzonen berechnen
    avg_performance_in_zones = df.groupby('HeartRateZone')['PowerOriginal'].mean()

    # Runden und in ganze Zahlen umwandeln
    avg_performance_in_zones = avg_performance_in_zones.round().astype(int)

    return avg_performance_in_zones


# Streamlit App
def main():
    st.title('Herzfrequenzanalyse')

    # Laden der Daten
    dateipfad = (
        "C:\\Users\\elisa\\Desktop\\MCI\\MGST_SS_2324(2)\\"
        "Programmierübung II\\pandas\\3_pandas\\EGK_App\\data\\activities\\activity.csv"
    )
    df = pd.read_csv(dateipfad)

    # Maximale Herzfrequenz eingeben
    max_hr = st.sidebar.number_input("Bitte geben Sie die maximale Herzfrequenz ein:", value=0, step=1)

    # Analyse durchführen, wenn der Button gedrückt wird
    analyze_button = st.sidebar.button("Analyse durchführen")

    if analyze_button:
        # Analyse der Herzfrequenz durchführen
        time_in_zones = analyze_heart_rate(df, max_hr)

        # Analyse der Leistung durchführen
        avg_performance_in_zones = analyze_performance(df)

        avg_performance_generel = df['PowerOriginal'].mean().round().astype(int)
        max_performance_generel = df['PowerOriginal'].max().round().astype(int)

    


        # Ergebnisse anzeigen
        st.subheader('Zeit in HF-Zonen (in mm˸ss):')
        st.write(time_in_zones)
        st.subheader('Durchschnittliche Leistung in den Herzfrequenzzonen (in Watt):')
        st.write(avg_performance_in_zones)
        st.subheader('Durchschnittliche Leistung gesamt (in Watt):')
        st.write(avg_performance_generel)
        st.subheader('Maximale Leistung (in Watt):')
        st.write(max_performance_generel)


    time = df.index/60

    

    # Zeitreihenplot erstellen
    fig = px.line(df, x=time, y=['PowerOriginal', 'HeartRate'], title="Leistung und HF über die Zeit", labels={"Duration": "Zeit [min]", "PowerOriginal": "Leistung [W]"})

    fig.update_xaxes(title_text='Dauer [min]')
    fig.update_yaxes(title_text='Herzfrequenz [bpm], Leistung [W]')
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
