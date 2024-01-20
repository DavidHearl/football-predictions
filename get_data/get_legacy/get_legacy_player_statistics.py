import os
import json
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import io


# The server will block the request if frequency exceeds 1 request per 3 seconds (20 requests per minute)
# Therefore, we need to add a delay to prevent the server from blocking the request, use 4 seconds for safety.
class LegacyPlayerStatistics:
	def __init__(self, legacy_seasons):
		self.legacy_seasons = legacy_seasons

	# Download all the player tables from the club url
	def get_player_data(self):
		print("Getting player data...")

		# Open the urls.json file and load the data
		with open('get_data/keys.json', 'r') as f:
			data = json.load(f)

		# Print a blank line to separate the output
		print()

		# Assign the player statistics tables to a variable
		player_statistics_tables = data['player_statistics_tables']

		# Assign the club urls to a variable
		club_urls = data['club_urls']

		for league in club_urls:
			for season in self.legacy_seasons:
				for item in club_urls[league][season]:
					# Add a delay to stop the server from blocking the request
					time.sleep(4)
					
					# Add a delay to try again if the request fails
					while True:
						try:
							# Download the page and convert to HTML
							html = requests.get(item[0], timeout=20)
							break
						except requests.exceptions.Timeout:
							time.sleep(900) # Wait 15 minutes before trying again
							print("Timeout occurred. Trying again in 15 minutes...")
							print("Current Time:", time.strftime("%H:%M:%S", time.localtime()))

						# Create a new folder for each team
						folder_name = os.path.join(f"raw_data/{league}/{season}/player_data", item[1])
						os.makedirs(folder_name, exist_ok=True)		
						print(folder_name)

						# Iterate through the player tables
						for i in range(len(player_statistics_tables)):
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
