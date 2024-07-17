import os
import os.path
import sys

import numpy as np

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

root_dir: str = "/media/terms/2TB_Movie/face_data_backup/data"
# root_dir: str = "/home/terms/ドキュメント/find_similar_faces/test"

if __name__ == '__main__':
    # ディレクトリのみを対象としたサブディレクトリの絶対パスのリストを取得
    sub_dir_path_list: list = [
        os.path.join(root_dir, sub_dir) 
        for sub_dir in os.listdir(root_dir) 
        if os.path.isdir(os.path.join(root_dir, sub_dir))
    ]
    # 各ディレクトリ内の要素数を保存するリスト
    element_counts = []

    # サブディレクトリのデータを読み込む
    for dir in sub_dir_path_list:
        npz_file = os.path.join(dir, "npKnown.npz")
        with np.load(npz_file) as data:
            name_list = data['name']
            element_counts.append(len(name_list))

    # 試行回数を計算
    total_trials = 0
    for i, count_i in enumerate(element_counts):
        for j, count_j in enumerate(element_counts[i+1:]):
            total_trials += count_i * count_j

    print(f"Total trials for cos_sim >= 0.4: {total_trials:,}")


