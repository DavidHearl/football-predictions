""" Scrapes squad specific data"""
import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


# URL to scrape
DATABASE_URL = "https://fbref.com/en/comps/9/Premier-League-Stats"


class TeamStatScraper:
	def __init__(self, database_url):
		self.database_url = database_url
		self.team_list = []
		self.team_urls = []

	def create_team_list(self):
		html = requests.get(self.database_url, timeout=20)
		home_page = StringIO(html.text)

		# Initialize BeautifulSoup
		soup_team_list = BeautifulSoup(home_page, features="lxml")

		# Find the Regular Season - Overall Table
		regular_season_overall = soup_team_list.select('table.stats_table')[0]

		teams = regular_season_overall.find_all('a', href=True)

		self.team_list = {team.text: [] for team in teams if 'squads' in team['href']}

		# Print the list of team names
		print(list(self.team_list.keys()))

	def create_links_to_team_page(self):
		html = requests.get(self.database_url, timeout=20)
		home_page = StringIO(html.text)

		# Initialize BeautifulSoup
		soup_team_links = BeautifulSoup(home_page, features="lxml")

		# Find the Regular Season - Overall Table
		regular_season_overall = soup_team_links.select('table.stats_table')[0]

		# Find all <a> tags within the table
		all_a_tags = regular_season_overall.find_all('a')

		# Extract the "href" attributes from the <a> tags
		all_href_attributes = [tag.get("href") for tag in all_a_tags]

		# Filter the href attributes to keep only those containing '/squads/'
		filtered_href_attributes = [href for href in all_href_attributes if '/squads/' in href]

		# Create full team URLs by appending the base URL
		self.team_urls = [f"https://fbref.com{link}" for link in filtered_href_attributes]

		# Print the list of team URLs
		print(self.team_urls)

	def create_player_list(self):
		for team_name in self.team_list.keys():
			html = requests.get(self.team_urls[list(self.team_list.keys()).index(team_name)], timeout=20)
			team_page = StringIO(html.text)

			soup = BeautifulSoup(team_page, features="lxml")
			standard_stats = soup.select('table.stats_table')[0]

			players = standard_stats.find_all('a', href=True)

			for player in players:
				player_href = player['href']

				# Check if the link contains 'players/' and does not contain 'summary'
				if '/players/' in player_href and 'summary' not in player_href:
					player_name = player.text
					self.team_list[team_name].append(player_name)

		# Print the team_list dictionary
		for team, players in self.team_list.items():
			print(f"{team}: {players}")

		self.create_folders_for_teams_and_players(self.team_list)

	def create_folders_for_teams_and_players(self, team_data):
		for team_name in team_data:
			# Create a directory for the team if it doesn't exist
			team_folder = os.path.join('teams', team_name)
			os.makedirs(team_folder, exist_ok=True)

			for player in team_data[team_name]:
				# Create a directory for the player within the team folder
				player_folder = os.path.join(team_folder, player)
				os.makedirs(player_folder, exist_ok=True)

				# Create a JSON file for each player
				player_data = {}  # Add player data here if needed
				json_file_path = os.path.join(player_folder, 'player_data.json')

				with open(json_file_path, 'w') as json_file:
					json.dump(player_data, json_file, indent=4)

		# Create a JSON file for each team
		self.save_team_data_to_json(team_data)

	def save_team_data_to_json(self, team_data):
		for team_name in team_data:
			team_folder = os.path.join('teams', team_name)
			json_file_path = os.path.join(team_folder, 'team_data.json')

			with open(json_file_path, 'w') as json_file:
				json.dump(team_data[team_name], json_file, indent=4)
				
	def add_data_to_team_json(self):
		# Get database url
		html = requests.get(self.database_url, timeout=20)
		home_page = StringIO(html.text)

		# Initialize BeautifulSoup
		soup_team_list = BeautifulSoup(home_page, features="lxml")

		# Find the Regular Season - Overall Table
		regular_season_overall = soup_team_list.select('table.stats_table')[0]

		# Variable names and their corresponding data-stat values
		variable_names = {
			"matches_played": "games",
			"matches_won": "wins",
			"matches_drawn": "ties",
			"matches_lost": "losses",
			"goals_for": "goals_for",
			"goals_against": "goals_against",
			"goal_difference" : "goal_diff",
			"points" : "points",
			"points_per_match" : "points_avg",
			"expected_goals" : "xg_for",
			"expected_goals_against" : "xg_against",
			"expected_goal_difference" : "xg_diff",
			"expected_goal_difference_per_90" : "xg_diff_per90",
			"stadium_attendance" : "attendance_per_g"
		}

		# Dictionary to store the results
		values = {}

		# Iterate through the variable names and data-stat values
		for variable_name, data_stat in variable_names.items():
			element = regular_season_overall.find("td", {"data-stat": data_stat})
			if element:
				values[variable_name] = element.get_text(strip=True)
			else:
				values[variable_name] = None

		print(values)

scraper = TeamStatScraper(DATABASE_URL)
# scraper.create_team_list()
# scraper.create_links_to_team_page()
# scraper.create_player_list()
scraper.add_data_to_team_json()