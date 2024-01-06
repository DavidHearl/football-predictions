import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import io

class ClubStatistics:
    def __init__(self, overall_statistics_url, overall_statistics_tables):
        self.overall_statistics_url = overall_statistics_url
        self.overall_statistics_tables = overall_statistics_tables

    # Download all the squad tables from the homepage
    def create_json(self):
        # Download the page and convert to HTML
        html = requests.get(self.overall_statistics_url, timeout=20)
        home_page = StringIO(html.text)

        # Initialize BeautifulSoup
        soup_team_list = BeautifulSoup(home_page, features="lxml")

         # Create a new folder
        folder_name = "raw_data/club_data"
        os.makedirs(folder_name, exist_ok=True)

        for i in range(len(self.overall_statistics_tables)):
            # Iterate through the 'stats table'
			# 'stats table' is the class of the table element
            data = soup_team_list.select('table.stats_table')[i]

            # Read the table using Pandas
            table = pd.read_html(io.StringIO(str(data)))[0]

            # Create a .JSON file using the strings from squad table
            json_filename = os.path.join(folder_name, f"{self.overall_statistics_tables[i]}.json")
            print(json_filename)

            # Open each .JSON file and convert tables to json data
            try:
                with open(json_filename, "w") as json_file:
                    json.dump(json.loads(table.to_json(orient="records")), json_file, indent=4)
            except Exception as e:
                print(f"Error: {e}")
