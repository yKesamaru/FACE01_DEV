"""Example program to create npKnown.npz file.

Summary:
    In this example you can learn how to make npKnown.npz file.
    ディレクトリ選択ダイアログでは'preset_face_images'ディレクトリを選択してください。
    それ以外の場合はエラーが発生します。
    'preset_face_images'ディレクトリを選択すると、同ディレクトリ内に'npKnown.npz'といくつかのフォルダが作成されます。

Example:
    .. code-block:: bash

        python3 example/make_npKnown_file.py

Source code:
    `make_npKnown_file.py <../example/make_npKnown_file.py>`_

Copyright Owner: Yoshitsugu Kesamaru
Please refer to the separate license file for the license of the code.
"""

import os
import sys
from tkinter import filedialog

import ttkbootstrap as ttk

# 現在のディレクトリを設定
dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)
from face01lib.load_preset_image import LoadPresetImage


def select_directory():
    """ディレクトリ選択ダイアログを表示し、選択したディレクトリを返す"""
    root = ttk.Window(themename="minty")
    root.withdraw()  # ウィンドウを非表示にする
    selected_directory = filedialog.askdirectory(
        title="ディレクトリを選択", initialdir=os.getcwd())
    root.destroy()  # ウィンドウを破棄する
    return selected_directory


if __name__ == '__main__':
    load_preset_image_obj = LoadPresetImage()

    # ダイアログを表示してディレクトリを選択
    root_dir = select_directory()
    if not root_dir:
        print("ディレクトリが選択されませんでした。プログラムを終了します。")
        sys.exit()

    # ディレクトリ内のすべてのpngファイルを処理
    for file_name in os.listdir(root_dir):
        if file_name.lower().endswith('.png'):
            file_path = os.path.join(root_dir, file_name)
            load_preset_image_obj.load_preset_image(
                deep_learning_model=1,
                RootDir=root_dir,  # npKnown.npzを作成するディレクトリ
                preset_face_imagesDir=root_dir  # 顔画像が格納されているディレクトリ
            )
