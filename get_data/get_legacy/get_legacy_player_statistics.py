import os
import json
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import io
import random


# The server will block the request if frequency exceeds 1 request per 3 seconds (20 requests per minute)
# Therefore, we need to add a delay to prevent the server from blocking the request, use 4 seconds for safety.
class LegacyPlayerStatistics:
	def __init__(self, legacy_seasons):
		self.legacy_seasons = legacy_seasons

	# Download all the player tables from the club url
	def get_player_data(self):
		print("-------------------------------------------")
		print("----------- Getting player data -----------")
		print("-------------------------------------------")

		# Open the urls.json file and load the data
		with open('get_data/keys.json', 'r') as f:
			data = json.load(f)

		# Assign the player statistics tables to a variable
		player_statistics_tables = data['player_statistics_tables']

		# Assign the club urls to a variable
		club_urls = data['club_urls']

		for league in club_urls:
			for season in self.legacy_seasons:
				for item in club_urls[league][season]:
					# Initialize a counter to track progress
					team_count = 0

					# Create a counter to track progress
					for league in club_urls:
						for season in self.legacy_seasons:
							location = f"raw_data/{league}/{season}/player_data"

							# Initialize a counter
							folder_count = 0

							# Iterate over the items in the directory
							for folder in os.listdir(location):
								# Check if the item is a directory
								if os.path.isdir(os.path.join(location, folder)):
									# If it is, increment the counter
									folder_count += 1

							# Match count = number of teams * number of matches per team
							team_count += folder_count

					current_count = 0

					# Print the current count and the total number of matches
					percentage = round((current_count / team_count) * 100, 4)
					time_remaining = round(((team_count - current_count) * 4) / 60)
					print(f"\nMatch {current_count} / {team_count} : Percentage: {percentage} % ETA: {time_remaining} minutes")

					# Add a delay to stop the server from blocking the request
					random_number = round(random.uniform(3, 5), 1)
					print(f"Current Time: {time.strftime('%H:%M:%S', time.localtime())}, Waiting {random_number} seconds...")
					print(f"Getting Player data for {item[1]} in {league}, {season} season\n")
					time.sleep(random_number)
					
					# Add a delay to try again if the request fails
					while True:
						try:
							# Download the page and convert to HTML
							html = requests.get(item[0], timeout=30)
							print(item[0])
							break
						except requests.exceptions.Timeout:
							print("Timeout occurred. Trying again in 15 minutes...")
							print("Current Time:", time.strftime("%H:%M:%S", time.localtime()))
							time.sleep(900) # Wait 15 minutes before trying again

					# Use list comprehension to iterate over the tables
					try:
						# Initialize BeautifulSoup
						soup_team_list = BeautifulSoup(html.text, features="lxml")

						tables = [
							pd.read_html(io.StringIO(str(data)))[0]
							for data in soup_team_list.select('table.stats_table')
						]
					except IndexError:
						print("IndexError occurred. Trying to get the html again...")
						time.sleep(900) # Wait 15 minutes before trying again
						html = requests.get(item[0], timeout=30)

						# Initialize BeautifulSoup
						soup_team_list = BeautifulSoup(html.text, features="lxml")

					# Create a new folder for each team
					folder_name = os.path.join(f"raw_data/{league}/{season}/player_data", item[1])
					os.makedirs(folder_name, exist_ok=True)		
					print(folder_name)

					for table_name, table in zip(player_statistics_tables, tables):
						# Create a .JSON file using the strings from squad table
						json_filename = os.path.join(folder_name, table_name + ".json")
						print(json_filename)

						# Create the directory if it doesn't exist
						os.makedirs(os.path.dirname(json_filename), exist_ok=True)

						# Open each .JSON file and convert tables to JSON data
						try:
							with open(json_filename, "w") as json_file:
								json.dump(json.loads(table.to_json(orient="records")), json_file, indent=4)
						except Exception as e:
							print(f"Error: {e}")
