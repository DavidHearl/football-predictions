import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

class MatchHistory:
	def __init__(self, club_urls, match_history_table):
		self.club_urls = club_urls
		self.match_history_table = match_history_table

	# Download all the player tables from the club url
	def get_fixtures(self):
		# Iterate through all the club urls
		for url in self.club_urls:
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
			
			# Remove hyphens from the team name and replace with a space
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
			
			# Replace special cases with their new values
			for special_case, replacement in special_cases.items():
				if special_case in team_name:
					team_name = team_name.replace(special_case, replacement)

			# Create a new folder for each team
			folder_name = os.path.join("match_history", team_name)
			os.makedirs(folder_name, exist_ok=True)		

			# -----------------------------------------------------------------

			# Iterate through the 'stats table'
			# 'stats table' is the class of the table element
			data = soup_team_list.select('table.stats_table')[1]

			# Read the table using Pandas
			table_data = pd.read_html(str(data))[0]

			# Extract href values from 'a' tags in the first column
			match_report_links = data.select('td:nth-of-type(17) a[href]')
			href_values = [link['href'] for link in match_report_links]

			# Replace the "Match Report" values with href values
			table_data["Match Report"] = href_values

			# Create a .JSON file using the strings from player table
			json_filename = os.path.join("match_history", team_name, "Scores & Fixtures.json")
			print(json_filename)

			# Create the directory if it doesn't exist
			os.makedirs(os.path.dirname(json_filename), exist_ok=True)

			# Open each .JSON file and convert tables to JSON data
			try:
				with open(json_filename, "w") as json_file:
					json.dump(json.loads(table_data.to_json(orient="records")), json_file, indent=4)
			except Exception as e:
				print(f"Error: {e}")


	def remove_non_league_games(self):
		# Specify the folder location to iterate through
		location = "match_history"

		for folder in os.listdir(location):
			file_path = os.path.join(location, folder, 'Scores & Fixtures.json')

			with open(file_path, 'r') as file:
				data = json.load(file)

			# Filter out data sets where 'Comp' is not 'Premier League'
			premier_league_data = [match for match in data if match.get("Comp") == "Premier League"]

			# Save the filtered data back to the JSON file
			with open(file_path, 'w') as file:
				json.dump(premier_league_data, file, indent=2)
