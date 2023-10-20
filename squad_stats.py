""" Scrapes squad specific data"""
import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


# URL to scrape
database_url = "https://fbref.com/en/comps/9/Premier-League-Stats"


class TeamStatScraper:
    def __init__(self, database_url):
        self.database_url = database_url
        self.html_string = self.download_page()

    def download_page(self):
        try:
            html = requests.get(database_url)
            if html.status_code == 200:
                html_string = StringIO(html.text)
                return html_string
            elif html.status_code == 429:
                print(f"Error: Too many requests. Status code: {html.status_code}")
            else:
                print(f"Error: Failed to retrieve data from {database_url}. Status code: {html.status_code}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def create_team_folders(self):
        league_table = pd.read_html(html_string, match="Regular season Table")

        regular_season_overall = league_table[0]
        team_folders = set(regular_season_overall["Squad"])
        for team_name in team_folders:
            team_folder = os.path.join("json", team_name)
            os.makedirs(team_folder, exist_ok=True)


scraper = TeamStatScraper(database_url)
scraper.create_team_folders()

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
