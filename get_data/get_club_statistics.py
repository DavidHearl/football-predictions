import os
import json
import time
from io import StringIO

import requests
import pandas as pd
from bs4 import BeautifulSoup


class ClubStatistics:
    def create_json(self):
        # Print a blank line to separate the output
        print()

        # Open the urls.json file and load the data
        with open('get_data/keys.json', 'r') as f:
            data = json.load(f)

        # Assign the overall_statistics_url to a variable
        overall_statistics_url = data['overall_urls'][0]
        overall_statistics_tables = data['overall_tables']

        # Use a session for multiple requests
        with requests.Session() as session:
            # Download the page and convert to HTML
            html = session.get(overall_statistics_url, timeout=20)

            # Initialize BeautifulSoup
            soup_team_list = BeautifulSoup(html.text, features="lxml")

            # Create a new folder
            folder_name = "raw_data/2023-2024/club_data"
            os.makedirs(folder_name, exist_ok=True)

            # Use list comprehension to iterate over the tables
            tables = [pd.read_html(StringIO(str(data)))[0] for data in soup_team_list.select('table.stats_table')]

            # Iterate over the tables and create a .JSON file for each table
            for table_name, table in zip(overall_statistics_tables, tables):
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
