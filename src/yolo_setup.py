from os import system, environ, pathsep, listdir, remove, mkdir
from os.path import isdir, join
from shutil import rmtree
from json import load


with open("config.json", "r", encoding="utf8") as config_file:
    _CONFIG = load(config_file)

environ["PATH"] += pathsep + _CONFIG["cuda_path"]

_CFG_DIR = join("darknet", "cfg")
_CFG_FILE_PATH = join(_CFG_DIR, "yolov4-custom.cfg")
_TARGET_CFG_FILE_PATH = join("cfg", "yolov4-custom.cfg")

_DARKNET_DATA_DIR = join("darknet", "data")

_BASE_IMAGE_PATH = join("raw_data", "images")
_CLASSES = [i for i in listdir(_BASE_IMAGE_PATH) if isdir(join(_BASE_IMAGE_PATH, i))]

for folder in ["data", "cfg"]:
    if not isdir(folder):
        mkdir(folder)


def main():
    _make_darknet()
    _remove_files()
    _setup_cfg_file()


def _make_darknet():
    if isdir("darknet"):
        print(
            f"Darknet already exists, do you want to re download and make it? (y/n) "
        )
        response = input()
        if response.lower() != "y":
            quit()
        else:
            print("\nREINSTALLING DARKNET (YOLO v4)")
            rmtree("darknet")

    system(f"bash {join('utils', 'bash', 'yolo_setup.sh')}")


def _remove_files():
    git_folder = join("darknet", ".git")

    if isdir(git_folder):
        rmtree(git_folder)

    rmtree(_DARKNET_DATA_DIR)

    for file in listdir(_CFG_DIR):
        if file == "yolov4-custom.cfg":
            continue
        if isdir(join(_CFG_DIR, file)):
            rmtree(join(_CFG_DIR, file))
        else:
            remove(join(_CFG_DIR, file))


def _setup_cfg_file():

    model_config = _CONFIG["model_config"]

    with open(_CFG_FILE_PATH, "r") as cfg_file:
        cfg = cfg_file.read().split("\n")

    max_batches = max(6000, len(_CLASSES) * 2000)
    cfg[5] = f"batch={model_config['training_cfg']['batch']}"
    cfg[6] = f"subdivisions={model_config['training_cfg']['subdivisions']}"
    cfg[7] = f"width={model_config['image_width']}"
    cfg[8] = f"height={model_config['image_height']}"
    cfg[9] = f"channels={model_config['channels']}"
    cfg[19] = f"max_batches={max_batches}"
    cfg[21] = f"steps={int(0.8 * max_batches)},{int(0.9 * max_batches)}"

    for i, line in enumerate(cfg):
        if line == "[yolo]":
            cfg[i - 4] = f"filters={(len(_CLASSES) + 5) * 3}"
            cfg[i + 3] = f"classes={len(_CLASSES)}"
            continue

        if line == "activation=linear":
            cfg[i] = "activation=relu"

    final = "\n".join(cfg)

    with open(_TARGET_CFG_FILE_PATH, "w") as cfg_file:
        cfg_file.write(final)


if __name__ == '__main__':
    main()