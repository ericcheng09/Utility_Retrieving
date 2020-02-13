from influxdb import InfluxDBClient
import time
import psutil
import os
import argparse
import docker
import signal


parser = argparse.ArgumentParser()
parser.add_argument("--IP", help="IP of database", dest="ip", default="127.0.0.1")
parser.add_argument("--port", help="Port of database", dest="port", default=8086)
parser.add_argument("--db", help="Name of database", dest="db", default="PM_Demo")
parser.add_argument("--user", help="User of database", dest="user", default="root")
parser.add_argument("--pass", help="Password of User", dest="password", default="root")
parser.add_argument("--path", help="Path of mounted disk", dest="path", default="/mnt/pmemdir")
parser.add_argument("--disk", help="Name of monitored disk", dest="disk", default="pmem0")
# parser.add_argument("--ID", help="Container ID to Monitor", dest="ID", default="847d265931b1")


args = parser.parse_args()
path = args.path
disk = args.disk
# containerID = args.ID

client = InfluxDBClient(host=args.ip, port=args.port, username=args.user, password=args.password, database=args.db)
docker_client = docker.APIClient(base_url="unix://var/run/docker.sock")

host = os.uname()[1]
disk_IO = tuple(psutil.disk_io_counters(perdisk=True)[disk])
read_bytes, read_time = disk_IO[2], disk_IO[4]
write_bytes, write_time = disk_IO[3], disk_IO[5]

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)
interrupted = False

containers = docker_client.containers()["Id"]


while True:
    data = []
    if interrupted:
        print("Closing...")
        break
    time.sleep(1)
    cpu_usage = psutil.cpu_percent()

    mem_total, mem_available, mem_usage = psutil.virtual_memory()[:3]

    disk_total, disk_available, disk_usage = (psutil.disk_usage(path)[0], \
                                              psutil.disk_usage(path)[1], psutil.disk_usage(path)[3])

    disk_IO = tuple(psutil.disk_io_counters(perdisk=True)[disk])

    read_bytes_per_sec = 0.0
    write_bytes_per_sec = 0.0
    if (disk_IO[4] - read_time) != 0:
        read_bytes_per_sec = (disk_IO[2] - read_bytes) / (disk_IO[4] - read_time) * 1000
    if (disk_IO[5] - write_time) != 0:
        write_bytes_per_sec = (disk_IO[3] - write_bytes) / (disk_IO[5] - write_time) * 1000

    read_bytes, read_time = disk_IO[2], disk_IO[4]
    write_bytes, write_time = disk_IO[3], disk_IO[5]


    # docker status
    for container in containers:
        docker_status = docker_client.stats(container, stream=False)
        pre_CPU_usage, pre_CPU_sys_Usage = docker_status["cpu_stats"]["cpu_usage"]["total_usage"], \
                                                docker_status["cpu_stats"]["system_cpu_usage"]
        docker_status = docker_client.stats(container, stream=False)
        docker_CPU = 0.0
        delta_cpu = docker_status["cpu_stats"]["cpu_usage"]["total_usage"] - pre_CPU_usage
        delta_cpu_sys = docker_status["cpu_stats"]["system_cpu_usage"] - pre_CPU_sys_Usage
        if delta_cpu > 0 and delta_cpu_sys > 0:
            docker_CPU = float(delta_cpu) / float(delta_cpu_sys) * \
                         len(docker_status["cpu_stats"]["cpu_usage"]["percpu_usage"]) * 100.0
        IOs = docker_status["blkio_stats"]["io_service_bytes_recursive"]

        docker_IO = [sum([stat["value"] for stat in IOs if stat["op"] == "Read"]), \
                     sum([stat["value"] for stat in IOs if stat["op"] == "Write"])]

        data.append(
            {
                "measurement": "Docker",
                "tags": {
                    "Host": host,
                    "Source": "Docker",
                    "Container": container,
                },
                "fields": {
                    "PIDs": docker_status["pids_stats"]["current"],
                    "Memory": docker_status["memory_stats"]["usage"] / docker_status["memory_stats"]["limit"],
                    "CPU": docker_CPU,
                    "Disk Input": docker_IO[0],
                    "Disk Output": docker_IO[1]

                }
            }
        )



    data.append(
        {
            "measurement": "CPU",
            "tags": {
                "Host": host,
                "Source": "Host"
            },
            "fields": {
                "CPU": cpu_usage
            }
        },

        {
            "measurement": "Memory",
            "tags": {
                "Host": host,
                "Source": "Host"
            },
            "fields": {
                "Total": mem_total,
                "Available": mem_available,
                "Used Percentage": mem_usage

            }
        },

        {
            "measurement": "Disk",
            "tags": {
                "Host": host,
                "Disk": disk,
                "Source": "Host"
            },
            "fields": {
                "Total": disk_total,
                "Available": disk_available,
                "Used Percentage": disk_usage

            }
        },

        {
            "measurement": "Disk Throughput",
            "tags": {
                "Host": host,
                "Disk": disk,
                "Source": "Host"
            },
            "fields": {
                "Read": read_bytes_per_sec,
                "Write": write_bytes_per_sec
            }
        }


    )
    client.write_points(data)


client.close()
docker_client.close()