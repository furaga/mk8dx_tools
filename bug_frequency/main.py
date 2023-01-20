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
from lib import cv_util, digit_ocr
import torch
import torchvision

game_screen_roi = [0, 0, 1655 / 1920, 929 / 1080]
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
        max(0, int(h * roi[1])):min(h, int(h * roi[3])),
        max(0, int(w * roi[0])):min(w, int(w * roi[2])),
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


def detect_rates(img):
    players_roi = [
        93 / 1920,
        84 / 1080,
        1827 / 1920,
        870 / 1080,
    ]
    players_img = crop_img(img, players_roi)
    h, w = players_img.shape[:2]
    players = []
    for x in range(2):
        for y in range(6):
            players.append(
                crop_img(players_img, [x / 2, y / 6, (x + 1) / 2, (y+1) / 6]))

    rates = []
    for i, p in enumerate(players):
        rate_img = crop_img(p, [0.75, 0.5, 0.995, 0.995])
        rate_img = cv2.cvtColor(rate_img, cv2.COLOR_BGR2GRAY)
        ret, rate = digit_ocr.detect_digit(255 - rate_img)
        if not ret:
            rate = 0
        if not (500 <= rate <= 99999):
            # invalid valie
            rate = 0
        rates.append(rate)
    #     cv2.imshow(f"r{i}", rate_img)
    # cv2.waitKey(0)

    return rates


def process(img_path, ocr_path):
    img = cv_util.imread_safe(img_path)
    if img_path.parent.stem.endswith("_frame"):
        img = crop_img(img, game_screen_roi)

    rates = detect_rates(img)

    course_img = crop_img(img, course_roi)
    race_type_img = crop_img(img, race_type_roi)

    course_feature = load_image_feature(img, course_roi)
    course_feature /= np.linalg.norm(course_feature)
    course_name, course_score = find_best_match_item(
        course_feature, thumbnail_features_dict)

    # detect race type (150cc, 200cc or mirror)
    if img_path.parent.stem.endswith("_150cc"):
        race_type_name, race_type_score = "150cc", 100
    elif img_path.parent.stem.endswith("_200cc"):
        race_type_name, race_type_score = "200cc", 100
    elif img_path.parent.stem.endswith("_mirror"):
        race_type_name, race_type_score = "mirror", 100
    else:
        race_type_feature = load_image_feature(img, race_type_roi)
        race_type_feature /= np.linalg.norm(race_type_feature)
        race_type_name, race_type_score = find_best_match_item(
            race_type_feature, race_type_features_dict)

    return course_name, race_type_name, rates


def main(args):
    initialize()
    race_type_dict = {}
    rows = []
#    for dirname in ["DLC1_frame", "DLC0_frame", "DLC0", "DLC1", "DLC2", "DLC3"]:
    for dirname in ["DLC2_150cc", "DLC2_200cc", "DLC2_mirror", "DLC3_150cc", "DLC3_200cc", "DLC3_mirror",]:
        #    for dirname in ["DLC1_frame"]:
        print("Processing", dirname)  # str(img_path))
        all_img_paths = list(args.img_dir.glob(f"{dirname}/*.png"))
        all_img_paths += list(args.img_dir.glob(f"{dirname}/*.jpg"))
        local_dict = {}
        for ii, img_path in enumerate(all_img_paths):
            ocr_path = args.ocr_dir / dirname / (img_path.stem + ".txt")
            course_name, race_type_name, rates = process(
                img_path, ocr_path)
            race_type_dict.setdefault(race_type_name, 0)
            race_type_dict[race_type_name] += 1
            local_dict.setdefault(race_type_name, 0)
            local_dict[race_type_name] += 1
            rows.append([course_name.split('_')[0], race_type_name,
                        dirname.split('_')[0], str(img_path)] + rates)
        local_dict["total"] = np.sum([v for _, v in local_dict.items()])
        print(local_dict)

    import pandas as pd
    df = pd.DataFrame(rows)
    df.to_csv("statistics.csv", header=[
              "cource", "type", "ver", "image_path"] + list(f"rate_{i}" for i in range(12)),
              index=None, encoding="sjis", errors="ignore")

    race_type_dict["total"] = np.sum([v for _, v in race_type_dict.items()])
    print(race_type_dict)

    # for n, img in course_img_dict.items():
    #     cv2.imwrite(n + ".png", img)


if __name__ == '__main__':
    args = parse_args()
    main(args)
