import harp
import harp.reader
from harp.reader import DeviceReader, _create_register_parser, _ReaderParams
from os import PathLike
from pathlib import Path
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import requests
from typing import TextIO
import io


def create_device(
    device_name: str, root_url: str = "https://raw.githubusercontent.com/harp-tech/device.{device_name}/main/device.yml"
):
    device_reader = create_reader(io.StringIO(get_device_yml(root_url.format(device_name=device_name))))
    return device_reader


def get_device_yml(url: str) -> str:
    r = requests.get(url, timeout=2)
    if r.status_code != 200:
        raise requests.exceptions.HTTPError(f"Failed to retrieve device YAML. Error code: {r.status_code}")
    else:
        return r.content.decode("utf-8")


def create_reader(
    device_yaml: TextIO,
    include_common_registers: bool = True,
    keep_type: bool = False,
) -> DeviceReader:

    device = harp.read_schema(device_yaml, include_common_registers)

    reg_readers = {
        name: _create_register_parser(device, name, _ReaderParams("", None, keep_type))
        for name in device.registers.keys()
    }
    return DeviceReader(device, reg_readers)


from typing import Optional, List
from os import PathLike
import glob
import json
import pandas as pd


def populate_software_events(target_folder="SoftwareEvents", root_path: PathLike = "."):
    _json_files = glob.glob(str(root_path / target_folder / "*.json"))
    return {Path(event).stem: parse_json(event) for event in _json_files}


def parse_json(path: PathLike):
    with open(path, "r") as f:
        data = pd.DataFrame([json.loads(event) for event in f.readlines()])
        data.rename(columns={"timestamp": "Seconds"}, inplace=True)
        data.set_index("Seconds", inplace=True)
    return data


def main():
    if len(sys.argv) < 2:
        print("Please provide a target path as an argument.")
        target_path = Path(r"C:\Users\bruno.cruz\Downloads\20240301T160321\20240301T160321")
        # return
    else:
        target_path = Path(sys.argv[1])


if __name__ == "__main__":
    main()
