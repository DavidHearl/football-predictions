"""
This script retrieves football data including club statistics, player statistics, and match history.
It provides a StatsProcessor class that processes the data using timing decorators.
"""

import time
from functools import wraps

from get_data.get_club_statistics import ClubStatistics
from get_data.get_player_statistics import PlayerStatistics
from get_data.get_match_history import MatchHistory

# Set the season
season = '2023-2024'

# Get Club Statistics
club_stats = ClubStatistics(season)

# Get Player Statistics
player_stats = PlayerStatistics()

# Get Fixtures
fixture_list = MatchHistory()

def timing_decorator(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		start_time = time.time()
		result = func(*args, **kwargs)
		end_time = time.time()
		print(f"{func.__name__} took {end_time - start_time} seconds")
		return result
	return wrapper

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
# stats_processor.process_player_stats()
# stats_processor.process_fixtures()
# stats_processor.process_remove_extra_data()
# stats_processor.process_create_match_folders()