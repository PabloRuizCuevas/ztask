

<p align="center">
  <img src="/images/use_example.png">
</p>

# <b>Ztask</b>

<b>Ztask</b> helps to log task in <a href="https://projects.zoho.eu" target="_top">zohoprojects</a> and complete the 
damned timesheets from the terminal using a 
<a href="https://taskwarrior.org/" target="_top">Taskwarrior</a> inspired syntax.

This little program is made by and for terminal enthusiasts, <b>enjoy it!</b>

## requirements

- python3
- requirements.txt:

You can install the requirements (preferably in pipenv/conda environment) using:

> python -m pip install -r requirements.txt

## ⚙️Installation:

Download directly script and set the variables at env_variables.py

Is convenient to set the alias "ztask", in ubuntu you can use the following alias:

> alias ztask='python3 <your_ztask_path>/ztask.py'

using an environment (conda) this will look like;

> alias ztask='conda activate <env_name> && python3 <your_ztask_path>/ztask.py'

## Usage:

Ztask, as it should be, is a <b>terminal user interface</b> that can be run with:

>python3 ztask.py (in the path) 

Or more conveniently using the alias <b>ztask</b>:

For printing my zoho task:

> ztask

Shows all the table, without truncating the table:

> ztask all_task :

Log the task in zoho:

> ztask log number_of_task 'date' hh:mm :

ztask date suports natural language such as: 'today', 'yesterday' etc

## Examples:

Log the task 4, two days ago with a duration of 7:30 hours:

> ztask log 4 '2 days ago' 07:30 

Log the taks 12 today 8 hours:

> ztask log 12 'today' 08:00

## 💾 env variables
you will need to set the following env variables in the env_variables.py file:

- client_id
- client_secret
- refresh_token 
- user_id

These variables can be found at https://api-console.zoho.eu, more information at env_variables.py
The user_id can be found at zoho projects, clicking in the right corner (user icon)

## other

For checking the formatted documentation:

> pip install mdv 
> mdv readme.md

