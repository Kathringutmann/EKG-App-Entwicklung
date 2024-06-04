import json
import pandas as pd
import plotly.express as px
import scipy.signal as signal

# %% Objekt-Welt

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

# Methode für find_peaks erstellen



class EKGdata:

## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        #pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])

    def find_peaks(self):
        x = self.df["Messwerte in mV"]
        #thresold auf größeren Wert setzen, um nur Peaks zu finden, die höher als 360 mV sind
        self.peaks = signal.find_peaks(x, height=340)
        return self.peaks

    def make_plot(self):

        # Erstellte einen Line Plot, mit der Zeit aus der x-Achse
        self.fig = px.line(self.df, x="Zeit in ms", y="Messwerte in mV")

        # show the peaks in the plot that are above the threshold
        self.fig.add_scatter(x=self.df["Zeit in ms"].iloc[self.peaks[0]], y=self.df["Messwerte in mV"].iloc[self.peaks[0]], mode='markers', marker=dict(color='blue', size=8))
        #return self.fig 


if __name__ == "__main__":
    print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    print(ekg_dict)
    ekg = EKGdata(ekg_dict)
    print(ekg.df.head())

    ekg.find_peaks()
    print(ekg.peaks)
    ekg.make_plot()
    ekg.fig.show()