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

known_video_orders = [
    "2022 03 13 16 41 00",
    "2022 07 01 21 21 02",
    "【マリカ8DX】レート2万耐久【テスト配信】",
    "【マリカ8DX】レート2万耐久（枠立て直し）【テスト配信】",
    "レート戦 20,694_",
    "野良とNITA",
    "レート戦2022_10_26",
    "チャレンジ→レート戦2022_10_29",
    "レート戦2022_10_31",
    "レート戦→NITA2022_11_26",
    "レート戦 with シェリンさん2022_11_02",
    "レート戦 with てんまさん2022_11_08",
    "レート戦 wtih シェリンさん2022_11_30",
    "レート戦 with シェリンさん2022_12_04",
    "レート2023_01_13 part2",
    "不眠レート",
    "3万達成レート",
    "レート with シェリンさん",
    "ちょっとレート",
]


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--csv_path', type=Path, default="statistics.csv")
    args = parser.parse_args()
    return args


def main(args):
    import pandas as pd
    df = pd.read_csv(args.csv_path, encoding="sjis")

    sorted_rows = []
    for row in df.values:
        key = Path(row[3]).stem.split('@')[0]
        second = Path(row[3]).stem.split('@')[1][:-2]
        if key in known_video_orders:
            index = known_video_orders.index(key)
        else:
            index = -1
        sorted_rows.append(list(row) + [index, int(second)])

    sorted_rows = sorted(sorted_rows, key=lambda r: (r[-2], r[-1]))

    # plot
    types = [r[1] for r in sorted_rows]
    ys = [1 if t == "mirror" else 0 for t in types]

    roll = 50
    ys_mean = [np.sum(ys[i:i+roll]) for i in range(0, len(ys) - roll)]
    print(ys, np.sum(ys))
    print(ys_mean)

    for i, row in enumerate(sorted_rows):
        if i % 10 == 0:
            print(i, row)

    import matplotlib.pyplot as plt
    plt.plot(ys_mean)
    plt.show()
    return

    # count
    video_dict = {}
    for row in sorted_rows:
        key = Path(row[3]).stem.split('@')[0]
        video_dict.setdefault(key, []).append(row)

    for key, rows in sorted(video_dict.items()):
        counter = {
            "150cc": 0,
            "200cc": 0,
            "mirror": 0,
        }
        for row in rows:
            counter[row[1]] += 1

        text = f"> {key}\n"
        for k, v in counter.items():
            text += f"{k}: {v} ({v / len(rows) * 100:.1f}%), "
        text += f"total: {len(rows)}"
        text = text.strip().strip(',')
        print(text)


if __name__ == '__main__':
    args = parse_args()
    main(args)
