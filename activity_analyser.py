import pandas as pd
import csv
import matplotlib as plt
import plotly.express as px

# Laden der Daten aus der activity.csv in einem DataFrame
df = pd.read_csv(r'C:\Programmierübungen_II\EKG-App-Entwicklung\data\activity.csv')

print(df.columns)


# Ermitteln des Mittelwerts der Leistung
average_performance = df['PowerOriginal'].mean()
print("Mittelwert der Leistung:", average_performance)

# Ermitteln des Maximalwerts der Leistung
max_performance = df['PowerOriginal'].max()
print("Maximalwert der Leistung:", max_performance)

# Erstellen eines interaktiven Plots, der die Leistung und die Herzfrequenz über die Zeit anzeigt
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
plt.plot(df['Duration'], df['PowerOriginal'], label='Leistung')
plt.plot(df['Duration'], df['HeartRate'], label='Herzfrequenz')
plt.xlabel('Zeit')
plt.ylabel('Wert')
plt.title('Leistung und Herzfrequenz über die Zeit')
plt.legend()
plt.show()
