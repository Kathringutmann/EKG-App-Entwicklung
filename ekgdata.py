import json
import pandas as pd
import plotly.express as px #Bibliothek für interaktive Plots
import scipy.signal as signal #Bibliothek für Signalverarbeitung
from dtw import dtw
import numpy as np
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
        # add a peak column to the dataframe
        self.df["Peak"] = False
        print(self.peaks[0])
        self.df.loc[self.peaks[0], "Peak"] = True
        
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

    def update_axis(self,range_start, range_end):
        self.fig.update_xaxes(range=[range_start, range_end])


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

    def herzschlag_abweichungen(self,schlag1 : int, schlag2 : int):
        
        df_schlag1 = self.df[self.df["Schlag"]==1]
        
        return 1.1 #float
    
    def herzschlag_bestimmen(self): #fügt df durchnummerierten Herzschläge hinzu
        self.df["Schlag"] = 0
       


        # Initialisiere eine neue Spalte 'Peak Group' mit NaN
        self.df['Peak Group'] = pd.NA

        # Zähler für die Peak-Gruppen
        counter = 0

        # Durch die Zeilen des DataFrame iterieren und die Peak-Gruppen zuweisen
        for i, row in self.df.iterrows():
            if row['Peak']:
                counter += 1
            self.df.at[i, 'Peak Group'] = counter

        print(self.df)

        
    def plot_herzschlag(self, nummer): 
        
        # Filtern des DataFrames für den gewünschten Herzschlag
        df_filtered = self.df[self.df['Peak Group'] == nummer]

        # Plotten des Herzschlags mit Plotly
        fig = px.line(df_filtered, x='Zeit in ms', y='Messwerte in mV', title=f'Herzschlag Nummer {nummer}', markers=True)
        fig.update_layout(xaxis_title='Zeit in ms', yaxis_title='Messwerte in mV', template='plotly_white')
        fig.show()
        
        return fig
        
    def herzschlag_durchschnitt(self, resample_length=100):
         # Extrahiere alle Herzschläge in eine Liste
        herzschlaege = []
        for group in self.df['Peak Group'].unique():
            df_group = self.df[self.df['Peak Group'] == group]
            herzschlaege.append(df_group['Messwerte in mV'].values)
        
        # Verwende den ersten Herzschlag als Referenz
        referenz = herzschlaege[0]
        
        # Warpe alle Herzschläge zur Referenz und berechne den Durchschnitt
        aligned_herzschlaege = []
        
        for herzschlag in herzschlaege:
            alignment = dtw(herzschlag, referenz, keep_internals=True)
            aligned_herzschlag = [herzschlag[idx] for idx in alignment.index1]
            aligned_herzschlaege.append(aligned_herzschlag)
        
        # Berechne den Durchschnitt über alle gewarpten Herzschläge hinweg
        resampled_herzschlaege = []
        for herzschlag in aligned_herzschlaege:
            resampled_herzschlag = np.interp(np.linspace(0, len(herzschlag) - 1, resample_length), np.arange(len(herzschlag)), herzschlag)
            resampled_herzschlaege.append(resampled_herzschlag)
        
        # Berechne den Durchschnitt über alle resampled Herzschläge hinweg
        avg_herzschlag = np.mean(resampled_herzschlaege, axis=0)
        
        # Erstellen eines DataFrames für den durchschnittlichen Herzschlag
        self.avg_df = pd.DataFrame({
            'Zeit in ms': np.linspace(self.df['Zeit in ms'].min(), self.df['Zeit in ms'].max(), len(avg_herzschlag)),
            'Durchschnitt Herzschlag': avg_herzschlag
        })
        
        return self.avg_df
    
    def plot_durchschnitt_herzschlag(self):
        #avg_df = self.berechne_durchschnitt_herzschlag()
        
        # Plotten des durchschnittlichen Herzschlags mit Plotly
        fig = px.line(self.avg_df, x='Zeit in ms', y='Durchschnitt Herzschlag', title='Durchschnittlicher Herzschlag')
        fig.update_layout(xaxis_title='Zeit in ms', yaxis_title='Messwerte in mV', template='plotly_white')
        fig.show()

        #df = None
        #return df
    
    def herzschlag_vergleich (self): # die 5 größen abweichungen der herzschläge werden angezeigt und und geplotted .ind 
        list = [] # für jeden einzelnen herzschlag alle datenpunkte vergleichen ---mit dtw  und dann resampel, damit alle die selbe länge haben.-- dann in der formel mean square error MSE in arrays..2 mit gleicher länge Formel:(array 1 - array2)**2) =MSE
        return list
    
# Testen der Klasse
if __name__ == "__main__":
    file = open("data/person_db.json")
    person_data = json.load(file)
    test_dict = EKGdata.load_by_id(person_data,2) 
    ekg = EKGdata(test_dict)
    ekg.find_peaks()
    ekg.herzschlag_bestimmen()
    print(ekg.df)
    #ekg.plot_herzschlag(2) #in appp noch anzeigen, und eingabefeld für testnummer hinzufügen
    avg_hs = ekg.herzschlag_durchschnitt()
    print(avg_hs)
    ekg.plot_durchschnitt_herzschlag()
    