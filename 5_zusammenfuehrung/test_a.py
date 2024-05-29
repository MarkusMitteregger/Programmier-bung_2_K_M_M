import streamlit as st
from PIL import Image
from datetime import datetime
import json

class Person:

    def calculate_age(self):
        today = datetime.today().year
        age = int(today) - self.date_of_birth
        return age
    
    def calc_max_HR (self):
        """Berechnet die maximale Herzfrequenz einer Person."""
        max_hr = 220 - self.age
        return max_hr
    
    
    @staticmethod
    def load_person_data():
        """Eine Funktion, die weiß, wo sich die Personendatenbank befindet und ein Dictionary mit den Personen zurückgibt."""
        with open("data/person_db.json", 'r') as file:
            person_data = json.load(file)
        return person_data

    @staticmethod
    def get_person_list(person_data):
        """Eine Funktion, die das Personendaten-Dictionary nimmt und eine Liste aller Personennamen zurückgibt."""
        list_of_names = []

        for eintrag in person_data:
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        return list_of_names

    @staticmethod
    def find_person_data_by_name(suchstring):
        """Eine Funktion, der Nachname, Vorname als ein String übergeben wird und die die Person als Dictionary zurückgibt."""
        person_data = Person.load_person_data()
        
        if suchstring == "None":
            return {}

        two_names = suchstring.split(", ")
        vorname = two_names[1]
        nachname = two_names[0]

        for eintrag in person_data:
            if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
                return eintrag
        else:
            return {}

    def __init__(self, person_dict):
        self.date_of_birth = person_dict["date_of_birth"]
        self.age = self.calculate_age() 
        self.max_hr = self.calc_max_HR ()
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]
        self.ekg_tests = person_dict["ekg_tests"]

    @staticmethod
    def load_by_id(person_id):
        """Instanziiert eine Person anhand der ID und der Datenbank."""
        person_data = Person.load_person_data()
        for entry in person_data:
            if entry["id"] == person_id:
                return Person(entry)
            else: continue

    def __init__(self, person_dict):
            self.date_of_birth = person_dict["date_of_birth"]
            self.age = self.calculate_age() 
            self.max_hr = self.calc_max_HR ()
            self.firstname = person_dict["firstname"]
            self.lastname = person_dict["lastname"]
            self.picture_path = person_dict["picture_path"]
            self.id = person_dict["id"]
            self.ekg_tests = person_dict["ekg_tests"]

    


P_3 = Person.load_by_id(1)
print(P_3.__dict__)