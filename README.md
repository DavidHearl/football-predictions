# Football Match Prediction

## General Operation

### Downloading Tables

### 


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
