from json import load
from utils.yolo_v4 import run as run_v4
from utils.yolo_v5 import run as run_v5

with open("config.json", "r") as file:
    _YOLO_VERSION = load(file)["yolo_version"]


def main():
    if _YOLO_VERSION == 4:
        run_v4.main()

    elif _YOLO_VERSION == 5:
        run_v5.main()


if __name__ == '__main__':
    main()