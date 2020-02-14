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
        keys = re.findall("[a-zA-Z]+=", output)
        values = re.findall("=[a-zA-Z0-9]+", output)

        for idx, key in enumerate(keys):
            tmp = data_dict.get(key[:len(key) - 1], [])
            tmp.append(values[idx][1:])
            data_dict[key[:len(key) - 1]] = tmp

        for idx, Dimm in enumerate(data_dict["DimmID"]):
            data.append(
                {
                    "measurement": "PMEM",
                    "tags": {
                        "Host": self.host,
                        "DIMM": Dimm,
                        "Source": "PMEM"
                    },
                    "fields": {
                        "MediaReads": int(data_dict["MediaReads"][idx], 0) * 64,
                        "MediaWrites": int(data_dict["MediaWrites"][idx], 0) * 64
                    }
                }
            )
        return data
