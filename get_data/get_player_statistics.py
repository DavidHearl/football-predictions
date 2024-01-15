import os
import json
import time
import io

import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class PlayerStatistics:
	def __init__(self, season):
		self.season = season

	# Download all the player tables from the club url
	def get_player_data(self):
		# Open the urls.json file and load the data
		with open('get_data/keys.json', 'r') as f:
			data = json.load(f)

		# Print a blank line to separate the output
		print()

		# Assign the player statistics tables to a variable
		player_statistics_tables = data['player_statistics_tables']
		base_url = "https://fbref.com"

		for league in data['leagues']:
			print(league)
			if league not in data['club_urls']:
				print(f"The league '{league}' is not present in 'club_urls'. Skipping...")
				continue

			for season in data['club_urls'][league]:
				base_folder = f"raw_data/{league}/{self.season}/player_data/"
				subfolders = sorted([f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))])
				urls = sorted(data['club_urls'][league][self.season])

				for subfolder, url in zip(subfolders, urls):
					# Create the folder name
					folder_name = os.path.join(base_folder, subfolder)

					# Create the url
					club_url = urljoin(base_url, url)

					# Add a delay to try again if the request fails
					while True:
						try:
							# Download the page and convert to HTML
							html = requests.get(club_url, timeout=20)
							break
						except requests.exceptions.Timeout:
							time.sleep(900) # Wait 15 minutes before trying again
							print("Timeout occurred. Trying again in 15 minutes...")
							print("Current Time:", time.strftime("%H:%M:%S", time.localtime()))

					# Initialize BeautifulSoup
					soup_team_list = BeautifulSoup(html.text, features="lxml")
					
					# Iterate through the player tables
					for i in range(len(player_statistics_tables)):
						# Sleep for half a second to avoid overloading the server
						time.sleep(1)

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
