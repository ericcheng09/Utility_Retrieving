import psutil
import os
import re


class HostUtil:

    def __init__(self):
        self.host = os.uname()[1]

    def get_data(self):
        data = []
        field = {}
        cpu_usage = psutil.cpu_percent()
        mem_total, mem_available, mem_usage = psutil.virtual_memory()[:3]
        field["CPU"] = cpu_usage
        field["Total Memory"] = mem_total
        field["Available Memory"] = mem_available
        field["Used Memory Percentage"] = mem_usage
        data.append(
            {
                "measurement": "Host",
                "tags": {
                    "Host": self.host,
                },
                "fields": field
            }
        )

        disks = psutil.disk_partitions()
        for disk in disks:
            device = disk[0].split("/")[-1]
            if disk[1] != None and disk[1] != "" and not device.startswith("loop"):
            # if disk[1] != None and disk[1] != "":
                device_usage = psutil.disk_usage(disk[1])
                data.append(
                    {
                        "measurement": "Disk",
                        "tags": {
                            "Host": self.host,
                            "Device": disk[0]
                        },
                        "fields": {
                            "Total": device_usage[0],
                            "Free": device_usage[2],
                            "Usage": device_usage[3]
                        }
                    }
                )

        disk_IO = psutil.disk_io_counters(perdisk=True)
        # ex:
        # {'disk0': sdiskio(read_count=12851269, write_count=11015139, read_bytes=337039777792, write_bytes=307435831296, read_time=7224758, write_time=2460473)}
        for disk, values in disk_IO.items():
            if not disk.startswith("loop"):
                data.append(
                    {
                        "measurement": "Disk IO",
                        "tags": {
                            "Host": self.host,
                            "Disk": disk
                        },
                        "fields": {
                            "Read": values[2],
                            "Write": values[3]
                        }
                    }
                )

        return data
