from os import listdir
from os.path import splitext, basename, join, isdir
from glob import iglob
from shutil import copytree

_BASE_DATA_PATH = "raw_data"
_TARGET_DIR = "data"

_BASE_IMAGE_PATH = join(_BASE_DATA_PATH, "images")

_BASE_DATASET_DIR = join(_BASE_DATA_PATH, "dataset")
_TARGET_DATASET_DIR = join(_TARGET_DIR, "dataset")

_CLASSES = [i for i in listdir(_BASE_IMAGE_PATH) if isdir(join(_BASE_IMAGE_PATH, i))]


def main(test_size: int):
    _create_test_train(test_size)
    _create_dataset_files()


def _create_test_train(test_size):
    file_train = open(join(_TARGET_DIR, "train.txt"), "w")
    file_val = open(join(_TARGET_DIR, "test.txt"), "w")
    counter = 1
    index_test = round(100 * test_size)

    for pathAndFilename in iglob(join(_BASE_DATASET_DIR, "*.jpg")):
        title, ext = splitext(basename(pathAndFilename))

        if counter == index_test:
            counter = 1
            file_val.write(f"{join(_BASE_DATASET_DIR, f'{title}.jpg')}\n")
        else:
            file_train.write(f"{join(_BASE_DATASET_DIR, f'{title}.jpg')}\n")
            counter += 1

    file_train.close()
    file_val.close()


def _create_dataset_files():
    data_file = join(_TARGET_DIR, "dataset.data")
    names_file = join(_TARGET_DIR, "dataset.names")

    with open(data_file, "w") as file:
        file.write(f"classes = {len(_CLASSES)}\n")
        file.write(f"train = {join('data', 'train.txt')}\n")
        file.write(f"valid = {join('data', 'test.txt')}\n")
        file.write(f"names = {join('data', 'dataset.names')}\n")
        file.write(f"backup = {join('darknet', 'backup')}")

    with open(names_file, "w") as file:
        for cls in _CLASSES:
            file.write(f"{cls}\n")

    copytree(_BASE_DATASET_DIR, _TARGET_DATASET_DIR)
