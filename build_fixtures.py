import os
import json
import requests
from bs4 import BeautifulSoup


class GetOdds:
	def __init__(self):
		self.base_url = ""
		self.season = "2023-2024"

	def get_odds(self):
		# -----------------------------------------------------------------
		# Create the matches
		# -----------------------------------------------------------------
		# Define folder location
		location = f"raw_data/{self.season}/match_data"

		matches = []

		for subfolder in os.listdir(location):
			# Creates a variable for the path to each team folder
			folder_path = os.path.join(location, subfolder)

			# Creates a variable for the 'Completed Matches' file
			file_path = os.path.join(folder_path, 'Scheduled Matches.json')

			# Opens the 'Completed Matches.json' file
			with open(file_path, 'r') as file:
				data = json.load(file)

			# Get the first item in the list
			first_match = data[0]

			# Find out if the match is home or away
			home_away = first_match.get('Venue', '')

			if home_away == 'Home':
				opponent = first_match.get('Opponent', '')
				date = first_match.get('Date', '')
				time = first_match.get('Time', '')
				url = first_match.get('Match Report', '')

				# Create a variable for the match
				match = {
					'teams': f"{subfolder} v {opponent}",
					'date': date,
					'time': time,
				}

				# Append the match to the list
				matches.append(match)

		# Sort the matches by date and time
		sorted_matches = sorted(matches, key=lambda x: (x['date'], x['time']))

		# Print the sorted matches
		for match in sorted_matches:
			print(match)

		# -----------------------------------------------------------------
		# Get the odds
		# -----------------------------------------------------------------
		# Download the page and convert to HTML
		# html = requests.get(self.base_url, timeout=20)

		# # Initialize BeautifulSoup
		# soup_team_list = BeautifulSoup(html.text, features="lxml")
		# print(soup_team_list)

		# # Find all elements with class "bestOddsButton_b3gzcta"
		# odds_elements = soup_team_list.find_all(class_="bestOddsButton_b3gzcta")

		# # Add the odds elements to the odds array
		# odds = []
		# for element in odds_elements:
		# 	odds.append(element.text)

		# # Print the odds
		# print(odds)


# Instantiate the GetOdds class
odds = GetOdds()
odds.get_odds()

