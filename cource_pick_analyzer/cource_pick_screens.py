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


def save_img(video_path, out_dir, h, m, s, img):
    out_path = out_dir / f"{video_path.stem}_{h:02d}h{m:02d}m{s:02d}s.jpg"
    cv_util.imwrite_safe(str(out_path), img)
    if DEBUG_MODE:
        cv2.imshow("img", cv2.resize(img, None, fx=0.5, fy=0.5))
        if ord('q') == cv2.waitKey(0):
            exit(0)


def process_video(video_path, out_dir):
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

        # TODO
        pass


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
