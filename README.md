# HelloAsso For SJB
Script to export data from helloasso to google spreadsheet

# How to
Read this to initialize a google cloud project that will allow a script to write into a spreadsheet

https://towardsdatascience.com/accessing-google-spreadsheet-data-using-python-90a5bc214fd2

# Requirements
python 3.6+

# Install
```
pip install -r requirements.txt
```

# HelloAsso API
To retrieve data from HelloAsso API, you must set the following environment variables :

```
export ORGANIZATION_ID=    # can be get here: https://api.helloasso.com/v3/organizations.json
export CAMPAIGN_ID=        # can be get here: call https://api.helloasso.com/v3/organizations/ORGANIZATION_ID/campaigns.json 

# Ask to HelloAsso Support to get your own user/password values
export API_KEY=
export API_USER=
```

# ToDo
- Use helloasso api instead of csv export
- Crontab the job to make export automatic (heroku ?)
- Email bill