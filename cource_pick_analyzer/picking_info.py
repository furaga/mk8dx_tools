import argparse
import cv2
import clip
import numpy as np
import pandas as pd
from pathlib import Path
from lib import cv_util, digit_ocr
import torch

course_roi = [0.72, 0.85, 0.84, 0.98]

race_type_features_dict = {}
thumbnail_feature_dict = {}
course_feature_dict = {}
course_img_dict = {}

device = "cuda" if torch.cuda.is_available() else "cpu"
model, clip_preprocess = clip.load('ViT-B/32', device)


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--img_dir', type=Path,
                        default="output/images/person0")
    parser.add_argument('--out_dir', type=Path,
                        default="output/picking_info")
    args = parser.parse_args()
    return args


def get_features(img):
    with torch.no_grad():
        p = cv_util.cv2pil(img)
        image = clip_preprocess(p).unsqueeze(0).to(device)
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


def prepare_reference_images():
    n_courses = set()
    for thumb_path in Path("data/courses").glob("*.png"):
        img = cv_util.imread_safe(str(thumb_path))
        thumb_feature = load_image_feature(img, [0, 0, 1, 0.8])
        thumbnail_feature_dict[thumb_path.stem + "_B"] = thumb_feature / \
            np.linalg.norm(thumb_feature)
        n_courses.add(thumb_path.stem.split('_')[0])

    print("# of courses =", len(n_courses))


def find_best_match_item(feature, feature_dict):
    score_list = []
    for n, f in feature_dict.items():
        similarity = feature @ f.T
        score_list.append((n, similarity[0][0]))

    score_list = sorted(score_list, key=lambda p: -p[1])
    return score_list[0]


def process(img_path):
    dx = 1425 - 980
    rois = [
        [(980 - 2 * dx) / 1920, 70 / 1080, (1385 - 2 * dx) / 1920, 345 / 1080],
        [(980 - dx) / 1920, 70 / 1080, (1385 - dx) / 1920, 345 / 1080],
        [980 / 1920, 70 / 1080, 1385 / 1920, 345 / 1080],
        [(980 + dx) / 1920, 70 / 1080, (1385 + dx) / 1920, 345 / 1080],
    ]

    img = cv_util.imread_safe(img_path)

    results = []
    for i, roi in enumerate(rois):
        course_feature = load_image_feature(img, roi)
       # cv2.imshow(f"img_{i}", cv_util.crop_img(img, roi))
        course_feature /= np.linalg.norm(course_feature)
        name, score = find_best_match_item(
            course_feature, thumbnail_feature_dict)
        results.append((name, score))

    return results


def main(args):
    global cur_ver

    prepare_reference_images()

    all_img_paths = list(args.img_dir.glob(f"*/*.png"))
    all_img_paths += list(args.img_dir.glob(f"*/*.jpg"))

    race_type_dict = {}
    rows = []
    for i, img_path in enumerate(all_img_paths):
        if i % 2 == 1:
            continue

        if i % 100 == 0:
            print(f"[{i}/{len(all_img_paths)}] Processing {str(img_path)}...")

        dirname = img_path.parent.stem
        cur_ver = dirname

        results1 = process(img_path)
        results2 = process(all_img_paths[i + 1])

        def _check(results):
            print(results)
            return len([r[1] > 0.8 for r in results[:3]]) >= 3 and results[3][0].split('_')[0] == "おまかせ"

        ret = None
        if _check(results1):
            ret = results1
        elif _check(results2):
            ret = results2

        row = []
        for r in results1:
            row.append(r[0])
            row.append(r[1])
        rows.append(row)

    # CSV出力
    out_path = args.out_dir / f"{args.img_dir.stem}.csv"
    out_path.parent.mkdir(exist_ok=True, parents=True)
    df = pd.DataFrame(rows)
    header = []
    for i in range(4):
        header += [f"course_{i}", f"score_{i}"]
    df.to_csv(out_path, header=header, index=None,
              encoding="sjis", errors="ignore")


if __name__ == '__main__':
    args = parse_args()
    main(args)
