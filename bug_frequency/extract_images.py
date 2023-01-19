# レース前のコース名と名前・レートが表示されている画面を探す
from pathlib import Path
import argparse
import cv2
from lib import cv_util


# video_path = Path(
#     r"E:\prog\python\mk8dx_tools\videos\【マリカ】レート15035 今月の目標は16200!!【岸堂天真ホロスターズ】.mp4")

def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--video_dir', type=Path,
                        default=r"E:\prog\python\mk8dx_tools\videos")
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


def process_video(video_path, out_dir):
    cap = cv2.VideoCapture(str(video_path))
    cap_length_sec = cap.get(cv2.CAP_PROP_FRAME_COUNT) / \
        cap.get(cv2.CAP_PROP_FPS)
    current_time = 0
    counter = 0
    while True:
        h = current_time // 3600
        m = (current_time % 3600) // 60
        s = current_time % 60
        # if current_time % 1000 == 0:
        #     print(
        #         f"[{100 * current_time / cap_length_sec:.1f}%] current_time={h:02d}h{m:02d}m{s:02d}s")

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
        out_path = out_dir / f"{video_path.stem}_{h:02d}h{m:02d}m{s:02d}s.jpg"
        cv_util.imwrite_safe(str(out_path), img)

        # cv2.imshow("img", cv2.resize(img, None, fx=0.5, fy=0.5))
        # if ord('q') == cv2.waitKey(1):
        #     break

        counter = 0
        current_time += 90


def main(args):
    all_video_paths = list(args.video_dir.glob("*/*.mp4"))
    for vi, video_path in enumerate(all_video_paths):
        print("==================================")
        print(f"[{vi+1}/{len(all_video_paths)}] {str(video_path)}")
        print("==================================")

        out_dir = Path("data/images_person2") / video_path.parent.stem
        out_dir.mkdir(exist_ok=True, parents=True)
        process_video(video_path, out_dir)


if __name__ == '__main__':
    args = parse_args()
    main(args)
