from os import listdir, makedirs
from os.path import join, isdir
from shutil import copy

_BASE_DATA_DIR = "raw_data"
_BASE_IMAGES_DIR = join(_BASE_DATA_DIR, "images")
_BASE_LABELS_DIR = join(_BASE_DATA_DIR, "labels")
_TARGET_DIR = join(_BASE_DATA_DIR, "dataset")

if not isdir(_TARGET_DIR):
    makedirs(_TARGET_DIR)

_CLASSES = [i for i in listdir(_BASE_IMAGES_DIR) if isdir(join(_BASE_IMAGES_DIR, i))]


def main(train_size):
    images = {file: join(_BASE_IMAGES_DIR, cls, file) for cls in _CLASSES for file in
              listdir(join(_BASE_IMAGES_DIR, cls)) if file.endswith(".jpg")}

    labels = {file: join(_BASE_LABELS_DIR, cls, file) for cls in _CLASSES for file in
              listdir(join(_BASE_LABELS_DIR, cls)) if file.endswith(".txt")}

    train_size = int(len(images) * train_size)

    images_path = join(_TARGET_DIR, "images")
    labels_path = join(_TARGET_DIR, "labels")

    train_images_path = join(images_path, "train")
    train_labels_path = join(labels_path, "train")

    test_images_path = join(images_path, "test")
    test_labels_path = join(labels_path, "test")

    for i in [train_images_path, train_labels_path, test_images_path, test_labels_path]:
        if not isdir(i):
            makedirs(i)

    for idx, file_data in enumerate(images.items()):
        file_jpg, file_jpg_path = file_data
        file_txt = file_jpg.replace(".jpg", ".txt")
        file_txt_path = labels[file_txt]

        if idx < train_size:
            copy(file_jpg_path, join(train_images_path, file_jpg))
            copy(file_txt_path, join(train_labels_path, file_txt))
        else:
            copy(file_jpg_path, join(test_images_path, file_jpg))
            copy(file_txt_path, join(test_labels_path, file_txt))
