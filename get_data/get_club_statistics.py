import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import time

class ClubStatistics:
    def __init__(self, overall_statistics_url, overall_statistics_tables):
        self.overall_statistics_url = overall_statistics_url
        self.overall_statistics_tables = overall_statistics_tables

    # Download all the squad tables from the homepage
    def create_json(self):
        # Print a blank line to separate the output
        print()

        # Use a session for multiple requests
        with requests.Session() as session:
            # Download the page and convert to HTML
            html = session.get(self.overall_statistics_url, timeout=20)

            # Initialize BeautifulSoup
            soup_team_list = BeautifulSoup(html.text, features="lxml")

            # Create a new folder
            folder_name = f"raw_data/club_data"
            os.makedirs(folder_name, exist_ok=True)

            # Use list comprehension to iterate over the tables
            tables = [pd.read_html(StringIO(str(data)))[0] for data in soup_team_list.select('table.stats_table')]

            for i, table in enumerate(tables):
                # Sleep for half a second to avoid overloading the server
                time.sleep(0.5)

                # Create a .JSON file using the strings from squad table
                json_filename = os.path.join(folder_name, f"{self.overall_statistics_tables[i]}.json")
                print(json_filename)

                # Open each .JSON file and convert tables to json data
                try:
                    with open(json_filename, "w") as json_file:
                        json.dump(json.loads(table.to_json(orient="records")), json_file, indent=4)
                except (FileNotFoundError, IOError) as e:
                    print(f"Error: {e}")

                # Print a blank line to separate the output 
                print()
