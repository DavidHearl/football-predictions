"""
Create the folder structure for all the leagues, the seasons, the clubs, and the player data
"""

import os
import json
import time
from io import StringIO

import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin


class CreateStructure:
    def __init__(self, season):
        self.season = season

    def folder_structure(self):
        # Open the urls.json file and load the data
        with open('get_data/keys.json', 'r') as f:
            data = json.load(f)

        # Create folder structure for each league and season
        # raw_data
        # ├── championship
        # │   ├── 2019-2020
        # │   │   ├── match_data
        for league in data['leagues']:
            for folder in data['folders']:
                os.makedirs(f"raw_data/{league}/{self.season}/{folder}", exist_ok=True)
        
        # Get the name of the overall statistics folder
        overall_statistics_table = "Regular Season - Overall"

        for league, url in zip(data['leagues'], data['overall_urls']):
            # Download the page and convert to HTML
            html = requests.get(url, timeout=20)

            # Initialize BeautifulSoup
            soup_team_list = BeautifulSoup(html.text, features="lxml")

            # Find the first table with class 'stats_table'
            table = soup_team_list.find('table', attrs={"class": "stats_table"})

            # Find all elements with data-stat property equal to 'team' within the first table
            team_elements = table.find_all('td', attrs={"data-stat": "team"})

            # Create an array to store the href values
            href_values = []

            # Iterate over the team elements and extract the href values
            for team_element in team_elements:
                href = team_element.find('a')['href']
                href_values.append(href)

            # Add the base URL to the href values
            base_url = "https://fbref.com"

            # Append the href values to the corresponding league and season
            if 'club_urls' not in data:
                data['club_urls'] = {}

            # Check if 'league' is in data['club_urls']
            if 'league' not in data['club_urls']:
                data['club_urls'][league] = {}

            # Check if 'season' is in data['club_urls']['league']
            if 'season' not in data['club_urls'][league]:
                data['club_urls'][league][self.season] = []

            # Reset the list
            data['club_urls'][league][self.season] = []

            # Iterate over the href values and add the base URL
            for url in href_values:
                merged_url = urljoin(base_url, url)
                # Append the href values to the corresponding league and season
                data['club_urls'][league][self.season].append([merged_url, ''])


        # Save the updated data back to the keys.json file
        with open('get_data/keys.json', 'w') as f:
            json.dump(data, f, indent=4)

        # Create a folder for each team within their respective league
        for league in data['club_urls']:
            for item in data['club_urls'][league][self.season]:
                # Check if the item is a list with at least one element
                if isinstance(item, list) and len(item) > 0:
                    url = item[0]
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

                # Append the href values to the corresponding league and season
                item[1] = team_name

                # Save the updated data back to the keys.json file
                with open('get_data/keys.json', 'w') as f:
                    json.dump(data, f, indent=4)

                # Create a new folder for each team
                folder_name = os.path.join(f"raw_data/{league}/{self.season}/player_data", team_name)
                os.makedirs(folder_name, exist_ok=True)

                # Create a new folder for each team
                folder_name = os.path.join(f"raw_data/{league}/{self.season}/match_data", team_name)
                os.makedirs(folder_name, exist_ok=True)
