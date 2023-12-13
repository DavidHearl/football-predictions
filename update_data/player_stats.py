import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

class PlayerTables:
	def __init__(self, database_urls, player_tables):
		self.database_urls = database_urls
		self.player_tables = player_tables

	# Download all the player tables from the club url
	def create_player_json(self):
		# Iterate through all the club urls
		for url in self.database_urls:
			# Download the page and convert to HTML
			html = requests.get(url, timeout=20)
			home_page = StringIO(html.text)

			# Initialize BeautifulSoup
			soup_team_list = BeautifulSoup(home_page, features="lxml")

			# -----------------------------------------------------------------
			# Create team folders

			# Split the URL by "/"
			url_parts = url.split("/")
			
			# Find the index of 'squads' in the URL
			squads_index = url_parts.index("squads")
			
			# Extract the part of the URL containing the team name
			team_name_with_hyphen = url_parts[squads_index + 2]
			
			# Check if the team name ends with "Stats" and remove it
			if team_name_with_hyphen.endswith("-Stats"):
				team_name_with_hyphen = team_name_with_hyphen[:-6]  # Remove the last 6 characters ("Stats")
			
			# Remove hyphens from the team name
			team_name = team_name_with_hyphen.replace('-', ' ')
			
			# Convert 'United' to 'Utd'
			if 'United' in team_name.split():
				team_name = team_name.replace('United', 'Utd')
			
			# Handle special cases
			special_cases = {
				'Brighton and Hove Albion': 'Brighton',
				'West Ham Utd': 'West Ham',
				'Wolverhampton Wanderers': 'Wolves',
				'Nottingham Forest': "Nott'ham Forest"
			}
			
			for special_case, replacement in special_cases.items():
				if special_case in team_name:
					team_name = team_name.replace(special_case, replacement)

			# Create a new folder for each team
			folder_name = os.path.join("raw_data/teams", team_name)
			os.makedirs(folder_name, exist_ok=True)		

			# -----------------------------------------------------------------

			# Iterate through the player tables
			for i in range(len(self.player_tables)):
				# Iterate through the 'stats table'
				# 'stats table' is the class of the table element
				data = soup_team_list.select('table.stats_table')[i]

				# Read the table using Pandas
				table_data = pd.read_html(str(data))[0]

				# Create a .JSON file using the strings from player table
				json_filename = os.path.join("raw_data/teams", team_name, f"{self.player_tables[i]}.json")
				print(json_filename)

				# Create the directory if it doesn't exist
				os.makedirs(os.path.dirname(json_filename), exist_ok=True)

				# Open each .JSON file and convert tables to JSON data
				try:
					with open(json_filename, "w") as json_file:
						json.dump(json.loads(table_data.to_json(orient="records")), json_file, indent=4)
				except Exception as e:
					print(f"Error: {e}")



database_urls = [
	"https://fbref.com/en/squads/18bb7c10/Arsenal-Stats",
	"https://fbref.com/en/squads/8602292d/Aston-Villa-Stats",
	"https://fbref.com/en/squads/4ba7cbea/Bournemouth-Stats",
	"https://fbref.com/en/squads/cd051869/Brentford-Stats",
	"https://fbref.com/en/squads/d07537b9/Brighton-and-Hove-Albion-Stats",
	"https://fbref.com/en/squads/943e8050/Burnley-Stats",
	"https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats",
	"https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats",
	"https://fbref.com/en/squads/d3fd31cc/Everton-Stats",
	"https://fbref.com/en/squads/fd962109/Fulham-Stats",
	"https://fbref.com/en/squads/822bd0ba/Liverpool-Stats",
	"https://fbref.com/en/squads/e297cd13/Luton-Town-Stats",
	"https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats",
	"https://fbref.com/en/squads/19538871/Manchester-United-Stats",
	"https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats",
	"https://fbref.com/en/squads/e4a775cb/Nottingham-Forest-Stats",
	"https://fbref.com/en/squads/1df6b87e/Sheffield-United-Stats",
	"https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats",
	"https://fbref.com/en/squads/7c21e445/West-Ham-United-Stats",
	"https://fbref.com/en/squads/8cec06e1/Wolverhampton-Wanderers-Stats"
]

player_tables = [
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

downloader = PlayerTables(database_urls, player_tables)
downloader.create_player_json()
