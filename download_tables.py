""" Downloads and Saves all tables locally """
import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

DATABASE_URL = "https://fbref.com/en/comps/9/Premier-League-Stats"

class DownloadTables:
	def __init__(self, database_url):
		self.database_url = database_url
		self.squad_tables = [
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
		self.player_tables = [
			"Standard Stats",
			"Goalkeeping",
			"Advanced Goalkeeping",
			"Shooting",
			"Passing",
			"Pass Types",
			"Goal and Shot Creation",
			"Defensive Actions",
			"Possession",
			"Playing Time",
			"Miscellaneous Stats"
		]

	def create_team_list(self):
		html = requests.get(self.database_url, timeout=20)
		home_page = StringIO(html.text)

		# Initialize BeautifulSoup
		soup_team_list = BeautifulSoup(home_page, features="lxml")

		for i in range(len(self.squad_tables)):
			# Find the Regular Season - Overall Table
			data = soup_team_list.select('table.stats_table')[i]

			# Read the table using Pandas
			table = pd.read_html(str(data))[0]

			# Save the DataFrame to a formatted JSON file in the "tables" folder
			folder_name = "raw_data/team_folders"
			os.makedirs(folder_name, exist_ok=True)
			print(self.squad_tables[i])
			json_filename = os.path.join(folder_name, f"{self.squad_tables[i]}.json")
			print(json_filename)

			try:
				with open(json_filename, "w") as json_file:
					json.dump(json.loads(table.to_json(orient="records")), json_file, indent=4)
			except Exception as e:
				print(f"Error: {e}")

# Create an instance of DownloadTables
downloader = DownloadTables("https://fbref.com/en/comps/9/Premier-League-Stats")

# Call the create_team_list method on the instance
downloader.create_team_list()


