"""test_api.py.

Summary:
    このスクリプトは、`face01lib/api.py`内の`Dlib_api`クラスの機能をテストします。
    初期化、画像読み込み、顔検出、エンコーディング、比較機能の正確性を検証します。

    - クラスの初期化が正しく行われるかをテスト。
    - 有効および無効なファイルパスでの画像読み込みを検証。
    - 顔がある画像とない画像での顔検出を確認。
    - 顔エンコーディングの次元と値の正確性を検証。
    - 顔の比較が期待通りの結果を返すことを確認。

Example:
    1. `pytest`コマンドを使用してテストを実行します。
    2. 必要な依存関係をインストールし、`tests/data`フォルダにテスト画像を用意してください。

License:
    This script is licensed under the terms provided by yKesamaru, the original author.
"""

import numpy as np
import pytest

from face01lib.api import Dlib_api


def test_dlib_api_initialization():
    """`Dlib_api`クラスの初期化をテストします。

    検証内容:
        - クラスがエラーなく初期化されること。
        - 必要なモデルや設定が正しく読み込まれること。
    """
    api = Dlib_api()
    assert api is not None


def test_JAPANESE_FACE_V1_model_compute_face_descriptor():
    """`JAPANESE_FACE_V1_model_compute_face_descriptor`メソッドをテストします。

    検証内容:
        - 有効な入力画像とランドマークから、正しい次元の特徴量が計算されること。
    """
    api = Dlib_api()
    image = api.load_image_file("tests/data/valid_face_image.png")
    locations = api.face_locations(image)
    raw_landmark = api._return_raw_face_landmarks(image, locations)[0]

    # 特徴量を計算
    descriptor = api.JAPANESE_FACE_V1_model_compute_face_descriptor(
        image,
        raw_landmark
    )

    # テスト: 正しい次元の特徴量が返されることを確認
    assert descriptor.shape == (1, 512)  # shape = (1, 512)


def test_load_image_file_valid():
    """`load_image_file`メソッドを有効な画像パスでテストします。

    検証内容:
        - メソッドが有効なnumpy配列を返すこと。
    """
    api = Dlib_api()
    image = api.load_image_file("tests/data/valid_face_image.png")
    assert isinstance(image, np.ndarray)
    assert image.ndim == 3  # RGB画像は3次元配列であるべき


def test_load_image_file_invalid():
    """`load_image_file`メソッドを無効な画像パスでテストします。

    検証内容:
        - 無効なパスに対して`FileNotFoundError`が発生すること。
    """
    api = Dlib_api()
    with pytest.raises(FileNotFoundError):
        api.load_image_file("tests/data/none.png")


def test_face_locations_with_faces():
    """`face_locations`メソッドを顔が含まれる画像でテストします。

    検証内容:
        - 少なくとも1つの顔が検出されること。
    """
    api = Dlib_api()
    image = api.load_image_file("tests/data/valid_face_image.png")
    locations = api.face_locations(image)
    assert len(locations) > 0  # 少なくとも1つの顔が検出されるべき


def test_face_locations_without_faces():
    """`face_locations`メソッドを顔が含まれない画像でテストします。

    検証内容:
        - 顔がない画像では空のリストが返されること。
    """
    api = Dlib_api()
    image = api.load_image_file("tests/data/invalid_face_image.png")
    locations = api.face_locations(image)
    assert len(locations) == 0


def test_face_encodings():
    """`face_encodings`メソッドで顔の特徴量抽出をテストします。

    検証内容:
        - メソッドが予想される次元のエンコーディングを返すこと。
        - エンコーディングのリスト長が検出された顔の数と一致すること。
    """
    api = Dlib_api()
    image = api.load_image_file("tests/data/valid_face_image.png")
    locations = api.face_locations(image)
    encodings = api.face_encodings(0, image, locations)
    assert len(encodings) == len(locations)  # エンコーディングの数は顔の数と一致するべき
    assert encodings[0].shape[0] == 128  # エンコーディングは128次元であるべき


def test_face_distance():
    """`face_distance`メソッドをテストします。

    検証内容:
        - 2つのエンコーディング間のユークリッド距離が正しく計算されること。
    """
    api = Dlib_api()
    encoding1 = np.array([0.0, 0.0, 0.0])  # 原点
    encoding2 = np.array([1.0, 0.0, 0.0])  # x軸方向に1
    encoding3 = np.array([0.0, 1.0, 0.0])  # y軸方向に1

    # 距離を計算
    result1 = api.face_distance([encoding1], encoding2)
    result2 = api.face_distance([encoding1], encoding3)

    # テスト: 距離が正しいことを確認
    assert np.isclose(result1[0], 1.0)  # 距離は1.0
    assert np.isclose(result2[0], 1.0)  # 距離は1.0


def test_cosine_similarity():
    """`cosine_similarity`メソッドをテストします。

    検証内容:
        - 2つのエンコーディング間のコサイン類似度が正しく計算されること。
        - 閾値を超えるかどうかが正しく判定されること。
    """
    api = Dlib_api()
    embedding1 = np.array([[1.0, 0.0, 0.0]])  # x軸方向
    embedding2 = np.array([1.0, 0.0, 0.0])  # x軸方向
    embedding3 = np.array([0.0, 1.0, 0.0])  # y軸方向

    # 類似度を計算
    result1, max_sim1 = api.cosine_similarity(embedding1, embedding2, threshold=0.5)
    result2, max_sim2 = api.cosine_similarity(embedding1, embedding3, threshold=0.5)

    # テスト: 類似度が正しいことを確認
    assert result1[0][0] is True  # 同じ方向なので閾値を超える
    assert np.isclose(max_sim1, 1.0)  # コサイン類似度は1.0
    assert result2[0][0] is False  # 異なる方向なので閾値を超えない
    assert np.isclose(max_sim2, 0.0)  # コサイン類似度は0.0


def test_percentage():
    """`percentage`メソッドをテストします。

    検証内容:
        - 入力されたcos_sim値に対して、計算された類似度パーセンテージが正しいこと。
        - 境界値や一般的な値に対して期待される結果を返すこと。
    """
    api = Dlib_api()

    # テストケース: (入力cos_sim, 期待される出力パーセンテージ)
    test_cases = [
        (np.float32(0.13243397), round(-23.71 * 0.13243397 ** 2 + 49.98 * 0.13243397 + 73.69, 2)),  # 実際の値
        (np.float32(0.5), round(-23.71 * 0.5 ** 2 + 49.98 * 0.5 + 73.69, 2)),  # 一般的な値
        (np.float32(-0.1), round(-23.71 * (-0.1) ** 2 + 49.98 * (-0.1) + 73.69, 2)),  # 負の値
    ]

    # 各テストケースを検証
    for cos_sim, expected_percentage in test_cases:
        result = api.percentage(cos_sim)
        assert result == pytest.approx(expected_percentage, rel=1e-2), (
            f"Failed for cos_sim={cos_sim}, got {result}, expected {expected_percentage}"
        )


# def test_compare_faces_same_person():
#     """
#     `compare_faces`メソッドを同一人物でテストします。

#     検証内容:
#         - 同じ顔のエンコーディングを比較すると、一致が検出されること。
#     """

#     # Dlib_apiのインスタンス生成
#     api = Dlib_api()

#     # テスト用既知の顔(同一人物の顔1)を読み込む
#     image1 = api.load_image_file("tests/data/person1.png")  # 画像の読み込み
#     locations1 = api.face_locations(image1)
#     encodings1 = api.face_encodings(
#         0,
#         image1,
#         locations1
#     )

#     # 比較対象(同一人物の顔2 = 今回は同じ画像を使用)を読み込む
#     image2 = api.load_image_file("tests/data/person1.png")  # 画像の読み込み
#     locations2 = api.face_locations(image2)
#     encodings2 = api.face_encodings(
#         0,
#         image2,
#         locations2
#     )

#     # compare_facesメソッドで比較する
#     # deep_learning_model=1, tolerance=0.4036..., threshold=0.4036... はデバッグから判明した値を仮置き
#     result, min_distance = api.compare_faces(
#         deep_learning_model=1,               # 追加; deep_learning_modelを1に指定
#         known_face_encodings=[encodings1[0]],  # 追加; 既知の顔エンコーディング(リスト)を渡す
#         face_encoding_to_check=encodings2[0],         # 追加; 比較対象の顔エンコーディング
#         tolerance=0.6,       # 追加; テストでデバッグした実際のtolerance値
#         threshold=0.4        # 追加; テストでデバッグした実際のthreshold値
#     )

#     # テスト: 同一人物と判定されることを確認
#     assert result[0][0] is True, f"同一人物と判定されませんでした: result={result}"  # 日本語コメント
#     assert min_distance <= 0.6, f"距離が許容範囲を超えています (distance={min_distance})"  # 日本語コメント


# # def test_compare_faces_different_person():
#     """`compare_faces`メソッドを異なる人物でテストします。

#     検証内容:
#         - 異なる顔のエンコーディングを比較すると、一致が検出されないこと。
#     """
#     api = Dlib_api()

#     # テスト用既知の顔エンコーディングを作成
#     image1 = api.load_image_file("tests/data/person1.png")
#     locations1 = api.face_locations(image1)
#     encodings1 = api.face_encodings(0, image1, locations1)

#     # 異なる画像を比較対象としてエンコーディング
#     image2 = api.load_image_file("tests/data/person2.png")
#     locations2 = api.face_locations(image2)
#     encodings2 = api.face_encodings(0, image2, locations2)

#     # 比較
#     result, min_distance = api.compare_faces(0, [encodings1[0]], encodings2[0])

#     # テスト: 異なる人物と判定されることを確認
#     assert result[0][0] is False  # 一致が検出されない
#     assert min_distance > 0.6  # 距離が許容範囲を超える
