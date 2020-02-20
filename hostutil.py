import psutil
import os


class HostUtil:

    def __init__(self, disk_paths, perdisk, disks):
        self.host = os.uname()[1]
        self.perdisk = perdisk
        self.disks = disks
        self.disk_paths = disk_paths

    def get_data(self):
        data = []
        field = {}
        cpu_usage = psutil.cpu_percent()
        mem_total, mem_available, mem_usage = psutil.virtual_memory()[:3]
        field["CPU"] = cpu_usage
        field["Total Memory"] = mem_total
        field["Available Memory"] = mem_available
        field["Used Memory Percentage"] = mem_usage

        disk_IO = tuple(psutil.disk_io_counters(perdisk=True))
        # ex:
        # {'disk0': sdiskio(read_count=12851269, write_count=11015139, read_bytes=337039777792, write_bytes=307435831296, read_time=7224758, write_time=2460473)}
        for disk, values in disk_IO:
            values_tuple = tuple(values)
            field[disk + "_Read"] = values_tuple[2]
            field[disk + "_Write"] = values_tuple[3]

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
