import subprocess
import tempfile
from PIL import Image
import shutil
import datetime
import os

import streamlit as st
import cv2
import numpy as np
import ffmpeg



def generate_output_filename(input_filename, suffix):
    # 入力ファイル名から拡張子を取り除く
    name, ext = os.path.splitext(input_filename)
    datetime_str = datetime.datetime.now().strftime("%Y%m%d")

    # 新しいファイル名を生成する
    output_filename = f"{name}-EFF_{datetime_str}{suffix}"
    return output_filename



def save_uploaded_file(uploaded_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix="." + uploaded_file.name.split('.')[-1]) as tmp_file:
            shutil.copyfileobj(uploaded_file, tmp_file)
            return tmp_file.name
    except Exception as e:
        st.error(f"ファイルの保存中にエラーが発生しました: {e}")
        return None



def get_video_duration(video_path):
    try:
        # ffprobeを使って動画の情報を取得
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                    "format=duration", "-of",
                                    "default=noprint_wrappers=1:nokey=1", video_path],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        # 出力から動画の長さ（秒）を取得
        duration = round(float(result.stdout), 1)
        encode_duration = round((duration*0.4) / 60, 1)
        st.info(f"動画の長さ： {duration}秒")
        st.info(f"処理にかかる時間： およそ{encode_duration}分")
        return duration
    except Exception as e:
        print(f"Error getting video duration: {e}")
        return 0



def process_video(video_path, output_path, has_no_audio:bool, has_hfi:bool, ambiguity:str, show_logs:bool):
    
    audio_bitrate_kbps = 0 if has_no_audio else 256
    duration = get_video_duration(video_path)

    if ambiguity == "Mid":

        bitrate = 16
        bright = 0.4
        saturation = 0.5
        lpf = 300

    elif ambiguity == "Classic":

        bitrate = 1
        bright = 0
        saturation = 1
        lpf = 5000

    elif ambiguity == "Low":

        bitrate = 32
        bright = 0.3
        saturation = 0.6
        lpf = 500

    elif ambiguity == "High": 

        bitrate = 8
        bright = 0.45
        saturation = 0.4
        lpf = 220

    elif ambiguity == "Extreme": 

        bitrate = 4
        bright = 0.5
        saturation = 0.4
        lpf = 170

    
    video_filters = ("fps=30," + ("scale=trunc(iw/2)*2:trunc(ih/2)*2") + 
                    f",eq=brightness={bright}:saturation={saturation}:contrast=0.5" +
                    f",gblur=sigma=1:steps=2:planes=15:sigmaV=-1"
                    )
    

    audio_filters = f"highpass=f=30,lowpass=f={lpf}" if has_hfi else f"highpass=f=20,lowpass=f=18000"
    
    if not has_no_audio:
        if ambiguity == "Classic":

            video_filters = "fps=30," + ("scale=trunc(iw/2)*2:trunc(ih/2)*2")

            ffmpeg_command = (
            ffmpeg
            .input(video_path)
            .output(output_path, vcodec='libx264', acodec='aac', audio_bitrate='256k', 
                    video_bitrate=f'{bitrate}k', vf=video_filters, af=audio_filters)
            .overwrite_output()
            .compile()
            )
        else:
            ffmpeg_command = (
                ffmpeg
                .input(video_path)
                .output(output_path, vcodec='libx264', acodec='aac', audio_bitrate='256k', 
                        crf=f'{bitrate}k', vf=video_filters, af=audio_filters)
                .overwrite_output()
                .compile()
            )

    else:
        ffmpeg_command = (
            ffmpeg
            .input(video_path)
            .output(output_path, vcodec='libx264', video_bitrate=f'{bitrate}k', vf=video_filters, an=None)
            .overwrite_output()
            .compile()
        )

    # ffmpegコマンドを実行
    try:
        process = subprocess.run(ffmpeg_command, text=True, capture_output=True)
        if process.returncode != 0:
            st.error(f"ffmpeg error: {process.stderr}")

    except Exception as e:
        st.error(f"処理中にエラーが発生しました: {e}")




def main():

    st.set_page_config(
        page_title = "Ambiguous World",
        page_icon = "🦋",
        layout = "centered",
        initial_sidebar_state = "collapsed",
        menu_items = {
            'Get Help': 'https://github.com/omitanc/blueberry',
            'About': "H.264の圧縮ノイズを逆手に取ったビデオエフェクターです。"
        }
    )

    st.title("🦋 Ambiguous World")
    st.subheader("H.264の圧縮ノイズを逆手に取ったビデオエフェクターです。")
    
    st.write("\n  \n")
    st.write("\n  \n")

    is_devmode = st.sidebar.checkbox("Developer mode")

    
    files = st.file_uploader("ファイルをアップロードしてください", type=['mov', 'mp4', "quicktime"], accept_multiple_files = True)
    
    with st.expander("あいまいさ設定（Ambiguity Adjustment）", expanded=False):
        if not is_devmode:
            ambiguity = st.radio(label="",
                        options=("Classic", "Low", "Mid", "High", "Extreme"), index=2, horizontal=True,
                        )
        else:
            ambiguity = st.text_input("カスタム指定", value="")

    
    st.write("\n  \n")
    st.text("オプション")
    

    has_no_audio = st.checkbox("音声を除去する", False, help="音声を除去します。")
    has_hfi = st.checkbox("Hearing from the INSIDE", True, help="こもった曖昧な音になります。Classicモードでは無効です。")
    
    # ファイルがアップロードされていない場合はここで終了
    if len(files) == 0:
        st.info("ファイルをアップロードしてください。")
        st.stop()

    # アップロードされたファイルを処理
    for file in files:
        if file is None:
            st.warning("ファイルがアップロードされていません。")
            st.stop()
        
        saved_file_path = save_uploaded_file(file)


        st.write("\n  \n")

        if st.button('エフェクト処理開始', use_container_width=True):
            output_filename = generate_output_filename(file.name, ".mp4" if "video" in file.type else ".jpg")
            output_file_path = os.path.join(tempfile.gettempdir(), output_filename)
            
            if saved_file_path:

                with st.spinner("処理中..."):
                    
                    process_video(saved_file_path, output_file_path, has_no_audio, has_hfi, ambiguity, is_devmode)
                    st.success("動画処理が完了しました。")
                    st.video(output_file_path)
                    # ダウンロードボタンを表示
                    with open(output_file_path, "rb") as file:
                        btn = st.download_button(
                            label="ダウンロード",
                            data=file,
                            file_name=output_filename,
                            mime="video/mp4",
                            use_container_width=True
                        )
            else:
                st.error("サポートされていないファイル形式です。")



if __name__ == "__main__":
    main()