from json import load
from utils.common import bbox_tool, convert


with open("config.json", "r") as file:
    _CONFIG = load(file)

_YOLO_VERSION = _CONFIG["yolo_version"]
_TRAIN_SIZE = _CONFIG["training_size"]
_TEST_SIZE = 1 - _TRAIN_SIZE


def main():
    bbox_tool.main()
    convert.main()

    if _YOLO_VERSION == 4:
        _yolo_v4()

    elif _YOLO_VERSION == 5:
        _yolo_v5()


def _yolo_v4():
    from utils.yolo_v4 import structure_dataset, process

    structure_dataset.main()
    process.main(_TEST_SIZE)


def _yolo_v5():
    from utils.yolo_v5 import structure_dataset, process

    structure_dataset.main(_TRAIN_SIZE)
    process.main()


if __name__ == '__main__':
    main()