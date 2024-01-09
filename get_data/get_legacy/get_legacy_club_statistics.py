import os
import json
import time
from io import StringIO
from urllib.parse import urlparse

import requests
import pandas as pd
from bs4 import BeautifulSoup


class LegacyClubStatistics:
    def __init__(self, legacy_seasons):
        self.legacy_seasons = legacy_seasons

    def create_json(self):
        # Print a blank line to separate the output
        print()

        # Open the urls.json file and load the data
        with open('get_data/keys.json', 'r') as f:
            data = json.load(f)

        # Get the list of table names, used for json file names
        overall_statistics_tables = data['overall_tables']

        # Link for reference: "https://fbref.com/en/comps/9/2022-2023/2022-2023-Premier-League-Stats"
        for season in self.legacy_seasons:
            # Create the url for each season
            url = f"https://fbref.com/en/comps/9/{season}/{season}-Premier-League-Stats"

            # Sleep for half a second to avoid overloading the server
            time.sleep(0.5)

            # Use a session for multiple requests
            with requests.Session() as session:
                # Download the page and convert to HTML
                html = session.get(url, timeout=20)

                # Initialize BeautifulSoup
                soup_team_list = BeautifulSoup(html.text, features="lxml")

                # Use list comprehension to iterate over the tables
                tables = [
                    pd.read_html(StringIO(str(data)))[0]
                    for data in soup_team_list.select('table.stats_table')
                ]

                # ------------------------------------------------------------

                # Check if 'club_urls' key already exists in the data
                if 'club_urls' in data:
                    club_urls = data['club_urls']
                else:
                    club_urls = {}

                # Check if the season is already in the club_urls
                if season not in club_urls:
                    # Get the urls for each club
                    # Find the first table with class 'stats_table'
                    first_table = soup_team_list.select_one('table.stats_table')

                    # Find all elements with data-stat property equal to 'team' within the first table
                    team_elements = first_table.find_all('td', attrs={"data-stat": "team"})

                    # Create an array to store the href values
                    href_values = []

                    # Iterate over the team elements and extract the href values
                    for team_element in team_elements:
                        href = team_element.find('a')['href']
                        href_values.append(href)

                    club_urls[season] = href_values

                # Update the club_urls in the keys.json file
                data['club_urls'] = club_urls

                # Save the updated data to the keys.json file
                with open('get_data/keys.json', 'w') as f:
                    json.dump(data, f, indent=4)

                # ------------------------------------------------------------

                # Create a new folder
                folder_name = f"raw_data/{season}/club_data"
                os.makedirs(folder_name, exist_ok=True)

                # Iterate over the tables and create a .JSON file for each table
                for table_name, table in zip(overall_statistics_tables, tables):
                    # Remove leading and trailing whitespace from the table name
                    table_name = table_name.strip()

                    # Sleep for half a second to avoid overloading the server
                    time.sleep(0.5)

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
