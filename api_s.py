import requests
from bs4 import BeautifulSoup
import pandas as pd
from fuzzymatcher import DataPreprocessor
from fuzzywuzzy import process
import csv

country_list = [
    "United States",
    "Canada",
    "Germany",
    "France",
    "Japan",
    "Australia",
    "India",
    "Brazil",
    "South Africa",
    "China",
    "Russia",
    "Mexico",
    "Italy",
    "Spain",
    "Sweden",
    "Norway",
    "Argentina",
    "Saudi Arabia",
    "Turkey",
    "Indonesia"
]

class ZipCodeData:
    def __init__(self, kraj) -> None:
        self.kraj = kraj

    def scrape_zip_data(self): 
        url = "https://sl.wikipedia.org/wiki/Seznam_po%C5%A1tnih_%C5%A1tevilk_v_Sloveniji"
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, "html.parser")

        zip_codes = []

        for ul in soup.find(class_="mw-content-ltr mw-parser-output").find_all('ul'):
            for li in ul.find_all("li"):
                data = str(li.text)
                zip_codes.append(data)

        split_data = [data.split('-') for data in zip_codes if '-' in data]
        cleaned_data = []

        for line in split_data:
            if len(line) > 2:
                line = [''.join(line[:2])] + line[2:]
            cleaned_data.append(line)

        df = pd.DataFrame(cleaned_data, columns=["Kraj", "Zip"])
        df["Zip"] = df["Zip"].str.strip()
        df['Kraj'] = df['Kraj'].str.strip()
        df.to_csv("C:\\Users\\Jernej\\Documents\\OOP\\database_files\\zip_codes.csv", index = False)
    
    
    def get_zip_data(self):
        kraj_data = self.kraj.capitalize()
        data_info = {}

        with open("C:\\Users\\Jernej\\Documents\\OOP\\database_files\\zip_codes.csv", "r+", encoding = "utf-8") as f:
                file_data = csv.reader(f)
                for kraj, code in file_data:
                    data_info[kraj] = code 
                if kraj_data in data_info.keys():
                    return data_info[kraj_data]
                
                else:
                    suggestion = FindAMatch(value = self.kraj, choices = list(data_info.keys()))
                    return suggestion.find_match()                


#Make sure to index a return value when using this class to catch a tuples value depending if the value is valid or not.
#Since tuple here always returns two values, FIRSTL: bool, SECOND: a valid value or raises and error message.

class FindAMatch:
    def __init__(self, value, choices) -> None:
        self.value = value
        self.choices = choices
        
    def find_match(self):
        if not self.value or not self.value.strip():
            return False, "Empty value, please try again!"
      
        choices = self.choices
        choices = process.extract(self.value, choices)

        hash_choices = {}
        for a, b in choices:
            hash_choices[a] = b
        
        max_key, max_value = max(hash_choices.items(), key=lambda x: x[1])
        if max_value < 80:
            return False, f"{self.value} is incorrect, did you maybe mean: {' | '.join(hash_choices)} ?"
        return True, max_key


if __name__ == "__main__":
    e = FindAMatch(value="sdasdasd", choices=country_list).find_match()
    print(e)
    