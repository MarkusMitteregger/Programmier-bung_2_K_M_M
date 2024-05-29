import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

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
    df['HeartRateZone'] = df['HeartRate'].apply(lambda x: get_heart_rate_zone(x, max_hr))
    time_in_zones = df.groupby('HeartRateZone')['Duration'].sum()
    time_in_zones = time_in_zones.apply(lambda x: '{:02}:{:02}'.format(int(x) // 60, int(x) % 60))
    return time_in_zones

# Funktion zur Analyse der Leistung
def analyze_performance(df):
    avg_performance_in_zones = df.groupby('HeartRateZone')['PowerOriginal'].mean()
    avg_performance_in_zones = avg_performance_in_zones.round().astype(int)
    return avg_performance_in_zones

# Streamlit App
def main():
    st.title('Herzfrequenzanalyse')
    dateipfad = ("data/activities/activity.csv")

    df = pd.read_csv(dateipfad)
    max_hr = st.sidebar.number_input("Bitte geben Sie die maximale Herzfrequenz ein:", value=0, step=1)
    analyze_button = st.sidebar.button("Analyse durchführen")

    if analyze_button:
        time_in_zones = analyze_heart_rate(df, max_hr)
        avg_performance_in_zones = analyze_performance(df)
        avg_performance_generel = df['PowerOriginal'].mean().round().astype(int)
        max_performance_generel = df['PowerOriginal'].max().round().astype(int)

        st.subheader('Zeit in HF-Zonen (in mm˸ss):')
        st.write(time_in_zones)
        st.subheader('Durchschnittliche Leistung in den Herzfrequenzzonen (in Watt):')
        st.write(avg_performance_in_zones)
        st.subheader('Durchschnittliche Leistung gesamt (in Watt):')
        st.write(avg_performance_generel)
        st.subheader('Maximale Leistung (in Watt):')
        st.write(max_performance_generel)

        time = df.index / 60

        fig = go.Figure()

        # Herzfrequenz und Leistung über die Zeit plotten
        fig.add_trace(go.Scatter(x=time, y=df['HeartRate'], mode='lines', name='Heart Rate'))
        fig.add_trace(go.Scatter(x=time, y=df['PowerOriginal'], mode='lines', name='Power'))

        # Herzfrequenzzonen als Bereiche hinzufügen
        fig.add_hrect(y0=0, y1=0.6*max_hr, fillcolor="lightblue", opacity=0.2, line_width=0)
        fig.add_hrect(y0=0.6*max_hr, y1=0.7*max_hr, fillcolor="lightgreen", opacity=0.2, line_width=0)
        fig.add_hrect(y0=0.7*max_hr, y1=0.8*max_hr, fillcolor="yellow", opacity=0.2, line_width=0)
        fig.add_hrect(y0=0.8*max_hr, y1=0.9*max_hr, fillcolor="orange", opacity=0.2, line_width=0)
        fig.add_hrect(y0=0.9*max_hr, y1=1.0*max_hr, fillcolor="red", opacity=0.2, line_width=0)

        fig.update_layout(
            title="Leistung und Herzfrequenz über die Zeit",
            xaxis_title='Dauer [min]',
            yaxis_title='Herzfrequenz [bpm], Leistung [W]'
        )

        st.plotly_chart(fig)

    mood = st.slider("Wie war dein Befinden?", 0, 10, 5)
    st.write("Ich habe mich während der Aktivität", mood, "gefühlt. 0 = schlecht, 10 = super")

if __name__ == "__main__":
    main()
