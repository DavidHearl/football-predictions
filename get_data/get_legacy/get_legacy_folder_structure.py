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
    def __init__(self, legacy_seasons):
        self.legacy_seasons = legacy_seasons

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
            for season in self.legacy_seasons:
                for folder in data['folders']:
                    os.makedirs(f"raw_data/{league}/{season}/{folder}", exist_ok=True)
        
        # Get the name of the overall statistics folder
        overall_statistics_table = "Regular Season - Overall"

        for league in data['leagues']:
            for season in self.legacy_seasons:
                if league == 'premier_league':
                    url = f"https://fbref.com/en/comps/9/{season}/{season}-Premier-League-Stats"
                elif league == 'championship':
                    url = f"https://fbref.com/en/comps/10/{season}/{season}-Championship-Stats"
                elif league == 'la_liga':
                    url = f"https://fbref.com/en/comps/12/{season}/{season}-La-Liga-Stats"
                elif league == 'ligue_1':
                    url = f"https://fbref.com/en/comps/13/{season}/{season}-Ligue-1-Stats"

                # Add delay to prevent server from blocking the request
                time.sleep(4)
                
                # Add a delay to try again if the request fails
                while True:
                    try:
                        # Download the page and convert to HTML
                        html = requests.get(url, timeout=20)
                        break
                    except requests.exceptions.Timeout:
                        time.sleep(900) # Wait 15 minutes before trying again
                        print("Timeout occurred. Trying again in 15 minutes...")
                        print("Current Time:", time.strftime("%H:%M:%S", time.localtime()))

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
                if league not in data['club_urls']:
                    data['club_urls'][league] = {}

                # Check if 'season' is in data['club_urls']['league']
                if season not in data['club_urls'][league]:
                    data['club_urls'][league][season] = []


                # Iterate over the href values and add the base URL
                for link in href_values:
                    merged_url = urljoin(base_url, link)
                    # Append the href values to the corresponding league and season
                    data['club_urls'][league][season].append([merged_url, ''])

                # Save the updated data back to the keys.json file
                with open('get_data/keys.json', 'w') as f:
                    json.dump(data, f, indent=4)

                for item in data['club_urls'][league][season]:
                    # Check if the item is a list with at least one element
                    if isinstance(item, list) and len(item) > 0:
                        url = item[0]
                        # Split the URL by "/"
                        url_parts = url.split("/")

                    # Find the index of 'squads' in the URL
                    squads_index = url_parts.index("squads")

                    # Extract the part of the URL containing the team name
                    team_name_with_hyphen = url_parts[squads_index + 3]
                        
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
                    folder_name = os.path.join(f"raw_data/{league}/{season}/player_data", team_name)
                    os.makedirs(folder_name, exist_ok=True)

                    # Create a new folder for each team
                    folder_name = os.path.join(f"raw_data/{league}/{season}/match_data", team_name)
                    os.makedirs(folder_name, exist_ok=True)
