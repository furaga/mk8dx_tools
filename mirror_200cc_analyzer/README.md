# mirror_200cc_anaylyer

マリオカートの8DXの野良レートのミラー率・200cc率を分析するためのツール群です。  
YouTubeのプレイ動画をダウンロードして、画像解析で各レースの情報を取得・集計しています。

<b>集計結果の例 https://docs.google.com/spreadsheets/d/1WAXeMbnZSGLMuhsiXlfcwdMkFvxd_VcAwz0979yXSVE/edit?usp=sharing </b>


## セットアップ

PowerShell + Python 3.8.10 + CUDA11.8

```powershell
# python 3.8.10, CUDA Version 11.8
python -m pip install -U pip
python -m pip install -r ../requirements.txt
python -m pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
python -m pip install git+https://github.com/openai/CLIP.git
```

## YouTube動画のダウンロード

```
python download_youtube.py --target person0 --out_dir output/videos
```

成功すると、`output/vidoes/person0` 以下にダウンロードした動画が保存されます。  
`--target` にはダウンロード対象の配信者を指定してください。（READMEではperson0の例のみ記載）  
配信者・動画URLの一覧はdownload_youtube.py内で定義されています。  


## 参加者一覧画面の抽出

各レース前に表示される参加者一覧画面を各動画から抽出します。  

```
python playerlist_screens.py --video_dir output/videos/person0 --out_dir output/images
```

成功すると下のような画像が `output/images/person0` 以下に保存されます。

<img src="doc/playerlist.png">

## レース詳細情報の取得

参加者一覧画面を画像解析して、レースの詳細情報を取得します。  

```
python race_information.py --img_dir output/images/person0 --out_dir output/race_information
```

成功すると `output/race_information/person0.csv` が出力されます。

具体的には以下を取得してCSV出力します。
- 種目（150cc/200cc/mirror）
- コース名
- 参加者のレート

合わせて、以下の情報もCSVに出力されます。
- 画像パス
- プレイ時期 (DLC0/DLC1/DLC2/DLC3)
    - DLC0: ~2022/3/17
    - DLC1: 2022/3/18~2022/8/4
    - DLC2: 2022/8/5~2022/12/7
    - DLC3: 2022/12/8~

<img src="doc/race_information.png">


## 集計

```
python count.py --out_dir output/race_information
```

成功すると、ミラー率, 200cc率の集計結果がコンソール出力されます。
