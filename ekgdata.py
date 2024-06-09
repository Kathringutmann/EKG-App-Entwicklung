import json
import pandas as pd
import plotly.express as px
import scipy.signal as signal
import streamlit as st
import plotly.graph_objects as go


# %% Objekt-Welt

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

# Methode für find_peaks erstellen

class EKGdata:

## Konstruktor der Klasse soll die Daten einlesen

    @staticmethod
    def load_by_id(person_data,id):
        """ Eine Funktion"""
        
        for person in person_data:
            #print(person)
            for test in person["ekg_tests"]:
                #print(test)
                if test["id"] == id:
                    #print(id)
                    return test

        return {}


    def __init__(self, ekg_dict):
        #übergibt die Daten aus dem Dictionary in die Klasse
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])
        self.peaks = self.find_peaks()
        self.peaks_plot = self.get_peaks_df()  
        self.hr = self.estimate_hr_peaks()
        self.fig = None
        self.fig_hr = None
        self.heartrate_time = pd.DataFrame({"Time in s": self.peaks_plot["Zeit in ms"]/1000, "Heartrate": self.hr})
        

    def find_peaks(self):
        x = self.df["Messwerte in mV"]
        #thresold auf größeren Wert setzen, um nur Peaks zu finden, die höher als 340 mV sind
        self.peaks = signal.find_peaks(x, height=340)
        return self.peaks
    
    #neuen DataFrame erstellen, der auf den Zeitpunkten der Peaks basiert
    def get_peaks_df(self):
        return self.df.iloc[self.peaks[0]]

    def make_plot(self):

        # Erstellte einen Line Plot, mit der Zeit aus der x-Achse
        self.fig = px.line(self.df, x="Zeit in ms", y="Messwerte in mV")
        self.fig_hr = px.line(self.heartrate_time, x="Time in s", y="Heartrate", title="Herzfrequenz über die Zeit")

        # show the peaks in the plot that are above the threshold
        self.fig.add_scatter(x=self.df["Zeit in ms"].iloc[self.peaks[0]], y=self.df["Messwerte in mV"].iloc[self.peaks[0]], mode='markers', marker=dict(color='blue', size=8))
        #return self.fig 

    # errechne die Heart Rate aus dem neuen DataFrame mit den Peaks
    def estimate_hr_peaks(self):
        # Zeitdifferenz zwischen den Peaks in ms
        rr_intervall = self.get_peaks_df()["Zeit in ms"].diff()
        # Heart Rate steht im Verhältnis zur Zeitdifferenz mit dem Kehrwert HeartRate = 1/RR-Intervall
        self.hr = 1 / rr_intervall
        return self.hr
    
    # Binde den Plot in Streamlit ein
    def show_plot(self):
        st.plotly_chart(self.fig)
        st.plotly_chart(self.fig_hr)

if __name__ == "__main__":
    file = open("data/person_db.json")
    person_data = json.load(file)
    test_dict = EKGdata.load_by_id(person_data,2)
    ekg = EKGdata(test_dict)
    print(ekg.id)
    print(ekg.date)
    print(ekg.data)
    print(ekg.peaks)
    print(ekg.peaks_plot)
    print(ekg.hr)
    print(ekg.heartrate_time)

    ekg_dict = person_data[0]["ekg_tests"][0]
    print(ekg_dict)
    ekg = EKGdata(ekg_dict)
    print(ekg.df.head())
    
    #Zeige Graf der Peaks
    ekg.find_peaks()
    ekg.make_plot()
    ekg.fig.show()

    #Zeige Plot zwischen Herzfrequenz und Zeit
    ekg.get_peaks_df()
    ekg.estimate_hr_peaks()
    ekg.make_plot()
    ekg.fig_hr.show()

