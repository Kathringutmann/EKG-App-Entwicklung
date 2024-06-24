import json

class Person:
    
    @staticmethod # Statische Methode, die unabhängig von einer Instanz der Klasse aufgerufen werden kann
    def load_person_data():
        """" Eine Funktion, die die Personendaten aus einer JSON-Datei lädt und als Dictionary zurückgibt"""
        file = open("data/person_db.json")
        person_data = json.load(file)
        return person_data

    @staticmethod
    def get_person_list(person_data):
        """Eine Funktion, die das Personen-Dictionary übergeben bekommt und eine Liste aller Personennamen zurückgibt"""
        list_of_names = [] # Liste für die Namen der Personen

        for eintrag in person_data: # Für jeden Eintrag im Personen-Dictionary
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"]) # Füge den Namen zur Liste hinzu
        return list_of_names # Gebe die Liste zurück
    
    @staticmethod
    def find_person_data_by_name(suchstring): #suchstring = "Huber, Julian"
        """ Eine Funktion der Nachname, Vorname als ein String übergeben wird und die die Person als Dictionary zurück gibt"""
        person_data = Person.load_person_data()
        #print(suchstring)
        if suchstring == "None": # Wenn kein Name übergeben wird, gebe ein leeres Dictionary zurück
            return {}

        two_names = suchstring.split(", ") # Trenne den String in Nachname und Vorname
        vorname = two_names[1] # Vorname ist das zweite Element
        nachname = two_names[0] # Nachname ist das erste Element

        for eintrag in person_data: # Für jeden Eintrag im Personen-Dictionary
            print(eintrag)
            if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname): # Wenn der Nachname und Vorname übereinstimmen
                print()

                return eintrag # Gebe den Eintrag zurück
        else:
            return {} # Wenn kein Eintrag gefunden wurde, gebe ein leeres Dictionary zurück
    
    def get_test_ids(self):
        """Eine Funktion, die die Test-IDs einer Person zurückgibt."""
        person_id = self.id
        person_data = Person.load_person_data() # Personendaten laden
    
        test_ids = [] # Liste für die Test-IDs
        for person in person_data: # Für jede Person im Personen-Dictionary
            if person['id'] == person_id: # Wenn die ID der Person übereinstimmt
                for test in person['ekg_tests']: # Für jeden Test der Person
                    test_ids.append(test['id']) # Füge die Test-ID zur Liste hinzu
    
        return test_ids # Gebe die Liste der Test-IDs zurück

    
    def __init__(self, person_dict) -> None:
        """Initialisiert ein Person-Objekt mit den Daten aus dem übergebenen Dictionary."""
        self.date_of_birth = person_dict["date_of_birth"] # Geburtsdatum
        self.firstname = person_dict["firstname"] # Vorname
        self.lastname = person_dict["lastname"] # Nachname
        self.picture_path = person_dict["picture_path"] # Bildpfad
        self.id = person_dict["id"] # ID

    def get_age(self):
        """Eine Funktion, die das Alter einer Person berechnet und zurückgibt."""
        return 2024 - int(self.date_of_birth) #dieses Jahr - Geburtsjahr
    
    def calc_max_hr(self):
        """Eine Funktion, die die maximale Herzfrequenz einer Person berechnet und zurückgibt."""
        return 220 - self.get_age() #220 - Alter (220 wegen der Formel zur Berechnung der maximalen Herzfrequenz)
    
    
if __name__ == "__main__":
    print("This is a module with some functions to read the person data") #Dieser Code wird nur ausgeführt, wenn das Modul direkt ausgeführt wird
    persons = Person.load_person_data() #Personendaten laden
    person_names = Person.get_person_list(persons) #Namen der Personen in Liste speichern
    print(person_names) #Namen der Personen ausgeben
    person_dict = Person.find_person_data_by_name("Huber, Julian") #Personendaten für die ausgewählte Person laden
    person1 = Person(person_dict) #Person-Objekt erstellen
    print(person1.firstname) #Vorname der Person ausgeben
    #person1 = Person(person_dict)
    test_ids = Person.get_test_ids(person1) #Test-IDs für die ausgewählte Person speichern
    print(test_ids) #Test-IDs ausgeben
    