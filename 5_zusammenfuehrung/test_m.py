import json
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import streamlit as st
import plotly.graph_objects as go

class EKGdata:

## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])
        self.peaks = self.find_peaks(self.df["Messwerte in mV"].copy(), 340)   
        self.heartrate = self.calc_heartrate()
        #self.max_heartrate = self.calc_max_heartrate()


    def make_plot(self):
        # Erstellte einen Line Plot, der ersten 10000 Werte mit der Zeit auf der x-Achse
        fig = px.line(self.df.head(10000), x="Zeit in ms", y="Messwerte in mV", title="EKG Plot")

        # Füge die Peaks hinzu
        peaks_x = self.df["Zeit in ms"][self.peaks[:20]]
        peaks_y = self.df["Messwerte in mV"][self.peaks[:20]]
        fig.add_trace(go.Scatter(x=peaks_x, y=peaks_y, mode='markers+text', name='Peaks', text=["R"]*len(peaks_x),
                                 textposition="top center", marker=dict(color='red', size=10)))

        # Zeige das Plot in Streamlit an
        st.plotly_chart(fig)

    @staticmethod   # Decorator um die Methode als static zu kennzeichnen
    def load_by_id(id):
        file = open("data/person_db.json")
        person_data = json.load(file)
        for person in person_data:
            for ekg_test in person["ekg_tests"]:
                if ekg_test["id"] == id:
                    return EKGdata(ekg_test)
                else: continue

    def find_peaks(self, series, threshold, respacing_factor=5):
        """
        A function to find the peaks in a series
        Args:
            - series (pd.Series): The series to find the peaks in
            - threshold (float): The threshold for the peaks
            - respacing_factor (int): The factor to respace the series
        Returns:
            - peaks (list): A list of the indices of the peaks
        """
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
    
    def calc_heartrate(self):
        timehr = np.array(self.df["Zeit in ms"][self.peaks])
        t_puls = (timehr[1:] - timehr[:-1])
        t_puls = np.delete(t_puls, np.where(t_puls < 0))
        heartr = (1 / np.mean(t_puls[10:-10]))*60*1000    
        return heartr

    def calc_max_heartrate(self):
        timehr = np.array(self.df["Zeit in ms"][self.peaks])
        t_puls = (timehr[1:] - timehr[:-1])
        t_puls = np.delete(t_puls, np.where(t_puls < 0))
        max_heartrate = (1 / np.min(t_puls[10:-10]))*60*1000
        return max_heartrate
                

ekg_1 = EKGdata.load_by_id(2)
ekg_1.make_plot()
print(ekg_1.heartrate)





