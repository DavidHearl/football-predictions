""" Scrapes data from fbref.com """
import requests
from bs4 import BeautifulSoup


def get_team_links():
    """ Gets league table """
    # Website URL Variable
    standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

    # Download HMTL Data
    data = requests.get(standings_url)

    soup = BeautifulSoup(data.text, "html.parser")

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


get_team_links()
