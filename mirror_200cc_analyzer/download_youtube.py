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
            # "https://youtu.be/7j9KzSo6zm4",
            # "https://youtu.be/ffVHnt5fbBk",
            # "https://youtu.be/uLjv7WtFtzI",
            # "https://youtu.be/5UCMvIapZj8",
            # "https://youtu.be/AbC-pF6BtYs",
            # "https://youtu.be/SvD2sq_MC6M",
            # "https://youtu.be/EaLF_iamLS8",
            # "https://youtu.be/myRbZuLVMUI",
            # "https://youtu.be/MfaYATfkaOE",
            # "https://youtu.be/krAOw371nrQ",
            # "https://youtu.be/zT48SKgRA90",
            # "https://youtu.be/6QZesTzLQUs",
            # "https://youtu.be/oR8ICuBWuIA",
            # "https://youtu.be/O__SGOEI5bA",
            # "https://youtu.be/eUjhYkkjelE",
            # "https://youtu.be/kkeX_Llx-8I",
            # "https://youtu.be/O__SGOEI5bA",
            # "https://youtu.be/Z3_RTxMJ1Jk",
            # "https://youtu.be/-nC3VugBGx4",
            # "https://youtu.be/bwiOUuCuewk",
            # "https://youtu.be/7UnX2RjY5AE",
            "https://youtu.be/QArpuH9I_Ds",
            "https://youtu.be/-HGHVr_I_mE",
            "https://youtu.be/BUbD6BW8XtU",
            "https://youtu.be/NH-PkfGzXvE",
            "https://youtu.be/rJes27rqBiI",
            "https://youtu.be/gNcNXiLPpVc",
            "https://youtu.be/JoqN01XdEPI",
            "https://youtu.be/rqne4gJvnXM",
            "https://youtu.be/FGbE6dsDEi8",
            "https://youtu.be/xE6fhuuprX4",
            "https://youtu.be/gxNUEgxMm0o",
            "https://youtu.be/eejiMnWah0U",
            "https://youtu.be/6VIWyz9vVI0",
            "https://youtu.be/2A3y44J4QQw",
            "https://youtu.be/uoxYkwJHsrY",
            "https://youtu.be/6VIWyz9vVI0",
            "https://youtu.be/Wb5zvaZdHdE",
            "https://youtu.be/ou4T_zikz8M",
            "https://youtu.be/OnfQPgsAGKU",
            "https://youtu.be/dDkPm0787is",
            "https://youtu.be/-Mpjjzoy2v8",
            "https://youtu.be/JjgQmAbwRqo",
            "https://youtu.be/xLY0t5KWkjI",
            "https://www.youtube.com/live/lLBjEJG4l3M",
            "https://www.youtube.com/live/971ZkCRuHYw",
            "https://www.youtube.com/live/6U_M8eODhKo",
            "https://www.youtube.com/live/jv8MqSejUmQ",
            "https://www.youtube.com/live/CAq9D4_xFc4",
            "https://www.youtube.com/live/En5MLKfHnXY",
            "https://www.youtube.com/live/ip8dhzaQfXw",
            "https://www.youtube.com/live/rYNrnKTxK60",
            "https://www.youtube.com/live/G3LmYuqto5U",
            "https://www.youtube.com/live/WGa8UL2MIP4",
            "https://www.youtube.com/live/eIpgCcby7sE",
            "https://www.youtube.com/live/48NWNePDTzg",
            "https://www.youtube.com/live/yAlCcZ8HIt0",
            "https://www.youtube.com/live/6m4iI86RveA",
            "https://www.youtube.com/live/lYy8sCV-zGo",
            "https://www.youtube.com/live/1L_8JVDA3o0",
            "https://www.youtube.com/live/FRsg58a7BbE",
            "https://www.youtube.com/live/xBC0BbxlqyU",
            "https://www.youtube.com/live/m6HGoG7l8Qc",
            "https://www.youtube.com/live/QBYzp1zxeB0",
            "https://www.youtube.com/live/4Z0J1cmMWIo",
            "https://www.youtube.com/live/RXRYkmqlzYg",
            "https://www.youtube.com/live/qAF9hUDy5QA",
            "https://www.youtube.com/live/btKMZ1Mil2E",
            "https://www.youtube.com/live/qGKTtDbR0RQ",
            "https://www.youtube.com/live/xpBdoFVcxqM",
            "https://www.youtube.com/live/SIuKsyLjx_k",
            "https://www.youtube.com/live/EbTb9_XmoNo",
            "https://www.youtube.com/live/0Hio3WtLzS8",
            "https://www.youtube.com/live/PnDGWsq2lDg",
            "https://www.youtube.com/live/SBjSYuFYREM",
            "https://www.youtube.com/live/D4tase_ZpPo",

            "https://www.youtube.com/live/3_E_5ChnHMo",
            "https://www.youtube.com/live/tspcL7rbPoQ",
            "https://www.youtube.com/live/JvFforC6Leo",
            "https://www.youtube.com/live/X4PlKUKbITE",
            "https://www.youtube.com/live/wYP5uO87LEs",
            "https://www.youtube.com/live/OEktvjPTmD8",
            "https://www.youtube.com/live/YHtACSLnZpo",
            "https://www.youtube.com/live/KGhP9vr_yY8",
            "https://www.youtube.com/live/ta9xW-H8hwA",
            "https://www.youtube.com/live/xLY0t5KWkjI",
            "https://www.youtube.com/live/xxtcSHeliv0",
            "https://www.youtube.com/live/QnW7gTYUZ5o",
            "https://www.youtube.com/live/cRWPZ610i9k",
            "https://www.youtube.com/live/xVROwVEmQ8I",
            "https://www.youtube.com/live/ZkJycVRtAtc",
            "https://www.youtube.com/live/Cmos26tmRmA",
            "https://www.youtube.com/live/jDAE-qg4Zdw",
            "https://www.youtube.com/live/gL_x_0ZieCY",
            "https://www.youtube.com/live/uNr67Tkl-W4",
            "https://www.youtube.com/live/NTUBHLcOcPM",
            "https://www.youtube.com/live/pK63q0EIqSw",
            "https://www.youtube.com/live/Kh5fMG7ZBKU",
            "https://www.youtube.com/live/KhdbKAHqiB8",
            "https://www.youtube.com/live/pK63q0EIqSw",
            "https://www.youtube.com/live/Kh5fMG7ZBKU",
            "https://www.youtube.com/live/KhdbKAHqiB8",
            "https://www.youtube.com/live/QYWG6lCG9Ps?feature=share",
            "https://www.youtube.com/live/aYP9XG790aQ?feature=share",
            "https://www.youtube.com/live/EP1Eixr76R4?feature=share",
            "https://www.youtube.com/live/j2xTsy1iTv4?feature=share",
            "https://www.youtube.com/live/4j9w47UFG10?feature=share",
            "https://www.youtube.com/live/2ApErMb_QLM?feature=share",
            "https://www.youtube.com/live/VWK2B3gKtvU?feature=share",
            "https://www.youtube.com/live/z1g4zHEXmW0?feature=share",
            "https://www.youtube.com/live/frbV2fhE9ao?feature=share",
            "https://www.youtube.com/live/g2eJYfMw82I?feature=share",            
            "https://www.youtube.com/live/X1LUqYLEguk?feature=share",            
            "https://www.youtube.com/live/1uTqPLreNv0?feature=share",            
            "https://www.youtube.com/live/g-gYyTuq394?feature=share",            
            "https://www.youtube.com/live/EbTb9_XmoNo?feature=share",            
            "https://www.youtube.com/live/puuPrq276MQ?feature=share",            
            "https://www.youtube.com/live/lrsD5dq4uD4?feature=share",            
            "https://www.youtube.com/live/aIcDciLRqlY?feature=share",            
            "https://www.youtube.com/live/qR5jU_SkAzQ?feature=share",            
            "https://www.youtube.com/live/RP0tpbA31RU?feature=share",            
            "https://www.youtube.com/live/agPTqdXPpCI?feature=share",            
            "https://www.youtube.com/live/IyustP8aGnA?feature=share",            
            "https://www.youtube.com/live/fMgcmcBfuYc?feature=share",            
            "https://www.youtube.com/live/OE58xfBLSOI?feature=share",            
            "https://www.youtube.com/live/M5Q0Aol_S4Q?feature=share",            
            "https://www.youtube.com/live/_pTRF9rjuy8?feature=share",            
            "https://www.youtube.com/live/ztqeT34loHQ?feature=share",            
            "https://www.youtube.com/live/LbS9htuwPls?feature=share",            
            "https://www.youtube.com/live/WLNqU62DME8?feature=share",            
            "https://www.youtube.com/live/pWlDgryH9OQ?feature=share",            
            "https://www.youtube.com/live/YK9eeXjsVQ0?feature=share",            
            "https://www.youtube.com/live/LKK7ErT-i4Q?feature=share",            
            "https://www.youtube.com/live/Gyi4IIp6fjk?feature=share",            
            "https://www.youtube.com/live/Y_CwvF0eod0?feature=share",            
            "https://www.youtube.com/live/Lm7ZpW_9Nz0?feature=share",            
            "https://www.youtube.com/live/xi7xdCJui6U?feature=share",            
            "https://www.youtube.com/live/-hda6TlqWag?feature=share",            
            "https://www.youtube.com/live/B0_TOw0b6qU?feature=share",            
            "https://www.youtube.com/live/luBhaRVAnxA?feature=share",            
            "https://www.youtube.com/live/WGa8UL2MIP4?feature=share",            
            "https://www.youtube.com/live/Cim_xMVapCI?feature=share",            
            "https://www.youtube.com/live/2_7ilbU37LM?feature=share",            
            "https://www.youtube.com/live/2euuIZxvm14?feature=share",            
            "https://www.youtube.com/live/GTptMnUfRXA?feature=share",            
            "https://www.youtube.com/live/j-5Jqzyo5Lw?feature=share",            
            "https://www.youtube.com/live/fg3qkfgOYjc?feature=share",            
            "https://www.youtube.com/live/QI_stLMJRGY?feature=share",            
            "https://www.youtube.com/live/E-eJi-IhMe0?feature=share",            
            "",            
            "",            
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
