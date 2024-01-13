import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from urllib.parse import urljoin
import io
import time
import re
import codecs


class LegacyMatchHistory:
	def __init__(self, legacy_seasons):
		self.legacy_seasons = legacy_seasons

	# Download all the player tables from the club url
	def get_fixtures(self):
		base_url = "https://fbref.com"

		# Open the urls.json file and load the data
		with open('get_data/keys.json', 'r') as f:
			data = json.load(f)

		# Create an iterator for the club urls
		items = iter(data['club_urls'].items()) 
		
		# Skip the first item in the iterator (Skip the current season)
		next(items) 

		for season, urls in items:
			# Add a delay to prevent the server from blocking the request
			time.sleep(1)

			# Iterate through all the club urls
			for url in urls:
				club_url = urljoin(base_url, url)
				print(club_url)

				# Add a delay to prevent the server from blocking the request
				time.sleep(2)

				# Download the page and convert to HTML
				html = requests.get(club_url, timeout=20)

				# Initialize BeautifulSoup
				soup_team_list = BeautifulSoup(html.text, features="lxml")

				# Split the URL by "/"
				url_parts = club_url.split("/")
				print(url_parts)
				
				# Find the index of 'squads' in the URL
				squads_index = url_parts.index("squads")
				
				# Extract the part of the URL containing the team name
				team_name_with_hyphen = url_parts[squads_index + 3]
				print(team_name_with_hyphen)
				
				# Check if the team name ends with "Stats" and remove it
				if team_name_with_hyphen.endswith("-Stats"):
					team_name_with_hyphen = team_name_with_hyphen[:-6]  # Remove the last 6 characters ("Stats")
					print(team_name_with_hyphen)
				
				# Remove hyphens from the team name and replace with a space
				team_name = team_name_with_hyphen.replace('-', ' ')
				print(team_name)
				
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
				folder_name = os.path.join(f"raw_data/{season}/match_data", team_name)
				os.makedirs(folder_name, exist_ok=True)

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
					json_filename = os.path.join(folder_name, "Scores & Fixtures.json")
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


	def clean_fixtures(self):
		for season in self.legacy_seasons:
			# Specify the folder location to iterate through
			folder_location = f"raw_data/{season}/match_data"

			# Iterate through each folder in the specified location
			for subfolder in os.listdir(folder_location):
				# Create a variable for the 'Scores & Fixtures.json' file
				fixture_list_path = os.path.join(folder_location, subfolder, 'Scores & Fixtures.json')

				# Create a variable for the Completed Matches & Scheduled Matches
				completed_match_path = os.path.join(folder_location, subfolder, 'Completed Matches.json')		
				scheduled_match_path = os.path.join(folder_location, subfolder, 'Scheduled Matches.json')

				# Create the directory if it doesn't exist
				os.makedirs(os.path.dirname(completed_match_path), exist_ok=True)
				os.makedirs(os.path.dirname(scheduled_match_path), exist_ok=True)

				# Read the JSON data from the file
				with open(fixture_list_path, 'r') as file:
					all_match_data = json.load(file)

				# Filter the data to only include Premier League matches
				league_data = [
					match
					for match in all_match_data
					if (
						match.get("Comp") == "Premier League"  # Check if 'Comp' is 'Premier League'
					)
				]

				# Save the filtered data back to the JSON file
				with open(fixture_list_path, 'w') as file:
					json.dump(league_data, file, indent=2)

				# -----------------------------------------------------------------

				with open(fixture_list_path, 'r') as file:
					league_data = json.load(file)

				# Filter the data to only include matches that have been played
				completed_matches = [
					match
					for match in league_data
					if (
						match.get("Result") is not None
					)
				]

				# Filter the data to only include matches that have NOT been played
				scheduled_matches = [
					match
					for match in league_data
					if (
						match.get("Result") is None
					)
				]

				# Save the filtered data back to the JSON file
				with open(completed_match_path, 'w') as file:
					json.dump(completed_matches, file, indent=2)
				
				# Save the filtered data back to the JSON file
				with open(scheduled_match_path, 'w') as file:
					json.dump(scheduled_matches, file, indent=2)


	def create_match_folders(self):
		for season in self.legacy_seasons:
			location = f"raw_data/{season}/match_data"
			base_url = 'https://fbref.com'

			# Open the urls.json file and load the data
			with open('get_data/keys.json', 'r') as f:
				data = json.load(f)

			# Assign the match statistics tables to a variable
			match_statistics_tables = data['match_statistics_tables']

			# Selects each team folder within 'match_history'
			for folder in os.listdir(location):
				# Add a delay to prevent the server from blocking the request
				time.sleep(4)

				# Creates a variable for the path to each team folder
				folder_path = os.path.join(location, folder)

				# Creates a variable for the 'Completed Matches' file
				file_path = os.path.join(folder_path, 'Completed Matches.json')

				# Opens the 'Completed Matches.json' file
				with open(file_path, 'r') as file:
					data = json.load(file)

				# Selects each match within the 'completed matches.json' file
				for match in data:
					# Add a delay to prevent the server from blocking the request
					time.sleep(3)
					
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
						with requests.Session() as session:
							# Download the page and convert to HTML
							html = session.get(match_url, timeout=20)

							# Initialize BeautifulSoup
							soup_match_report = BeautifulSoup(html.text, features="lxml")

							# Find all 'div' tags with class 'score'
							goals = soup_match_report.find_all('div', {'class': 'score'})
							expected_goals = soup_match_report('div', {'class': 'score_xg'})

							# Print the contents of each 'div' tag
							goals = [goals[0].text, goals[1].text]
							expected_goals = [expected_goals[0].text, expected_goals[1].text]

							# Match Overview
							lineup_div_home = soup_match_report.find('div', {'class': 'lineup', 'id': 'a'})
							lineup_div_away = soup_match_report.find('div', {'class': 'lineup', 'id': 'b'})

							# Find all 'td' tags within the selected div
							td_tags_home = lineup_div_home.find_all('td')
							td_tags_away = lineup_div_away.find_all('td')

							home_team = []
							away_team = []

							# Find 'a' tags within each 'td' tag and print the contents
							for td in td_tags_home:
								a_tag = td.find('a')
								if a_tag is not None:
									home_team.append(a_tag.text)

							for td in td_tags_away:
								b_tag = td.find('a')
								if b_tag is not None:
									away_team.append(b_tag.text)

							team_stats_div = soup_match_report.find('div', {'id': 'team_stats_extra'})

							# Find all 'div' tags within the selected div
							div_tags = team_stats_div.find_all('div')

							# Print the contents of each 'div' tag that doesn't have a class attribute and is numeric
							numeric_values = []
							for div in div_tags:
								if not div.has_attr('class') and div.text.isdigit():
									numeric_values.append(int(div.text))

							fouls = [numeric_values[0], numeric_values[1]]
							corners = [numeric_values[2], numeric_values[3]]
							crosses = [numeric_values[4], numeric_values[5]]
							touches = [numeric_values[6], numeric_values[7]]
							tackles = [numeric_values[8], numeric_values[9]]
							interceptions = [numeric_values[10], numeric_values[11]]
							aerials_won = [numeric_values[12], numeric_values[13]]
							clearances = [numeric_values[14], numeric_values[15]]
							offsides = [numeric_values[16], numeric_values[17]]
							goal_kicks = [numeric_values[18], numeric_values[19]]
							throw_ins = [numeric_values[20], numeric_values[21]]
							long_balls = [numeric_values[22], numeric_values[23]]
					

							# Find all 'div' tags with class 'score'
							goals = soup_match_report.find_all('div', {'class': 'score'})
							expected_goals = soup_match_report('div', {'class': 'score_xg'})

							# Print the contents of each 'div' tag
							goals = [goals[0].text, goals[1].text]
							expected_goals = [expected_goals[0].text, expected_goals[1].text]

							# Match Overview
							lineup_div_home = soup_match_report.find('div', {'class': 'lineup', 'id': 'a'})
							lineup_div_away = soup_match_report.find('div', {'class': 'lineup', 'id': 'b'})

							# Create a dictionary for the match overview data
							match_overview = {
								'goals': goals,
								'expected_goals': expected_goals,
								'home_team': home_team,
								'away_team': away_team,
								'fouls': fouls,
								'corners': corners,
								'crosses': crosses,
								'touches': touches,
								'tackles': tackles,
								'interceptions': interceptions,
								'aerials_won': aerials_won,
								'clearances': clearances,
								'offsides': offsides,
								'goal_kicks': goal_kicks,
								'throw_ins': throw_ins,
								'long_balls': long_balls
							}

							overview_path = os.path.join(match_folder_path, 'Match Overview.json')
							print(overview_path)

							# Write the match overview data to the JSON file
							with open(overview_path, 'w') as file:
								json.dump(match_overview, file, indent=4)

							tables = soup_match_report.select('table.stats_table')
							table_length = len(tables)
							print(f"Number of Tables: {table_length}")

							for i in range(8):
								# Add a delay to prevent the server from blocking the request
								time.sleep(2)

								# Selects different table set for home and away teams
								if home_away == 'Home':
									if i != 7:
										if i < table_length:
											data = tables[i]
										else:
											continue
									else:
										if 15 < table_length:
											data = tables[15]
										else:
											continue
								else:
									if i != 7:
										if i + 7 < table_length:
											data = tables[i + 7]
										else:
											continue
									else:
										if 16 < table_length:
											data = tables[16]
										else:
											continue
										
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
