# Tornado Test Project

<a href="https://tornado-test-task.herokuapp.com/" target="_blank">
  <img src="https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white"></a>

The project was written to gain experience in writing Tornado Applications,
consolidate skills in working with databases and parsing.

## About
Parsing ip addresses from a website and adding them to a database. The Tornado web application
processes six handlers that allow users to log in, output all data from a table in JSON format or a table.

## Requirements
``` 
bcrypt~=3.2.2
prettytable~=3.3.0
PyYAML==6.0
selenium~=4.2.0
SQLAlchemy~=1.4.36
tornado==6.1
parsel~=1.6.0
psycopg2~=2.9.3
coloredlogs~=15.0.1
concurrent_log_handler~=0.9.20
```

## Install 
```shell
$ git clone https://github.com/deviati0n/tornado_test.git <project_name>
$ cd <project_name>
$ pip install -r requirements.txt
```

## Run project

Rename `default.yaml` to `config.yaml` and change the values to your own.

### Run scraper

* Argument `--dry_run`:
  * `true` - data output to the console
  * `false` - fill the table in the DB
  * `json` - returns data in json format
  
```shell
$ python run_scraper.py
```

### Run API
```shell
$ python run_api.py
```





