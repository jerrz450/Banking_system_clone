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
import sys
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

    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()

    async def collect_and_validate_address(self, retries = 4):

        validators = {
            "Country" : self.validate_country1,
            "Huome Name": self.validate_name,
            "Home Number": self.validate_num,
            "Postal code" : self.postal_code,
            "City" : self.validate_city
        }

     
        address_info = {}

        for key, item in validators.items():
            count = 0 
            while count < retries:
                data = input(f"Enter {key}: ")
                data1 = item(data)
                if data1[0]:
                    if len(data1) >= 2:
                        address_info[key] = data1[1]
                    else:
                        address_info[key] = data1
                    break
                else:
                    count += 1
                    self.clear_screen()
                    print(data1[1])

            else:
                # This else block runs if the while loop completes without a break
                sys.exit("Too many retries, please try again later.")

        return address_info
                
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    async def validate_country1(country):
        result = GetCountryCode(country).run()

        if result[0]:
            return result
        else:
            return result
        
    @staticmethod
    def validate_num(num: str) -> bool:

        if re.fullmatch(r"^[a-zA-Z]{0,3}[0-9]{1,6}[a-zA-Z]{0,3}$", num) is not None:
            return [True, num]
        else:
            return [False, f"{num} is not correct, please try again!"]

    @staticmethod
    def validate_name(name: str) -> bool:

        if re.fullmatch(r"^[a-zA-Z\s.]+(?:[\s./-][a-zA-Z\s.]+)*$", name) is not None:
            return [True, name]
        else:
            return [False, f"{name} is not correct, please try again!"]
    
    @staticmethod 
    def postal_code(post_code : str):
        if post_code:
            return [True, post_code]
        else:
            return [False, f"{post_code} is not correct, please try again!"]
    
    @staticmethod
    def validate_city(city):
        if city:
            return [True, city]
        else:
            return [False, f"sdasdasdd"]
        
if __name__ == "__main__":
    asyncio.run(Address().collect_and_validate_address())
         
