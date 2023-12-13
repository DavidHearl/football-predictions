import pandas as pd

# Pandas terminal settings
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 200)

squad_tables = [
    "raw_data/squad_data/Regular Season - Overall.json",
    # "raw_data/squad_data/Regular Season - Home/Away.json",
    "raw_data/squad_data/Squad Standard Stats - Squad Stats.json",
    "raw_data/squad_data/Squad Standard Stats - Opponent Stats.json",
    "raw_data/squad_data/Squad Goalkeeping - Squad Stats.json",
    "raw_data/squad_data/Squad Goalkeeping - Opponent Stats.json",
    "raw_data/squad_data/Squad Advanced Goalkeeping - Squad Stats.json",
    "raw_data/squad_data/Squad Advanced Goalkeeping - Opponent Stats.json",
    "raw_data/squad_data/Squad Shooting - Squad Stats.json",
    "raw_data/squad_data/Squad Shooting - Opponent Stats.json",
    "raw_data/squad_data/Squad Passing - Squad Stats.json",
    "raw_data/squad_data/Squad Passing - Opponent Stats.json",
    "raw_data/squad_data/Squad Pass Types - Squad Stats.json",
    "raw_data/squad_data/Squad Pass Types - Opponent Stats.json",
    "raw_data/squad_data/Squad Goal and Shot Creation - Squad Stats.json",
    "raw_data/squad_data/Squad Goal and Shot Creation - Opponent Stats.json",
    "raw_data/squad_data/Squad Defensive Actions - Squad Stats.json",
    "raw_data/squad_data/Squad Defensive Actions - Opponent Stats.json",
    "raw_data/squad_data/Squad Possession - Squad Stats.json",
    "raw_data/squad_data/Squad Possession - Opponent Stats.json",
    "raw_data/squad_data/Squad Playing Time - Squad Stats.json",
    "raw_data/squad_data/Squad Playing Time - Opponent Stats.json",
    "raw_data/squad_data/Squad Miscellaneous Stats - Squad Stats.json",
    "raw_data/squad_data/Squad Miscellaneous Stats - Opponent Stats.json"
]

for table in squad_tables:
    # Load data
    data = pd.read_json(table)
    # Print the table
    print(data)
