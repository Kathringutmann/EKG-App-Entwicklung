
import pandas as pd
import matplotlib.pyplot as plt

# CSV-Datei laden
def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df

# Zeit und Leistung normalisieren
def normalize_data(df, power_column='PowerOriginal'):
    # Überprüfen, ob die Spalten vorhanden sind
    if power_column not in df.columns:
        raise ValueError("Die angegebene Spalte für Leistung ist nicht im DataFrame vorhanden.")
    
    # Zeit in Sekunden als Index verwenden
    df['TimeInSeconds'] = df.index

    # Nur relevante Spalten behalten
    normalized_df = df[['TimeInSeconds', power_column]].dropna()
    normalized_df.columns = ['TimeInSeconds', 'PowerInWatts']
    
    return normalized_df

# Power-Curve Diagramm erstellen
def plot_power_curve(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['TimeInSeconds'], df['PowerInWatts'], marker='o', linestyle='-')
    ax.set_title('Leistungsverlauf')
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Power (Watts)')
    ax.grid(True)
    return fig