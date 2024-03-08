"""
Main program to run the model and generate a prediction.
"""
import json

class Run:
	def __init__(self):
		pass

	def simplify():
		# Open the odds.json file
		with open('odds.json', 'r') as file:
			odds_json = json.load(file)

		# Get the home team
		home_team = odds_json[0]['home_team']

		print(home_team)  # Prints: Arsenal
