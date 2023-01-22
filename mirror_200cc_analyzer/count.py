import re
import argparse
import cv2
import clip
import numpy as np
from glob import glob
import os
import sys
from pathlib import Path
from playsound import playsound
import pyocr
from PIL import Image, ImageEnhance
from lib import cv_util
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--race_info_dir', type=Path,
                        default="output/race_information")
    args = parser.parse_args()
    return args


def print_counter(label, d):
    total = np.sum([v for _, v in d.items()])
    text = f"[{label}] "
    for k, v in d.items():
        prob = v / total * 100
        text += f"{k}: {v} ({prob:.1f}%), "
    text += f"total: {total}"
    text = text.strip().strip(',')
    print(text)


def create_counter():
    return {"150cc": 0, "mirror": 0, "200cc": 0, }


def main(args):
    all_csv_paths = list(args.race_info_dir.glob("*.csv"))

    all_total_counter = create_counter()
    all_ver_counter = {f"DLC{i}": create_counter() for i in range(4)}

    for csv_path in all_csv_paths:
        df = pd.read_csv(csv_path, encoding="sjis")

        total_counter = create_counter()
        ver_counter = {}
        for row in df.values:
            ver = row[2]
            race_type = row[1]
            ver_counter.setdefault(
                ver, create_counter())
            ver_counter[ver][race_type] += 1
            total_counter[race_type] += 1

        for k in total_counter.keys():
            all_total_counter[k] += total_counter[k]

        for v in ver_counter.keys():
            for k in ver_counter[v].keys():
                all_ver_counter[v][k] += ver_counter[v][k]

        print("-----------------------")
        print(csv_path.stem)
        print("-----------------------")

        for ver, d in ver_counter.items():
            print_counter(ver, d)
        print_counter("TOTAL", total_counter)

    print("-----------------------")
    print("ALL")
    print("-----------------------")

    for ver, d in all_ver_counter.items():
        print_counter(ver, d)
    print_counter("TOTAL", all_total_counter)


if __name__ == '__main__':
    args = parse_args()
    main(args)
