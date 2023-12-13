import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

class TeamTables:
    def __init__(self, database_url, squad_tables):
        self.database_url = database_url
        self.squad_tables = squad_tables

    # Download all the squad tables from the homepage
    def create_squad_json(self):
        # Download the page and convert to HTML
        html = requests.get(self.database_url, timeout=20)
        home_page = StringIO(html.text)

        # Initialize BeautifulSoup
        soup_team_list = BeautifulSoup(home_page, features="lxml")

        for i in range(len(self.squad_tables)):
            # Iterate through the 'stats table'
			# 'stats table' is the class of the table element
            data = soup_team_list.select('table.stats_table')[i]

            # Read the table using Pandas
            table = pd.read_html(str(data))[0]

            # Create a new folder
            folder_name = "raw_data/squad_data"
            os.makedirs(folder_name, exist_ok=True)

            # Create a .JSON file using the strings from squad table
            json_filename = os.path.join(folder_name, f"{self.squad_tables[i]}.json")

            # Open each .JSON file and convert tables to json data
            try:
                with open(json_filename, "w") as json_file:
                    json.dump(json.loads(table.to_json(orient="records")), json_file, indent=4)
            except Exception as e:
                print(f"Error: {e}")

squad_tables = [
	"Regular Season - Overall",
	"Regular Season - Home/Away",
	"Squad Standard Stats - Squad Stats",
	"Squad Standard Stats - Opponent Stats",
	"Squad Goalkeeping - Squad Stats",
	"Squad Goalkeeping - Opponent Stats",
	"Squad Advanced Goalkeeping - Squad Stats",
	"Squad Advanced Goalkeeping - Opponent Stats",
	"Squad Shooting - Squad Stats",
	"Squad Shooting - Opponent Stats",
	"Squad Passing - Squad Stats",
	"Squad Passing - Opponent Stats",
	"Squad Pass Types - Squad Stats",
	"Squad Pass Types - Opponent Stats",
	"Squad Goal and Shot Creation - Squad Stats",
	"Squad Goal and Shot Creation - Opponent Stats",
	"Squad Defencive Actions - Squad Stats",
	"Squad Defencive Actions - Opponent Stats",
	"Squad Possession - Squad Stats",
	"Squad Possession - Opponent Stats",
	"Squad Playing Time - Squad Stats",
	"Squad Playing Time - Opponent Stats",
	"Squad Miscellaneous Stats - Squad Stats",
	"Squad Miscellaneous Stats - Opponent Stats"
]

database_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

# Create an instance of PlayerTables
test_instance = TeamTables(database_url, squad_tables)

# Call the create_team_folders method on the instance
test_instance.create_squad_json()
