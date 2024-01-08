import time
from functools import wraps

from get_data.get_club_statistics import ClubStatistics
from get_data.get_player_statistics import PlayerStatistics
from get_data.get_match_history import MatchHistory

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
club_stats = ClubStatistics()

# Get Player Statistics
player_stats = PlayerStatistics()

# Get Fixtures
# fixture_list = MatchHistory(club_urls, match_history_table, match_statistics_tables)

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
	def __init__(self, club_stats, player_stats): # , fixture_list
		self.club_stats = club_stats
		self.player_stats = player_stats
		# self.fixture_list = fixture_list

	@timing_decorator
	def process_club_stats(self):
		self.club_stats.create_json()

	@timing_decorator
	def process_player_stats(self):
		self.player_stats.create_json()

	# @timing_decorator
	# def process_fixtures(self):
	# 	self.fixture_list.get_fixtures()

	# @timing_decorator
	# def process_remove_extra_data(self):
	# 	self.fixture_list.remove_extra_data()

	# @timing_decorator
	# def process_create_match_folders(self):
	# 	self.fixture_list.create_match_folders()


# Create an instance of StatsProcessor
stats_processor = StatsProcessor(club_stats, player_stats) # , fixture_list

# Call the methods on the instance, which are now wrapped with the timing_decorator
stats_processor.process_club_stats()
stats_processor.process_player_stats()
# stats_processor.process_fixtures()
# stats_processor.process_remove_extra_data()
# stats_processor.process_create_match_folders()