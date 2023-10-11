""" Scrapes data from fbref.com """
import os
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


# URLs to be scraped for data
database_url = "https://fbref.com/en/comps/9/Premier-League-Stats"


def scrape_and_save_league_table():
    """ Scrape and save the league table data """
    try:
        # Download HTML data from the specified URL
        html_data = requests.get(database_url)

        # Check if the request was successful
        if html_data.status_code == 200:
            # Wrap the HTML content in a StringIO object
            html_io = StringIO(html_data.text)

            # Use pd.read_html to extract tables from the HTML
            matches = pd.read_html(html_io, match="Regular season Table")

            # Check if matches contains at least two tables
            if len(matches) >= 2:
                # Extract data from matches[0] (e.g., league table)
                data_0 = matches[0]

                # Create a folder for each "Squad" in the "json" directory
                squad_folders = set(data_0["Squad"])
                for squad_name in squad_folders:
                    squad_folder = os.path.join("json", squad_name)
                    os.makedirs(squad_folder, exist_ok=True)

                    # Create an empty "Players" folder within each team folder
                    players_folder = os.path.join(squad_folder, "Players")
                    os.makedirs(players_folder, exist_ok=True)

                # Extract data from matches[1] (e.g., home and away stats)
                data_1 = matches[1]

                # Convert the data to JSON objects with indentation
                json_data_0 = data_0.to_json(orient='records', indent=4)
                json_data_1 = data_1.to_json(orient='records', indent=4)

                # Save the JSON data for league table and home/away in the "json" folder
                file_path_0 = os.path.join("json", "league_table.json")
                file_path_1 = os.path.join("json", "home_away.json")

                with open(file_path_0, "w") as json_file_0:
                    json_file_0.write(json_data_0)

                with open(file_path_1, "w") as json_file_1:
                    json_file_1.write(json_data_1)

                print(f'JSON data for league table has been saved to {file_path_0}')
                print(f'JSON data for home/away stats has been saved to {file_path_1}')
            else:
                print("Error: Unable to find necessary tables in the HTML data.")
        else:
            print(f"Error: Failed to retrieve data from {database_url}. Status code: {html_data.status_code}")
    except Exception as e:
        print(f"Error: {str(e)}")


def get_team_scores():
    """ Gets team links from table and fetches data for each team """
    # Downloads data from HTML
    html_data = requests.get(database_url)

    # Initialise soup
    soup = BeautifulSoup(html_data.text, "html.parser")

    # Parse the first table
    standings_table = soup.select('table.stats_table')[0]

    # Find all 'a' tags
    links = standings_table.find_all('a')

    # Loop through 'a' tags and fetch data for each team
    for link in links:
        try:
            # Get the content of the <a> tag (e.g., "Tottenham")
            team_name = link.get_text()
            # Get the href attribute (e.g., "/en/squads/361ca564/Tottenham-Hotspur-Stats")
            href = link.get("href")

            # Check if the href contains '/squads/'
            if '/squads/' in href:
                # Construct the full team URL
                team_url = f"https://fbref.com{href}"

                team_data = requests.get(team_url)
                html_io = StringIO(team_data.text)

                # Use pd.read_html with the StringIO object
                matches = pd.read_html(html_io, match="Scores & Fixtures")

                # Extract data from the "Scores & Fixtures" table
                scores_and_fixtures = matches[0]

                # Create a folder for the team in the "json" directory
                team_folder = os.path.join("json", team_name)
                os.makedirs(team_folder, exist_ok=True)

                # Save the "Scores & Fixtures" data for the team as a JSON file
                json_data = scores_and_fixtures.to_json(orient='records', indent=4)
                file_path = os.path.join(team_folder, "scores_and_fixtures.json")

                with open(file_path, "w") as json_file:
                    json_file.write(json_data)

                print(f'Scores and Fixtures data for {team_name} has been saved to {file_path}')
        except Exception as e:
            print(f"Error fetching data for {team_name}: {str(e)}")


# Call the function to scrape and save the data
scrape_and_save_league_table()

# Call the function to pull teams scores and fixtures.
get_team_scores()
