import json
import streamlit as st

def get_person_data():
    """Öffnet die Datenbank und gibt ein Dictionary der Personendaten zurück."""
    
    file = open("data/person_db.json") #Öffnen der Json Datei
    person_data = json.load(file) #Laden der Daten aus der Json Datei
    return person_data #Rückgabe der Daten als Dictionary


def get_name(person_data):
    """Eine Funktion, die das Personen-Dictionary übergeben bekommt und eine Liste aller Personennamen zurückgibt."""
    names = [] #Liste für die Namen der Personen
    for person_dict in person_data: #Für jeden Eintrag im Personen-Dictionary
       names.append(person_dict["lastname"] + ", " + person_dict["firstname"]) #Füge den Namen zur Liste hinzu
    return names #Gebe die Liste zurück


def find_person_data_by_name(name):
    """Eine Funktion der Nachname, Vorname als ein String übergeben wird und die die Person als Dictionary zurück gibt"""
    two_names = name.split(", ") #Trenne den String in Nachname und Vorname
    vorname = two_names[1] #Vorname ist das zweite Element
    nachname = two_names[0] #Nachname ist das erste Element

    person_data = get_person_data() #Personendaten laden
 
    for eintrag in person_data: #Für jeden Eintrag im Personen-Dictionary
     if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname): #Wenn der Nachname und Vorname übereinstimmen
        return eintrag #Gebe den Eintrag zurück
    

#Test 
if __name__ == "__main__":
    person_data = get_person_data() #Personendaten laden
    names = get_name(person_data) #Namen der Personen in Liste speichern
    print(names) #Namen der Personen ausgeben
    print(find_person_data_by_name("Heyer, Yannic")["picture_path"]) #Bildpfad der Person ausgeben
    