import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from urllib.parse import urljoin
import io
import time

class MatchHistory:
	def __init__(self, match_history_table):
		self.match_history_table = match_history_table

	# Download all the player tables from the club url
	def get_fixtures(self):
		i = 0

		# Open the urls.json file and load the data
		with open('get_data/keys.json', 'r') as f:
			data = json.load(f)

		# Assign the club_urls to a variable
		club_urls = data['club_urls']

		# Iterate through all the club urls
		for url in club_urls:
			# Download the page and convert to HTML
			html = requests.get(url, timeout=20)
			home_page = StringIO(html.text)

			# Initialize BeautifulSoup
			soup_team_list = BeautifulSoup(home_page, features="lxml")

			# -----------------------------------------------------------------
			# Get the team name and create a folder for each team
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
			folder_name = os.path.join("raw_data/2023-2024/match_data", team_name)
			os.makedirs(folder_name, exist_ok=True)		

			# -----------------------------------------------------------------

			# Iterate through the 'stats table'
			# 'stats table' is the class of the table element
			data = soup_team_list.select('table.stats_table')[1]

			# Read the table using Pandas
			table_data = pd.read_html(io.StringIO(str(data)))[0]

			# Extract content from 'td' elements in the 17th column
			td_17_content = [td.contents[0] if td.contents else None for td in data.select('td:nth-of-type(17)')]

			# Generate href_values based on the content of 'td' elements
			href_values = []
			for content in td_17_content:
				if content and content.name == 'a' and 'href' in content.attrs:
					href_values.append(content['href'])
				else:
					href_values.append("Match Postponed")

			# Ensure the lengths match
			if len(href_values) == len(table_data):
				# Replace the "Match Report" values with href values
				table_data["Match Report"] = href_values

				# Create a .JSON file using the strings from player table
				json_filename = os.path.join("raw_data/2023-2024/match_data", team_name, "Scores & Fixtures.json")
				print(json_filename)

				# Create the directory if it doesn't exist
				os.makedirs(os.path.dirname(json_filename), exist_ok=True)

				# Open each .JSON file and convert tables to JSON data
				try:
					with open(json_filename, "w") as json_file:
						json.dump(json.loads(table_data.to_json(orient="records")), json_file, indent=4)
				except Exception as e:
					print(f"Error while writing JSON file: {e}")
			else:
				print("Error: Length mismatch between href_values and table_data")
				print(f"Length of href_values: {len(href_values)}")
				print(f"Number of rows in table_data: {len(table_data)}")


	def remove_extra_data(self):
		# Specify the folder location to iterate through
		folder_location = "raw_data/2023-2024/match_data"

		# Iterate through each folder in the specified location
		for subfolder in os.listdir(folder_location):
			file_path = os.path.join(folder_location, subfolder, 'Scores & Fixtures.json')

			# Read the JSON data from the file
			with open(file_path, 'r') as file:
				all_match_data = json.load(file)

			filtered_data = [
				match
				for match in all_match_data
				if (
					match.get("Comp") == "Premier League"  # Check if 'Comp' is 'Premier League'
					and match.get("Referee") is not None   # Check if 'Referee' is not null
				)
			]

			# Save the filtered data back to the JSON file
			with open(file_path, 'w') as file:
				json.dump(filtered_data, file, indent=2)


	def create_match_folders(self):
		location = "raw_data/2023-2024/match_data"
		base_url = 'https://fbref.com'

		# Open the urls.json file and load the data
		with open('get_data/keys.json', 'r') as f:
			data = json.load(f)

		# Assign the club_urls to a variable
		match_statistics_tables = data['match_statistics_tables']

		# Selects each team folder within 'match_history'
		for folder in os.listdir(location):
			# Creates a variable for the path to each team folder
			folder_path = os.path.join(location, folder)

			# Creates a variable for the 'Scores & Fixtures.json' file
			file_path = os.path.join(folder_path, 'Scores & Fixtures.json')

			# Opens the 'Scores & Fixtures.json' file
			with open(file_path, 'r') as file:
				data = json.load(file)

			# Selects each match within the 'Scores & Fixtures.json' file
			for match in data:
				time.sleep(1)
				# Creates variables for each column in the JSON file
				opponent = match.get('Opponent', '')
				home_away = match.get('Venue', '')
				url = match.get('Match Report', '')
				suspended = match.get('Notes', '')

				# Create a subfolder for each match
				match_folder_name = f"{folder} vs {opponent} - {home_away}"
				match_folder_path = os.path.join(folder_path, match_folder_name)

				# Create the directory if it doesn't exist
				os.makedirs(match_folder_path, exist_ok=True)

				# Create the URL for each match
				match_url = urljoin(base_url, url)
				print(match_url)

				# -----------------------------------------------------------------
				# Download the match report
				# -----------------------------------------------------------------

				if suspended != 'Match Suspended':
					# Download the page and convert to HTML
					html = requests.get(match_url, timeout=20)
					match_page = StringIO(html.text)

					# Initialize BeautifulSoup
					soup_match_report = BeautifulSoup(match_page, features="lxml")

					for i in range(8):
						# Add a delay to prevent the server from blocking the request
						time.sleep(0.5)

						# Selects different table set for home and away teams
						if home_away == 'Home':
							if i != 7:
								data = soup_match_report.select('table.stats_table')[i]
							else:
								data = soup_match_report.select('table.stats_table')[15]
						else:
							if i != 7:
								data = soup_match_report.select('table.stats_table')[i + 7]
							else:
								data = soup_match_report.select('table.stats_table')[16]
								

						# Read the table using Pandas
						table = pd.read_html(io.StringIO(str(data)))[0]

						# Create a .JSON file using the strings from player table
						json_filename = os.path.join(match_folder_path, f"{match_statistics_tables[i]}.json")
						print(json_filename)

						# Open each .JSON file and convert tables to json data
						try:
							with open(json_filename, "w") as json_file:
								json.dump(json.loads(table.to_json(orient="records")), json_file, indent=4)
						except Exception as e:
							print(f"Error: {e}")
				else:
					print(f"Match Suspended, data skipped.")

				# Add some spacing between each match
				print()
