import os
import json
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import io

class LegacyPlayerStatistics:
	def __init__(self, legacy_seasons):
		self.legacy_seasons = legacy_seasons

	# Download all the player tables from the club url
	def create_json(self):
		# Set the base url
		base_url = "https://fbref.com"

		# Print a blank line to separate the output
		print()

		# Open the urls.json file and load the data
		with open('get_data/keys.json', 'r') as f:
			data = json.load(f)

		# Assign the player statistics tables to a variable
		player_statistics_tables = data['player_statistics_tables']	

		# Iterate through all the legacy seasons
		for season in self.legacy_seasons:
			# Access 'club_urls' from `data`
			try:
				legacy_club_urls = data['club_urls'][season]
			except KeyError:
				print("The key 'club_urls' does not exist in the data.")

			# -----------------------------------------------------------------
			# Try below to fix the KeyError, I have no idea why it is working.
			# -----------------------------------------------------------------	
			# To resolve this, you should check the self.legacy_seasons and data['club_urls'] 
			# to ensure that for every season in self.legacy_seasons, there is a corresponding 
			# key in data['club_urls']. If some seasons are missing in data['club_urls'], 
			# you'll need to add them or handle the missing data appropriately in your code.

			# Iterate through all the club urls
			for url in legacy_club_urls:
				# Join the base_url with the club url
				club_url = urljoin(base_url, url)

				with requests.Session() as session:
					# Download the page and convert to HTML
					html = session.get(club_url, timeout=20)

					# Initialize BeautifulSoup
					soup_team_list = BeautifulSoup(html.text, features="lxml")

					# Split the URL by "/"
					url_parts = club_url.split("/")
					
					# Find the index of 'squads' in the URL
					squads_index = url_parts.index("squads")
					
					# Extract the part of the URL containing the team name
					team_name_with_hyphen = url_parts[squads_index + 3]
					
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
					
					# Replace the team name with the special case name
					team_name = special_cases.get(team_name, team_name)

					# Create a new folder for each team
					folder_name = os.path.join(f"raw_data/{season}/player_data", team_name)
					os.makedirs(folder_name, exist_ok=True)		
					print(folder_name)

					# Iterate through the player tables
					for i in range(len(player_statistics_tables)):
						# Sleep for half a second to avoid overloading the server
						time.sleep(0.5)

						# Iterate through the 'stats table'
						# 'stats table' is the class of the table element
						data = soup_team_list.select('table.stats_table')[i]

						# Read the table using Pandas
						table_data = pd.read_html(io.StringIO(str(data)))[0]

						# Create a .JSON file using the strings from player table
						json_filename = os.path.join(folder_name, f"{player_statistics_tables[i]}.json")
						print(json_filename)

						# Create the directory if it doesn't exist
						os.makedirs(os.path.dirname(json_filename), exist_ok=True)

						# Open each .JSON file and convert tables to JSON data
						try:
							with open(json_filename, "w") as json_file:
								json.dump(json.loads(table_data.to_json(orient="records")), json_file, indent=4)
						except Exception as e:
							print(f"Error: {e}")
