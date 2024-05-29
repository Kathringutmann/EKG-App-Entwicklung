##%
import pandas as pd
import matplotlib.pyplot as plt

# CSV-Datei laden
def load_csv(file_path):
    df = pd.read_csv(file_path)
    df["Duration"] = df.index
    return df

# Diagramm erstellen
def plot_data(df):
    # Beispiel: Plot der Duration gegen Distance
    plt.figure(figsize=(10, 6))
    plt.plot(df['Duration'], df['PowerOriginal'], marker='o', linestyle='-')
    
    # Diagramm beschriften
    plt.title('Duration vs PowerOriginal')
    plt.xlabel('Duration')
    plt.ylabel('PowerOriginal')
    
    # Diagramm anzeigen
    plt.grid(True)
    plt.show()
    
def compute_powercurve (df):
    powerlist = []
    timelist =[]
    
    for powerlevel in range(int(df["PowerOriginal"].min()),int(df["PowerOriginal"].max()),10):
        powerlist.append(powerlevel)
        timelist.append(find_duration_powerlevel(df, powerlevel))
    
    df =pd.DataFrame({"Leistung" : powerlist,
                      "Zeit" : timelist})
    
    return df
    
    
def find_duration_powerlevel(df, powerlevel):
    max_duration = 0
    current_duration = 0
    List_durations = []
    exceeding = False
    
    for index, row in df.iterrows():
        current_power = row["PowerOriginal"]
        
        if current_power > powerlevel:
            exceeding = True
            current_duration += 1  # Eine Sekunde zur Dauer hinzufügen
            
        else:
            if exceeding:
                List_durations.append(current_duration)
                current_duration = 0
                exceeding = False
    
    max_duration = max(List_durations)

    return max_duration

def plot_data(power_curve_df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(power_curve_df['Zeit'], power_curve_df['Leistung'], marker='o', linestyle='-')
    ax.set_title('Power Curve')
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Power (Watts)')
    ax.grid(True)
    return fig
    
    
def main():
    # Pfad zur CSV-Datei angeben
    file_path = r"C:\Programmierübungen_II\EKG-App-Entwicklung\activity.csv"
    
    # Daten laden
    df = load_csv(file_path)
    
    # Daten plotten
    #plot_data(df)
    #print(find_duration_powerlevel (df, 250))
    
    power_curve_df = compute_powercurve(df)
    print(power_curve_df)
    fig = plot_data(power_curve_df)
    fig.show()
    

if __name__ == '__main__':
    main()

