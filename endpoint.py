import re
from urllib3 import PoolManager

import constant


def generate_output(verbose: str) -> None:
    output = (
        "\n=========================> LINKTEST <=========================\n\n"
        f"{verbose}"
        "\n\n==============================================================\n"
    )
    print(output.expandtabs(2))


def main() -> None:
    verbose = ""
    dead_link = 0
    http = PoolManager()

    for path in constant.FILE_PATH:
        verbose += f"FILE: {path}\n"

        with open(path) as file:
            matches = re.findall(constant.URL_REGEX, file.read())

        if not len(matches):
            verbose += "\tLink not found!\n"
            continue

        for link in matches:
            response = http.request("GET", link)

            if response.status != 200:
                dead_link += 1
                verbose += f"\t{link} - STATUS: {response.status}\n"

    if not bool(dead_link):
        generate_output("All links are good!")
    else:
        generate_output(f"{verbose}\nERROR: {dead_link} dead links found!")
        exit(1)


if __name__ == "__main__":
    main()
