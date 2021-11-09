from json import load
from os import system, listdir
from os.path import join


with open(join("utils", "yolo_v5", "model_config.json"), "r") as cfg:
    _CONFIG = load(cfg)

_WEIGHTS = _CONFIG["weights"]
_IMG_SIZE = _CONFIG["img_size"]
_BATCH_SIZE = _CONFIG["batch_size"]
_EPOCHS = _CONFIG["epochs"]
_CFG = _CONFIG["cfg_file"]

_YOLO_TRAIN_DIR = join("yolov5", "runs", "train")
try:
    _TRAINED_WEIGHTS = join("runs", "train", f"exp{len(listdir(_YOLO_TRAIN_DIR))}", "weights", "best.pt")
except FileNotFoundError:
    _TRAINED_WEIGHTS = _WEIGHTS


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
    cmd = "cd yolov5;" \
          f"python train.py --img {_IMG_SIZE} --batch {_BATCH_SIZE} --epochs {_EPOCHS} " \
          f"--data ../dataset/dataset.yaml --weights {_WEIGHTS} --cfg {_CFG}"

    system(cmd)


def _test():
    cmd = "cd yolov5;" \
          f"python detect.py --img {_IMG_SIZE} --weights {_TRAINED_WEIGHTS}"

    system(cmd)
