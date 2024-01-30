"""
This script retrieves legacy football data including club statistics, player statistics, and match history.
It provides a StatsProcessor class that processes the data using timing decorators.
"""

import time
from functools import wraps

from get_data.get_legacy.get_legacy_folder_structure import CreateStructure
from get_data.get_legacy.get_legacy_club_statistics import LegacyClubStatistics
from get_data.get_legacy.get_legacy_player_statistics import LegacyPlayerStatistics
from get_data.get_legacy.get_legacy_match_history import LegacyMatchHistory

# Set the legacy seasons
legacy_seasons = [
	'2022-2023',
	'2021-2022',
	'2020-2021',
	'2019-2020',
	'2018-2019',
	'2017-2018'
]

# Get methods and pass through the variables
folder_structure = CreateStructure(legacy_seasons)
club_legacy = LegacyClubStatistics(legacy_seasons)
player_legacy = LegacyPlayerStatistics(legacy_seasons)
match_legacy = LegacyMatchHistory(legacy_seasons)

def timing_decorator(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		start_time = time.time()
		result = func(*args, **kwargs)
		end_time = time.time()
		print(f"{func.__name__} took {end_time - start_time} seconds")
		return result
	return wrapper

class LegacyStatsProcessor:
	def __init__(self, club_legacy, player_legacy, match_legacy, folder_structure):
		self.folder_structure_instance = folder_structure
		self.club_legacy = club_legacy
		self.player_legacy = player_legacy
		self.match_legacy = match_legacy

	@timing_decorator
	def folder_structure(self):
		self.folder_structure_instance.folder_structure()
	
	@timing_decorator
	def process_club_stats(self):
		self.club_legacy.get_club_data()

	@timing_decorator
	def process_player_stats(self):
		self.player_legacy.get_player_data()

	@timing_decorator
	def process_fixtures(self):
		self.match_legacy.get_fixtures()

	@timing_decorator
	def process_clean_fixtures(self):
		self.match_legacy.clean_fixtures()

	@timing_decorator
	def process_create_match_folders(self):
		self.match_legacy.create_match_folders()


# Create an instance of LegacyStatsProcessor
legacy_stats_processor = LegacyStatsProcessor(club_legacy, player_legacy, match_legacy, folder_structure)

# Call the methods on the instance, which are now wrapped with the timing_decorator
# legacy_stats_processor.folder_structure()
# legacy_stats_processor.process_club_stats()
# legacy_stats_processor.process_player_stats()
# legacy_stats_processor.process_fixtures()
legacy_stats_processor.process_clean_fixtures()
legacy_stats_processor.process_create_match_folders()
