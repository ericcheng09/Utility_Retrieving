import psutil
import os


class HostUtil:

    def __init__(self, paths, perdisk, disks):
        pass

    def get_data(self):
        data = []

        host = os.uname()[1]
        # disk_IO = tuple(psutil.disk_io_counters(perdisk=True)[disk])
        # read_bytes, read_time = disk_IO[2], disk_IO[4]
        # write_bytes, write_time = disk_IO[3], disk_IO[5]


        cpu_usage = psutil.cpu_percent()

        mem_total, mem_available, mem_usage = psutil.virtual_memory()[:3]

        disk_total, disk_available, disk_usage = (psutil.disk_usage(path)[0], \
                                                  psutil.disk_usage(path)[1], psutil.disk_usage(path)[3])

        # disk_IO = tuple(psutil.disk_io_counters(perdisk=True)[disk])
        #
        # read_bytes_per_sec = 0.0
        # write_bytes_per_sec = 0.0
        # if (disk_IO[4] - read_time) != 0:
        #     read_bytes_per_sec = (disk_IO[2] - read_bytes) / (disk_IO[4] - read_time) * 1000
        # if (disk_IO[5] - write_time) != 0:
        #     write_bytes_per_sec = (disk_IO[3] - write_bytes) / (disk_IO[5] - write_time) * 1000
        #
        # read_bytes, read_time = disk_IO[2], disk_IO[4]
        # write_bytes, write_time = disk_IO[3], disk_IO[5]



        return data
