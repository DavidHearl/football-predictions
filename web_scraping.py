""" Scrapes data from fbref.com """
import json
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

    # Wrap the HTML content in a StringIO object
    html_io = StringIO(html_data.text)

    # Use pd.read_html with the StringIO object
    matches = pd.read_html(html_io, match="Regular season Table")

    # Extract data from matches[0]
    data_0 = matches[0]

    # Convert the data to a JSON object with indentation
    json_data_0 = data_0.to_json(orient='records', indent=4)

    # Save the JSON data from matches[0] to a file
    file_path_0 = "./json/league_table.json"
    with open(file_path_0, "w") as json_file_0:
        json_file_0.write(json_data_0)

    print(f'JSON data from matches[0] has been saved to {file_path_0}')

    # Extract data from matches[1]
    data_1 = matches[1]

    # Convert the data to a JSON object with indentation
    json_data_1 = data_1.to_json(orient='records', indent=4)

    # Save the JSON data from matches[1] to a file
    file_path_1 = "./json/home_away.json"
    with open(file_path_1, "w") as json_file_1:
        json_file_1.write(json_data_1)

    print(f'JSON data from matches[1] has been saved to {file_path_1}')


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
