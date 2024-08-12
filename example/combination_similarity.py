"""顔画像ファイルの全組み合わせを計算する例.

Summary:
    このシンプルなコード例では、日本人専用として学習された顔学習モデルであるJAPANESE FACE V1を用いて、顔画像同士の全ての組み合わせを計算します。

    顔画像ファイルが異なるディレクトリに配置され、また各ディレクトリにはすでに`npKnown.npz`ファイルが作成済みなものと想定しています。

    このコードは`Zenn`の記事のコード例です。

    `【faiss】なにこれすごい。顔データセットの間違い探し 成功編③ <https://zenn.dev/ykesamaru/articles/4e40e0285b0b66>`_

    詳しくは上記記事をご参照ください。
    このコード例では組み合わせパターンが爆発的に大きくなると処理時間もそれに応じて爆発的に大きくなるコード例を示しています。

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

root_dir: str = "assets/data"

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
                # # output.txtとして外部ファイルに出力
                # with open("output.txt", mode="a") as f:
                #     f.write(f"{name_1},{name_2},{cos_sim}\n")
                # stdoutに出力
                print(f"{name_1},{name_2},{cos_sim}")
            # print(f"{name_1} and {name_2} : {cos_sim}")
