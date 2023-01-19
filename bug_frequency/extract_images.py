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


video_path = r"E:\prog\python\mk8dx_tools\videos\【マリカ】レート15035 今月の目標は16200!!【岸堂天真ホロスターズ】.mp4"


game_screen_roi = [0, 0, 1655 / 1920, 929 / 1080]

race_type_roi = [0.16, 0.85, 0.24, 0.98]
course_roi = [0.72, 0.85, 0.84, 0.98]

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load('ViT-B/32', device)


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--img_dir', type=Path, default="data/images")
    parser.add_argument('--ocr_dir', type=Path, default="data/ocr")
    args = parser.parse_args()
    return args


def get_features(img):
    with torch.no_grad():
        p = cv_util.cv2pil(img)
        image = preprocess(p).unsqueeze(0).to(device)
        features = model.encode_image(image)
        return features.cpu().numpy()


def crop_img(img, roi):
    h, w = img.shape[:2]
    img = img[
        int(h * roi[1]):int(h * roi[3]),
        int(w * roi[0]):int(w * roi[2]),
    ]
    return img


def load_image_feature(img, roi=None):
    if roi is not None:
        img = crop_img(img, roi)
    feature = get_features(img)
    return feature


race_type_features_dict = {}
thumbnail_features_dict = {}

course_feature_dict = {}
course_img_dict = {}


def initialize():
    for type_path in Path("data/race_type").glob("*.png"):
        img = cv_util.imread_safe(str(type_path))
        type_feature = load_image_feature(img, [0, 0, 1, 1])
        race_type_features_dict[type_path.stem] = type_feature / \
            np.linalg.norm(type_feature)

    for thumb_path in Path("data/thumbnails").glob("*.png"):
        img = cv_util.imread_safe(str(thumb_path))
        thumb_feature = load_image_feature(img, [0, 0, 1, 0.8])
        thumbnail_features_dict[thumb_path.stem] = thumb_feature / \
            np.linalg.norm(thumb_feature)

    for thumb_path in Path("data/thumbnails_2").glob("*.png"):
        img = cv_util.imread_safe(str(thumb_path))
        thumb_feature = load_image_feature(img, [0, 0, 1, 0.8])
        thumbnail_features_dict[thumb_path.stem + "_A"] = thumb_feature / \
            np.linalg.norm(thumb_feature)


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


def process(img, course_img, race_type_img):
    course_feature = load_image_feature(img, course_roi)
    course_feature /= np.linalg.norm(course_feature)
    course_name, course_score = find_best_match_item(
        course_feature, thumbnail_features_dict)

    race_type_feature = load_image_feature(img, race_type_roi)
    race_type_feature /= np.linalg.norm(race_type_feature)
    race_type_name, race_type_score = find_best_match_item(
        race_type_feature, race_type_features_dict)

    return course_name, course_score, race_type_name, race_type_score


def main(args):
    initialize()
    cap = cv2.VideoCapture(video_path)
    cap_length_sec = cap.get(cv2.CAP_PROP_FRAME_COUNT) / \
        cap.get(cv2.CAP_PROP_FPS)
    current_time = 0
    counter = 0
    while True:
        if current_time % 1000 == 0:
            print(f"[{100 * current_time / cap_length_sec:.1f}%] current_time",
                  current_time, "sec")

        cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)
        ret, img = cap.read()
        if not ret:
            break

        br = get_black_ratio(img)
        if not (0.2 < br < 0.4):
            current_time += 2
            continue

        wr = get_white_ratio(img)
        if not (wr > 0.15):
            current_time += 2
            continue

        counter += 1
        if counter < 2:
            current_time += 2
            continue

        cource_img = crop_img(img, course_roi)
        race_type_img = crop_img(img, race_type_roi)
        course_name, course_score, race_type_name, race_type_score = process(
            img, cource_img, race_type_img)

        print(f"[{100 * current_time / cap_length_sec:.1f}%] current_time",
              current_time, "sec")
        print(int(wr * 100), int(br * 100), "|", course_name,
              course_score, race_type_name, race_type_score)

        cv2.imwrite(f"{current_time:08d}sec.jpg", img)

        # cv2.imshow("img", cv2.resize(img, None, fx=0.5, fy=0.5))
        # cv2.imshow("cource_img", cource_img)
        # cv2.imshow("race_type_img", race_type_img)
        # if ord('q') == cv2.waitKey(1):
        #     break

        counter = 0
        current_time += 90


if __name__ == '__main__':
    args = parse_args()
    main(args)
