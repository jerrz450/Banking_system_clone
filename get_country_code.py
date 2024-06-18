import asyncio
import aiofiles
import pandas as pd
import os
import time
from api_s import FindAMatch

class GetCountryCode:
    def __init__(self, country):
        self.country = country

    async def file_exists_check(self):
        file_path = "C:\\Users\\Jernej\\Documents\\OOP\\database_files\\zip_codes.csv"
        data = await self.check_file(file_path)
        if data:
            final = await self.pull_data(file_path=file_path, file_mode=data[0])
            return final
        return None

    async def check_file(self, file_path):
        if os.path.exists(file_path):
            async with aiofiles.open(file_path, mode="r+") as file:
                await file.seek(0, os.SEEK_END)
                tell = await file.tell()
                if tell:
                    await file.seek(0)
                    choice = ("r+", True)
                else:
                    choice = ("w+", False)
            return choice
        else:
            print("File does not exist!")
            return None

    async def get_table(self):
        table_data = await self.get_pandas(url="https://www.iban.com/country-codes")
        df = pd.DataFrame(table_data, columns=['Country', "Alpha-2 code"])
        return df

    async def get_pandas(self, url="https://www.iban.com/country-codes"):
        html = pd.read_html(url)
        df = pd.DataFrame(html[0], columns=['Country', "Alpha-2 code"])
        df['Country'] = df['Country'].str.split('(').str[0].str.strip()
        pd.set_option('display.max_rows', None)
        return df

    async def write_to_csv(self, df, file_path) -> None:
        async with aiofiles.open(file_path, mode='w', encoding='utf-8') as file:
            await file.write(df.to_csv(index=False))

    async def pull_data(self, file_path, file_mode):
        async with aiofiles.open(file_path, mode=file_mode, encoding='utf-8') as file:
            if file_mode == "w+":
                result = await self.get_table()
                await self.write_to_csv(df=result, file_path=file_path)
                print("Wrote data to a file.")
            else:
                data_frame = pd.read_csv(file_path, index_col=False)
                code_alpha = await self.read_df_data(data_frame, self.country)
                return code_alpha

    async def read_df_data(self, df: pd.DataFrame, country):
        list_of_matches = await self.get_list(df)
        tasks = [self.get_fuzzy_match(value1=country, list_choices=list_of_matches)]
        country_data = await asyncio.gather(*tasks)
        final_data = await self.get_match(df, country_data[0][1])

        if final_data:
            return [True, final_data]
        else:
            return [False, country_data[0][1]]

    async def get_fuzzy_match(self, value1, list_choices):
        matches = FindAMatch(value=value1, choices=list_choices).find_match()
        return matches

    async def get_match(self, df: pd.DataFrame, country):
        try:
            code = df[df["Country"].str.lower().str.strip() == country.lower().strip()]
            code = code.iloc[0, 1]
            return code
        except IndexError:
            return False

    async def get_list(self, df: pd.DataFrame):
        list_values = list(df["Country"].str.lower())
        return list_values

    async def run(self):
        data = await self.file_exists_check()
        return data

if __name__ == "__main__":
    code_c =input("Country: ")
    data_input = asyncio.run(GetCountryCode(code_c).run())
    print(data_input[1])