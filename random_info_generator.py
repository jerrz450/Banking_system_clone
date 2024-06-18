import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import sys
from get_country_code import GetCountryCode
import re
from country_api import GetData, Vectorize_Dataframe
from aiohttp import ClientResponseError
import os
import pandas as pd


# Assuming these functions are defined elsewhere in your code
# from get_country_code import GetCountryCode
# from country_api import GetData, Vectorize_Dataframe
# from aiohttp import ClientResponseError

def validate_num(num: str):
    if re.fullmatch(r"^[a-zA-Z]{0,3}[0-9]{1,6}[0-9]{0,3}$", num):
        return True, num
    else:
        return False, f"{num} is not correct, please try again!"

def validate_city(city):
    if city:
        return True, city
    else:
        return False, "City is not correct, please try again!"

def validate_country1(country):
    try:
        result = GetCountryCode(country).run()
        if result[0]:
            data = GetData(code=result[1]).run_zipcode_api_call()
            return True, data
        else:
            return False, f"---> {result[1]}  <---"
        
    except ClientResponseError:
        return False, "Api Error" 

def _clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def helper_function(function, prompt, pool=None):
    for _ in range(3):
        data = input(prompt).strip()
        if pool:
            future = pool.submit(function, data).start()
            return future

        else:
            valid, result = function(data)
            if valid:
                return result
            else:
                return valid
        
    sys.exit("Too many tries")

def prompt():

    with ThreadPoolExecutor(max_workers=3) as pool:
        
        country_input = helper_function(validate_country1, "Country: ", pool)
        city_input = helper_function(validate_city, "City: ")
        postal_code_input = helper_function(validate_num, "Post code: ")

        count = 0
        while country_input.result()[0] is False:
            print("Please try again!")
            country_input = helper_function(validate_country1, "Country: ", pool)
            count += 1
            if count == 3:    
                sys.exit("Too many tries, please try again later!")
        else:
            print("Good continiue")


        print("All inputs are correct.")
        print(f"Country Data: {country_input}")
        print(f"City: {city_input}")
        print(f"Post Code: {postal_code_input}")
    


if __name__ == "__main__":
    prompt()


#address_info = {"Country_df": country_result, "City": city, "Post code": postal_code, "County": None, "State": None}

 #   gather_data_future = pool.submit(
#
##gather_dataframe_data,##  
##city1=address_info["City"],
##postal_code1=address_info["Post code"],
##df1=address_info["Country_df"],
##county = address_info["County"], 
#state = address_info["State"]
#)

#data2 = gather_data_future.result()

#print(data2)