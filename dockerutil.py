import docker
import os


class DockerUtil:

    def __init__(self, base_url, include_all, containers):
        self.client = docker.APIClient(base_url=base_url)
        if include_all:
            # include all containers
            self.containers = [c["Id"] for c in self.client.containers()]
        else:
            # include specific containers listed in config.ini
            self.containers = containers
        self.host = os.uname()[1]
        self.containers_status = {}
        for container in self.containers:
            self.containers_status[container] = self.client.stats(container, decode=True)

    def get_data(self):
        data = []
        for container in self.containers:
            try:

                # Get CPU info
                status = self.containers_status[container].next()
                pre_cpu_usage, pre_cpu_sys_usage = status["cpu_stats"]["cpu_usage"]["total_usage"], \
                                                   status["cpu_stats"]["system_cpu_usage"]
                status = self.containers_status[container].next()

                # total_usage       : CPU usage by container
                # system_cpu_usage  : CPU usage of entire system
                # it needs to be multiplied by num of core, so for a 4 cores, CPU usage can be 0% to 400%
                CPU = 0.0
                delta_cpu = status["cpu_stats"]["cpu_usage"]["total_usage"] - pre_cpu_usage
                delta_cpu_sys = status["cpu_stats"]["system_cpu_usage"] - pre_cpu_sys_usage
                if delta_cpu > 0 and delta_cpu_sys > 0:
                    CPU = float(delta_cpu) / float(delta_cpu_sys) * status["cpu_stats"]["online_cpus"] * 100.0

                # Get Read/Write info
                read_docker, write_docker = 0, 0
                for stat in status["blkio_stats"]["io_service_bytes_recursive"]:
                    if stat["op"] == "Read":
                        read_docker += int(stat["value"])
                    elif stat["op"] == "Write":
                        write_docker += int(stat["value"])

                data.append(
                    {
                        "measurement": "Docker",
                        "tags": {
                            "Host": self.host,
                            "Container": container,
                        },
                        "fields": {
                            "PIDs": status["pids_stats"]["current"],
                            # get Memory Usage
                            "Memory": float(status["memory_stats"]["usage"]) / float(status["memory_stats"]["limit"]) * 100.0,
                            "CPU": CPU,
                            "Disk Read": read_docker,
                            "Disk Write": write_docker

                        }
                    }
                )
            except Exception as e:
                print(e)
                print("Container {}'s status cannot be retrieved".format(container[:12]))
        return data
