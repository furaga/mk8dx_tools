# レース前のコース名と名前・レートが表示されている画面を探す
import torchvision
import torch
from lib import cv_util
from PIL import Image, ImageEnhance
import pyocr
from playsound import playsound
from pathlib import Path
import sys
import os
from glob import glob
import numpy as np
import clip
import argparse
import re
import cv2
import lib


video_path = Path(
    r"E:\prog\python\mk8dx_tools\videos\【マリカ】レート15035 今月の目標は16200!!【岸堂天真ホロスターズ】.mp4")


game_screen_roi = [0, 0, 1655 / 1920, 929 / 1080]

race_type_roi = [0.16, 0.85, 0.24, 0.98]
course_roi = [0.72, 0.85, 0.84, 0.98]

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load('ViT-B/32', device)


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--img_dir', type=Path, default="data/images")
    args = parser.parse_args()
    return args


def crop_img(img, roi):
    h, w = img.shape[:2]
    img = img[
        int(h * roi[1]):int(h * roi[3]),
        int(w * roi[0]):int(w * roi[2]),
    ]
    return img


def find_best_match_item(feature, feature_dict):
    score_list = []
    for n, f in feature_dict.items():
        similarity = (100.0 * feature @ f.T)
        score_list.append((n, similarity[0][0]))

    score_list = sorted(score_list, key=lambda p: -p[1])
    # for name, score in score_list[:3]:
    #     print(name, score)
    return score_list[0]


def get_white_ratio(img):
    h, w = img.shape[:2]
    white = cv2.inRange(img, (230, 230, 230), (255, 255, 255))
    wr = cv2.countNonZero(white) / (h * w)
    return wr


def get_black_ratio(img):
    h, w = img.shape[:2]
    black = cv2.inRange(img, (0, 0, 0), (3, 3, 3))
    br = cv2.countNonZero(black) / (h * w)
    return br


def main(args):
    cap = cv2.VideoCapture(str(video_path))
    cap_length_sec = cap.get(cv2.CAP_PROP_FRAME_COUNT) / \
        cap.get(cv2.CAP_PROP_FPS)
    current_time = 0
    counter = 0
    while True:
        h = current_time // 3600
        m = (current_time % 3600) // 60
        s = current_time % 60
        if current_time % 1000 == 0:
            print(
                f"[{100 * current_time / cap_length_sec:.1f}%] current_time={h:02d}h{m:02d}m{s:02d}s")

        cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)
        ret, img = cap.read()
        if not ret:
            break

        br = get_black_ratio(img)
        if not (0.22 < br):
            current_time += 2
            continue

        wr = get_white_ratio(img)
        if not (wr > 0.13):
            current_time += 2
            continue

        counter += 1
        if counter < 2:
            current_time += 2
            continue

        print(
            f"*[{100 * current_time / cap_length_sec:.1f}%] current_time={h:02d}h{m:02d}m{s:02d}s")
        print(int(wr * 100), int(br * 100))

        assert (3600 * h + m * 60 + s == current_time)
        lib.cv_util.imwrite_safe(f"{video_path.stem}_{h:02d}h{m:02d}m{s:02d}s.jpg", img)

        # cv2.imshow("img", cv2.resize(img, None, fx=0.5, fy=0.5))
        # if ord('q') == cv2.waitKey(1):
        #     break

        counter = 0
        current_time += 90


if __name__ == '__main__':
    args = parse_args()
    main(args)
