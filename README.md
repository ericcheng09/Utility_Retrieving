# Utility Retrieving

Scrape the utilities of system and docker containers and upload to influxDB.

## Install required packages.
```shell
pip install -r requirements.txt
```
Note: You may need to install gcc and python-devel for psutil.
```
usage: scraper.py [-h] [--IP IP] [--port PORT] [--db DB] [--user USER]
                  [--pass PASSWORD] [--path PATH] [--disk DISK] [--ID ID]

optional arguments:
  -h, --help       show this help message and exit
  --IP IP          IP of database
  --port PORT      Port of database
  --db DB          Name of database
  --user USER      User of database
  --pass PASSWORD  Password of User
  --path PATH      Path of mounted disk
  --disk DISK      Name of monitored disk
  --ID ID          Container ID to Monitor
```


```shell
python scraper.py 
```
