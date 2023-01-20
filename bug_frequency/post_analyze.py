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


def config_std_div_avg():
    def get_metric(rates): return np.std(rates) / np.mean(rates)
    span = 0.25
    x_label = "std/avg of rates"
    return get_metric, span, x_label


def config_std():
    def get_metric(rates): return np.std(rates)
    span = 2500
    x_label = "std of rates"
    return get_metric, span, x_label


def config_avg():
    def get_metric(rates): return np.mean(rates)
    span = 2500
    x_label = "avg of rates"
    return get_metric, span, x_label


def logistic_analysis(value_types):
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression()
    X_train = [[v] for v, _ in value_types]
    Y_train = [1 if t == "mirror" else 0 for _, t in value_types]
    model.fit(X_train, Y_train)
    regression_coefficient = model.coef_
    print(np.exp(regression_coefficient))


def main(args):
    #get_metric, span, x_label = config_std_div_avg()
    get_metric, span, x_label = config_std()

    import pandas as pd
    df = pd.read_csv(args.csv_path, encoding="sjis")

    sorted_rows = []
    for row in df.values:
        if row[2] == "DLC2" or row[2] == "DLC3":
            pass
        else:
            continue
        fname = Path(row[3]).stem
        if "@" in fname:
            key = Path(row[3]).stem.split('@')[0]
            second = int(Path(row[3]).stem.split('@')[1][:-2])
        else:
            key = Path(row[3]).stem.split('_')[0]
            second = Path(row[3]).stem.split('_')[-1][:-2]
        if key in known_video_orders:
            index = known_video_orders.index(key)
        else:
            index = -1
        # if row[2] != "DLC0":
        #     continue
        sorted_rows.append(list(row) + [index, second])

    sorted_rows = sorted(sorted_rows, key=lambda r: (r[-2], r[-1]))

    # plot
    types = [r[1] for r in sorted_rows]
    ys = [1 if t == "mirror" else 0 for t in types]

    rate_metrics = []
    mirrors = []

    thrs = [3000, 5000, 10000, 20000, 1e8]
    total_dict = {f"<{v}": 0 for v in thrs}
    occur_dict = {f"<{v}": 0 for v in thrs}

    value_types = []
    for row in sorted_rows:
        rates = [v for v in row[4:4+12] if 99999 >= v > 500]
        value = get_metric(rates)
        rate_metrics.append(value)
        mirrors.append(row[1] == "mirror")

        key = ""
        for v in thrs:
            if value <= v:
                key = f"<{v}"
                break

        total_dict[key] += 1
        if row[1] == "200cc":
            occur_dict[key] += 1

        value_types.append([value, row[1]])

    print(total_dict, occur_dict)
    for k in total_dict.keys():
        prob = occur_dict[k] / total_dict[k] if total_dict[k] > 0 else 0
        print(f"{k}: {100 * prob:.1f}% ({occur_dict[k]}/{total_dict[k]})")

    value_types = sorted(value_types)
    logistic_analysis(value_types)

    #
    #
    #
    print("==============================")

    grp1 = value_types[:len(value_types) // 3]
    grp2 = value_types[len(value_types) * 2 // 3:]
    for g in [grp1, grp2]:
        avg_value = np.mean([v for v, t in g])
        n_mirror = np.sum([t == "mirror" for v, t in g])
        n_200cc = np.sum([t == "200cc" for v, t in g])
        print(int(avg_value), len(g),
              f"mirror: {n_mirror} ({n_mirror / len(g) * 100:.1f}%)",
              f"200cc: {n_200cc} ({n_200cc / len(g) * 100:.1f}%)",
              )

    print("==============================")

    xs = []
    ys_200cc = []
    ys_mirror = []
    for value, _ in value_types:
        # 自分周辺のミラー率
        mirror, cc200, n = 0, 0, 0
        for value2, type2 in value_types:
            if value - span < value2 <= value + span:
                n += 1
                if type2 == "mirror":
                    mirror += 1
                if type2 == "200cc":
                    cc200 += 1
        if n > len(value_types) // 10:
            xs.append(value)
            ys_200cc.append(cc200 / n)
            ys_mirror.append(mirror / n)

    print("mirror corr", np.corrcoef(xs, ys_mirror)[0, 1])
    print("200cc corr", np.corrcoef(xs, ys_200cc)[0, 1])

    import matplotlib.pyplot as plt
  #  plt.ylim([0, 0.2])
    plt.xlabel(x_label)
    plt.ylabel("prob")
    plt.plot(xs, ys_mirror, "-", label="mirror")
    plt.plot(xs, ys_200cc, "-", label="200cc")
    plt.legend()
    plt.show()
#    return

    # count
    video_dict = {}
    for row in sorted_rows:
        # key = Path(row[3]).stem.split('@')[0]
        key = Path(row[2]).stem.split('@')[0]
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
