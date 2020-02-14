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

    def get_data(self):
        data = []
        for container in self.containers:
            try:
                status = self.client.stats(container, stream=False)

                pre_cpu_usage, pre_cpu_sys_Usage = status["cpu_stats"]["cpu_usage"]["total_usage"], \
                                                   status["cpu_stats"]["system_cpu_usage"]
                status = self.client.stats(container, stream=False)
                CPU = 0.0
                delta_cpu = status["cpu_stats"]["cpu_usage"]["total_usage"] - pre_cpu_usage
                delta_cpu_sys = status["cpu_stats"]["system_cpu_usage"] - pre_cpu_sys_Usage
                if delta_cpu > 0 and delta_cpu_sys > 0:
                    CPU = float(delta_cpu) / float(delta_cpu_sys) * \
                                 len(status["cpu_stats"]["cpu_usage"]["percpu_usage"]) * 100.0
                bytes_io = status["blkio_stats"]["io_service_bytes_recursive"]

                readwrite = [sum([stat["value"] for stat in bytes_io if stat["op"] == "Read"]),
                             sum([stat["value"] for stat in bytes_io if stat["op"] == "Write"])]
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
                            "Disk Input": readwrite[0],
                            "Disk Output": readwrite[1]

                        }
                    }
                )
            except:
                print("Container {}'s status cannot be retrieved".format(container[:12]))
        return data
