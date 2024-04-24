User
import json

def load_person_data():
    """A Function that knows where the person database is and returns a dictionary with the persons"""
    file = open("../data/person_db.json")
    person_data = json.load(file)
    return person_data

def get_person_list(person_data):
    """A Function that takes the persons-dictionary and returns a list auf all person names"""
    list_of_names = []

    for eintrag in person_data:
        list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
    return list_of_names


def find_person_data_by_name(suchstring):
    """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
    und die die Person als Dictionary zurück gibt"""

    person_data = load_person_data()
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


if __name__ == "__main__":
    # Opening JSON file
    file = open("../data/person_db.json")

    # Loading the JSON File in a dictionary
    person_data = json.load(file)

    person_data

    suchstring  = "Huber, Julian"

    # Teilt einen String in und speichert die Ergebnisse in einer Liste
    two_names = suchstring.split(", ")
    vorname = two_names[1]
    nachname = two_names[0]

    person_data = load_person_data()

    # Nun können wir vergleichen bis wir einen Treffer finden
    for eintrag in person_data:
        if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
            print(eintrag)
            
    suchstring  = "Huber, Julian"

    # Teilt einen String in und speichert die Ergebnisse in einer Liste
    two_names = suchstring.split(", ")
    vorname = two_names[1]
    nachname = two_names[0]

    person_data = load_person_data()

    # Nun können wir vergleichen bis wir einen Treffer finden
    for eintrag in person_data:
        if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
            print(eintrag)