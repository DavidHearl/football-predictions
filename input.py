import json

# Read the JSON file
with open('raw_data/squad_data/Regular Season - Overall.json', 'r') as file:
    data = json.load(file)

# Create an array of teams from the json file
squads = [entry['Squad'] for entry in data]

# Print the array of squads
print()
print("--------------------------------------------------")
print("Team Selection:")
print("--------------------------------------------------")
for i, squad in enumerate(squads, start=1):
    print(f"{i}. {squad}")
print("--------------------------------------------------", end='\n')

# Create a variable to select a squad using a number
selected_squad_number = int(input("Enter the number of the home team: "))
home_team = squads[selected_squad_number - 1]  # Adjust index to 0-based

print(f"You selected: {home_team}")
print("--------------------------------------------------", end='\n')

# Create another variable to select a squad using a different number
selected_squad_number_2 = int(input("Enter the number of the away team: "))
away_team = squads[selected_squad_number_2 - 1]  # Adjust index to 0-based

print(f"You selected: {away_team}")
print("--------------------------------------------------", end='\n')

print(f"{home_team} vs {away_team}")