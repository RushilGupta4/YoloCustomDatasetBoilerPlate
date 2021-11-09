from json import load
from utils.yolo_v4 import yolo_setup_v4
from utils.yolo_v5 import yolo_setup_v5


with open("config.json", "r") as file:
    _CONFIG = load(file)

_YOLO_VERSION = _CONFIG["yolo_version"]
_TRAIN_SIZE = _CONFIG["training_size"]
_TEST_SIZE = 1 - _TRAIN_SIZE


def main():
    if _YOLO_VERSION == 4:
        yolo_setup_v4.main()

    elif _YOLO_VERSION == 5:
        yolo_setup_v5.main()


if __name__ == '__main__':
    main()