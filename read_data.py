import json

def get_person_data():
    """opens the data base and returns a dictionary of the persondata"""
    #Opening Json File
    file = open("data/person_db.json")

    #Loading the Json File in a dictionary
    person_data = json.load(file)
    return person_data

def get_name(person_data):
    """returns a list of names of the people in the database"""
    names = []
    for person_dict in person_data:
       names.append(person_dict["lastname"] + ", " + person_dict["firstname"])
    return names


#Suchen vom Bild der gesuchten Person

def find_person_data_by_name(name):
    
# Teilt einen String in und speichert die Ergebnisse in einer Liste
    two_names = name.split(", ")
    vorname = two_names[1]
    nachname = two_names[0]

    person_data = get_person_data()
 
    for eintrag in person_data:
     if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
        return eintrag
    
    # Anlegen des Session State. Bild, wenn es kein Bild gibt
    if 'picture_path' not in st.session_state:
        st.session_state.picture_path = 'data/pictures/none.jpg'

    # ...

    # Suche den Pfad zum Bild, aber nur wenn der Name bekannt ist
    if st.session_state.current_user in person_names:
        st.session_state.picture_path = read_data.find_person_data_by_name(st.session_state.current_user)["picture_path"]

    # ...

    # Öffne das Bild und Zeige es an
    image = Image.open("../" + st.session_state.picture_path)
    st.image(image, caption=st.session_state.current_user)
    
    
#Test 
if __name__ == "__main__":
    
    person_data = get_person_data()
    names = get_name(person_data)
    
    print(names)
    print(find_person_data_by_name("Heyer, Yannic")["picture_path"])
    