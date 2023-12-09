""" Downloads and Saves all tables locally """
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

	# Create a folder for each team
	def create_team_folders(self):
		# Load Regular Season - Overall.json
		league_table = "raw_data/squad_data/Regular Season - Overall.json"

		with open(league_table, "r") as json_file:
			data = json.load(json_file)

		# Extract the "Squads" from the JSON data
		teams = [entry["Squad"] for entry in data]

		for team in teams:
			# Create a new folder for each team
			folder_name = os.path.join("raw_data/teams", team)
			os.makedirs(folder_name, exist_ok=True)

		return teams

	# Download all the squad tables from the homepage
	def create_player_json(self):
		for url in self.database_urls:
			# Download the page and convert to HTML
			html = requests.get(url, timeout=20)
			home_page = StringIO(html.text)

			# Initialize BeautifulSoup
			soup_team_list = BeautifulSoup(home_page, features="lxml")

			# Extract team name from the URL
			team_name = url.split("/")[-2]

			# Create a new folder for each team
			folder_name = os.path.join("raw_data/teams", team_name, "player_data")
			os.makedirs(folder_name, exist_ok=True)

			# Iterate through the player tables
			for i in range(len(self.player_tables)):
				# Iterate through the 'stats table'
				# 'stats table' is the class of the table element
				data = soup_team_list.select('table.stats_table')[i]

				# Read the table using Pandas
				table_data = pd.read_html(str(data))[0]

				# Create a .JSON file using the strings from player table
				json_filename = os.path.join(folder_name, f"{self.player_tables[i]}.json")
				print(json_filename)

				# Open each .JSON file and convert tables to JSON data
				try:
					with open(json_filename, "w") as json_file:
						json.dump(json.loads(table_data.to_json(orient="records")), json_file, indent=4)
				except Exception as e:
					print(f"Error: {e}")


database_urls = [
	"https://fbref.com/en/squads/18bb7c10/Arsenal-Stats",
	"https://fbref.com/en/squads/8602292d/Aston-Villa-Stats",
	"https://fbref.com/en/squads/4ba7cbea/Bournemouth-Stats"
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
],

downloader = PlayerTables(database_urls, player_tables)
downloader.create_player_json()
