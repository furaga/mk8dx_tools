# レース前のコース名と名前・レートが表示されている画面を探す
from pathlib import Path
import argparse
import cv2
from lib import cv_util

DEBUG_MODE = False


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--video_dir', type=Path,
                        default="output/videos/person0")
    parser.add_argument('--out_dir', type=Path, default="output/images")
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
    return score_list[0]


def get_white_ratio(img):
    h, w = img.shape[:2]
    # Ad-hoc: https://youtu.be/yhFYxC70S0U明度フィルタが乗っているのでしきい値調整
    thr = 220 if "yhFYxC70S0U" not in str(args.video_dir.stem) else 195
    white = cv2.inRange(img, (thr, thr, thr), (255, 255, 255))
    wr = cv2.countNonZero(white) / (h * w)
    return wr


def get_black_ratio(img):
    h, w = img.shape[:2]
    # Ad-hoc: https://youtu.be/yhFYxC70S0U明度フィルタが乗っているのでしきい値調整
    thr = 15 if "yhFYxC70S0U" not in str(args.video_dir.stem) else 25
    black = cv2.inRange(img, (0, 0, 0), (thr, thr, thr))
    br = cv2.countNonZero(black) / (h * w)
    return br


def load_crop_info(video_path):
    fallback = [0, 0, 1, 1]
    crop_info_path = video_path.parent / "crop_info.txt"
    if not crop_info_path.exists():
        return fallback
    with open(crop_info_path, encoding="utf8") as f:
        for line in f:
            tokens = line.strip().split(',')
            print(tokens, video_path.name, video_path.name == tokens[0])
            if video_path.name == tokens[0]:
                w, h, x, y = [int(t) for t in tokens[1:5]]
                return [0, 0, x / w, y / h]
    return fallback


def save_img(video_path, out_dir, h, m, s, img):
    out_path = out_dir / f"{video_path.stem}_{h:02d}h{m:02d}m{s:02d}s.jpg"
    cv_util.imwrite_safe(str(out_path), img)
    if DEBUG_MODE:
        cv2.imshow("img", cv2.resize(img, None, fx=0.5, fy=0.5))
        if ord('q') == cv2.waitKey(0):
            exit(0)


def process_video(video_path, out_dir):
    roi = load_crop_info(video_path)

    if not DEBUG_MODE:
        if len(list(out_dir.glob(f"{video_path.stem}_*"))) > 0:
            print("Skip", str(video_path),
                  "because it seems to be already processed.")
            return

    cap = cv2.VideoCapture(str(video_path))
    cap_length_sec = cap.get(cv2.CAP_PROP_FRAME_COUNT) / \
        cap.get(cv2.CAP_PROP_FPS)
    current_time = 0

    debug_counter = 0
    flush_args = None
    step_sec = 3
    while True:
        h = current_time // 3600
        m = (current_time % 3600) // 60
        s = current_time % 60
        if DEBUG_MODE:
            debug_counter += 1
            if debug_counter % 100 == 0:
                print(
                    f"[{100 * current_time / cap_length_sec:.1f}%] current_time={h:02d}h{m:02d}m{s:02d}s")

        cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)
        ret, img = cap.read()
        if not ret:
            break

        img = crop_img(img, roi)

        br = get_black_ratio(img)
        if not (0.22 < br):
            current_time += step_sec
            if flush_args is not None:
                save_img(*flush_args)
                current_time += 120
                flush_args = None
            continue

        wr = get_white_ratio(img)
        if not (wr > 0.13):
            current_time += step_sec
            if flush_args is not None:
                save_img(*flush_args)
                current_time += 120
                flush_args = None
            continue

        print(
            f"*[{100 * current_time / cap_length_sec:.1f}%] current_time={h:02d}h{m:02d}m{s:02d}s")

        # 条件を満たさなくなる直前の成功例を実行したい
        flush_args = [video_path, out_dir, h, m, s, img]
        current_time += step_sec


def main(args):
    all_video_paths = list(args.video_dir.glob("*/*.mp4"))
    for vi, video_path in enumerate(all_video_paths):
        print("==================================")
        print(f"[{vi+1}/{len(all_video_paths)}] {str(video_path)}")
        print("==================================")

        out_dir = args.out_dir / video_path.parent.parent.stem / video_path.parent.stem
        out_dir.mkdir(exist_ok=True, parents=True)
        process_video(video_path, out_dir)


if __name__ == '__main__':
    args = parse_args()
    main(args)
