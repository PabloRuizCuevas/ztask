

<p align="center">
  <img src="https://github.com/PabloRuizCuevas/ztask/blob/master/images/use_example.png">
</p>

# <b>Ztask</b>

<b>Ztask</b> helps to log task in <a href="https://projects.zoho.eu" target="_top">zohoprojects</a> and complete the 
damned timesheets from the terminal using a 
<a href="https://taskwarrior.org/" target="_top">Taskwarrior</a> inspired syntax.

This little program is made by and for terminal enthusiasts, <b>enjoy it!</b>

## Requirements

You only need a distribution of python3 installed.

## ⚙️Installation:

You can install the requirements (preferably in an environment) using:

> pip install ztask

Download directly the script and set the variables at your user path in .ztask/env_variables.py, 
more details about these variables bellow.
 
If you install "ztask" in a environment you will need to initialize the environment before using ztask, 
for so sometimes is convenient to use an alias like:

> alias eztask='conda activate <env_name> && ztask'

## Usage:

Ztask, as it should be, is a <b>terminal user interface</b> that can be run with:

>python3 ztask.py (in the path) 

Or more conveniently using the alias <b>ztask</b>:

For printing my zoho task:

> ztask

Shows all the table, without truncating the table:

> ztask long

Log the task in zoho:

> ztask log number_of_task 'date' hh:mm

Ztask date suports natural language such as: 'today', 'yesterday' etc

## Examples:

Log the task 4, two days ago with a duration of 7:30 hours:

> ztask log 4 '2 days ago' 07:30 

Log the taks 12 today 8 hours:

> ztask log 12 'today' 08:00

## 💾 env variables

For using the program you will need to create a folder called .ztask in your user path and a file called .ztask 
the path would look something like: 

> C:\\Users\\YOUR USER NAME\\.ztask\\ztask.ini

Or in Unix based systems:

> /home/YOUR USER NAME/.ztask/ztask.ini

Set the following env variables in the env_variables.py file (copy paste and fill):

`[variables]`

`client_id = <YOUR CLIENT ID> `

`client_secret = <YOUR CLIENT SECRET> `

`refresh_token = <YOUR REFRESH TOKEN>`

`user_id = <YOUR USER ID>`

These variables can be found at https://api-console.zoho.eu after creating a self client.

You can get your refresh_token after getting the grant token. Go to self client same web and generate the grant token
using the scope:

`ZohoProjects.tasks.ALL,ZohoProjects.timesheets.ALL,ZohoProjects.projects.ALL,ZohoProjects.portals.READ,ZohoProjects.bugs.ALL`

Copy the grant_token and execute in the terminal:

> ztask get_refresh_token <YOUR GRANT TOKEN>

The user_id can be found at zoho projects, clicking in the right corner (user icon)

## other

For checking the formatted documentation:

> pip install mdv 
> mdv readme.md

