import json
import pandas as pd
import plotly.express as px
import scipy.signal as signal

# %% Objekt-Welt

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

# Methode für find_peaks erstellen



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
        #pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms'])
        
        self.df['Zeit in ms'] = self.df['Zeit in ms']-self.df['Zeit in ms'].min()
        #self.df = self.df.head(10000)


    def find_peaks(self):
        x = self.df["Messwerte in mV"]
        #thresold auf größeren Wert setzen, um nur Peaks zu finden, die höher als 360 mV sind
        self.peaks = signal.find_peaks(x, height=340)
        return self.peaks

    def make_plot(self):
        print(self.df.tail())
        # Erstellte einen Line Plot, mit der Zeit aus der x-Achse
        self.fig = px.line(self.df, x="Zeit in ms", y="Messwerte in mV")

        # show the peaks in the plot that are above the threshold
        self.fig.add_scatter(x=self.df["Zeit in ms"].iloc[self.peaks[0]], y=self.df["Messwerte in mV"].iloc[self.peaks[0]], mode='markers', marker=dict(color='blue', size=8))
       # Erstellte einen Line Plot, mit der Zeit aus der x-Achse
        #self.fig = px.line(self.df, x="Zeit in ms", y="Messwerte in mV")

    def update_axis(self,x_min,y_max):        
        # Set the x-axis range to 2.5 seconds
            self.fig.update_layout(
        xaxis=dict(range=[x_min, y_max])
    )

    
    # show the peaks in the plot that are above the threshold
        #self.fig.add_scatter(x=self.df["Zeit in ms"].iloc[self.peaks[0]], y=self.df["Messwerte in mV"].iloc[self.peaks[0]], mode='markers', marker=dict(color='blue', size=8))


if __name__ == "__main__":
    file = open("data/person_db.json")
    person_data = json.load(file)
    test_dict = EKGdata.load_by_id(person_data,3)
    ekg = EKGdata(test_dict)
    
    #print(ekg.df["Zeit in ms"].value_counts())
    #print(ekg.id)
    

      # Find the peaks
    ekg.find_peaks()
    
    # Create the plot
    ekg.make_plot()
    ekg.update_axis(0,5000)
    # Display the plot
    ekg.fig.show()
    
    