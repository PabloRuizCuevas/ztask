#!/usr/bin/env python

from env_variables import client_id, client_secret, refresh_token, user_id
from prettytable import PrettyTable, ORGMODE
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

import parsedatetime as pdt
import pandas as pd
import requests
import json
import sys
import re


class TablePrinter:

    def __init__(self):
        #                  ;background
        self.R = "\033[0;31;10m"  # RED
        self.G = "\033[0;32;10m"  # GREEN
        self.Y = "\033[0;33;10m"  # Yellow
        self.B = "\033[0;34;10m"  # Blue
        self.N = "\033[0m"  # Reset

    def colorize(self, df, key):
        df[key] = self.R + df[key] + self.N
        return df

    def colorize_header(self, df):
        df.columns = self.G + df.columns + self.N
        return df

    def print_table(self, df):
        df = self.colorize_header(df)
        x = PrettyTable()
        x.set_style(ORGMODE)
        x.field_names = list(df.keys())
        x.add_rows(df.values.tolist())
        print(x)


class ZohoClient:

    def __init__(self):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token = None
        self.headers = None
        self.get_access_token()
        self.counter = 0

    def get_access_token(self):
        """
        gets/refresh access token
        """
        account_url = 'https://accounts.zoho.eu'
        url = f'{account_url}/oauth/v2/token?refresh_token={self.refresh_token}&client_id={self.client_id}&client_secret={self.client_secret}&grant_type=refresh_token'
        try:
            self.access_token = self.post_request(url)["access_token"]
            self.headers = {'Authorization': f'Zoho-oauthtoken {self.access_token}'}
        except Exception:
            print('get access token failed')
            print('ztask get_refresh_token grant_token')

    def get_refresh_token(self, grant_token):
        """
        Not really working but kind of useful for first set up, need to change the grant_token
        haz esto desde la web  https://api-console.zoho.eu/client/{self.client_id}

        scope
        ZohoProjects.tasks.ALL,ZohoProjects.timesheets.ALL,ZohoProjects.projects.ALL,ZohoProjects.portals.READ,ZohoProjects.bugs.ALL
        copy the grant_token and run this function with it to get the refresh token
        """
        url = f'https://accounts.zoho.eu/oauth/v2/token?code={grant_token}&client_id={self.client_id}' \
              f'&client_secret={self.client_secret}&grant_type=authorization_code'
        r = requests.post(url)
        print("refresh_token:", json.loads(r.text)['refresh_token'])

    def request(self, fun, url, params=''):
        """
        Get request even if the token is expired
        """
        try:
            r = fun(url, params=params, headers=self.headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print('HTTPError maybe oauth expired, will be renovated...')
            print(r)
            self.get_access_token()
            if self.counter < 2:
                self.counter += 1
                r = fun(url, params=params, headers=self.headers)
            else:
                print("limit trials exceeded")
                print('generate new refresh token using get_refresh_token grant_token')
        return json.loads(r.text)

    def post_request(self, url, params=''):
        """
        post request even if the token is expired, maybe a decorator would be better...
        or making a new token all the time... don't know
        """
        return self.request(requests.post, url, params=params)

    def get_request(self, url, params=''):
        """
        Get request even if the token is expired
        """
        return self.request(requests.get, url, params=params)


class DateParser:

    def __init__(self):
        pass

    @staticmethod
    def natural_date(string_date):
        """
        from natural language to date
        """
        cal, now = pdt.Calendar(), datetime.now()
        return cal.parseDT(string_date, now)[0].strftime("%m-%d-%Y")

    def date(self, string_date):
        """ for printing dates from terminal """
        print('mm-dd-yyyy:', self.natural_date(string_date))

    @staticmethod
    def parse_hours(string):
        """
        This function parses different input hours,
        such as 7-20 in 07:20 or 4 into 04:00
        """
        reg = re.match("([0-9]{0,2})[:-]?([0-9]{0,2})", string)
        hours, minutes = int(reg[1].strip() or 0), int(reg[2].strip() or 0)
        return f'{hours:02d}:{minutes:02d}'

    def time(self, string):
        print(self.parse_hours(string))


class NoValue(Enum):
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)


class TaskBugType(NoValue):
    BUG = 'bugs'
    TASK = 'tasks'


@dataclass
class TaskBug:
    _id: str
    task_name: str
    project_id: int
    project_name: str
    completed: str
    status: str
    key: str


class ZohoManager(ZohoClient, DateParser):

    def __init__(self):
        """
        would be good to use env variables here
        """
        super().__init__()
        self.user_id = None
        self.url_portal = f"https://projectsapi.zoho.eu/restapi/portal"
        self.url_portals = self.url_portal + 's/'

        self.access_token = None
        self.portal_id = None

        self.get_user_data()
        self.get_my_portal()
        self.printer = TablePrinter()

    def get_user_data(self):
        """
        Can be obtained from zoho projects easily but would be better scripted
        """
        self.user_id = user_id

    def get_my_portal(self):
        """
        There is only one portal in thi case... could be hard coded
        """
        try:
            portals = self.get_request(self.url_portals)
            self.portal_id = portals['portals'][0]['id']
        except Exception:
            print('get_my_portal_failed')

    def my_task_bugs_raw(self, tasks_bugs: TaskBugType):  # tasks_bugs "tasks"|"bugs"
        url = f"{self.url_portal}/{self.portal_id}/my{tasks_bugs.value}/"
        return self.get_request(url)[tasks_bugs.value]

    @property
    def my_tasks_raw(self):
        return self.my_task_bugs_raw(TaskBugType.TASK)

    @property
    def my_bugs_raw(self):
        return self.my_task_bugs_raw(TaskBugType.BUG)

    def make_task_bugs_list(self, tasks_bugs: TaskBugType):
        """
        Fetches my task into a df
        """
        tasks = []
        for task in self.my_task_bugs_raw(tasks_bugs):
            if tasks_bugs == TaskBugType.TASK:
                info = (task['name'], task['project']['id'], task['project']['name'],
                        task['completed'], task['status']['name'])
            elif tasks_bugs == TaskBugType.BUG:
                info = (task['title'], task['project_id'], task['project_name'], task['closed'], task['status']['type'])
            else:
                raise print("tasks_bugs should be either task or bug")
            task_dict = TaskBug(task['id'], *info, task['key'])
            tasks.append(asdict(task_dict))
        return tasks

    def make_dataframe(self, task_bug_list):
        """Makes a df from task bug list"""
        tasks = task_bug_list
        tasks = pd.DataFrame(tasks).sort_values(by=['project_name'])
        tasks = self.parse_task_type(tasks)
        tasks = tasks[~tasks.status.isin(['Task Completed', 'Closed', 'Cancelled'])]
        return tasks.reset_index(drop=True)

    @staticmethod
    def parse_task_type(df):
        """converts task key identifier in task or issue str"""
        df['key'] = df['key'].str.extract(r'-([IT])[0-9]*$')
        df['key'] = df['key'].replace("T", "Task")
        df['key'] = df['key'].str.replace("I", "Bug")
        return df

    @property
    def my_task(self):
        return self.make_dataframe(self.make_task_bugs_list(TaskBugType.TASK))

    @property
    def my_bugs(self):
        return self.make_dataframe(self.make_task_bugs_list(TaskBugType.BUG))

    @property
    def my_task_bugs(self):
        task_bugs_list = self.make_task_bugs_list(TaskBugType.TASK) + self.make_task_bugs_list(TaskBugType.BUG)
        return self.make_dataframe(task_bugs_list)

    def get_task_from_simple_id(self, task_simple_id):
        return self.my_task_bugs.loc[int(task_simple_id)]

    def log(self, task_simple_id, date, hours):
        """
        Main function to log task
        """

        task = self.get_task_from_simple_id(task_simple_id)
        task_id, project_id = task['_id'], task['project_id']
        date = self.natural_date(date)
        hours = self.parse_hours(hours)

        tasks_bugs = task['key'].lower()+'s'
        url = f"{self.url_portal}/{self.portal_id}/projects/{project_id}/{tasks_bugs}/{task_id}/logs/"
        params = {"date": date, "bill_status": "Billable", "hours": hours, "owner": self.user_id}
        r = self.post_request(url, params=params)
        print(f"Task {task_simple_id}: {task['task_name']}, logged :)")
        return r

    def update(self, task_simple_id, params):
        """
        Update task from params and task id
        """
        task = self.get_task_from_simple_id(task_simple_id)
        url = f"{self.url_portal}/{self.portal_id}/projects/{task['project_id']}/tasks/{task['id']}/"
        print(url)
        r = self.post_request(url, params=str(params))
        if "error" not in dict(r):
            print(f"Task {task_simple_id} {task['task_name']} Updated :)")
        else:
            print(r)
        return r

    def list(self):
        """
        tasks list
        """
        df = self.my_task_bugs[['project_name', 'task_name', 'status', 'key']].copy()
        df['type'] = df['key'].str.replace("Bug", "Issue")
        df['task name'] = df['task_name'].str.slice(0, 50)
        df['project name'] = df['project_name'].str.slice(0, 18)
        df['status'] = df['status'].str.slice(0, 15)
        df['index'] = df.index.values
        self.printer.print_table(df[['index', 'project name', 'task name', 'status', 'type']])

    def all_task(self):
        """gets all my task, even closed ones"""
        tasks = self.my_task_bugs
        self.printer.print_table(tasks[['project_name', 'task_name', 'status']])
        return tasks

    def __str__(self):
        """ prints task"""
        self.list()
        return ""


if __name__ == '__main__':

    ztask = ZohoManager()
    if len(sys.argv) == 1:
        ztask.list()
    else:
        getattr(ztask, sys.argv[1])(*sys.argv[2:])

