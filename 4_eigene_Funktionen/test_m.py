import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def find_peaks(series, threshold, respacing_factor=5):
    """ A function to find the peaks in a series
Args:
    - series (pd.Series): The series to find the peaks in
    - threshold (float): The threshold for the peaks
    - respacing_factor (int): The factor to respace the series
Returns:
    - peaks (list): A list of the indices of the peaks"""
# Respace the series
    series = series.iloc[::respacing_factor]

# Filter the series
    series = series[series>threshold]


    peaks = []
    last = 0
    current = 0
    next = 0

    for index, row in series.items():
        last = current
        current = next
        next = row

        if last < current and current > next and current > threshold:
            peaks.append(index-respacing_factor)

    return peaks


#Funktion zum einlesen der EKG-Daten
def ekg_read_txt():
    df = pd.read_csv("data/ekg_data/01_Ruhe.txt", sep = "\t")
    df.columns = ['Messwerte in mV', 'Zeit in ms']
    return df

#Funktion zum einlesen der Activity Daten
def activity_read_csv():
    df = pd.read_csv("C:\\Users\\elisa\\Desktop\\MCI\\MGST_SS_2324(2)\\Programmierübung II\\Programmieren3\\Programmieruebung_2_K_M_M\\data\\activities\\activity.csv", sep = ",")
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


#ekg_df = ekg_read_txt()
activity_df = activity_read_csv()
#print(ekg_df)

#plt.plot(ekg_df["Zeit in ms"][:1000], ekg_df["Messwerte in mV"][:1000])
#plt.show()

power_curve = calc_powercurve(activity_df)
#plt.plot(power_curve["Time_Window"], power_curve["Power"])
#plt.show()

#best_effort(activity_df, 5)