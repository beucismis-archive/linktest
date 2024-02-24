import re
from urllib3 import PoolManager

import constants


output = str()
total_dead_link = 0
http = PoolManager()


def generate_output(output: str) -> None:
    print(
        (
            "\n=========================> LINKTEST <========================="
            f"\n\n{output}\n\n"
            "==============================================================\n"
        ).expandtabs(2)
    )


def main():
    for path in constants.FILE_PATHS:
        output += f"FILE: {path}\n"

        with open(path) as file:
            matches = re.findall(constants.URL_REGEX, file.read())

        if not len(matches):
            output += "\tLink not found!\n"
            continue

        for link in matches:
            response = http.request("GET", link)

            if response.status != 200:
                total_dead_link += 1
                output += f"\t{link} - STATUS: {response.status}\n"

    if not bool(dead_link):
        generate_output("All links are good!")
    else:
        generate_output(f"{output}\nERROR: {total_dead_link} dead links found!")
        exit(1)


if __name__ == "__main__":
    main()
