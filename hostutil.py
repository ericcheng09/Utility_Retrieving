import psutil
import os


class HostUtil:

    def __init__(self, disk_paths, perdisk, disks):
        self.host = os.uname()[1]

        self.perdisk = perdisk
        self.disks = disks
        self.disk_paths = disk_paths
        self._disk_counters = []
        self._disk_prepocess()
        pass

    def _disk_prepocess(self):
        if self.perdisk:

            for disk in self.disks:
                self._disk_counters.append(tuple(psutil.disk_io_counters(perdisk=True)[disk]))
        else:
            self._disk_counters.append(tuple(psutil.disk_io_counters()))

    def get_data(self):

        data = []
        cpu_usage = psutil.cpu_percent()
        mem_total, mem_available, mem_usage = psutil.virtual_memory()[:3]
        data.append(
            {
                "measurement": "Host",
                "tags": {
                    "Host": self.host,
                },
                "fields": {
                    "CPU": cpu_usage,
                    "Total Memory": mem_total,
                    "Available Memory": mem_available,
                    "Used Memory Percentage": mem_usage
                }
            }
        )



        # CPU
        # cpu_usage = psutil.cpu_percent()
        # data.append(
        #     {
        #         "measurement": "CPU",
        #         "tags": {
        #             "Host": self.host,
        #             "Source": "Host"
        #         },
        #         "fields": {
        #             "CPU": cpu_usage
        #         }
        #     }
        # )

        # Memory
        # mem_total, mem_available, mem_usage = psutil.virtual_memory()[:3]
        # data.append(
        #     {
        #         "measurement": "Memory",
        #         "tags": {
        #             "Host": self.host,
        #             "Source": "Host"
        #         },
        #         "fields": {
        #             "Total": mem_total,
        #             "Available": mem_available,
        #             "Used Percentage": mem_usage
        #
        #         }
        #     }
        # )

        # # Disk usage
        # for disk_path in self.disk_paths:
        #
        #     disk_total, disk_used, disk_available, disk_usage = psutil.disk_usage(disk_path)[:]
        #     data.append(
        #         {
        #             "measurement": "Disk",
        #             "tags": {
        #                 "Host": self.host,
        #                 "Disk/Path": disk_path,
        #                 "Source": "Host"
        #             },
        #             "fields": {
        #                 "Total": disk_total,
        #                 "Used": disk_used,
        #                 "Available": disk_available,
        #                 "Used Percentage": disk_usage
        #
        #             }
        #         }
        #     )

        # # TODO: Definition of Throughput
        # # Disk throughput
        # if self.perdisk:                         
        #     for idx, disk in enumerate(self.disks):
        #         disk_IO = tuple(psutil.disk_io_counters(perdisk=True)[disk])
        #         read_bytes_per_sec = 0.0
        #         write_bytes_per_sec = 0.0
        #         if (disk_IO[4] - self._disk_counters[idx][4]) != 0:
        #             read_bytes_per_sec = (disk_IO[2] - self._disk_counters[idx][2]) / (
        #                         disk_IO[4] - self._disk_counters[idx][4]) * 1000
        #         if (disk_IO[5] - self._disk_counters[idx][5]) != 0:
        #             write_bytes_per_sec = (disk_IO[3] - self._disk_counters[idx][3]) / (
        #                         disk_IO[5] - self._disk_counters[idx][5]) * 1000
        #         self._disk_counters[idx] = disk_IO
        #         data.append(
        #             {
        #                 "measurement": "Disk Throughput",
        #                 "tags": {
        #                     "Host": self.host,
        #                     "Disk": self.disks[idx],
        #                     "Source": "Host"
        #                 },
        #                 "fields": {
        #                     "Read": read_bytes_per_sec,
        #                     "Write": write_bytes_per_sec
        #                 }
        #             }
        #         )
        # else:
        #     disk_IO = tuple(psutil.disk_io_counters())
        #     read_bytes_per_sec = 0.0
        #     write_bytes_per_sec = 0.0
        #     if (disk_IO[4] - self._disk_counters[0][4]) != 0:
        #         read_bytes_per_sec = (disk_IO[2] - self._disk_counters[0][2]) / (disk_IO[4] - self._disk_counters[0][4]) * 1000
        #     if (disk_IO[5] - self._disk_counters[0][5]) != 0:
        #         write_bytes_per_sec = (disk_IO[3] - self._disk_counters[0][3]) / (disk_IO[5] - self._disk_counters[0][5]) * 1000
        #     self._disk_counters[0] = disk_IO
        #     data.append(
        #         {
        #             "measurement": "Disk Throughput",
        #             "tags": {
        #                 "Host": self.host,
        #                 "Disk": self.disks[0],
        #                 "Source": "Host"
        #             },
        #             "fields": {
        #                 "Read": read_bytes_per_sec,
        #                 "Write": write_bytes_per_sec
        #             }
        #         }
        #     )

        return data
