# Football Match Prediction

## How to run & What happens

### Get Data

#### 1: Run ```py get_data.py```

This will create a folder for the current season within the <span style="color:yellow">raw_data</span> folder.

3 subfolders will be created, <span style="color:yellow">club_data</span>,  <span style="color:yellow">player_data</span>, <span style="color:yellow">match_data</span> each folder will be populated with stats. 

- raw_data
    - 2023-2024
        - club_data
        - player_data
        - match_data

#### 2: Run ```py correct_data.py```

This will create multiple folders for the previous seasons within the <span style="color:yellow">raw_data</span> folder.

The folder structure will follow the same rules as above.

- raw_data
    - 2023-2024
        - club_data
        - player_data
        - match_data
    - 2022-2023
        - club_data
        - player_data
        - match_data
    - ...

### 3:


## To Do List

1. In ```get_match_history.py``` modify the remove_extra_data folder to:
    - remove non premier league games
    - save the upcomming games next to the Scores & Fixtures.json instead of deleting them

2. Look at spliting the "club_urls" by season, look to populate this within the ```get_club_data```

3. Finish off retrieving legacy data

## Create Virtual Environment

Firstly we must create a virtual environment within Visual Studio.
``` 
# Windows
py -m venv ./venvwin

# Mac OS
python3 -m venv ./venvmac
```

Once the virtual environment folder has been created we must initalise the environment.

```
# Windows
source ./venvwin/scripts/activate

# Mac OS
source ./venvmac/bin/activate
```

We can check that the location of pip has changed with this comand.
We want the location to be the newly created ./venv folder.

```
which pip
```

When we are finished with the project we can exit the environment with this command.
```
deactivate
```

## Install Dependancies

If there is already a requirements.txt file then you can start by upgrading pip to the latest version.

Then you can install the requirements with the commands below.
```
# Windows
python.exe -m pip install --upgrade pip

# Mac OS
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

If more dependancies have been installed then you can push an update to the requirements.txt file with the command below.
```
pip freeze --local > requirements.txt
```

## Terminal

Change the Location

```
cd "C:\Local Storage\GitHub\football-predictions"
```

Get the data tables

```
# Windows
python run.py

# MacOS
python3 run.py
```
