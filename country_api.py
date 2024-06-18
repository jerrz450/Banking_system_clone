import asyncio
import aiohttp
import time
import json
import urllib.parse
from api_s import FindAMatch
import pandas as pd
import numpy as np
import timeit
import os
from get_country_code import GetCountryCode
import re

class GetData:
    def __init__(self, code) -> None:
        self.code = code

        self.headers = {
                'X-Parse-Application-Id': f'{os.environ.get("4_APP_API_ID")}', 
                'X-Parse-REST-API-Key': f'{os.environ.get("4_APP_API_PASS")}'
                        }
        self.url = f"https://parseapi.back4app.com/classes/Worldzipcode_{self.code}?limit=5000000000000000000"

    async def fetch_data_country(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers= self.headers) as response:
                response.raise_for_status()
                data = await response.json()
                df = pd.json_normalize(data, 'results')
                df.drop(columns=['adminCode3', 'accuracy', 'createdAt', 'updatedAt', 'geoPosition.__type', 'geoPosition.latitude', 'geoPosition.longitude'], inplace=True)
                return df

class Vectorize_Dataframe:

    def __init__(self, df, city, postal_code, county=None, state=None) -> None:
        self.df = df
        self.postal_code = postal_code
        self.city = city
        self.county = county or None
        self.state = state or None

          
    async def gather_df_data(self):
        if self.county is not None or self.state is not None:
            city = self.df["placeName"].str.contains(self.city, na=False)
            state = self.df["adminName1"].str.contains(self.state, na=False)
            county = self.df["adminName2"].str.contains(self.county, na=False)
            postal_code = self.df["postalCode"].str.contains(self.postal_code)

            match_count = city.astype(int) + state.astype(int) + county.astype(int) + postal_code.astype(int)

            top_match_indices = match_count.nlargest(10).index  # Get top 10 matches

            return self.df.loc[top_match_indices]
        else:
            city = self.df["placeName"].str.contains(self.city, na=False)
            postal_code = self.df["postalCode"].str.contains(self.postal_code)

            match_count = city.astype(int) + postal_code.astype(int)

            top_match_indices = match_count.nlargest(10).index  # Get top 10 matches

            return self.df.loc[top_match_indices]
        
    @staticmethod
    async def get_match(match, list_choices):
        matched = FindAMatch(value=match, choices=list_choices).find_match()
        return matched

    async def run_gather_df(self):

        data_df = await self.gather_df_data()
  
        return data_df


if __name__ == "__main__":
    
    
    data2 = asyncio.run(GetData("US").fetch_data_country())
    start = time.perf_counter()
    data1 = asyncio.run(Vectorize_Dataframe(df = data2, city= "Los Angeles", postal_code= "9000").run_gather_df())
    end = time.perf_counter()

    print(data1)
    print(f"Task ended in {end - start} seconds!")
    #data = GetData(city = city, postal_code = postal_code, code = country_code[1], county= None, state= None).run_zipcode_api_call()


def test():
    async def call_api(self):
        
        async with aiohttp.ClientSession() as session:
            tasks =  [self.get_whole(session, self.url)]
            results = await asyncio.gather(*tasks)
            list_data = [self.get_place_data(df = results, place = "Los Angeles")]

            whole_result = await asyncio.gather(*list_data)
            match_result = await self.get_match(match= self.place, list_choices= whole_result)

            if match_result[0]:
                task2 = [self.get_content(session, self.get_query(place = match_result[1]))]
                results2 = await asyncio.gather(*task2)
                one_result = await self.process_results_one(results2[0])
                return one_result

    def get_query(self, place, fields=["placeName", "adminName1", "adminName2", "adminName3"]):
        regex_pattern = f".*{place}.*"
        query = {"$or": [{field: {"$regex": regex_pattern, "$options": "i"}} for field in fields]}
        query1 = json.dumps(query)
        encoded = urllib.parse.quote_plus(query1)
        url = self.base_url + encoded
        return url

    async def get_content(self, session, url):
        async with session.get(url, headers= self.headers) as response:
            response.raise_for_status()
            data = await response.json()
            return dict(data)

    async def proccess_result_whole(self,result):
        list1 = [result[data] for data in ["placeName", "adminName1", "adminName2", "adminName3"] if result[data]]
        final_list = ''.join(list1)
        return final_list
        
    async def process_results_one(self, result):
        if not result['results']:
            return False
        else:
            sample_dict = result['results']
            return sample_dict
        
    async def get_place_data(self, df : pd.DataFrame):
        if self.county is not None or self.state is not None: 
            city = df["placeName"].str.contains("Chicago", na= False)
            state = df["adminName1"].str.contains("Illinois",na= False)
            county = df["adminName2"].str.contains("'Cook County", na= False)
            postal_code = df["postalCode"].str.contains("60601")

            match_count = city.astype(int) + state.astype(int) + county.astype(int) + postal_code.astype(int) 
            
            max_match_index = match_count.idxmax()

            return df.loc[max_match_index] if match_count[max_match_index] > 0 else False
        else:
            city = df["placeName"].str.contains(self.city, na= False)
            postal_code = df["postalCode"].str.contains(self.postal_code)

            match_count = city.astype(int) + postal_code.astype(int)

            max_match_index = match_count.idxmax()

            return df.loc[max_match_index] if match_count[max_match_index] > 0 else False

    async def get_match(self, match, list_choices):
        matched = FindAMatch(value= match, choices= list_choices).find_match()
        return matched
    