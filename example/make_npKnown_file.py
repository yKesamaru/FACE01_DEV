"""`npKnown.npz`ファイルを作成するコードの例.

Summary:
    このエグザンプルでは、`npKnown.npz`ファイルの作成手順を学びます。
    ディレクトリを選択すると、そのディレクトリに含まれる顔画像ファイルを全て読み込み、人物名とその512次元特徴量データをデータセットとして保存します。

    ディレクトリ選択ダイアログでは'preset_face_images'ディレクトリ、あるいはこちらで用意したデータセット（"assets/data/"以下のディレクトリ）を選択してください。
    それ以外の場合はエラーが発生します。

    'preset_face_images'ディレクトリを選択すると、同ディレクトリ内に'npKnown.npz'といくつかのフォルダが作成されます。
    既に'npKnown.npz'ファルがある場合、終了します。その場合は'npKnown.npz'ファイルを手動で削除してから、再度実行してみましょう。

    このコードを実行するには開発用パッケージを追加インストールする必要があります。
    具体的にはrequirements_dev.txtをインストールしてください。

    .. code-block:: bash

        pip install -r requirements_dev.txt

Example:
    .. code-block:: bash

        python3 example/make_npKnown_file.py

    .. image:: ../docs/img/make_noKnown_file.png
        :scale: 100%
        :alt: make_noKnown_file

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

    # npKnown.npz ファイルが存在するか確認
    npz_file_path = os.path.join(root_dir, 'npKnown.npz')
    if not os.path.exists(npz_file_path):
        # npKnown.npz ファイルが存在しない場合のみ処理を実行
        # ディレクトリ内のすべてのpngファイルを処理
        for file_name in os.listdir(root_dir):
            if file_name.lower().endswith('.png'):
                file_path = os.path.join(root_dir, file_name)
                load_preset_image_obj.load_preset_image(
                    deep_learning_model=1,
                    RootDir=root_dir,  # npKnown.npzを作成するディレクトリ
                    preset_face_imagesDir=root_dir  # 顔画像が格納されているディレクトリ
                )
    else:
        print("npKnown.npz ファイルは既に存在するため、処理を終了します。")
