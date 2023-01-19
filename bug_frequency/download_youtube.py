from pytube import YouTube

# 岸堂天真さん
video_urls = [
    'https://youtu.be/2T9CSdLG4Uc',
    "https://youtu.be/tSje7fBabcU",
    "https://youtu.be/qkQpFmBagOk",
    "https://youtu.be/hNBsv_xw2dM",
    "https://youtu.be/X_T8d5vHusU",
    "https://youtu.be/KH1N5K-d7ZY",
    "https://youtu.be/bpujYlvwE-Q",
    "https://youtu.be/vv05PaMeXXE",
    "https://youtu.be/5bQt063y8Tw",
    "https://youtu.be/JAre5u7M8fM",
    "https://youtu.be/wcDW6ok_2u0",
    "https://youtu.be/H10NutNHJYo",
    "https://youtu.be/uwO357yKr24",
    "https://youtu.be/GD8Mam46TK4",
    "https://youtu.be/I9zX_XDf5hw",
    "https://youtu.be/p-SZeBtdLeo",
    "https://youtu.be/8nePRlD_C1w",
    # ここより上はDLC3
    "https://youtu.be/pEJQqG6H3L8",
    "https://youtu.be/IngTu2nA9Yk",
    "https://youtu.be/-JD_JFeumPM",
    "https://youtu.be/_i4fSyhT1Us",
    "https://youtu.be/L5N8yC-tuso",
    "https://youtu.be/zSb7EcicOW8",
    "https://youtu.be/FrAopgit4fU",
    "https://youtu.be/7Mouo4NC42U",
    "https://youtu.be/tAomMmPvyHQ",
    "https://youtu.be/SfXhjZPHiOU",
    "https://youtu.be/IzGbDA7MFLQ",
    "https://youtu.be/miocd9sWJ-Q",
    "https://youtu.be/KjZqY223-GY",
    "https://youtu.be/2SlMKr6TSpk",
    "https://youtu.be/CQlZPk3En_w",
]

for url in video_urls:
    stream = YouTube(url).streams.filter(
        file_extension='mp4').order_by('resolution').desc().first()
    print("Downloading", url, stream.title)
#    stream.download("E:/prog/python/mk8dx_tools/videos")
    print
