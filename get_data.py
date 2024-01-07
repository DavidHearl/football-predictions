import time
from functools import wraps

from get_data.get_club_statistics import ClubStatistics
from get_data.get_player_statistics import PlayerStatistics
from get_data.get_match_history import MatchHistory

# ClubStatistics
overall_statistics_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

overall_statistics_tables = [
	"Regular Season - Overall",
	"Regular Season - Home or Away",
	"Squad Standard Stats - Squad Stats",
	"Squad Standard Stats - Opponent Stats",
	"Squad Goalkeeping - Squad Stats",
	"Squad Goalkeeping - Opponent Stats",
	"Squad Advanced Goalkeeping - Squad Stats",
	"Squad Advanced Goalkeeping - Opponent Stats",
	"Squad Shooting - Squad Stats",
	"Squad Shooting - Opponent Stats",
	"Squad Passing - Squad Stats",
	"Squad Passing - Opponent Stats",
	"Squad Pass Types - Squad Stats",
	"Squad Pass Types - Opponent Stats",
	"Squad Goal and Shot Creation - Squad Stats",
	"Squad Goal and Shot Creation - Opponent Stats",
	"Squad Defencive Actions - Squad Stats",
	"Squad Defencive Actions - Opponent Stats",
	"Squad Possession - Squad Stats",
	"Squad Possession - Opponent Stats",
	"Squad Playing Time - Squad Stats",
	"Squad Playing Time - Opponent Stats",
	"Squad Miscellaneous Stats - Squad Stats",
	"Squad Miscellaneous Stats - Opponent Stats"
]

# Player Statistics
club_urls = [
	"https://fbref.com/en/squads/18bb7c10/Arsenal-Stats",
	"https://fbref.com/en/squads/8602292d/Aston-Villa-Stats",
	"https://fbref.com/en/squads/4ba7cbea/Bournemouth-Stats",
	"https://fbref.com/en/squads/cd051869/Brentford-Stats",
	"https://fbref.com/en/squads/d07537b9/Brighton-and-Hove-Albion-Stats",
	"https://fbref.com/en/squads/943e8050/Burnley-Stats",
	"https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats",
	"https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats",
	"https://fbref.com/en/squads/d3fd31cc/Everton-Stats",
	"https://fbref.com/en/squads/fd962109/Fulham-Stats",
	"https://fbref.com/en/squads/822bd0ba/Liverpool-Stats",
	"https://fbref.com/en/squads/e297cd13/Luton-Town-Stats",
	"https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats",
	"https://fbref.com/en/squads/19538871/Manchester-United-Stats",
	"https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats",
	"https://fbref.com/en/squads/e4a775cb/Nottingham-Forest-Stats",
	"https://fbref.com/en/squads/1df6b87e/Sheffield-United-Stats",
	"https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats",
	"https://fbref.com/en/squads/7c21e445/West-Ham-United-Stats",
	"https://fbref.com/en/squads/8cec06e1/Wolverhampton-Wanderers-Stats"
]

player_statistics_tables = [
	"Standard Stats",
	"Goalkeeping",
	"Advanced Goalkeeping",
	"Shooting",
	"Passing",
	"Pass Types",
	"Goal and Shot Creation",
	"Defensive Actions",
	"Possession",
	"Playing Time",
	"Miscellaneous Stats"
]

match_statistics_tables = [
	"Summary",
	"Passing",
	"Pass Types",
	"Defensive Actions",
	"Posession",
	"Miscellaneous Stats",
	"Goalkeeping",
	"Shots"
]

# Match History
match_history_table = 'Scores & Fixtures'

# Get Club Statistics
club_stats = ClubStatistics(overall_statistics_url, overall_statistics_tables)

# Get Player Statistics
player_stats = PlayerStatistics(club_urls, player_statistics_tables)

# Get Fixtures
fixture_list = MatchHistory(club_urls, match_history_table, match_statistics_tables)

def timing_decorator(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		start_time = time.time()
		result = func(*args, **kwargs)
		end_time = time.time()
		print(f"{func.__name__} took {end_time - start_time} seconds")
		return result
	return wrapper

# Call the create_team_list method on the instance
# club_stats.create_json()
# player_stats.create_json()
# fixture_list.get_fixtures()
# fixture_list.remove_extra_data()
# fixture_list.create_match_folders()

class StatsProcessor:
	def __init__(self, club_stats, player_stats, fixture_list):
		self.club_stats = club_stats
		self.player_stats = player_stats
		self.fixture_list = fixture_list

	@timing_decorator
	def process_club_stats(self):
		self.club_stats.create_json()

	@timing_decorator
	def process_player_stats(self):
		self.player_stats.create_json()

	@timing_decorator
	def process_fixtures(self):
		self.fixture_list.get_fixtures()

	@timing_decorator
	def process_remove_extra_data(self):
		self.fixture_list.remove_extra_data()

	@timing_decorator
	def process_create_match_folders(self):
		self.fixture_list.create_match_folders()


# Create an instance of StatsProcessor
stats_processor = StatsProcessor(club_stats, player_stats, fixture_list)

# Call the methods on the instance, which are now wrapped with the timing_decorator
stats_processor.process_club_stats()
stats_processor.process_player_stats()
stats_processor.process_fixtures()
stats_processor.process_remove_extra_data()
stats_processor.process_create_match_folders()