"""LOFによる外れ値検出スクリプト.

Summary:
    このスクリプトは、指定したディレクトリ内の512次元ベクトルデータ（npKnown.npz形式）を読み込み、Local Outlier Factor（LOF）アルゴリズムを使用して外れ値検出を行います。
    コサイン類似度を基準にして各データの異常スコアを計算し、スコアが閾値を超えるデータを外れ値として判定し、指定のディレクトリに移動します。
    顔認証データセットの一貫性を保つためのツールとして利用できます。

    このスクリプトは、データの正規化、LOFによるスコア計算、外れ値の判定とファイルの移動を行います。

    このコードは`Zenn`の記事のコード例です。

    `コサイン類似度データの中の外れ値をもつファイルを見つける方法 <https://zenn.dev/ykesamaru/articles/bc10aa51772130>`_

    詳しくは上記記事をご参照ください。

Example:
    .. code-block:: bash

        python3 example/LOF_Outlier_Detection.py /path/to/dataset

Source code:
    `LOF_Outlier_Detection.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/LOF_Outlier_Detection.py>`_
"""


import argparse
import os
import shutil
import time

import numpy as np
from sklearn.neighbors import LocalOutlierFactor


def main(root_dir):
    # 処理開始時刻を記録
    start_time = time.time()

    # ベクトルの次元数
    dimension = 512

    # データ格納用のリスト
    all_model_data = []
    all_name_list = []
    all_dir_list = []  # ディレクトリ情報も保存

    # サブディレクトリを探索してデータを読み込む
    for subdir, dirs, files in os.walk(root_dir):
        npz_file = os.path.join(subdir, 'npKnown.npz')
        if os.path.exists(npz_file):
            with np.load(npz_file) as data:
                model_data = data['efficientnetv2_arcface']
                name_list = data['name']

                # model_dataの形状を確認
                print(f"元のmodel_dataの形状: {model_data.shape}")

                # 余分な次元を削除して形状を (N, 512) にする
                model_data = model_data.squeeze()
                if model_data.ndim == 1:
                    # データが一つだけの場合
                    model_data = model_data.reshape(1, -1)
                elif model_data.ndim > 2:
                    # 予期しない次元がある場合
                    model_data = model_data.reshape(-1, dimension)

                # 修正後の形状を確認
                print(f"修正後のmodel_dataの形状: {model_data.shape}")

                # データの次元数が想定通りであることを確認
                assert model_data.shape[1] == dimension, f"データの次元数が{dimension}である必要があります。"

                # 正規化前のデータの最大値・最小値を確認
                print(f"正規化前のデータの最大値: {np.max(model_data)}, 最小値: {np.min(model_data)}")

                # NaNや無限大の値が含まれていないかチェック
                if np.isnan(model_data).any() or np.isinf(model_data).any():
                    raise ValueError("正規化前のmodel_dataにNaNまたは無限大の値が含まれています。")

                # ゼロベクトルがないか確認
                norms = np.linalg.norm(model_data, axis=1)
                if np.any(norms == 0):
                    raise ValueError("ゼロノルムのベクトルが含まれています。")

                # L2正規化を行う
                model_data = model_data / norms[:, np.newaxis]

                # 正規化後のデータの最大値・最小値を確認
                print(f"正規化後のデータの最大値: {np.max(model_data)}, 最小値: {np.min(model_data)}")

                # 正規化後の異常値をチェック
                if np.isnan(model_data).any() or np.isinf(model_data).any():
                    raise ValueError("正規化後のmodel_dataにNaNまたは無限大の値が含まれています。")

                # リストに追加
                all_model_data.append(model_data)
                all_name_list.extend(name_list)
                all_dir_list.extend([subdir] * len(name_list))

    # データをnumpy配列に変換
    if len(all_model_data) == 0:
        raise ValueError("データが読み込まれていません。ファイルパスとデータ形式を確認してください。")
    all_model_data = np.vstack(all_model_data)

    # データ数を確認
    print(f"データ数: {len(all_model_data)}")

    # LOFによる外れ値検出
    print("LOFによる外れ値検出を行います。")

    # LOFモデルの作成
    n_neighbors = min(20, len(all_model_data) - 1)  # データ数に応じて近傍数を設定
    lof = LocalOutlierFactor(n_neighbors=n_neighbors, metric='cosine')

    # LOFスコアの計算（negative_outlier_factor_属性を取得）
    y_pred = lof.fit_predict(all_model_data)
    lof_scores = -lof.negative_outlier_factor_

    # LOFスコアの最大値・最小値を確認
    print(f"LOFスコアの最大値: {np.max(lof_scores)}, 最小値: {np.min(lof_scores)}")

    # 外れ値を判定する閾値を設定（例：LOFスコアが1.5以上を外れ値とする）
    outlier_threshold = 1.5

    # 外れ値のリスト
    outliers = []

    # 各データ点について外れ値かどうかを判定
    for idx, score in enumerate(lof_scores):
        # LOFスコアが閾値を超える場合は外れ値として記録
        if score > outlier_threshold:
            outliers.append({
                "名前": all_name_list[idx],
                "ディレクトリ": all_dir_list[idx],
                "LOFスコア": score
            })
            print(f"外れ値検出: 名前: {all_name_list[idx]}, ディレクトリ: {all_dir_list[idx]}, LOFスコア: {score:.4f}")

    # 外れ値ファイルを保存するディレクトリを作成（同名のディレクトリがない場合のみ）
    outlier_dir = os.path.join(root_dir, "外れ値ファイル")
    if not os.path.exists(outlier_dir):
        os.makedirs(outlier_dir)

    # npKnown.npz ファイルを削除
    npz_file_path = os.path.join(root_dir, 'npKnown.npz')
    if os.path.exists(npz_file_path):
        os.remove(npz_file_path)

    # 外れ値を移動
    for outlier in outliers:
        # 外れ値ファイルのパスを生成
        src_path = os.path.join(outlier["ディレクトリ"], outlier["名前"])
        dst_path = os.path.join(outlier_dir, outlier["名前"])

        # ファイルを外れ値ファイルディレクトリに移動
        shutil.move(src_path, dst_path)

    # 処理時間を計算して出力
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    print(f"処理時間: {int(minutes)}分 {seconds:.2f}秒")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LOFによる外れ値検出")
    parser.add_argument("root_dir", type=str, help="データのルートディレクトリのパスを指定してください")
    args = parser.parse_args()
    main(args.root_dir)
