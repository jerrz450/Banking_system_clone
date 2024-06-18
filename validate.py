import json
import urllib.parse
import requests
import pandas as pd
import time
import os
from api_s import FindAMatch

"""VALIDATE NAME"""

def validate_name(input_data):
    if isinstance(input_data, list):
        final_name = " ".join(input_data)
    elif isinstance(input_data, str):
        final_name = " ".join(input_data.split())
    else:
        print("Input must be a string or a list.")
        return False

    flagged = {"values": []}

    for char in final_name:
        for i in char:
            if not i.isalpha() and not i.isspace():  
                flagged["values"].append(i)

    if not flagged["values"]:
        print("Name validation passed.")
        return True
    else:
        flagged_chars = flagged["values"]
        name1 = final_name
        name2 = "".join("^" if char in flagged_chars and not char.isspace() else " " for char in name1)
        combined_output = name1 + '\n' + name2
        print(combined_output)
        return False

"""GET COUNTRIE INFO API"""

class GetCountry:

    def __init__(self) -> None:
        #Initializing the class
        self.file_path = file_path = "C:\\Users\\Jernej\\Documents\\OOP\\database_files\\alpha_codes.csv" #Path of the csv file where the data is stored

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0: #Here we check if the file exists and if its empty or not
            self.choice = "r+"  #If file exists and has size more than 0, than we assign the "r+" (read) mode for the context manager mode.
        else:
            self.choice = "w+" #"""If it file path doesnt exists or is empty, than we prepare for writing data to a file
                                        #-- Probably i'll need to make this diffrently, so program will handle the case if file doesnt exist
                                            #to create a file.""" 
#Main function for retriving data
    def get_country_data(self):

        with open(self.file_path, mode= self.choice, encoding= 'utf-8') as file: #Mode chosen above, encoding due to characters in strings.

            if self.choice == "w+":
                html = pd.read_html("https://www.iban.com/country-codes") #Pulling tables from URL
                df = pd.DataFrame(html[0], columns=['Country', "Alpha-2 code"]) #Specifying columns, excluding index, creating DF
                def remove_parenthesses(string : str): 
                    if "(" in string: 
                        return string[:string.index("(")].strip()  #For those strings that contain (, we slice the string so we exclude any.
                    else:  
                        return string #If there is no (, we return normal string
                    
                df["Country"] = df["Country"].apply(remove_parenthesses) #This executes the funcion for removing parenthesses
                df.to_csv(file) #Write to a csv file
        
        #In most cases, this will get executed, reading from a file to retrieve Alpha-2 code of the country.
            else:
                df = pd.read_csv(file) #Read from csv file
 
                for i in range(4):
                    self.country = input("Country: ")

                    result = df[df["Country"].str.lower() == self.country.lower()] #Try searching for country
                    if not result.empty: #If country is found, and variable result is not empty
                        data1 = result.iloc[0]["Alpha-2 code"] #We locate the 0 index row and column Alpha code, to retrive the Country code

                        return data1 #Return the code and break the loop
                        
                        #if there's a typo in the country, program handles this by matching with the list of all countries to find the one that mathces.
                    else:
                        values1 = list(df["Country"].str.lower()) #list of all the countries in DF for the matches
                        value1 = self.country.strip() #Strip whitespaces for the country variable
                        match = FindAMatch(value=value1, choices = values1).find_match() #Class that is in other file that looks for a match and returns a tuple with the 3 most matching ones.
                            
                        if not match[0]:
                            print(match[1])
                            continue

                        elif match[0]:
                            data2 = df[df["Country"].str.lower() == match[1].lower()] #Searches the DF with the corrected string.
                            return data2.iloc[0]["Alpha-2 code"] #Locates it and returns it
                        
                return f"Couldn't find a {self.country} after {i + 1} tries, please try again"

if __name__ == "__main__":
    start = time.perf_counter()
    country = GetCountry().get_country_data()
    end = time.perf_counter()

    print(country)
    print(end-start)

class CountriesDataApi(GetCountry):
    def __init__(self, place) -> None:
        self.place = place
        self.path =  "C:\\Users\\Jernej\\Documents\\OOP\\database_files\\alpha_codes.csv"
        self.code_country = GetCountry().get_country_data()


        if not self.code_country:
            raise ValueError(f"Alpha code for country '{self.code_country}' not found.")
        self.link = f"https://parseapi.back4app.com/classes/Worldzipcode_{self.code_country}?limit=10&where="
        self.fields = ["placeName", "adminName1", "adminName2", "adminName3"]

    def api_data(self):
        data_p = self.query_encode_input()
        link1 = self.link + data_p
        headers = {
            'X-Parse-Application-Id': '3bQHtMIFu1cLnHo0My7AhOTwZgnmUCqmytJBaB3J', 
            'X-Parse-REST-API-Key': 'Tg8LGUCYxxajwrnhEtH24FV5iNujLorWunI0D9zf'
        }

        response = requests.get(link1, headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            print(response.content.decode('utf-8'))
    
    def query_encode_input(self):
        query = {"$or": [{field: self.place} for field in self.fields]}
        json_s = json.dumps(query)
        encoded = urllib.parse.quote_plus(json_s)
        return encoded

    def main(self):
        self.api_data()
        

            


