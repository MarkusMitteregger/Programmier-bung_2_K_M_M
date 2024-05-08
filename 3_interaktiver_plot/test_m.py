import pandas as pd
import numpy as np
import plotly.express as px



def ekg_read_csv():

    df = pd.read_csv("data/ekg_data/01_Ruhe.txt", sep = "\t")
    df.columns = ['Messwerte in mV', 'Zeit in ms']
    return df

def activity_read_csv():
    df = pd.read_csv("data/activities/activity.csv", sep = ",")
    return df


def mean_power(df):
    mean_power = df.mean()
    return mean_power

def max_power(df):
    max_power = df.max()
    return max_power



ekg_frame = ekg_read_csv()
#print(ekg_frame)
activity_frame = activity_read_csv()
print(activity_frame.PowerOriginal)
print(activity_frame.PowerOriginal.mean()) # --> keine eigene Funktion dafür nötig eig
print(max_power(activity_frame.PowerOriginal))
