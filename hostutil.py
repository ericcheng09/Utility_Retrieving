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

        disks = psutil.disk_partitions()
        for disk in disks:
            if disk[1] != None or disk[1] != "":
                # device = re.findall("/[a-zA-Z0-9]*")
                device_usage = psutil.disk_usage(disk[1])
                mega_byes = float(device_usage[0]) / 1024 / 1024
                if mega_byes < 1024:
                    field[disk[0] + " Usage ({} MiB)".format(round(mega_byes, 2))] = device_usage[3]
                else:
                    field[disk[0] + " Usage ({} GiB)".format(round(mega_byes/1024, 2))] = device_usage[3]
                capacity =  float(device_usage[0]) / 1024 / 1024/ 1024# convert to Gib
                field[disk[0] + " Usage ({} GiB)".format(capacity)] = device_usage[3]



        # disk_IO = tuple(psutil.disk_io_counters(perdisk=True))
        disk_IO = psutil.disk_io_counters(perdisk=True)
        # ex:
        # {'disk0': sdiskio(read_count=12851269, write_count=11015139, read_bytes=337039777792, write_bytes=307435831296, read_time=7224758, write_time=2460473)}
        for disk, values in disk_IO.items():
            # values_tuple = tuple(values)
            field[disk + "_Read"] = values[2]
            field[disk + "_Write"] = values[3]

        data.append(
            {
                "measurement": "Host",
                "tags": {
                    "Host": self.host,
                },
                "fields": field
            }
        )


        return data
