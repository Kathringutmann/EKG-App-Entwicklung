import json
import pandas as pd
import plotly.express as px #Bibliothek für interaktive Plots
import scipy.signal as signal #Bibliothek für Signalverarbeitung

# %% Objekt-Welt

class EKGdata:

## Konstruktor der Klasse soll die Daten einlesen
    @staticmethod
    def load_by_id(person_data,id):
        """ Eine Funktion"""
        for person in person_data:
            for test in person["ekg_tests"]:
                if test["id"] == id:
                    return test
        return {}
        

    def __init__(self, ekg_dict):
        #Konstruktor der Klasse, der die Daten einliest
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms'])
        self.df['Zeit in ms'] = self.df['Zeit in ms'] - self.df['Zeit in ms'].min()

    #Methode für Peakfinder erstellen
    def find_peaks(self):
        x = self.df["Messwerte in mV"]
        self.peaks = signal.find_peaks(x, height=340)
        return self.peaks
    
    #neuen DataFrame erstellen, der auf den Zeitpunkten der Peaks basiert
    def get_peaks_df(self):
        return self.df.iloc[self.peaks[0]]

    #Methode für Plot erstellen
    def plot_time_series(self):
        # Erstellte einen Line Plot, mit der Zeit aus der x-Achse
        self.fig = px.line(self.df, x="Zeit in ms", y="Messwerte in mV",
                           range_x=[100,110],
                           range_y=[self.df["Messwerte in mV"].min(), self.df["Messwerte in mV"].max()])
        # show the peaks in the plot that are above the threshold
        self.fig.add_scatter(x=self.df["Zeit in ms"].iloc[self.peaks[0]], y=self.df["Messwerte in mV"].iloc[self.peaks[0]], mode='markers' ,marker=dict(color='red', size=8), name='Peaks')
        #achsenskalierung anpassen
        self.fig.update_yaxes(range=[self.df["Messwerte in mV"].min(), self.df["Messwerte in mV"].max()])
        self.fig.update_xaxes(range=[self.df["Zeit in ms"].min(), self.df["Zeit in ms"].max()])

        return self.fig 


    #Methode für die Herzfrequenz erstellen
    # errechne die Heart Rate aus dem neuen DataFrame mit den Peaks
    def estimate_hr_peaks(self):
        # Zeitdifferenz zwischen den Peaks in ms
        rr_intervall = self.get_peaks_df()["Zeit in ms"].diff()
        # Heart Rate steht im Verhältnis zur Zeitdifferenz mit dem Kehrwert HeartRate = 1/RR-Intervall
        self.hr = 1 / rr_intervall
        #überschrift für die Spalte erstellen
        return self.hr
    
    #Methode für den Plot der Herzfrequenz erstellen
    def make_plot_hr(self):
        peaks_df = self.get_peaks_df().iloc[1:] #ersten Wert entfernen, da er nicht relevant ist
        self.fig_hr = px.line(x=self.get_peaks_df()["Zeit in ms"], y=self.hr, title='Heart Rate Over Time', labels={'x': 'Time (ms)', 'y': 'Heart Rate (bpm)'})
        #return self.fig_hr

# Testen der Klasse
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
    
    #print("This is a module with some functions to read the EKG data")
    
    ekg_dict = person_data[0]["ekg_tests"][0]
    print(ekg_dict)
    ekg = EKGdata(ekg_dict)
    print(ekg.df.head())
    
    #Zeige Graf
    ekg.find_peaks()
    ekg.plot_time_series()
    ekg.fig.show()

    #Zeige Plot der Peaks
    ekg.get_peaks_df()
    ekg.estimate_hr_peaks()
    ekg.make_plot_hr()
    ekg.fig_hr.show()