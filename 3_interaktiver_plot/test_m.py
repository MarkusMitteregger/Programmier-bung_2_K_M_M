import pandas as pd
import numpy as np
import plotly.express as px


#Funktion zum einlesen der EKG-Daten
def ekg_read_txt():
    df = pd.read_csv("data/ekg_data/01_Ruhe.txt", sep = "\t")
    df.columns = ['Messwerte in mV', 'Zeit in ms']
    return df

#Funktion zum einlesen der Activity Daten
def activity_read_csv():
    df = pd.read_csv("data/activities/activity.csv", sep = ",")
    return df

#Zonen einteilung der Herzfrequenz
def heartrate_zones(df, maxhr):
    for index, observation in df.iterrows():
        hr = observation["HeartRate"]
        if hr < 0.6 * maxhr:
            df.at[index, "HeartrateZones"] = "Zone_1"
        elif hr < 0.7 * maxhr:
            df.at[index, "HeartrateZones"] = "Zone_2"
        elif hr < 0.8 * maxhr:
            df.at[index, "HeartrateZones"] = "Zone_3"
        elif hr < 0.9 * maxhr:
            df.at[index, "HeartrateZones"] = "Zone_4"
        else:
            df.at[index, "HeartrateZones"] = "Zone_5"
    return df
#Zoneneinteilung --> Durchschnittliche Leistung
def poweravg_zones(df):
    poweravg = df.groupby("HeartrateZones")["PowerOriginal"].mean().round().astype(int)
    return poweravg

#Zoneneinteilung --> Zeit
def time_zones(df):
    time_in_zones = df.groupby('HeartrateZones')['Duration'].sum().apply(lambda secunds: '{} min : {} s'.format(int(secunds) // 60, int(secunds) % 60))
    return time_in_zones




ekg_frame = ekg_read_txt()
activity_frame = activity_read_csv()

print(activity_frame.PowerOriginal.mean()) # --> keine eigene Funktion dafür nötig eig
print(max_power(activity_frame.PowerOriginal))
print(activity_frame.PowerOriginal.max())
#print(activity_frame.HeartRate)
activity_frame = heartrate_zones(activity_frame, 200)
print(time_zones(activity_frame))