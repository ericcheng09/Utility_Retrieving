# Utility Retrieving

Retrieve the  system, docker containers and PMEM information and upload to a influxDB Database.


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
## Configuration
Config.ini
```
[BASIC]
Host		= True                          ; Retrieve system utilities
Docker		= True                          ; Retrieve containers' utilities
PMEM		= True                          ; Retrieve PMEMs' utilities
ip		    = 127.0.0.1                     ; IP of machine that hosts database
port		= 8086                          ; port of machine that hosts database
database	= PM_Demo                       ; Name of the database
user		= edci                          ; Username of the database
password	= edci                          ; Password of the database
[DOCKER]
base_url    = unix://var/run/docker.sock    ; URL to the Docker server
include_all = True                          ; if true, then all the containers' info will be retrieved
[DOCKER.CONTAINERS]
container1 =                                ; list the container ids desired to retrieve, only used when include_all is False
[HOST]
[PMEM]
```

## Running
```shell
sudo python uploader.py
```



