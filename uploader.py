from influxdb import InfluxDBClient
import argparse
import signal
import time

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)


interrupted = False
parser = argparse.ArgumentParser()
parser.add_argument("--IP", help="IP of database", dest="ip", default="127.0.0.1")
parser.add_argument("--port", help="Port of database", dest="port", default=8086)
parser.add_argument("--db", help="Name of database", dest="db", default="PM_Demo")
parser.add_argument("--user", help="User of database", dest="user", default="root")
parser.add_argument("--pass", help="Password of User", dest="password", default="root")


args = parser.parse_args()
client = InfluxDBClient(host=args.ip, port=args.port, username=args.user, password=args.password, database=args.db)

while True:
    data = []
    if interrupted:
        print("Closing...")
        break
    time.sleep(1)

    client.write_points(data)


client.close()
