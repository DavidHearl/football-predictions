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
        self.team_list = {}  # Initialize an empty dictionary to store team names and player lists
        self.team_urls = []

    def create_team_list(self):
        html = requests.get(self.database_url, timeout=10)
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
        html = requests.get(self.database_url, timeout=10)
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
            html = requests.get(self.team_urls[list(self.team_list.keys()).index(team_name)], timeout=10)
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



scraper = TeamStatScraper(DATABASE_URL)
scraper.create_team_list()
scraper.create_links_to_team_page()
scraper.create_player_list()



# Tables

# Regular Season - Overall
# Regular Season - Home/Away
# Squad Standard Stats - Squad Stats
# Squad Standard Stats - Opponent Stats
# Squad Goalkeeping - Squad Stats
# Squad Goalkeeping - Opponent Stats
# Squad Advanced Goalkeeping - Squad Stats
# Squad Advanced Goalkeeping - Opponent Stats
# Squad Shooting - Squad Stats
# Squad Shooting - Opponent Stats
# Squad Passing - Squad Stats
# Squad Passing - Opponent Stats
# Squad Pass Types - Squad Stats
# Squad Pass Types - Opponent Stats
# Squad Goal and Shot Creation - Squad Stats
# Squad Goal and Shot Creation - Opponent Stats
# Squad Defencive Actions - Squad Stats
# Squad Defencive Actions - Opponent Stats
# Squad Possession - Squad Stats
# Squad Possession - Opponent Stats
# Squad Playing Time - Squad Stats
# Squad Playing Time - Opponent Stats
# Squad Miscellaneous Stats - Squad Stats
# Squad Miscellaneous Stats - Opponent Stats
