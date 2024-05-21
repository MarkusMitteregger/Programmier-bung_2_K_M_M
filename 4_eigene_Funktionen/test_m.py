import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def find_peaks(ekg_data):
    print("noch nicht gemacht")



#Funktion zum einlesen der EKG-Daten
def ekg_read_txt():
    df = pd.read_csv("data/ekg_data/01_Ruhe.txt", sep = "\t")
    df.columns = ['Messwerte in mV', 'Zeit in ms']
    return df

#Funktion zum einlesen der Activity Daten
def activity_read_csv():
    df = pd.read_csv("data/activities/activity.csv", sep = ",")
    return df


#berechnet die Powercurve
def calc_powercurve(df):
    df_clean = df.dropna(subset = "PowerOriginal")
    array_best_effort = []
    array_time_window = []
    for window in range(1200):
        value = best_effort(df_clean, window)
        array_best_effort.append(value)
        array_time_window.append(window)
    powercurve_df = pd.DataFrame({"Power" : array_best_effort, "Time_Window" : array_time_window})
    return powercurve_df
        
def best_effort(df, window):
    value = df["PowerOriginal"].rolling(window).mean()
    return value.max()


ekg_df = ekg_read_txt()
activity_df = activity_read_csv()
#print(ekg_df)

#plt.plot(ekg_df["Zeit in ms"][:1000], ekg_df["Messwerte in mV"][:1000])
#plt.show()

power_curve = calc_powercurve(activity_df)
plt.plot(power_curve["Time_Window"], power_curve["Power"])
plt.show()

#best_effort(activity_df, 5)