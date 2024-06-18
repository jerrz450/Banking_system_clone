import asyncio
from concurrent.futures import ThreadPoolExecutor
import aiohttp
import os
import pandas as pd
from country_api import GetData, Vectorize_Dataframe
from get_country_code import GetCountryCode
from aiohttp import ClientResponseError
import numpy as np
import time
import re
import sys
import logging

logging.basicConfig(level= logging.WARNING, format= "%(levelname)s - %(message)s - [in %(filename)s:%(lineno)d]")


class UserPromptsGather:

    def __init__(self) -> None:
        self.show1 = True
    
    @staticmethod
    def _clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def validate_post_code(self, post_code):
        validation = re.fullmatch(r"^[a-zA-Z]{0,3}[0-9]{1,6}[a-zA-Z]{0,3}$", post_code)
        if validation:
            return True
        else:
            return False
        
    def validate_city(self, city):
        if isinstance(city, str) and not None and len(city) > 1:
            return True
        elif len(city) <= 0:
            return False
        
    def validate_state_county(value):
        try:
            if len(value) == 0:
                return None
            return isinstance(value, str) and len(value) > 0
        except (ValueError, TypeError) as e:
            logging.error("Exception occured {e}, probably the integer was entered.")
            return False
            
    
    async def ainput(self, prompt: str, func_ = None, retries = 4) -> str:
        for attempt in range(retries):
            with ThreadPoolExecutor(2, f"AsyncInput_{prompt}") as executor:
                main_data_prompt = await asyncio.get_event_loop().run_in_executor(executor, input, prompt)
                if func_ is not None:
                    validate_call = await asyncio.get_event_loop().run_in_executor(executor, func_, main_data_prompt)
                    print(validate_call)
                    if validate_call:
                        return main_data_prompt
                    elif func_ == self.validate_state_county and validate_call is None:
                        return validate_call
                    else:
                        self._clear_screen()
                        print(f"{'Empty value' if len(main_data_prompt) <= 0 else main_data_prompt} is not correct, please try again!")
                else:
                    return main_data_prompt
        return False  
       
    async def vectorize_df(self, df, post_code, city, county, state):
        data = await asyncio.gather(Vectorize_Dataframe(df=df, postal_code=post_code, city=city, county=county, state=state).run_gather_df())
        return data

    async def write_nan(self, df):
        df['adminName2'] = np.where(df["adminName2"].astype(bool), df["adminName2"], np.nan)
        df['adminName1'] = np.where(df["adminName1"].astype(bool), df["adminName1"], np.nan)
        return df

    async def check_for_prompts(self, df):
        df = await self.write_nan(df)

        admin_name1 = df["adminName1"].isna().all()
        admin_name2 = df["adminName2"].isna().all()

        if not admin_name2 or not admin_name1:
            self.show1 = False
        else:
            self.show1 = True

    async def main(self, count = 0):
        while True:
            country = await self.ainput("Country: ", func_= None)
            data = await asyncio.gather(GetCountryCode(country).run())
            if data[0][0]:
                country_data_task = asyncio.create_task(GetData(data[0][1]).fetch_data_country())
            else:
                self._clear_screen()
                count += 1
                print(data[0][1])
                if count <= 6:
                    continue
                sys.exit("Too manu retries - {count}, please try again!")       

            postal_code = await self.ainput("Post code: ", self.validate_post_code)
            if not postal_code:
                self._clear_screen()
                print("The inputs are not correct, please try again!")
                continue

            city = await self.ainput("City: ", self.validate_city)

            if not postal_code or not city:

                user_message = f"An error occurred with the input, value is probably not correct. Please try again!"
                developer_message = f"Error occured {ValueError}"

                self._clear_screen()
                print(user_message)
                logging.warning(developer_message)

                continue

            retrieved_data = await country_data_task
            bg_task = asyncio.create_task(self.check_for_prompts(retrieved_data))
            await bg_task

            county, state = (await self.ainput("County [Or press enter to skip]: ", self.validate_state_county), await self.ainput("State [Or press enter to skip]: ", self.validate_state_county)) if not self.show1 else (None, None)
            try:
                if country and city and postal_code: 
                    final = await self.vectorize_df(retrieved_data, post_code=postal_code, city=city, county=county, state=state)
                    return final
                else:
                    self._clear_screen()
                    print("Some values are not correct, please try again!")
                    continue

            except (ValueError, ClientResponseError) as e:
                self._clear_screen()
                user_message = "An error occurred with your input. Please try again!"
                developer_message = f"Input error: {e}"
                
                # Display a user-friendly message
                print(user_message)
                
                # Log the detailed message for the developer
                logging.warning(developer_message)

    def gather_user_data(self):
        data = asyncio.run(self.main())
        return data


if __name__ == "__main__":
    result = UserPromptsGather().gather_user_data()
    print(result)

# show1 = True
    
# async def ainput(prompt: str = "") -> str:
#     with ThreadPoolExecutor(1, f"AsyncInput_{prompt}") as executor:
#         return await asyncio.get_event_loop().run_in_executor(executor, input, prompt)

# async def check_nan(df):
#     df['adminName2'] = np.where(df["adminName2"].astype(bool), df["adminName2"], np.nan)
#     df['adminName1'] = np.where(df["adminName1"].astype(bool), df["adminName1"], np.nan)
#     return df

# async def check_for_prompts(final):
#     global show1
#     df = final[0]
#     df = await check_nan(df)

#     admin_name1 = df["adminName1"].isna().all()
#     admin_name2 = df["adminName2"].isna().all()

#     if not admin_name2 or not admin_name1:
#         list1 = df["adminName2"][df["adminName2"].astype(bool)].tolist()
#         data1 = df["adminName2"].apply(lambda x: x if x else np.nan)
#         show1= False
#     else:
#         show1= True

# async def gather_data():
#     global show1
#     final = await asyncio.gather(GetData("US").fetch_data_country())
#     bg_task = asyncio.create_task(check_for_prompts(final))
    
#     country = await ainput("Country: ")
#     postal_code = await ainput("Post code: ")
#     city = await ainput("City: ")

#     await bg_task

#     if show1 == False:            
#         county = await ainput("County: ")
#         state = await ainput("State: ")
#         return "Eureka"
    
#     return "Not county"
