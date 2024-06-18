from dataclasses import dataclass, field
import random
import re
import os
import time
from itertools import chain
from validate import validate_name, CountriesDataApi
from api_s import ZipCodeData
from country_api import GetData
import asyncio
from get_country_code import GetCountryCode

@dataclass
class User:
    first_name: str
    last_name: str
    address: str
    phone_num: str
    email: str
    username: str
    password: str

@dataclass
class NameandID:
    full_name: dict
    id: int = field(default_factory=lambda: NameandID.generate_id(), init=False)
    name: str = field(init=False)
    surname: str = field(init=False)
   
    def __post_init__(self):
        self.name = ' '.join(self.full_name["Name"])
        self.surname = ' '.join(self.full_name["Surname"])
        full_name1 = f"{self.name} {self.surname}"

        if not validate_name(full_name1):
            raise ValueError(f"Invalid name: {full_name1}")

    @staticmethod
    def generate_id() -> int:
        return random.randint(1000000, 9999999)

class FullName:
    def __init__(self) -> None:
        self.name_input = None

    def prompt_user_full_name(self) -> bool:
        attempts = 0
        while attempts < 5:
            try:
                self.name_input = {
                    "Name": input('Name: ').strip().split(),
                    "Surname": input('Surname: ').strip().split()
                }
                NameandID(full_name=self.name_input)
                return True
            except ValueError:
                attempts += 1
                self._clear_screen()
                print("Invalid input. Please enter a valid name and surname.")
                time.sleep(2)
        self._clear_screen()
        print("Too many invalid attempts. Please try again later.")
        return False

    @staticmethod
    def _clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

class Address:
     
    def collect_and_validate_input(self) -> dict:
        validators = {
            "Country" : self.validate_country,
            "Home Name": self.validate_name,
            "Home Number": self.validate_num,
            "Postal code" : self.postal_code,
            "City" : self.validate_city
        }

        address_info = {}
        for field, validator in validators.items():
            while True:
                user_input = input(f"{field}: ").strip()
                if validator(user_input):
                    address_info[field] = validator[0]
                    break
                else:
                    self._clear_screen()
                    print("Invalid input, please try again.")
                    time.sleep(1)
        return address_info

    @staticmethod
    def validate_num(num: str) -> bool:
        return (num, re.fullmatch(r"^[a-zA-Z]{0,3}[0-9]{1,6}[a-zA-Z]{0,3}$", num) is not None)

    @staticmethod
    def validate_name(name: str) -> bool:
        return (name, re.fullmatch(r"^[a-zA-Z\s.]+(?:[\s./-][a-zA-Z\s.]+)*$", name) is not None)
    
    @staticmethod
    def validate_country(country : str):
        result = GetCountryCode(country).run()
        return (result)
    
    @staticmethod 
    def postal_code(post_code : str):
        return (post_code)
    
    @staticmethod
    def validate_city(city):
        return (city)
    
    @staticmethod
    def _clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    result = Address().collect_and_validate_input()
    print(result)