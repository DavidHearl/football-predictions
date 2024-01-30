import os
import json
import time
from io import StringIO
from urllib.parse import urlparse

import requests
import pandas as pd
from bs4 import BeautifulSoup
import random


# The server will block the request if frequency exceeds 1 request per 3 seconds (20 requests per minute)
# Therefore, we need to add a delay to prevent the server from blocking the request, use 4 seconds for safety.
class LegacyClubStatistics:
    def __init__(self, legacy_seasons):
        self.legacy_seasons = legacy_seasons

    def get_club_data(self):
        print("Getting club data...")

        # Open the urls.json file and load the data
        with open('get_data/keys.json', 'r') as f:
            data = json.load(f)
        
        # Get the list of table names, used for json file names
        overall_statistics_tables = data['overall_statistics_tables']

        # Link for reference: "https://fbref.com/en/comps/9/2022-2023/2022-2023-Premier-League-Stats"
        for league in data['leagues']:
            for season in self.legacy_seasons:
                if league == 'premier_league':
                    url = f"https://fbref.com/en/comps/9/{season}/{season}-Premier-League-Stats"
                elif league == 'championship':
                    url = f"https://fbref.com/en/comps/10/{season}/{season}-Championship-Stats"
                elif league == 'la_liga':
                    url = f"https://fbref.com/en/comps/12/{season}/{season}-La-Liga-Stats"
                elif league == 'ligue_1':
                    url = f"https://fbref.com/en/comps/13/{season}/{season}-Ligue-1-Stats"

                # Print a blank line to separate the output
                print()
                print("Current Time:", time.strftime("%H:%M:%S", time.localtime()))

                # Add a delay to stop the server from blocking the request
                random_number = random.uniform(3, 5)
                print(f"Waiting {random_number} seconds...")
                time.sleep(random_number)
                print()

                folder_name = f"raw_data/{league}/{season}/club_data"

                # Add a delay to try again if the request fails
                while True:
                    try:
                        # Download the page and convert to HTML
                        html = requests.get(url, timeout=20)
                        break
                    except requests.exceptions.Timeout:
                        print("Timeout occurred. Trying again in 15 minutes...")
                        print("Current Time:", time.strftime("%H:%M:%S", time.localtime()))
                        print()
                        time.sleep(900) # Wait 15 minutes before trying again

                # Initialize BeautifulSoup
                soup_team_list = BeautifulSoup(html.text, features="lxml")

                # Use list comprehension to iterate over the tables
                tables = [
                    pd.read_html(StringIO(str(data)))[0]
                    for data in soup_team_list.select('table.stats_table')
                ]

                # Iterate over the tables and create a .JSON file for each table
                for table_name, table in zip(overall_statistics_tables, tables):
                    # Create a .JSON file using the strings from squad table
                    json_filename = os.path.join(folder_name, table_name + ".json")
                    print(json_filename)

                    # Open each .JSON file and convert tables to json data
                    try:
                        with open(json_filename, "w") as json_file:
                            json.dump(json.loads(table.to_json(orient="records")), json_file, indent=4)
                    except (FileNotFoundError, IOError) as e:
                        print(f"Error: {e}")

                # Print a blank line to separate the output 
                print()
