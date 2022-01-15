# ztask

This project helps to log task in zoho.

## installation:
install python and requirements:

set the alias in your bash aliases:
alias ztask='python3 ztask.py'

## usage:

ztask as it should be is a terminal user interface.

ztask : for seeing a task list
ztask all_task : shows all the task even closed ones
ztask log number_of_task 'date' hh:mm : log the task in zoho

ztask date suports natural language such as: 'today', 'yesrday' etc

## examples:

ztask log 4 '2 days ago' 07:30 

will log the task 4, two days ago with a duration of 7:30

ztask log 12 'today' 08:00

will log the taks 12 today 8 hours

## env variables
you will need to set the following env variables in the .env file:
 
ZOHO_CLIENT=<Write here your zoho client id>
ZOHO_CLIENT_SECRET=<Write here your zoho client secret>
ZOHO_REFRESH_TOKEN=<Write here your zoho refresh token>


## other

for check the formated documentation

pip install mdv 
mdv readme.md

