# Utility Retrieving

Scrape the utilities of system and docker containers and upload to influxDB.

## Install required packages.
```shell
pip install -r requirements.txt
```
Note: You may need to install gcc and python-devel for psutil.
```
usage: uploader.py [-h] [--config CONFIG_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG_PATH  path of config file

```


```shell
sudo python uploader.py
```

