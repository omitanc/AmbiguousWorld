# AmbiguousWorld

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blueberry.streamlit.app/)

<br>

H.264の圧縮ノイズを逆手に取ったエフェクターです。何が映っているか、ギリギリわかるくらいの曖昧さまで画質や色、動きを劣化させ、現実離れした綺麗で不思議な世界を演出します。

---


# 環境構築



### 依存関係のインストール

```python
brew install ffmpeg
```

<br>

```python
pip install -r requirements.txt
```

---

# WebUIの起動


```python
streamlit run app.py
```

<br>

# 参考

- [OpenCV Official Docs](https://docs.opencv.org/4.0.1/d4/da8/group__imgcodecs.html#ga292d81be8d76901bff7988d18d2b42ac)
- [FFmpeg Codecs Documentation](https://ffmpeg.org/ffmpeg-codecs.html#libx264_002c-libx264rgb)
- [Python, OpenCVで画像ファイルの読み込み、保存](https://note.nkmk.me/python-opencv-imread-imwrite/)
- [Streamlitのレイアウトとコンテナを見てみよう](https://welovepython.net/streamlit-layout-container/#toc4)
- [【ffmpeg】ffmpegコマンドの備忘録(タイムラプス、切り抜き、アニメGIF、ビットレート指定、コーデック、音消し、手振れ補正、明るさ）](https://qiita.com/riversun/items/6ff25fe8620457342a5e)
- [非エンジニアが音響知識だけでffmpegのコードサンプル作ってみた](https://tech-blog.voicy.jp/entry/2021/12/07/130000)
- [FFmpegで動画と画像をブレンド合成して透過する](https://askthewind.hatenablog.com/entry/2018/12/22/140629)

<br>

開発者テスト環境：python 3.11.8, MacOS 12.5
