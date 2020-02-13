from influxdb import InfluxDBClient
import argparse, configparser
import signal
import time
import hostutil, dockerutil, pmemutil


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

if bool(config["BASIC"]["Host"]):
    source.append(hostutil.HostUtil())

if bool(config["BASIC"]["Docker"]):
    source.append(dockerutil.DockerUtil(config["DOCKER"]["base_url"],
                                        config["DOCKER"]["include_all"],
                                        [container for container in config.items("DOCKER.CONTAINERS")])
                  )

if bool(config["BASIC"]["PMEM"]):
    # source.append(pmemutil.PMEM())
    pass

while True:
    data = []
    if interrupted:
        print("Closing...")
        break
    time.sleep(1)
    for s in source:
        source.extend(s.get_data())

    client.write_points(data)
client.close()
