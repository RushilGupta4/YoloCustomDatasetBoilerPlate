"""

This script is to convert the txt annotation files to appropriate format needed by YOLO

"""

from os import listdir, makedirs
from os.path import join, splitext, isdir
from PIL import Image


_BASE_DATA_PATH = "raw_data"
_BASE_IMAGE_PATH = join(_BASE_DATA_PATH, "images")
_BASE_LABEL_PATH = join(_BASE_DATA_PATH, "labels")
_CLASSES = [i for i in listdir(_BASE_IMAGE_PATH) if isdir(join(_BASE_IMAGE_PATH, i))]


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return x, y, w, h


def main():

    for cls_id, cls in enumerate(_CLASSES):
        print(f"\nStarting Operations For Class - {cls}")

        mypath = join(_BASE_IMAGE_PATH, cls)
        outpath = join(_BASE_LABEL_PATH, cls)

        if not isdir(outpath):
            makedirs(outpath)

        """ Get input text file list """
        txt_name_list = [i for i in listdir(mypath) if i.endswith(".txt") and i != "images_list.txt"]

        """ Process """
        for idx, txt_name in enumerate(txt_name_list):
            print(f"Class {cls} | File {idx + 1}")

            """ Open input text files """
            txt_path = join(mypath, txt_name)
            txt_file = open(txt_path, "r")
            lines = txt_file.read().split('\n')

            """ Open output text files """
            txt_outpath = join(outpath, txt_name)
            txt_outfile = open(txt_outpath, "w")

            """ Convert the data to YOLO format """
            ct = 0
            for line in lines:
                if len(line) >= 2:
                    ct += 1
                    elems = line.split(' ')

                    xmin = elems[0]
                    xmax = elems[2]
                    ymin = elems[1]
                    ymax = elems[3]

                    img_path = join(_BASE_IMAGE_PATH, cls, f"{splitext(txt_name)[0]}.jpg")
                    im = Image.open(img_path)
                    w = int(im.size[0])
                    h = int(im.size[1])

                    b = (float(xmin), float(xmax), float(ymin), float(ymax))
                    bb = convert((w, h), b)

                    txt_outfile.write(f"{cls_id} {' '.join([str(a) for a in bb])}\n")