import os
import json
import time
from io import StringIO

import requests
import pandas as pd
from bs4 import BeautifulSoup
import json


class ClubStatistics:
	def __init__(self, season):
		self.season = season

	def create_json(self):
		# Print a blank line to separate the output
		print()

		# Open the urls.json file and load the data
		with open('get_data/keys.json', 'r') as f:
			data = json.load(f)

		# Assign the overall_statistics_url to a variable
		overall_statistics_url = data['overall_urls'][0]
		overall_statistics_tables = data['overall_tables']

		# Use a session for multiple requests
		with requests.Session() as session:
			# Download the page and convert to HTML
			html = session.get(overall_statistics_url, timeout=20)

			# Initialize BeautifulSoup
			soup_team_list = BeautifulSoup(html.text, features="lxml")

			# Use list comprehension to iterate over the tables
			tables = [
				pd.read_html(StringIO(str(data)))[0]
				for data in soup_team_list.select('table.stats_table')
			]

			# ------------------------------------------------------------

			# Check if 'club_urls' key already exists in the data
			if 'club_urls' in data:
				club_urls = data['club_urls']
			else:
				club_urls = {}

			# Convert overall_statistics_url to a string if it is a list
			if isinstance(overall_statistics_url, list):
				overall_statistics_url = overall_statistics_url[0]

			# Add new values to club_urls only if the season is not already present
			if self.season not in club_urls:
				# Find the first table with class 'stats_table'
				first_table = soup_team_list.select_one('table.stats_table')

				# Find all elements with data-stat property equal to 'team' within the first table
				team_elements = first_table.find_all('td', attrs={"data-stat": "team"})

				# Create an array to store the href values
				href_values = []

				# Iterate over the team elements and extract the href values
				for team_element in team_elements:
					href = team_element.find('a')['href']
					href_values.append(href)

				club_urls[self.season] = href_values

			data['club_urls'] = club_urls

			# Save the updated data to the keys.json file
			with open('get_data/keys.json', 'w') as f:
				json.dump(data, f, indent=4)

			# ------------------------------------------------------------

			# Create a new folder
			folder_name = f"raw_data/{self.season}/club_data"
			os.makedirs(folder_name, exist_ok=True)
			
			# Iterate over the tables and create a .JSON file for each table
			for table_name, table in zip(overall_statistics_tables, tables):
				# Sleep for half a second to avoid overloading the server
				time.sleep(0.5)

				# Create a .JSON file using the strings from squad table
				json_filename = os.path.join(folder_name, table_name + ".json")
				print(json_filename)

				# Open each .JSON file and convert tables to json data
				try:
					with open(json_filename, "w") as json_file:
						json.dump(json.loads(table.to_json(orient="records")), json_file, indent=4)
				except (FileNotFoundError, IOError) as e:
					print(f"Error: {e}")
	
			# Print a blank line to separate the output 
			print()
