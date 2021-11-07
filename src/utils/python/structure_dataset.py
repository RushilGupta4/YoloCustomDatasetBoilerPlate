from os import listdir, remove, makedirs
from os.path import join, isdir, splitext
from glob import glob
from shutil import copy


_BASE_DATA_DIR = "raw_data"
_BASE_IMAGES_DIR = join(_BASE_DATA_DIR, "images")
_BASE_LABELS_DIR = join(_BASE_DATA_DIR, "labels")
_TARGET_DIR = join(_BASE_DATA_DIR, "dataset")

if not isdir(_TARGET_DIR):
    makedirs(_TARGET_DIR)

_CLASSES = [i for i in listdir(_BASE_IMAGES_DIR) if isdir(join(_BASE_IMAGES_DIR, i))]


def main():

    old_files = [join(_TARGET_DIR, i) for i in listdir(_TARGET_DIR) if i != ".gitignore"]
    for old_file in old_files:
        remove(old_file)

    for cls in _CLASSES:
        cls_img_path = join(_BASE_IMAGES_DIR, cls)
        cls_labels_path = join(_BASE_LABELS_DIR, cls)

        images = [img for img in listdir(cls_img_path) if img.endswith(".jpg")]

        for image in images:
            name = len(glob(join(_TARGET_DIR, "*.jpg")))

            img_source = join(cls_img_path, image)
            img_destination = join(_TARGET_DIR, f"{name}.jpg")

            label_source = join(cls_labels_path, f"{splitext(image)[0]}.txt")
            label_destination = join(_TARGET_DIR, f"{name}.txt")

            copy(img_source, img_destination)
            copy(label_source, label_destination)


if __name__ == '__main__':
    main()
