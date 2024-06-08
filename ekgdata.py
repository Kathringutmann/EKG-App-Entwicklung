import json
import pandas as pd
import plotly.express as px
import scipy.signal as signal

class EKGdata:
    @staticmethod
    def load_by_id(person_data, id):
        for person in person_data:
            for test in person["ekg_tests"]:
                if test["id"] == id:
                    return test
        return {}

    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms'])
        self.df['Zeit in ms'] = self.df['Zeit in ms'] - self.df['Zeit in ms'].min()

    def find_peaks(self):
        x = self.df["Messwerte in mV"]
        self.peaks = signal.find_peaks(x, height=340)
        return self.peaks

    def make_plot(self):
        self.fig = px.line(self.df, x="Zeit in ms", y="Messwerte in mV")
        self.fig.add_scatter(x=self.df["Zeit in ms"].iloc[self.peaks[0]], y=self.df["Messwerte in mV"].iloc[self.peaks[0]], mode='markers', marker=dict(color='red', size=8))

    def update_axis(self, x_min, x_max):
        self.fig.update_layout(
            xaxis=dict(range=[x_min, x_max])
        )

if __name__ == "__main__":
    file = open("data/person_db.json")
    person_data = json.load(file)
    test_dict = EKGdata.load_by_id(person_data, 3)
    ekg = EKGdata(test_dict)

    ekg.find_peaks()
    ekg.make_plot()
    ekg.update_axis(0, 5000)
    ekg.fig.show()
