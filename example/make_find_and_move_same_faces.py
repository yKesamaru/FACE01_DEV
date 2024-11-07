"""同一の512次元データを持つファイルをsame_faceフォルダに移動するコードの例.

Summary:
    このスクリプトは、指定したディレクトリとそのサブディレクトリ内にある`npKnown.npz`ファイルを読み込み、
    512次元の顔認識ベクトルのコサイン類似度に基づいて同一の顔画像を検出し、
    同一と判断された画像ファイルを各サブディレクトリごとの`same_face`フォルダに移動します。
    `same_face`フォルダは各サブディレクトリに存在しない場合は自動で作成されます。

    各`npKnown.npz`ファイルには、人物名とその512次元の特徴量データが含まれており、このデータを基に
    類似性を評価します。類似度が閾値以上のものは同一とみなし、重複する顔画像を`same_face`フォルダに集約します。

    このコードを実行するには、numpyやshutilといったライブラリが必要です。

Example:
    .. code-block:: bash

        python3 example/make_find_and_move_same_faces.py /path/to/root_dir --threshold 0.95

Source code:
    `make_find_and_move_same_faces.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/make_find_and_move_same_faces.py>`__
"""

import argparse
import os
import shutil  # ファイル移動用ライブラリ
import time

import numpy as np


def main(root_dir, threshold=0.95):
    """
    npKnown.npzファイルを読み込み、コサイン類似度が閾値以上の場合に、
    同一の顔画像と判断してファイルを各サブディレクトリのsame_faceフォルダに移動します。

    Args:
        root_dir (str): 処理対象のルートディレクトリのパス。
        threshold (float): コサイン類似度の閾値（0から1の間で指定可能）。デフォルトは0.95。

    Summary:
        指定されたディレクトリ内の顔認識データを取得し、コサイン類似度に基づいて類似する顔画像を検出します。
        各サブディレクトリごとにsame_faceフォルダを作成し、重複した画像をそのフォルダに移動します。

    Returns:
        None
    """
    # 処理開始時刻を記録
    start_time = time.time()

    # 全データ格納用のリスト
    all_embeddings = []
    all_paths = []
    subdir_map = {}

    # サブディレクトリを探索してデータを読み込む
    for subdir, dirs, files in os.walk(root_dir):
        npz_file = os.path.join(subdir, 'npKnown.npz')
        if os.path.exists(npz_file):
            with np.load(npz_file) as data:
                model_data = data['efficientnetv2_arcface']
                name_list = data['name']

                # model_dataの形状を確認して正規化
                model_data = model_data.squeeze()
                if model_data.ndim == 1:
                    model_data = model_data.reshape(1, -1)

                # 各ベクトルとファイルパスをリストに追加し、サブディレクトリごとのマッピングを作成
                for idx, embedding in enumerate(model_data):
                    all_embeddings.append(embedding)
                    file_path = os.path.join(subdir, name_list[idx])
                    all_paths.append(file_path)
                    subdir_map[file_path] = subdir  # 各ファイルとそのサブディレクトリを関連付け

    # ベクトルを正規化（コサイン類似度の計算に必要）
    all_embeddings = np.array(all_embeddings)
    norms = np.linalg.norm(all_embeddings, axis=1, keepdims=True)
    normalized_embeddings = all_embeddings / norms

    # ファイルが移動されたかを追跡するフラグ
    moved_flags = [False] * len(all_embeddings)

    # コサイン類似度の閾値を用いて比較
    for i in range(len(normalized_embeddings)):
        if moved_flags[i]:
            continue
        for j in range(i + 1, len(normalized_embeddings)):
            if moved_flags[j]:
                continue
            # コサイン類似度を計算
            cos_sim = np.dot(normalized_embeddings[i], normalized_embeddings[j])
            if cos_sim >= threshold:
                # 同一データと判断した場合、適切なサブディレクトリにファイルを移動
                duplicate_path = all_paths[j]
                subdir = subdir_map[duplicate_path]
                same_face_dir = os.path.join(subdir, 'same_face')  # サブディレクトリごとのsame_faceフォルダ

                # サブディレクトリごとにsame_faceフォルダが存在しなければ作成
                if not os.path.exists(same_face_dir):
                    os.makedirs(same_face_dir)

                print(f"同一データ検出: {all_paths[i]} と {duplicate_path}（類似度: {cos_sim:.4f}）")
                shutil.move(duplicate_path, os.path.join(same_face_dir, os.path.basename(duplicate_path)))
                moved_flags[j] = True

    # 処理時間を計算して出力
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    print(f"処理時間: {int(minutes)}分 {seconds:.2f}秒")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="コサイン類似度を用いて同一の顔画像を検出し、各サブディレクトリのsame_faceフォルダに移動")
    parser.add_argument("root_dir", type=str, help="データのルートディレクトリのパスを指定してください")
    parser.add_argument("--threshold", type=float, default=0.95, help="コサイン類似度の閾値（デフォルト: 0.95）")
    args = parser.parse_args()
    main(args.root_dir, threshold=args.threshold)
