from os import system
from os.path import join
from json import load

with open("config.json", "r", encoding="utf8") as config_file:
    _CONFIG = load(config_file)["model_config"]

_CFG_LOCATION = join("darknet", "cfg")
_CFG_NAME = "yolov4-custom.cfg"

_TRAIN_BATCHES = _CONFIG["training_cfg"]["batch"]
_TRAIN_SUBDIVISIONS = _CONFIG["training_cfg"]["subdivisions"]

_TEST_BATCHES = _CONFIG["testing_cfg"]["batch"]
_TEST_SUBDIVISIONS = _CONFIG["testing_cfg"]["subdivisions"]


def main():
    train, test = False, False

    while True:
        response = input("\nWhat mode do you want to use? (train/test)\n")

        if response == "train":
            train = True
        elif response == "test":
            test = True
        else:
            print("Invalid Input")
            continue
        break

    if train:
        cmd = f"cd {_CFG_LOCATION};" \
              f"sed -i 's/batch={_TEST_BATCHES}/batch={_TRAIN_BATCHES}/' {_CFG_NAME};" \
              f"sed -i 's/subdivisions={_TEST_SUBDIVISIONS}/subdivisions={_TRAIN_SUBDIVISIONS}/' {_CFG_NAME};"

        system(cmd)
        return

    if test:
        cmd = f"cd {_CFG_LOCATION};" \
              f"sed -i 's/batch={_TRAIN_BATCHES}/batch={_TEST_BATCHES}/' {_CFG_NAME};" \
              f"sed -i 's/subdivisions={_TRAIN_SUBDIVISIONS}/subdivisions={_TEST_SUBDIVISIONS}/' {_CFG_NAME};"
        system(cmd)
        return


if __name__ == '__main__':
    main()
