import os
import json
import requests
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup


class GetOdds:
	def __init__(self):
		self.base_url = "https://www.betexplorer.com/football/england/premier-league/fixtures"
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
					'teams': f"{subfolder} - {opponent}",
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
		html = requests.get(self.base_url, timeout=20)

		# Initialize BeautifulSoup
		soup_team_list = BeautifulSoup(html.text, features="lxml")

		# Find the <a> tag with the class "in-match"
		in_match_tag = soup_team_list.find('a', class_='in-match')

		# Get the values from the 2 spans
		if in_match_tag:
			spans = in_match_tag.find_all('span')
			if len(spans) >= 2:
				value1 = spans[0].text
				value2 = spans[1].text
				print(value1, value2)
			else:
				print("Not enough spans found.")
		else:
			print("No <a> tag with class 'in-match' found.")

		# Save soup_team_list to an HTML file
		with open("soup_team_list.html", "w") as file:
			file.write(soup_team_list.prettify())

		# Find all the button elements with the data-odd attribute
		buttons = soup_team_list.find_all('button', attrs={'data-odd': True})

		# Extract the values of the data-odd attribute
		odds_values = [button['data-odd'] for button in buttons]

		# Print the odds values
		for odd_value in odds_values:
			print(odd_value)


# Instantiate the GetOdds class
odds = GetOdds()
odds.get_odds()
