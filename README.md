# HelloAsso For SJB

Script to export data from helloasso to google spreadsheet

# How to

Read this to initialize a google cloud project that will allow a script to write into a spreadsheet

https://towardsdatascience.com/accessing-google-spreadsheet-data-using-python-90a5bc214fd2

# Requirements

python 3.6+

# Install

## Virtual environment (optional but definitely the best way)

The best way is to use a python virtual environment.

- Install pip if it is not
- Install venv

```
pip install venv
```

- Clone the repository

```
git clone https://github.com/fabiolab/ha4sjb.git
```

- At the root directory of the projet, install the virtual environment:

```
python -m venv pyth3 -p /usr/bin/python3
```

> - pyth3 will be the name of your virtual env
> - change /usr/bin/python3 to make it match to the python3 path on your environment

This command will create a pyth3 (or whatever you chose for the virtual environment name) in the root directory.

- Run the venv:

```
./pyth3/bin/activate
``` 

From there, all the command you run will use the python3 virtual env you have created

- Install the dependencies:

```
pip install -r requirements.txt
```

## Set the environment variables (HelloAsso API)

To retrieve data from HelloAsso API, the following environment variables must be set first:

```
export ORGANIZATION_ID=    # can be get here: https://api.helloasso.com/v3/organizations.json
export CAMPAIGN_ID=        # can be get here: https://api.helloasso.com/v3/organizations/ORGANIZATION_ID/campaigns.json 

# Contact HelloAsso support to get your own user/password values
export API_KEY=
export API_USER=
```

# Run the HelloAsso exporter

The exporter script gets all the data from a given HelloAsso campaign to a given google spreadsheet. The script only
adds new rows: it makes no deletion nor change to avoid loose of hand added data. The script loads every items from
HelloAsso campaign, but only add new items to the google spreasheet: for this, it checks the helloasso id (first column)

## Shell script

You can use the export.sh bash script to run the transfert between HelloAsso and Google Spreadsheet. Create a `.env`
file that set the environment variables values

```
export ORGANIZATION_ID=
export CAMPAIGN_ID= 	
export API_KEY=
export API_USER=
export GOOGLE_SPREADSHEET=
export PYTHON_VENV_DIR=
export GOOGLE_CREDENTIALS=   # Content of the google auth credentials file
```

Make the script executable and run it (it requires `bash` installed on your system and located in `/bin/bash`):

```
./export.sh
```

## Python script

The script may be run with python (env variables must be set first):

```
python exporter.py
```

# Heroku notes

To automate the job run with an heroku account, follow these
steps : https://devcenter.heroku.com/articles/clock-processes-python

You will have to set the env variables with the Dashboard or with the CLi:

```
heroku config:set ORGANIZATION_ID=
heroku config:set CAMPAIGN_ID=
heroku config:set API_KEY=
heroku config:set API_USER=
heroku config:set GOOGLE_SPREADSHEET=
heroku config:set GOOGLE_FOLDER_ID=

GOOGLE_CREDENTIALS => use the dashboard and put the content of the credentials.json file
```

- The `runtime.txt` must contains the python version to use
- The project must have a `requirements.txt`
- The `Procfile` file associates a name (export) to the command to run

To deploy the app, use the heroku cli:

```
git push heroku master
```

And add the task to lauch:

```
heroku ps:scale export=1
```

# ToDo

[x] Use helloasso api instead of csv export
[x] Crontab the job to make export automatic
[ ] Email bill
[x] Backup HelloAsso files (medical certificates) to Google Drive

# New year

- Connect to Heroku and change the variables
- Don't forget to share the new spreadsheat with the user (fabio35@local-incline-263914.iam.gserviceaccount.com)