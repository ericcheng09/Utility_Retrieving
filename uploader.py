from influxdb import InfluxDBClient
import argparse, configparser
import signal
import time
import hostutil, dockerutil, pmemutil
from distutils.util import strtobool

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


signal.signal(signal.SIGINT, signal_handler)
interrupted = False

parser = argparse.ArgumentParser()
parser.add_argument("--config", help="path of config file", dest="config_path", default="./config.ini")
args = parser.parse_args()
config_path = args.config_path

config = configparser.ConfigParser()
config.read(config_path)

client = InfluxDBClient(host=config["BASIC"]["ip"],
                        port=int(config["BASIC"]["port"]),
                        username=config["BASIC"]["user"],
                        password=config["BASIC"]["password"],
                        database=config["BASIC"]["database"])

source = []

if strtobool(config["BASIC"]["Host"]):
    source.append(hostutil.HostUtil(
    [path for _, path in config.items("HOST.DISKPATH")],
    strtobool(config["HOST"]["perdiks"]),
    [disk for _, disk in config.items("HOST.DISK")])
    )

if strtobool(config["BASIC"]["Docker"]):
    source.append(dockerutil.DockerUtil(
        config["DOCKER"]["base_url"],
        config["DOCKER"]["include_all"],
        [container for container in config.items("DOCKER.CONTAINERS")])
    )

if strtobool(config["BASIC"]["PMEM"]):
    source.append(pmemutil.PMEM())



while True:
    data = []
    if interrupted:
        print("Closing...")
        break
    time.sleep(1)
    for s in source:
        data.extend(s.get_data())

    client.write_points(data)
client.close()
