"""指定されたディレクトリ内のすべてのnpKnown.npzファイルを読み込み、faissを使用して指定された組み合わせのコサイン類似度を検出するコードの例.

Summary:
    この例では、指定されたディレクトリ内のすべてのnpKnown.npzファイルを読み込み、faissを使用して指定された組み合わせのコサイン類似度を検出する方法を学ぶことができます。

Results:
    プロジェクトルートディレクトリにoutput.csvが作成されます。

Example:
    .. code-block:: bash

        python3 example/faiss_combination_similarity.py

.. image:: ../assets/images/one_point_R.png
    :width: 70%
    :alt: one point

この例では扱う顔画像ファイル数が非常に少ないためfaissには向いていないです💦

学習モデルの大規模データセットに用いると良いでしょう⭐️'' （その場合はnlistの値を変えてくださいね💗）



Source code:
    `faiss_combination_similarity.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/faiss_combination_similarity.py>`_
"""

# Operate directory: Common to all examples
import os.path
import sys

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

import os
import time

import faiss
import numpy as np

from face01lib.load_preset_image import LoadPresetImage

if __name__ == '__main__':

    # 処理開始時刻を記録
    start_time = time.time()

    load_preset_image_obj = LoadPresetImage()

    # FAISSインデックスの設定
    dimension = 512  # ベクトルの次元数
    nlist = 4  # クラスタ数（Default: 100）
    # 量子化器を作成（内積を使用）
    quantizer = faiss.IndexFlatIP(dimension)
    # IVFフラットインデックスを作成
    index = faiss.IndexIVFFlat(
        quantizer, dimension, nlist, faiss.METRIC_INNER_PRODUCT)

    # DEBUG:
    # print(os.getcwd())

    # データのルートディレクトリ
    root_dir = os.getcwd()
    # カレントディレクトリを変更
    data_dir = os.path.join(root_dir, 'assets/data/')
    # DEBUG:
    # print(os.getcwd())

    # サブディレクトリのリストを作成
    sub_dir_path_list = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]

    # データ格納用のリスト
    all_model_data = []
    all_name_list = []
    all_dir_list = []  # ディレクトリ情報も保存

    # サブディレクトリにnpKnown.npzがあれば削除し、再度作成する
    for sub_dir in sub_dir_path_list:
        npz_file = os.path.join(sub_dir, "npKnown.npz")
        if os.path.exists(npz_file):
            os.remove(npz_file)
            print(f"Deleted: {npz_file}")
        else:
            print(f"File not found: {npz_file}")

        load_preset_image_obj.load_preset_image(
            deep_learning_model=1,
            RootDir=os.path.join(data_dir, sub_dir),  # npKnown.npzを作成するディレクトリ
            preset_face_imagesDir=os.path.join(data_dir, sub_dir)  # 顔画像が格納されているディレクトリ
        )

    # 各サブディレクトリからデータを読み込む
    for dir in sub_dir_path_list:
        npz_file = os.path.join(data_dir, dir, "npKnown.npz")
        with np.load(npz_file) as data:
            model_data = data['efficientnetv2_arcface']
            name_list = data['name']
            # データの形状を変更し、L2正規化を行う
            model_data = model_data.reshape((model_data.shape[0], -1))
            faiss.normalize_L2(model_data)
            # データをリストに追加
            all_model_data.append(model_data)
            all_name_list.extend(name_list)
            all_dir_list.extend([dir] * len(name_list))

    # データをnumpy配列に変換
    all_model_data = np.vstack(all_model_data)

    # 量子化器を訓練し、データを追加
    index.train(all_model_data)  # type: ignore
    index.add(all_model_data)  # type: ignore

    # 類似度が高い要素を検索
    k = 10
    D, I = index.search(all_model_data, k)  # type: ignore

    # 結果を保存
    processed_pairs = set()  # 既に処理されたペアを保存するセット
    with open("output.csv", "a") as f:
        for i in range(D.shape[0]):
            for j in range(D.shape[1]):
                # ペアをアルファベット順にソートしてタプルとして保存
                sorted_pair = tuple(sorted([all_name_list[i], all_name_list[I[i, j]]]))
                # コサイン類似度が0.4以上で、同じディレクトリでない場合、かつ、まだ処理されていないペアの場合に出力
                if D[i, j] >= 0.4 and all_dir_list[i] != all_dir_list[I[i, j]] and sorted_pair not in processed_pairs:
                    f.write(f"{all_name_list[i]},{all_name_list[I[i, j]]},{D[i, j]}\n")
                    processed_pairs.add(sorted_pair)  # ペアを処理済みとしてセットに追加

    # 処理時間を計算して出力
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    print(f"処理時間: {int(minutes)}分 {seconds:.2f}秒")
