""" Scrapes data from fbref.com """
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


# URLs to be scraped for data
database_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

def get_current_table():
    """ Get the current league table """
    # Downloads data from HTML
    html_data = requests.get(database_url)

    # Initialise soup
    soup = BeautifulSoup(html_data.text, "html.parser")

    # Parse the first table
    league_table = soup.select('table.stats_table')[0]

    # Wrap the HTML content in a StringIO object
    html_io = StringIO(html_data.text)

    # Use pd.read_html with the StringIO object
    matches = pd.read_html(html_io, match="Regular season Table")

    print(matches)


def get_team_scores():
    """ Gets team links from table """
    # Downloads data from HTML
    html_data = requests.get(database_url)

    # Initialise soup
    soup = BeautifulSoup(html_data.text, "html.parser")

    # Parse the first table
    standings_table = soup.select('table.stats_table')[0]

    # Final all 'a' tags
    links = standings_table.find_all('a')

    # Final all href's within the standings table
    links = [l.get("href") for l in links]

    # Filter out 'href's which do not contain '/squads/'
    links = [l for l in links if '/squads/' in l]

    # Concatonate strings to create full links
    team_urls = [f"https://fbref.com{l}" for l in links]

    # Print the list of team urls
    for x in team_urls:
        print(x)

    print('')

    # Loop through team URLs and fetch data for each team
    for team_url in team_urls:
        team_data = requests.get(team_url)
        html_io = StringIO(team_data.text)

        # Use pd.read_html with the StringIO object
        matches = pd.read_html(html_io, match="Scores & Fixtures")
        print(matches)


get_current_table()
# get_team_scores()
