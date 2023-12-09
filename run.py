from download_tables import DownloadTables

# Create an instance of DownloadTables
downloader = DownloadTables("https://fbref.com/en/comps/9/Premier-League-Stats")

# Call the create_team_list method on the instance
downloader.create_squad_json()
