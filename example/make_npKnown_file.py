"""プリセット画像をロードし、npKnown.npzファイルの存在を確認するコードの例.

Summary:
    このコードは、ディレクトリ選択ダイアログを表示し、選択したディレクトリに`npKnown.npz`ファイルが存在するか確認します。
    ファイルが存在しない場合は、プリセット画像を使用して`npKnown.npz`ファイルを作成します。

Example:
    .. code-block:: bash

        python3 example/make_npKnown_file.py

Source code:
    `make_npKnown_file.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/make_npKnown_file.py>`_
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
        title="ディレクトリを選択。`assets/data/a`を選択してみましょう。", initialdir=os.getcwd())
    root.destroy()  # ウィンドウを破棄する
    return selected_directory


if __name__ == '__main__':
    load_preset_image_obj = LoadPresetImage()

    # ダイアログを表示してディレクトリを選択
    root_dir = select_directory()
    if not root_dir:
        print("ディレクトリが選択されませんでした。プログラムを終了します。")
        sys.exit()

    # 選択したディレクトリ内の全てのサブディレクトリを取得
    for subdir_name in os.listdir(root_dir):
        subdir_path = os.path.join(root_dir, subdir_name)
        if os.path.isdir(subdir_path):
            # npKnown.npz ファイルが存在するか確認
            npz_file_path = os.path.join(subdir_path, 'npKnown.npz')
            if not os.path.exists(npz_file_path):
                # npKnown.npz ファイルが存在しない場合のみ処理を実行
                load_preset_image_obj.load_preset_image(
                    deep_learning_model=1,
                    RootDir=subdir_path,  # npKnown.npzを作成するディレクトリ
                    preset_face_imagesDir=subdir_path  # 顔画像が格納されているディレクトリ
                )
            else:
                print(f"npKnown.npz ファイルは既に存在するため、ディレクトリ {subdir_name} をスキップします。")
        else:
            print(f"{subdir_name} はディレクトリではないため、スキップします。")
