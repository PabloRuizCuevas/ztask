# ztask

ztask helps to log task in zoho from the terminal using a taskwarrior inspired syntax.

## installation:
install python3 and requirements from requirements.txt:

set the alias in your bash aliases:
alias ztask='python3 /your_ztask_path/ztask.py'

## usage:

ztask, as it should be, is a terminal user interface can be run with:

python3 ztask.py (in the path) 

Or using an alias "ztask":

ztask : for seeing a task list
ztask all_task : shows all the task even closed ones
ztask log number_of_task 'date' hh:mm : log the task in zoho

ztask date suports natural language such as: 'today', 'yesterday' etc

## examples:

ztask log 4 '2 days ago' 07:30 

will log the task 4, two days ago with a duration of 7:30

ztask log 12 'today' 08:00

will log the taks 12 today 8 hours

## env variables
you will need to set the following env variables in the env_variables.py file:

-client_id
-client_secret
-refresh_token 

These variables can be found at https://api-console.zoho.eu, more information at env_variables.py

## other

for check the formated documentation

pip install mdv 
mdv readme.md

