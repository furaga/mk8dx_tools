import argparse
from pathlib import Path
from pytube import YouTube
import re

all_video_urls = {
    "after_wave5": {
        "DLC5": [
            # "https://youtu.be/duCKLdMCXrU",
            # "https://youtu.be/fDaaAIbASV0",
            # "https://youtu.be/bBmvcrky3yQ",
            # "https://youtu.be/AA4F-7k_9WE",
            # "https://youtu.be/npeQVQ--zls",
            # "https://youtu.be/cDXfvlS5iqo",
            #  "https://youtu.be/bI0412Xemww",
            # "https://youtu.be/w668MIh2XF4",
            # "https://youtu.be/90s5zvxWEfU",
            # "https://youtu.be/xTbAdbjjqN4",
            # "https://youtu.be/3gFWMlNK_zU",
            # "https://youtu.be/EiuNRqh_1aY",
            # "https://youtu.be/5-MMMnP8tg0",
            # "https://youtu.be/JDP79HKhhCE",
            # "https://youtu.be/F2dsGeO8_0M",
            # "https://youtu.be/GuDPbU5RkwY",x
            # "https://youtu.be/pECAFRyMzX4",
            # #
            # "https://youtu.be/7qP8xTIUj7w",
            # "https://youtu.be/Tugbr0RnLaA",
            # "https://youtu.be/xmvEad6t_pE",
            # "https://youtu.be/WOuoRmdX6kE",
            # "https://youtu.be/YapaTvU2h8s",
            # "https://youtu.be/7UZ3rkycZGg",
            # "https://youtu.be/jZvfVfBbwV4",
            # "https://youtu.be/kF5eTwuxDMk",
            # --------------------
            # "https://youtu.be/xrqKRskihXw",
            # "https://youtu.be/MLOmcjIxulU",
            # "https://youtu.be/KJ0qHCvHoi8",
            # "https://youtu.be/yxUB7jhUwog",
            # "https://youtu.be/wdNBk86boxU",
            # "https://youtu.be/n88wSw-cEV8",
            # "https://youtu.be/SeARaNWuaho",
            # "https://youtu.be/ZI3djYaSv2A",
            # # "https://youtu.be/foX_rXOoHTk",
            # "https://youtu.be/v3qLLfzuZPw",
            # "https://youtu.be/NHBMexihuoI",
            # "https://youtu.be/sI-ruzgj3Bc",
            # "https://youtu.be/BAXqpvue9Wg",
            # "https://youtu.be/jelh5tvHeiU",
            # "https://youtu.be/xOKctXfCFq4",
            # "https://youtu.be/XA5JByVZ82I",
            # "https://youtu.be/7fKAbC33Hyk",
            # "https://youtu.be/5HbX1fiOWpA",
            # "https://youtu.be/9ZUuQg6E7UI",
            # "https://youtu.be/YJiIIk32WiQ",
            # "https://youtu.be/wtICVPS02GI",
            # "https://youtu.be/_FUGM4RmTDI",
            # "https://youtu.be/cNEJ6phsvpM",
            # "https://youtu.be/nouFUz7UKHM",
            # "https://youtu.be/SSgCpv2OOpQ",
            # "https://youtu.be/Q8Xa9P4ktQM",
            # "https://youtu.be/-1KiDxgq2iA",
            # "https://youtu.be/cBVoGEKksNU",
            # "https://youtu.be/D8yvYPbvBiw",
            # "https://youtu.be/jckLC3bL_uc",
            # "https://youtu.be/dlgfneVf5gY",
            # "https://youtu.be/hLwROtXHkF4",
            # "https://youtu.be/8BNu8yr2sNw",
            # "https://youtu.be/QCBJPZoLtIU",
            # "https://youtu.be/MRcW7Os1WiI",
            # "https://youtu.be/4i0zQSFFlIY",
            # "https://youtu.be/09pxdxzErlM",
            # "https://youtu.be/XXtC5BJ-pOI",
            # "https://youtu.be/heMkjn3D024",
            # "https://youtu.be/3FWuF_nEiTQ",
            # "https://youtu.be/c1YZWgQoMpo",
            # "https://youtu.be/Qe2UxfX8IGU",
            "https://youtu.be/7j9KzSo6zm4",
            "https://youtu.be/ffVHnt5fbBk",
            "https://youtu.be/uLjv7WtFtzI",
            "https://youtu.be/5UCMvIapZj8",
            "https://youtu.be/AbC-pF6BtYs",
            "https://youtu.be/SvD2sq_MC6M",
            "https://youtu.be/EaLF_iamLS8",
            "https://youtu.be/myRbZuLVMUI",
            "https://youtu.be/MfaYATfkaOE",
            "https://youtu.be/krAOw371nrQ",
            "https://youtu.be/zT48SKgRA90",
            "https://youtu.be/6QZesTzLQUs",
            "https://youtu.be/oR8ICuBWuIA",
            "https://youtu.be/O__SGOEI5bA",
            "https://youtu.be/eUjhYkkjelE",
            "https://youtu.be/kkeX_Llx-8I",
            "https://youtu.be/O__SGOEI5bA",
            "https://youtu.be/gxNUEgxMm0o",
            "https://youtu.be/Z3_RTxMJ1Jk",
            "https://youtu.be/xE6fhuuprX4",
            "https://youtu.be/-nC3VugBGx4",
            "https://youtu.be/bwiOUuCuewk",
            "https://youtu.be/7UnX2RjY5AE",
            "https://youtu.be/QArpuH9I_Ds",
            "https://youtu.be/-HGHVr_I_mE",
            "https://youtu.be/BUbD6BW8XtU",

            NH-PkfGzXvE
            rJes27rqBiI
            gNcNXiLPpVc
            "https://youtu.be/JoqN01XdEPI",
            "https://youtu.be/rqne4gJvnXM",
            "https://youtu.be/FGbE6dsDEi8",
        ],
    },
}


def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--target", type=str, default="after_wave5")
    parser.add_argument(
        "--out_dir", type=Path, default=r"E:\prog\python\mk8dx_tools\videos"
    )
    args = parser.parse_args()
    return args


def download_videos(video_urls, person_name, out_dir):
    for k, urls in video_urls.items():
        for url in urls:
            try:
                # 動画情報取得
                print("URL:", url)
                stream = (
                    YouTube(url)
                    .streams.filter(file_extension="mp4")
                    .order_by("resolution")
                    .desc()
                    .first()
                )

                # 出力フォルダ・ファイル名
                out_video_dir = out_dir / person_name / k
                out_video_dir.mkdir(exist_ok=True, parents=True)
                fname = stream.title + "-" + (url.split("/")[-1])
                fname = re.sub(r'[\\|/|:|?|.|"|<|>|\|]', "", fname)
                fname += ".mp4"

                if (
                    not (out_video_dir / "done" / fname).exists()
                    and not (out_video_dir / fname).exists()
                ):
                    # ダウンロードして保存
                    print("Downloading", url, "to", str(out_video_dir / fname))
                    stream.download(str(out_video_dir), fname)
            except Exception as e:
                print("Error:", url, str(e))


def main(args):
    download_videos(all_video_urls[args.target], args.target, args.out_dir)


if __name__ == "__main__":
    main(parse_args())
