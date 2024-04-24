import json

# Opening JSON file
file = open("../data/person_db.json")

# Loading the JSON File in a dictionary
person_data = json.load(file)

person_data

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

