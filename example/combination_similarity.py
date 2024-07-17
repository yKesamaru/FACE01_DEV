"""License for the Code.

Copyright Owner: Yoshitsugu Kesamaru
Please refer to the separate license file for the license of the code.
"""

"""Example of calculating of all combinations of face image files.

Summary:
    This is a sample code that calculates the similarity of all combinations of face image files,
    using the efficientnetv2_arcface.onnx model, which is a Japanese-only learning model.

Example:
    .. code-block:: bash
    
        python3 example/combination_similarity.py
        
Source code:
    `combination_similarity.py <../example/combination_similarity.py>`_
"""
# Operate directory: Common to all examples
import os
import os.path
import sys
from itertools import combinations, product

import numpy as np
from tqdm import tqdm

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

    # サブディレクトリの組み合わせを生成
    for combo in tqdm(combinations(sub_dir_path_list, 2)):
        dir1, dir2 = combo
        npz_file1 = os.path.join(dir1, "npKnown.npz")
        npz_file2 = os.path.join(dir2, "npKnown.npz")

        # npzファイルを読み込む
        with np.load(npz_file1) as data:
            model_data_list_1 = data['efficientnetv2_arcface']
            name_list_1 = data['name']
        with np.load(npz_file2) as data:
            model_data_list_2 = data['efficientnetv2_arcface']
            name_list_2 = data['name']
        for (name_1, element1), (name_2, element2) in product(zip(name_list_1, model_data_list_1), zip(name_list_2, model_data_list_2)):
            emb1 = element1.flatten()
            emb2 = element2.flatten()
            cos_sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

            # コサイン類似度が0.4以上の場合、出力
            if cos_sim >= 0.4:
                with open("output.txt", mode="a") as f:
                    f.write(f"{name_1},{name_2},{cos_sim}\n")
            # print(f"{name_1} and {name_2} : {cos_sim}")