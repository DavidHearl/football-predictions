import json

# Specify the path to the odds.json file
filepath = "odds.json"

# Read the contents of the JSON file
with open(filepath, "r") as file:
    data = json.load(file)

# Extract the home teams and away teams
home_teams = [match["home_team"] for match in data]
away_teams = [match["away_team"] for match in data]

for i in range(len(home_teams)):
    print(f"{home_teams[i]} vs {away_teams[i]}")    













