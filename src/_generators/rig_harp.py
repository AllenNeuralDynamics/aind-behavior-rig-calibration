import datetime
import os
from typing import TypedDict

import jinja2
import requests
import yaml

WHOAMI_REMOTE = "https://raw.githubusercontent.com/harp-tech/protocol/refs/heads/main/whoami.yml"


class HarpBoard(TypedDict):
    name: str
    whoami: int
    is_clock: bool
    class_name: str


def fetch_who_am_i_list(remote: str = WHOAMI_REMOTE) -> dict:
    response = requests.get(remote)
    response.raise_for_status()
    parsed = yaml.load(response.content, Loader=yaml.FullLoader)["devices"]
    return {whoami: name for whoami, name in zip(parsed.keys(), map(lambda x: x.get("name"), parsed.values()))}


def sanitize_to_pascal_case(name: str) -> str:
    if not name.isalnum() or not name[0].isupper():
        name = "".join(word.capitalize() for word in name.split("_"))
    return name


clock_boards = ["ClockSynchronizer", "TimestampGeneratorGen1", "TimestampGeneratorGen3", "WhiteRabbit"]
boards = [
    HarpBoard(name=name, whoami=whoami, is_clock=name in clock_boards, class_name=sanitize_to_pascal_case(name))
    for whoami, name in fetch_who_am_i_list().items()
]


def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(current_directory, "templates")))
    template = environment.get_template("harp.j2")

    template.stream(generation_time=datetime.datetime.now(datetime.timezone.utc), boards=boards).dump(
        os.path.join(current_directory, "../../src/aind_behavior_services/rig/_harp_gen.py")
    )


if __name__ == "__main__":
    main()
