"""
npKnown.npzファイルを並列処理で作成するスクリプト.

Summary:
    このスクリプトは、指定されたディレクトリ以下のサブディレクトリを並列処理し、
    各サブディレクトリ内にnpKnown.npzファイルを効率的に作成します。
    並列処理を利用することで、従来の逐次処理よりも高速にファイルを生成できます。

Features:
    - 並列処理を使用して実行速度を向上。
    - サブディレクトリごとにnpKnown.npzファイルを作成。
    - 既存のnpKnown.npzファイルをスキップする仕組み。

Requirements:
    - ttkbootstrap
    - concurrent.futures
    - face01lib.load_preset_image

Example:
    ターミナルで以下のコマンドを実行してスクリプトを起動します。

    ```bash
    python3 example/make_npKnown_parallel.py
    ```

Example:
    実行後、ディレクトリ選択ダイアログが表示されます。
    選択したディレクトリ内のすべてのサブディレクトリに対して、
    並列処理を利用してnpKnown.npzファイルが生成されます。

Source code:
    `make_npKnown_parallel.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/make_npKnown_parallel.py>`__
"""

import os
import sys
from concurrent.futures import ProcessPoolExecutor
from tkinter import filedialog

import ttkbootstrap as ttk

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)
from face01lib.load_preset_image import LoadPresetImage


def select_directory():
    root = ttk.Window(themename="minty")
    root.withdraw()
    selected_directory = filedialog.askdirectory(
        title="ディレクトリを選択。`assets/data/a`を選択してみましょう。", initialdir=os.getcwd())
    root.destroy()
    return selected_directory


def process_subdir(dirpath):
    load_preset_image_obj = LoadPresetImage()  # 各プロセスでインスタンスを生成

    npz_file_path = os.path.join(dirpath, 'npKnown.npz')

    if os.path.exists(npz_file_path):
        print(f"{npz_file_path} は既に存在します。処理をスキップします。")
        return

    image_files = [file for file in os.listdir(dirpath) if file.lower().endswith('.png')]
    if image_files:
        print(f"{npz_file_path} を作成します...")
        load_preset_image_obj.load_preset_image(
            deep_learning_model=1,
            RootDir=dirpath,
            preset_face_imagesDir=dirpath
        )
        print(f"{npz_file_path} を作成しました。")
    else:
        print(f"{dirpath} に画像ファイルが見つかりませんでした。処理をスキップします。")


def create_npz_for_all_subdirs_parallel(root_dir, num_processes=4):
    subdirs = [os.path.join(dirpath) for dirpath, _, _ in os.walk(root_dir)]
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        executor.map(process_subdir, subdirs)


if __name__ == '__main__':
    root_dir = select_directory()
    if not root_dir:
        print("ディレクトリが選択されませんでした。プログラムを終了します。")
        sys.exit()

    create_npz_for_all_subdirs_parallel(root_dir, num_processes=4)
