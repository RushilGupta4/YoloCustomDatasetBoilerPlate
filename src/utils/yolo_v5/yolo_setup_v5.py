from json import load
from os import system, remove
from os.path import isdir, join, isfile
from shutil import rmtree

_BASE_DATASET_DIR = join("raw_data", "dataset")
_TARGET_DATASET_DIR = "dataset"

_BASE_YAML_PATH = join(_TARGET_DATASET_DIR, "dataset.yaml")
_TARGET_YAML_PATH = join("yolov5", "dataset.yaml")

with open(join("utils", "yolo_v5", "model_config.json"), "r") as f:
    _WEIGHTS = load(f)["weights"]


def main():
    _get_yolo()
    _clean_yolo_dir()


def _get_yolo():
    if isdir("yolov5"):
        print(
            f"Yolo v5 already exists, do you want to re download and make it? (y/n) "
        )
        response = input()
        if response.lower() != "y":
            quit()
        else:
            print("\nREINSTALLING YOLO v5")
            rmtree("yolov5")

    cmd = "git clone https://github.com/ultralytics/yolov5;" \
          "cd yolov5;" \
          "pip install -r requirements.txt;" \
          f"wget https://github.com/ultralytics/yolov5/releases/download/v6.0/{_WEIGHTS};" \
          "cd ..;"

    system(cmd)


def _clean_yolo_dir():
    folders = [".git", ".github"]
    files = [".pre-commit-config.yaml", ".dockerignore", ".gitignore", "CONTRIBUTING.md"]

    for folder in folders:
        path = join("yolov5", folder)
        if isdir(path):
            rmtree(path)

    for file in files:
        path = join("yolov5", file)
        if isfile(path):
            remove(path)
