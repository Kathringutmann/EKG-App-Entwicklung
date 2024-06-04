import json
import pandas as pd
import plotly.express as px

# %% Objekt-Welt

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

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
        #pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])


    def make_plot(self):

        # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
        self.fig = px.line(self.df.head(2000), x="Zeit in ms", y="Messwerte in mV")
        #return self.fig 


if __name__ == "__main__":
    file = open("data/person_db.json")
    person_data = json.load(file)
    test_dict = EKGdata.load_by_id(person_data,2)
    ekg = EKGdata(test_dict)
    print(ekg.id)
    
    #print("This is a module with some functions to read the EKG data")

    #ekg_dict = person_data[0]["ekg_tests"][0]
    #print(ekg_dict)
    #ekg = EKGdata(ekg_dict)
    #print(ekg.df.head())