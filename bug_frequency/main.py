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
import torch
import torchvision

thumbnail_roi = [0.72, 0.85, 0.84, 0.98]

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load('ViT-B/32', device)


def get_features(img):
    with torch.no_grad():
        p = cv_util.cv2pil(img)
        image = preprocess(p).unsqueeze(0).to(device)
        features = model.encode_image(image)
        return features.cpu().numpy()


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--img_dir', type=Path, default="data/images")
    parser.add_argument('--ocr_dir', type=Path, default="data/ocr")
    args = parser.parse_args()
    return args


def process(img_path, ocr_path):
    img = cv_util.imread_safe(img_path)
    h, w = img.shape[:2]
    thumnail = img[
        int(h * thumbnail_roi[1]):int(h * thumbnail_roi[3]),
        int(w * thumbnail_roi[0]):int(w * thumbnail_roi[2]),
    ]

    cv2.imshow("img", cv2.resize(img, None, fx=0.8, fy=0.8))
    cv2.imshow("thumnail", thumnail)

    feature = get_features(thumnail)
    feature /= np.linalg.norm(feature)

    ls = []
    for thumb_path in Path("data/thumbnails").glob("*.png"):
        t = cv_util.imread_safe(str(thumb_path))
        t = t[: int(t.shape[0] * 0.9), :]
        feature_t = get_features(t)
        feature_t /= np.linalg.norm(feature_t)
        similarity = (100.0 * feature @ feature_t.T)
        ls.append((thumb_path.stem, similarity[0][0]))

    ls = sorted(ls, key=lambda p: -p[1])

    for name, score in ls[:5]:
        print(name, score)

        # values, indices = similarity[0].topk(5)

        # # Print the result
        # print("\nTop predictions:\n")
        # for value, index in zip(values, indices):
        #     print(f"{cifar100.classes[index]:>16s}: {100 * value.item():.2f}%")
        # t =

    if ord('q') == cv2.waitKey(0):
        exit(0)


def main(args):
    # for dirname in ["DLC0", "DLC1", "DLC2", "DLC3"]:
    for dirname in ["DLC2", "DLC3"]:
        all_img_paths = args.img_dir.glob(f"{dirname}/*.png")
        for img_path in all_img_paths:
            print("Processing", str(img_path))
            ocr_path = args.ocr_dir / dirname / (img_path.stem + ".txt")
            process(img_path, ocr_path)


if __name__ == '__main__':
    args = parse_args()
    main(args)
