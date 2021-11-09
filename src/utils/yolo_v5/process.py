from os import listdir
from os.path import join, isdir
from shutil import move

_BASE_IMAGE_PATH = join("raw_data", "images")
_CLASSES = [i for i in listdir(_BASE_IMAGE_PATH) if isdir(join(_BASE_IMAGE_PATH, i))]


def main():
    dataset_yaml = join("raw_data", "dataset",  "dataset.yaml")

    with open(dataset_yaml, "w") as file:
        file.write(f"train: {join('..', 'dataset', 'images', 'train')}\n")
        file.write(f"val: {join('..', 'dataset', 'images', 'test')}\n\n")
        file.write(f"nc: {len(_CLASSES)}\n\n")
        file.write(f"names: {_CLASSES}")

    move(join("raw_data", "dataset"), "dataset")
