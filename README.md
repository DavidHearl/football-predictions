# Football Match Prediction

## How to run & What happens

1. Run ```py get_data.py``` this will create 2 folders within <span style="color:yellow">raw_data</span>.
    - <span style="color:yellow">teams</span>
    - <span style="color:yellow">squad_data</span>

2. Run ```py correct_data.py``` this will take the raw data and correct errors and remove unwanted fields. 
    - To modify the keys, see `upadate_data/key_corrections.py`
    - To remove data see the <span style="color:yellow">remove_keys</span> function in ```correct_data.py```
3. Run ```py match_results.py``` to download all the previous fixtures & results



## To Do List
1. Add teams and team data to print_table.py

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
