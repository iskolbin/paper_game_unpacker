# Needed:
#   1. PDF with paper-game (from printgames.ru, for instance)
#   2. Config in JSON

from PIL import Image
from PIL import ImageDraw
from sys import argv
import pdf2image
import json
import os

pdf_path, config_path = argv[1], argv[2]

with open(config_path, "r") as f:
    config = json.load(f)

if "name" in config and not os.path.exists(config["name"]):
    os.makedirs(config["name"])

print("Converting PDF to list of images")
images = pdf2image.convert_from_path(pdf_path)

def img_out_path(name):
    return ((config["name"] + "/") if "name" in config else "") + name + ".png"

def process_grid(img, conf, idx):
    direction = conf.get("direction", [1, 1])
    xy = conf.get("xy", [0, 0])
    spacing = conf.get("spacing", [0, 0])
    dim = conf["dim"]
    naming = conf["naming"]
    naming_counter = conf.get("naming_counter", 0)
    size = conf["size"]
    col_it = range(dim[0]) if direction[0] > 0 else range(dim[0] - 1, -1, -1)
    row_it = range(dim[1]) if direction[1] > 0 else range(dim[1] - 1, -1, -1)
    i = 0
    for col in col_it:
        for row in row_it:
            x, y = xy[0] + col * (size[0] + spacing[0]), xy[1] + row * (size[1] + spacing[1])
            name = naming.format(naming_counter)
            out_path = img_out_path(name)
            print("  Writing image {} of {} to {}".format(i + 1, dim[0] * dim[1], out_path))
            naming_counter += 1
            img.crop((x, y, x + size[0], y + size[1])).save(out_path, "PNG")
            i = i + 1

def process_custom(img, conf, idx):
    i = 0
    for name, rect in conf["images"].items():
        out_path = img_out_path(name)
        print("  Writing image {} of {} to {}".format(i + 1, len(conf["images"]), out_path))
        img.crop(tuple(rect)).save(out_path, "PNG")
        i = i + 1

def process_page(img, conf, idx):
    if conf["type"] == "grid": process_grid(img, conf, idx)
    elif conf["type"] == "custom": process_custom(img, conf, idx)

for i, page_conf in enumerate(config["pages"]):
    print("Processing {} of {}".format(i + 1, len(config["pages"])))
    if len(page_conf) == 0: continue
    process_page(images[i], page_conf, i)
