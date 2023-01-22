# mirror_200cc_anaylyer

マリオカートの8DXの野良レートのミラー率・200cc率を分析するためのツール群です。  
YouTubeのプレイ動画をダウンロードして、画像解析で各レースの情報を取得・集計しています。

Windows11のPowerShellで動作を確認しています。使用したpythonのバージョンは3.8.10です。


## セットアップ

PowerShell + Python 3.8.10 + CUDA11.8

```powershell
# python 3.8.10, CUDA Version 11.8
python -m pip install -U pip
python -m pip install -r ../requirements.txt
python -m pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
python -m pip install git+https://github.com/openai/CLIP.git
```


## 

```
python download_youtube --out_dir output/videos/person1
```


##

```
python playerlist_screens.py --video_dir output/videos/personX --out_dir output/images
```


##

```
python race_information.py --video_dir output/videos/personX --out_dir output/images
```



##

```
python post_analyze.py 
```


