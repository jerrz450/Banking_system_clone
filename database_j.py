import json
import os
from validate import validate_name
import random
from reusable_menu import MainMenu
import numpy as np

class Database:
    
    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def append_to_json_file(self, user_info):

        try:
            if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
                with open(self.file_path, 'r+') as file:
                    data = json.load(file)
                    if isinstance(data, list): 
                        data.append(user_info)
                        file.seek(0)
                        file.truncate()
                        json.dump(data, file, indent=4)
                    else:
                        raise ValueError("File content is not a list")
            else:
                with open(self.file_path, 'w') as file:
                    json.dump([user_info], file, indent=4)
            print("Data appended successfully.")
        except (IOError, ValueError) as e:
            print(f"Error handling file: {e}")

    def search_database(self):
        self.name  = input("Name: ").strip().lower()
        self.surname  = input("Surname: ").strip().lower()
        self.city = input("City: ").strip().lower()
                
        with open(self.file_path, "r") as read:
            users_db = json.load(read)
            id_dict = {search["ID"]: search for search in users_db if search["Name"] == self.name and search["Surname"] == self.surname and search["City"] == self.city}
            if not id_dict:
                if not validate_name(input_data= [self.name, self.surname, self.city]):
                    print("This might've been the problem.")
                else:
                    print("No user found")
            else:
                
                print(id_dict)


