from get_data.get_club_statistics import ClubStatistics
from get_data.get_player_statistics import PlayerStatistics

# ClubStatistics
overall_statistics_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

overall_statistics_tables = [
	"Regular Season - Overall",
	"Regular Season - Home/Away",
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

# match_history = "https://www.football-data.co.uk/englandm.php"

# Get Club Statistics
club_stats = ClubStatistics(overall_statistics_url, overall_statistics_tables)

# Get Player Statistics
player_stats = PlayerStatistics(club_urls, player_statistics_tables)

# Call the create_team_list method on the instance
club_stats.create_json()
player_stats.create_json()


