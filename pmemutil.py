import os
import subprocess
import re


class PMEM():

    def __init__(self):
        self.host = os.uname()[1]
        self.command = "ipmctl show -performance MediaReads,MediaWrites"


    def get_data(self):
        data = []
        output = str(subprocess.check_output(self.command, shell=True))
        data_dict = {}
        for s in output.split("\\n"):
            key = re.findall("[a-zA-Z]+=", s)[0]
            key = key[:len(key) - 1]
            value = re.findall("=[a-zA-Z0-9]+", s)[0][1:]
            data_dict[key] = data_dict.get(key, default=[]).append(int(value, 0) * 64)


        for idx in range(len(data_dict["DimmID"])):


            data.append(
                {
                    "measurement": "PMEM",
                    "tags": {
                        "Host": self.host,
                        "DIMM": data_dict["DimmID"][idx],
                        "Source": "PMEM"
                    },
                    "fields": {
                        "MediaReads": data_dict["MediaReads"][idx],
                        "MediaWrites": data_dict["MediaWrites"][idx]
                    }
                }
            )
        return data
