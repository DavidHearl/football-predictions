from get_data.get_legacy.get_legacy_club_statistics import LegacyClubStatistics
from get_data.get_legacy.get_legacy_player_statistics import LegacyPlayerStatistics

# Set the legacy seasons
legacy_seasons = [
	'2022-2023',
	'2021-2022',
	'2020-2021',
	'2019-2020',
	'2018-2019',
	'2017-2018'
]

club_legacy = LegacyClubStatistics(legacy_seasons)
player_legacy = LegacyPlayerStatistics(legacy_seasons)

# club_legacy.create_json()
player_legacy.create_json()
