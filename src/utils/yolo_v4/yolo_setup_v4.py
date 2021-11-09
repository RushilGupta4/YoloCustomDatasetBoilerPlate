from os import system, environ, pathsep, listdir, remove, mkdir
from os.path import isdir, join
from shutil import rmtree
from json import load

with open("config.json", "r", encoding="utf8") as config_file:
    _CONFIG = load(config_file)

with open(join("utils", "yolo_v4", "model_config.json"), "r", encoding="utf8") as config_file:
    _CONFIG_FILE_NAME = load(config_file)["config_file_name"]

environ["PATH"] += pathsep + _CONFIG["cuda_path"]

_CFG_DIR = join("darknet", "cfg")
_CFG_FILE_PATH = join(_CFG_DIR, _CONFIG_FILE_NAME)
_TARGET_CFG_FILE_PATH = join("cfg", _CONFIG_FILE_NAME)

_DARKNET_DATA_DIR = join("darknet", "data")

_BASE_IMAGE_PATH = join("raw_data", "images")
_CLASSES = [i for i in listdir(_BASE_IMAGE_PATH) if isdir(join(_BASE_IMAGE_PATH, i))]

_STATUS_PATH = join("utils", "yolo_v4", "status.txt")


def main():
    if isdir("cfg"):
        rmtree("cfg")
    mkdir("cfg")

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

    cmd = "git clone https://github.com/AlexeyAB/darknet;" \
          "cd darknet;" \
          "sed -i 's/OPENCV=0/OPENCV=1/' Makefile;" \
          "sed -i 's/GPU=0/GPU=1/' Makefile;" \
          "sed -i 's/CUDNN=0/CUDNN=1/' Makefile;" \
          "sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile;" \
          "sed -i 's/LIBSO=0/LIBSO=1/' Makefile;" \
          "make;" \
          "wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137;" \
          "chmod +x ./darknet"

    system(cmd)


def _remove_files():
    git_folder = join("darknet", ".git")

    if isdir(git_folder):
        rmtree(git_folder)

    rmtree(_DARKNET_DATA_DIR)

    for file in listdir(_CFG_DIR):
        if file == _CONFIG_FILE_NAME:
            continue
        if isdir(join(_CFG_DIR, file)):
            rmtree(join(_CFG_DIR, file))
        else:
            remove(join(_CFG_DIR, file))


def _setup_cfg_file():

    max_batches = max(6000, len(_CLASSES) * 2000)

    with open(join("utils", "yolo_v4", "model_config.json"), "r") as f:
        model_cfg = load(f)

    with open(_CFG_FILE_PATH, "r") as cfg_file:
        cfg = cfg_file.read().split("\n")

    replace_dict = {
        "activation=linear": "activation=relu",
        "learning_rate": f"learning_rate={model_cfg['learning_rate']}",
        "max_batches": f"max_batches={max_batches}",
        "steps": f"steps={int(0.8 * max_batches)},{int(0.9 * max_batches)}",
        "width": f"width={model_cfg['image_width']}",
        "height": f"height={model_cfg['image_height']}",
        "batch": f"batch={model_cfg['training_cfg']['batch']}",
        "subdivisions": f"subdivisions={model_cfg['training_cfg']['subdivisions']}",
        "channels": f"channels={model_cfg['channels']}",
    }

    for i, line in enumerate(cfg):
        if line == "[yolo]":
            while True:
                i -= 1
                if "filters" in cfg[i] and "=" in cfg[i]:
                    cfg[i] = f"filters={(len(_CLASSES) + 5) * 3}"
                    break

            while True:
                i += 1
                if "classes" in cfg[i] and "=" in cfg[i]:
                    cfg[i] = f"classes={len(_CLASSES)}"
                    break

            continue

        for replace_from, replace_to in replace_dict.items():
            if replace_from + "=" in line or replace_from + " =" in line:
                cfg[i] = replace_to

    final = "\n".join(cfg)

    with open(_TARGET_CFG_FILE_PATH, "w") as cfg_file:
        cfg_file.write(final)

    with open(_STATUS_PATH, "w") as file:
        file.write("train")


if __name__ == '__main__':
    main()
