import json

class Person:
    
    @staticmethod
    def load_person_data():
        """A Function that knows where te person Database is and returns a Dictionary with the Persons"""
        file = open("data/person_db.json")
        person_data = json.load(file)
        return person_data

    @staticmethod
    def get_person_list(person_data):
        """A Function that takes the persons-dictionary and returns a list auf all person names"""
        list_of_names = []

        for eintrag in person_data:
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        return list_of_names
    
    @staticmethod
    def find_person_data_by_name(suchstring):
        """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
        und die die Person als Dictionary zurück gibt"""

        person_data = Person.load_person_data()
        #print(suchstring)
        if suchstring == "None":
            return {}

        two_names = suchstring.split(", ")
        vorname = two_names[1]
        nachname = two_names[0]

        for eintrag in person_data:
            print(eintrag)
            if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
                print()

                return eintrag
        else:
            return {}
    
    def get_test_ids(self):
        person_id = self.id
        person_data = Person.load_person_data()
    
        test_ids = []
        for person in person_data:
            if person['id'] == person_id:
                for test in person['ekg_tests']:
                    test_ids.append(test['id'])
    
        return test_ids

    
    def __init__(self, person_dict) -> None:
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]

    def get_age(self):
        return 2024 - int(self.date_of_birth)
    
    def calc_max_hr(self):
        return 220 - self.get_age()
    
    
if __name__ == "__main__":
    print("This is a module with some functions to read the person data")
    persons = Person.load_person_data()
    person_names = Person.get_person_list(persons)
    print(person_names)
    person_dict = Person.find_person_data_by_name("Huber, Julian")
    
    person1 = Person(person_dict)
    print(person1.firstname)
    
    #person1 = Person(person_dict)

# Call the function
    test_ids = Person.get_test_ids(person1)
    print(test_ids)
    