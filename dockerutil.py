import docker
import os


class DockerUtil:

    def __init__(self, base_url, include_all, containers):

        self.client = docker.APIClient(base_url=base_url)
        if include_all:
            self.containers = [c["Id"] for c in self.client.containers()]
        else:
            self.containers = containers
        self.host = os.uname()[1]
        self.containers_status = {}
        for container in self.containers:
            self.containers_status[container] = self.client.stats(container, decode=True)

    def get_data(self):
        data = []
        for container in self.containers:
            try:
                status = self.containers_status[container].next()

                pre_cpu_usage, pre_cpu_sys_usage = status["cpu_stats"]["cpu_usage"]["total_usage"], \
                                                   status["cpu_stats"]["system_cpu_usage"]
                status = self.containers_status[container].next()

                CPU = 0.0
                delta_cpu = status["cpu_stats"]["cpu_usage"]["total_usage"] - pre_cpu_usage
                delta_cpu_sys = status["cpu_stats"]["system_cpu_usage"] - pre_cpu_sys_usage
                if delta_cpu > 0 and delta_cpu_sys > 0:
                    CPU = float(delta_cpu) / float(delta_cpu_sys) * \
                                 len(status["cpu_stats"]["cpu_usage"]["percpu_usage"]) * 100.0


                # bytes_io = status["blkio_stats"]["io_service_bytes_recursive"]
                read_docker, write_docker = 0, 0
                for stat in status["blkio_stats"]["io_service_bytes_recursive"]:
                    if stat["op"] == "Read":
                        read_docker += int(stat["value"])
                    elif stat["op"] == "Write":
                        write_docker += int(stat["value"])

                # readwrite = [sum([stat["value"] for stat in bytes_io if stat["op"] == "Read"]),
                #              sum([stat["value"] for stat in bytes_io if stat["op"] == "Write"])]
                data.append(
                    {
                        "measurement": "Docker",
                        "tags": {
                            "Host": self.host,
                            "Source": "Docker",
                            "Container": container,
                        },
                        "fields": {
                            "PIDs": status["pids_stats"]["current"],
                            "Memory": status["memory_stats"]["usage"] / status["memory_stats"]["limit"],
                            "CPU": CPU,
                            "Disk Read": read_docker,
                            "Disk Write": write_docker

                        }
                    }
                )
            except:
                print("Container {}'s status cannot be retrieved".format(container[:12]))
        return data
