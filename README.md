-venv Ordner erstellen: main.py -> rechts unten auf Zahlen -> in Suchleiste den Venv Ordner anklicken

-venv aktivieren, um in ide Umgebung verschiedene Sachen installieren -> Komandozeile erscheint grünes Venv und dann kann man mit pip install ... das gewünschte installieren

-read_data.py : json datei->Funktion, die datei einließt-> dictionary mit der Person erstellt-> Funktion: nur den Firstname extrahiert-> Einer leeren Liste werden die Namen übergeben -> Funktion die die namen anzeigt

-öffnen der Webseite: Im Terminal: streamlit run main.py 

mit #%% kann man auch einzelne zellen ausführen lassen 

öffnen der csv # Laden der Daten aus der activity.csv in einem DataFrame
df = pd.read_csv(r'C:\Programmierübungen_II\EKG-App-Entwicklung\data\activity.csv')


## Verwendung der App für Interaktiven Plot
- oben kann die maximale Herzfrequenz angepasst werden.
- dadurch werden die Zeitwerte in den verschiedenen Zonen angepasst.
- auch die durchschnittliche Leistung wird in den Herzfrequenzzonen von der maximalen Herzfrequenz abhängig angegeben.


-> im activity_analyser wird der dataframe geladen und die mittleren Messwerte berechnet. Außerdem wird auch der ausgegebene  Plot erstellt

-> in der 'main.py' = aufgabe2.py wird der interaktive Plot erstellt und auch die Zonenen der Herzfrequenzen werden erstellt. Es werden noch die weiteren Layoutanpassungen gemacht und die Daten der CSV Datei eingeladen.

## Strat der App:
streamlit run aufgabe2.py