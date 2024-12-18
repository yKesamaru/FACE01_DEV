"""npKnown.npzファイルを指定したディレクトリとそのサブディレクトリごとに作成するスクリプト.

Summary:
    このスクリプトは、ユーザーが指定したディレクトリとそのサブディレクトリ内にある顔画像ファイルに対して
    512次元特徴量データを用いたnpKnown.npzファイルを生成します。
    選択されたディレクトリ以下の各サブディレクトリについて、npKnown.npzファイルが既に存在する場合はスキップし、
    存在しない場合にのみ新たに作成します。

Requirements:
    - ttkbootstrap
    - face01lib.load_preset_image

Usage:
    ターミナルで以下のコマンドを実行してスクリプトを起動します。

    ```bash
    python3 example/make_npKnown_for_subdirs.py
    ```

Example:
    実行後、ディレクトリ選択ダイアログが表示され、処理対象のディレクトリを選択できます。
    選択したディレクトリ内のサブディレクトリごとにnpKnown.npzファイルが作成されます。

.. image:: ../assets/images/one_point_L.png
    :width: 70%
    :alt: one point

ディレクトリを再帰的に捜査してnpKnown.npzを作成します⭐️''

.. image:: ../assets/images/npKnown.png
    :width: 50%
    :alt: npKnown.npz



Source code:
    `make_npKnown_for_subdirs.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/make_npKnown_for_subdirs.py>`__
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
    """
    ディレクトリ選択ダイアログを表示し、ユーザーが選択したディレクトリのパスを返します。

    Returns:
        str: 選択されたディレクトリのパス。選択されなかった場合は空文字列を返します。
    """
    root = ttk.Window(themename="minty")
    root.withdraw()  # ウィンドウを非表示にする
    selected_directory = filedialog.askdirectory(
        title="ディレクトリを選択。`assets/data/a`を選択してみましょう。", initialdir=os.getcwd())
    root.destroy()  # ウィンドウを破棄する
    return selected_directory


def create_npz_for_all_subdirs(root_dir, load_preset_image_obj):
    """
    指定したディレクトリ以下の1階層目のサブディレクトリに対して、
    npKnown.npzファイルを作成します。

    Args:
        root_dir (str): ルートディレクトリのパス。
        load_preset_image_obj (LoadPresetImage): 画像読み込み用のオブジェクト。
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for subdir in dirnames:
            if subdir in ["not_me", "multipleFaces", "noFace", "same_default_files", "same_face"]:
                continue
            else:
                # npKnown.npz ファイルが存在する場合は処理をスキップ
                npz_file_path = os.path.join(dirpath, subdir, 'npKnown.npz')
                if os.path.exists(npz_file_path):
                    print(f"{npz_file_path} は既に存在します。処理をスキップします。")
                    continue
                else:
                    # ディレクトリ内に画像ファイルが存在するか確認
                    image_files = [file for file in filenames if file.lower().endswith('.png')]
                    if image_files:
                        print(f"{npz_file_path} を作成します...")
                        load_preset_image_obj.load_preset_image(
                            deep_learning_model=1,
                            RootDir=dirpath,               # npKnown.npzを作成するディレクトリ
                            preset_face_imagesDir=dirpath  # 顔画像が格納されているディレクトリ
                        )
                        print(f"{npz_file_path} を作成しました。")
                    else:
                        print(f"{dirpath} に画像ファイルが見つかりませんでした。処理をスキップします。")


if __name__ == '__main__':
    load_preset_image_obj = LoadPresetImage()

    # ダイアログを表示してディレクトリを選択
    root_dir = select_directory()
    if not root_dir:
        print("ディレクトリが選択されませんでした。プログラムを終了します。")
        sys.exit()

    # サブディレクトリごとにnpKnown.npzを作成
    create_npz_for_all_subdirs(root_dir, load_preset_image_obj)
