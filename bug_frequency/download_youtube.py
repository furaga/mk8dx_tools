from pytube import YouTube


from pathlib import Path


def download_videos(video_urls, person_name):
    import re
    for k, urls in video_urls.items():
        for url in urls:
            stream = YouTube(url).streams.filter(
                file_extension='mp4').order_by('resolution').desc().first()
            print("Downloading", url, stream.title)
            out_dir = "E:/prog/python/mk8dx_tools/videos/" + person_name + "/" + k
            Path(out_dir).mkdir(exist_ok=True, parents=True)
            fname = stream.title + "-" + (url.split('/')[-1])
            fname = re.sub(r'[\\|/|:|?|.|"|<|>|\|]', '', fname)
            fname += ".mp4"
            print("Saving", out_dir, "|", fname)
            stream.download(out_dir, fname)


# # 岸堂天真さん
# video_urls = [
#     'https://youtu.be/2T9CSdLG4Uc',
#     "https://youtu.be/tSje7fBabcU",
#     "https://youtu.be/qkQpFmBagOk",
#     "https://youtu.be/hNBsv_xw2dM",
#     "https://youtu.be/X_T8d5vHusU",
#     "https://youtu.be/KH1N5K-d7ZY",
#     "https://youtu.be/bpujYlvwE-Q",
#     "https://youtu.be/vv05PaMeXXE",
#     "https://youtu.be/5bQt063y8Tw",
#     "https://youtu.be/JAre5u7M8fM",
#     "https://youtu.be/wcDW6ok_2u0",
#     "https://youtu.be/H10NutNHJYo",
#     "https://youtu.be/uwO357yKr24",
#     "https://youtu.be/GD8Mam46TK4",
#     "https://youtu.be/I9zX_XDf5hw",
#     "https://youtu.be/p-SZeBtdLeo",
#     "https://youtu.be/8nePRlD_C1w",
#     # ここより上はDLC3
#     "https://youtu.be/pEJQqG6H3L8",
#     "https://youtu.be/IngTu2nA9Yk",
#     "https://youtu.be/-JD_JFeumPM",
#     "https://youtu.be/_i4fSyhT1Us",
#     "https://youtu.be/L5N8yC-tuso",
#     "https://youtu.be/zSb7EcicOW8",
#     "https://youtu.be/FrAopgit4fU",
#     "https://youtu.be/7Mouo4NC42U",
#     "https://youtu.be/tAomMmPvyHQ",
#     "https://youtu.be/SfXhjZPHiOU",
#     "https://youtu.be/IzGbDA7MFLQ",
#     "https://youtu.be/miocd9sWJ-Q",
#     "https://youtu.be/KjZqY223-GY",
#     "https://youtu.be/2SlMKr6TSpk",
#     "https://youtu.be/CQlZPk3En_w",
# ]


# 　https://www.youtube.com/watch?v=nzkk2hCIVdo&ab_channel=%E3%83%96%E3%83%A9%E3%83%83%E3%82%AD%E3%83%BC
# ブラッキーさん
video_urls = {
    # "DLC3": [
    #     "https://youtu.be/nzkk2hCIVdo",
    #     "https://youtu.be/75K-jf6kiNg",
    #     "https://youtu.be/EWku3jjfXpQ",
    #     "https://youtu.be/Q6KToe0jD1U",
    #     "https://youtu.be/Ny5KwmSNK90",
    # ],
    # "DLC2": [
    #     "https://youtu.be/XcWnOL9xZ1s",
    #     "https://youtu.be/ZnLUy6xvL_Y",
    #     "https://youtu.be/6DQyQ6DIMJs",
    #     "https://youtu.be/g0eY9QtyLPE",
    #     "https://youtu.be/e3b8op8IvtU",
    # ],
    "DLC2": [
        "https://youtu.be/zsL5n1IFU68",
        "https://youtu.be/QEpltEr0q4k",
        "https://youtu.be/YJWD_8gEKXs",
        "https://youtu.be/1fg5ZpZsagM",
        "https://youtu.be/53w-2r_KqbY",
        "https://youtu.be/Sh2z7_xQ8GU",
    ],
    # "DLC1": [
    #     "https://youtu.be/W9jHYnFrfzc",
    #     "https://youtu.be/SAvl3fT0mrA",
    #     "https://youtu.be/XgP2BNzrJdI",
    #     "https://youtu.be/7-wos2ZnFtQ",
    #     "https://youtu.be/BKZdgAR-vEg",
    # ],
    # "DLC0": [
    #     "https://youtu.be/fZdBFzbT6aU",
    #     "https://youtu.be/5pChjtll3mo",
    #     "https://youtu.be/WHrVlKHFFCQ",
    #     "https://youtu.be/6ZxshMoF31Q",
    #     "https://youtu.be/S4Wb_3Ey0eU",
    #     "https://youtu.be/69XUTaAdpOE",
    #     "https://youtu.be/1ztAJrB1GQE",
    #     "https://youtu.be/cCHJutf_PgI",
    #     "https://youtu.be/wG8IlC2fiaQ",
    #     "https://youtu.be/-U8P4xIGymY",
    #     "https://youtu.be/DGn9u5jBVDA",
    #     "https://youtu.be/CoiTdnxICSc",
    #     "https://youtu.be/qgYGBwHqY5s",
    # ],
}

download_videos(video_urls, "person3")

# シェリンさん
video_urls = {
    # "DLC3": [
    #     "https://youtu.be/xERDoA3mgIw",
    #     "https://youtu.be/VNLlwQSJSfE",
    #     "https://youtu.be/zm5VwwoQztI",
    #     "https://youtu.be/VszRAi9nVKY",
    #     "https://youtu.be/rkUcfa7GL70",
    # ],
    # "DLC2": [
    #     "https://youtu.be/gSM0HcdIOE8",
    #     "https://youtu.be/XleWTEZcM4E",
    #     "https://youtu.be/6XaYGemD6Ac",
    #     "https://youtu.be/MmaKrHaR9k0",
    #     "https://youtu.be/Pji7YOP8XLI",
    # ],
    "DLC2": [
        "https://youtu.be/uTxIxTwB0Wg",
        "https://youtu.be/c0isk0voHF0",
        "https://youtu.be/oJ7U3GQGgJ8",
        "https://youtu.be/mMPN5gRXR-c",
        "https://youtu.be/_71RHmtzTWQ",
    ],
    # "DLC1": [
    #     "https://youtu.be/vZLwTcXkbB4",
    #     "https://youtu.be/QDM3tvKEvOY",
    #     "https://youtu.be/Hv5r1LkhYkI",
    #     "https://youtu.be/0cZzGpwBArw",
    #     "https://youtu.be/08dkFLAHPMo",
    # ],
    # "DLC0": [
    #     "https://youtu.be/acsFSDFCv-Y",
    #     "https://youtu.be/dy8UdCgBxiM",
    #     "https://youtu.be/DbdzGSB3R6Y",
    #     "https://youtu.be/7pJUn-jVYvY",
    #     "https://youtu.be/iKb_qD6oFvc",
    # "https://youtu.be/aGOVGK3ZEuY",
    # "https://youtu.be/wJ_Y-0BW8XM",
    # ]
}

download_videos(video_urls, "person1")
