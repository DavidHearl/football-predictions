def create_match_folders(self):
		print("-------------------------------------------")
		print("---------- Creating match folders ---------")
		print("-------------------------------------------\n")

		base_url = 'https://fbref.com'

		# Open the urls.json file and load the data
		with open('get_data/keys.json', 'r') as f:
			data = json.load(f)

		# Assign the match statistics tables to a variable
		match_statistics_tables = data['match_statistics_tables']

		# Assign the club urls to a variable
		club_urls = data['club_urls']

		# Match Counter
		match_count = 0

    # Create a counter to track progress
    folder_counts = {}
    for league in club_urls:
        for season in self.legacy_seasons:
            location = f"raw_data/{league}/{season}/match_data"
            folder_counts[(league, season)] = sum(os.path.isdir(os.path.join(location, entry.name)) for entry in os.scandir(location))
            match_count += folder_counts[(league, season)] * ((folder_counts[(league, season)] - 1)*2)

    current_count = 0

		for league in club_urls:
			for season in self.legacy_seasons:
				location = f"raw_data/{league}/{season}/match_data"

				for folder in os.listdir(location):
					# Create the folder path
					folder_path = os.path.join(location, folder)

					# Create the directory if it doesn't exist
					file_path = os.path.join(folder_path, 'Completed Matches.json')

					with open(file_path, 'r') as file:
						data = json.load(file)

					for match in data:
						current_count += 1

						opponent = match.get('Opponent', '')
						home_away = match.get('Venue', '')
						url = match.get('Match Report', '')
						suspended = match.get('Notes', '')

						match_folder_name = f"{folder} vs {opponent} - {home_away}"
						match_folder_path = os.path.join(folder_path, match_folder_name)

						# Create the directory if it doesn't exist
						os.makedirs(match_folder_path, exist_ok=True)

						match_url = urljoin(base_url, url)
						
						# Print the current count and the total number of matches
						percentage = round((current_count / match_count) * 100, 4)
						time_remaining = round(((match_count - current_count) * 4) / 60)
						print(f"Match {current_count} / {match_count} : Percentage: {percentage} % ETA: {time_remaining} minutes")

						if suspended != 'Match Suspended':
							# Add a delay to stop the server from blocking the request
							random_number = round(random.uniform(3, 5), 1)
							print(f"Current Time: {time.strftime('%H:%M:%S', time.localtime())}, Waiting {random_number} seconds...")
							print(f"Creating Match Report for {folder} vs {opponent} - {home_away} in {league}, {season} season\nUrl: {match_url}")
							print(f"Folder Path: {match_folder_path}")
							time.sleep(random_number)

							while True:
								try:
									# Download the page and convert to HTML
									html = requests.get(match_url, timeout=20)
									break
								except requests.exceptions.Timeout:
									print("Timeout occurred. Trying again in 15 minutes...")
									print("Current Time:", time.strftime("%H:%M:%S", time.localtime()))
									time.sleep(900) # Wait 15 minutes before trying again

							# Initialize BeautifulSoup
							soup_match_report = BeautifulSoup(html.text, features="lxml")

							# Find all 'div' tags with class 'score'
							goals = soup_match_report.find_all('div', {'class': 'score'})
							expected_goals = soup_match_report('div', {'class': 'score_xg'})

							try:
								goals = [goals[0].text, goals[1].text]
								expected_goals = [expected_goals[0].text, expected_goals[1].text]
							except IndexError:
								print(soup_match_report)
								while True:
									try:
										# Download the page and convert to HTML
										html = requests.get(match_url, timeout=20)
										break
									except requests.exceptions.Timeout:
										print("Timeout occurred. Trying again in 15 minutes...")
										print("Current Time:", time.strftime("%H:%M:%S", time.localtime()))
										time.sleep(900) # Wait 15 minutes before trying again

										# Initialize BeautifulSoup
										soup_match_report = BeautifulSoup(html.text, features="lxml")

										# Find all 'div' tags with class 'score'
										goals = soup_match_report.find_all('div', {'class': 'score'})
										expected_goals = soup_match_report('div', {'class': 'score_xg'})

							while True:
								try:
									# Match Overview
									lineup_div_home = soup_match_report.find('div', {'class': 'lineup', 'id': 'a'})
									lineup_div_away = soup_match_report.find('div', {'class': 'lineup', 'id': 'b'})

									# Ensure lineup_div_home is not None before calling find_all
									if lineup_div_home is not None:
										td_tags_home = lineup_div_home.find_all('td')
									else:
										td_tags_home = []

									# Ensure lineup_div_away is not None before calling find_all
									if lineup_div_away is not None:
										td_tags_away = lineup_div_away.find_all('td')
									else:
										td_tags_away = []

									home_team = []
									away_team = []

									# Find 'a' tags within each 'td' tag and print the contents
									for td in td_tags_home:
										a_tag = td.find('a')
										if a_tag is not None:
											home_team.append(a_tag.text)

									for td in td_tags_away:
										b_tag = td.find('a')
										if b_tag is not None:
											away_team.append(b_tag.text)

									team_stats_div = soup_match_report.find('div', {'id': 'team_stats_extra'})

									# Find all 'div' tags within the selected div
									div_tags = team_stats_div.find_all('div')

									# Print the contents of each 'div' tag that doesn't have a class attribute and is numeric
									numeric_values = []
									for div in div_tags:
										if not div.has_attr('class') and div.text.isdigit():
											numeric_values.append(int(div.text))

									fouls = [numeric_values[0], numeric_values[1]]
									corners = [numeric_values[2], numeric_values[3]]
									crosses = [numeric_values[4], numeric_values[5]]
									touches = [numeric_values[6], numeric_values[7]]
									tackles = [numeric_values[8], numeric_values[9]]
									interceptions = [numeric_values[10], numeric_values[11]]
									aerials_won = [numeric_values[12], numeric_values[13]]
									clearances = [numeric_values[14], numeric_values[15]]
									offsides = [numeric_values[16], numeric_values[17]]
									goal_kicks = [numeric_values[18], numeric_values[19]]
									throw_ins = [numeric_values[20], numeric_values[21]]
									long_balls = [numeric_values[22], numeric_values[23]]
							

									# Find all 'div' tags with class 'score'
									goals = soup_match_report.find_all('div', {'class': 'score'})
									expected_goals = soup_match_report('div', {'class': 'score_xg'})

									# Print the contents of each 'div' tag
									goals = [goals[0].text, goals[1].text]
									expected_goals = [expected_goals[0].text, expected_goals[1].text]

									# Match Overview
									lineup_div_home = soup_match_report.find('div', {'class': 'lineup', 'id': 'a'})
									lineup_div_away = soup_match_report.find('div', {'class': 'lineup', 'id': 'b'})

									# Create a dictionary for the match overview data
									match_overview = {
										'goals': goals,
										'expected_goals': expected_goals,
										'home_team': home_team,
										'away_team': away_team,
										'fouls': fouls,
										'corners': corners,
										'crosses': crosses,
										'touches': touches,
										'tackles': tackles,
										'interceptions': interceptions,
										'aerials_won': aerials_won,
										'clearances': clearances,
										'offsides': offsides,
										'goal_kicks': goal_kicks,
										'throw_ins': throw_ins,
										'long_balls': long_balls
									}

									overview_path = os.path.join(match_folder_path, 'Match Overview.json')

									# Write the match overview data to the JSON file
									with open(overview_path, 'w') as file:
										json.dump(match_overview, file, indent=4)

									tables = soup_match_report.select('table.stats_table')
									table_length = len(tables)
									print(overview_path)

									for i in range(8):
										# Selects different table set for home and away teams
										if home_away == 'Home':
											if i != 7:
												if i < table_length:
													data = tables[i]
												else:
													continue
											else:
												if 15 < table_length:
													data = tables[15]
												else:
													continue
										else:
											if i != 7:
												if i + 7 < table_length:
													data = tables[i + 7]
												else:
													continue
											else:
												if 16 < table_length:
													data = tables[16]
												else:
													continue
												
										# Read the table using Pandas
										table = pd.read_html(io.StringIO(str(data)))[0]

										# Create a .JSON file using the strings from player table
										json_filename = os.path.join(match_folder_path, f"{match_statistics_tables[i]}.json")
										print(json_filename)

										# Open each .JSON file and convert tables to json data
										try:
											with open(json_filename, "w") as json_file:
												json.dump(json.loads(table.to_json(orient="records")), json_file, indent=4)
										except Exception as e:
											print(f"Error: {e}")
										except requests.exceptions.HTTPError as e:
											print(f"HTTP Error: {e}")
									else:
										print(f"Match Suspended, data skipped.")
									
									print()
								except Exception as e:
									print(f"An error occurred waiting 5 Minutes: {e}")
									time.sleep(300)


							
