from os import system
from os.path import join
from json import load

with open(join("utils", "yolo_v4", "model_config.json"), "r", encoding="utf8") as config_file:
    _CONFIG = load(config_file)

_CFG_LOCATION = "cfg"

_CFG_NAME = _CONFIG["config_file_name"]

_TRAIN_BATCHES = _CONFIG["training_cfg"]["batch"]
_TRAIN_SUBDIVISIONS = _CONFIG["training_cfg"]["subdivisions"]

_TEST_BATCHES = _CONFIG["testing_cfg"]["batch"]
_TEST_SUBDIVISIONS = _CONFIG["testing_cfg"]["subdivisions"]

_STATUS_PATH = join("utils", "yolo_v4", "status.txt")
with open(_STATUS_PATH, "r") as f:
    _CURRENT_STATUS = f.read().replace("\n", "")


def main():
    while True:
        response = input("\nWhat do you want to do? (train/test)\n")

        if response == "train":
            _train()
        elif response == "test":
            _test()
        else:
            print("Invalid Input")
            continue
        break


def _train():
    if _CURRENT_STATUS == "test":
        cmd = f"cd {_CFG_LOCATION};" \
              f"sed -i 's/batch={_TEST_BATCHES}/batch={_TRAIN_BATCHES}/' {_CFG_NAME};" \
              f"sed -i 's/subdivisions={_TEST_SUBDIVISIONS}/subdivisions={_TRAIN_SUBDIVISIONS}/' {_CFG_NAME};"
        system(cmd)

        with open(_STATUS_PATH, "w") as file:
            file.write("train")

    cmd = f"./darknet/darknet detector train data/dataset.data " \
          f"{join('cfg', _CFG_NAME)} darknet/yolov4.conv.137 -dont_show -map"
    system(cmd)


def _test():
    if _CURRENT_STATUS == "train":
        cmd = f"cd {_CFG_LOCATION};" \
              f"sed -i 's/batch={_TRAIN_BATCHES}/batch={_TEST_BATCHES}/' {_CFG_NAME};" \
              f"sed -i 's/subdivisions={_TRAIN_SUBDIVISIONS}/subdivisions={_TEST_SUBDIVISIONS}/' {_CFG_NAME};"
        system(cmd)

        with open(_STATUS_PATH, "w") as file:
            file.write("test")

    cmd = f"./darknet/darknet detector test data/dataset.data {join('cfg', _CFG_NAME)} " \
          f"{join('darknet', 'backup', 'yolov4-custom_best.weights')} test.jpg -thresh 0.3"
    system(cmd)
