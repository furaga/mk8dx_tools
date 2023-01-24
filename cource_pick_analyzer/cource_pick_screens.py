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


def get_hms(seconds):
    return seconds // 3600, (seconds % 3600) // 60, seconds % 60


def save_img(video_path, out_dir, current_time, img):
    h, m, s = get_hms(current_time)
    out_path = out_dir / f"{video_path.stem}_{h:02d}h{m:02d}m{s:02d}s.jpg"
    cv_util.imwrite_safe(str(out_path), img)
    if DEBUG_MODE:
        cv2.imshow("img", cv2.resize(img, None, fx=0.5, fy=0.5))
        if ord('q') == cv2.waitKey(0):
            exit(0)


def calc_iou(a, b):
    # a, bは矩形を表すリストで、a=[xmin, ymin, xmax, ymax]
    ax_mn, ay_mn, ax_mx, ay_mx = a[0], a[1], a[2], a[3]
    bx_mn, by_mn, bx_mx, by_mx = b[0], b[1], b[2], b[3]

    a_area = (ax_mx - ax_mn + 1) * (ay_mx - ay_mn + 1)
    b_area = (bx_mx - bx_mn + 1) * (by_mx - by_mn + 1)

    abx_mn = max(ax_mn, bx_mn)
    aby_mn = max(ay_mn, by_mn)
    abx_mx = min(ax_mx, bx_mx)
    aby_mx = min(ay_mx, by_mx)
    w = max(0, abx_mx - abx_mn + 1)
    h = max(0, aby_mx - aby_mn + 1)
    intersect = w*h

    iou = intersect / (a_area + b_area - intersect)
    return iou


def picking_screen(img):
    img = cv2.resize(img, (128, 72))
    # print(img.shape)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)

    dx = 1425 - 980
    rois = [
        [(980 - 2 * dx) / 1920, 70 / 1080, (1385 - 2 * dx) / 1920, 345 / 1080],
        [(980 - dx) / 1920, 70 / 1080, (1385 - dx) / 1920, 345 / 1080],
        [980 / 1920, 70 / 1080, 1385 / 1920, 345 / 1080],
        [(980 + dx) / 1920, 70 / 1080, (1385 + dx) / 1920, 345 / 1080],
    ]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    roi_bin = cv2.adaptiveThreshold(gray, 255,
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
                                    max(int(min(height, width) / 8), 1) * 2 + 1, 2)

    _, _, stats = cv2.connectedComponentsWithStats(roi_bin)[:3]
    if len(stats) < len(rois):
        return False, None

    best_matches = []
    for roi in rois:
        iou_stats = []
        for stat in stats:
            # stat = [領域の左上のx座標, 領域の左上のy座標, 領域の幅, 領域の高さ, 面積]
            x, y = stat[0], stat[1]
            w, h = stat[2], stat[3]
            stat_roi = [x / width, y / height,
                        (x + w) / width, (y + h) / height]
            iou = calc_iou(stat_roi, roi)
            iou_stats.append((iou, stat))
        iou_stats = sorted(iou_stats, key=lambda k: -k[0])
        best_matches.append(iou_stats[0])

    if len([1 for iou, _ in best_matches if iou > 0.93]) >= 3:
        return True, img

    return False, None


def picked_screen(img):
    pass


def process_video(video_path, out_dir):
    cap = cv2.VideoCapture(str(video_path))
    current_time = 0

    while True:
        cap.set(cv2.CAP_PROP_POS_MSEC, int(current_time * 1000))
        ret, img = cap.read()
        if not ret:
            break

        is_picking, _ = picking_screen(img)
        if is_picking:
            print("found: current_time =", current_time, "sec")

            # サムネが薄いときを切り取らないように検出1秒後の画像を保存する
            # -> 逆にミスりがちなのでやっぱりやめておく
            # current_time += 0.5
            #cap.set(cv2.CAP_PROP_POS_MSEC, int(current_time * 1000))
            #ret, img = cap.read()
            #if not ret:
            #    break
            save_img(video_path, out_dir, int(current_time), img)

            current_time += 120

        current_time += 1


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
