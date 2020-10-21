"""convert_coco2binary_taks.py
Convert the 81 classes in coco annotations to {0, 1} for foreground/background classification task.
"""
__author__ = "Yang Liu"
__email__ = "lander14@outlook.com"

import json
import os
import sys


def convert(fpath: str, out: str):
    with open(fpath, 'r') as f:
        data = json.load(f)

    for i, _ in enumerate(data['annotations']):
        if data['annotations'][i]['category_id'] > 81:
            print(data['annotations'][i])
            sys.exit()
        data['annotations'][i]['category_id'] = 1

    # # store as new json file
    # with open(out, 'w') as f:
    #     json.dump(data, f)
    print("done")


if __name__ == "__main__":
    root_dir = "/home/kloping/OpenSet_MOT/data/coco/annotations/"
    train_set = "instances_train2017.json"
    val_set = "instances_val2017.json"

    train_out = root_dir + "binary_instances_train2017.json"
    val_out = root_dir + "binary_instances_val2017.json"

    convert(root_dir + train_set, train_out)
    convert(root_dir + val_set, val_out)

