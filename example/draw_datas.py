"""Example of to draw datas using matplotlib.

Summary:
    このエグザンプルコードコードでは、顔のエンコードデータからをMatplotlibを使用して可視化します。

Example:
    .. code-block:: bash

        python3 example/draw_datas.py

Result:
    .. image:: ../docs/img/4_times.png
        :scale: 50%
        :alt: 4 times

    .. image:: ../docs/img/20_times.png
        :scale: 50%
        :alt: 20 times

.. note::

    この例では学習モデルをdlibに指定、つまりconfig.iniでdeep_learning_modelを0にしてください。

Source code:
    `draw_datas.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/draw_datas.py>`_
"""

# 全ての例に共通するディレクトリの操作
import os.path
import sys

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

from typing import Dict

import matplotlib.pyplot as plt
import numpy as np

from face01lib.api import Dlib_api
from face01lib.Core import Core
from face01lib.Initialize import Initialize
from face01lib.logger import Logger
from face01lib.video_capture import VidCap


def f_norm(face_encoded_list, face_encoded_data):
    """フロベニウスノルムを返す関数。

    Args:
        face_encoded_list (List): 顔エンコードリスト
        face_encoded_data (np.NDArray): 顔エンコードデータ (np.ndarray)

    Returns:
        Any: フロベニウスノルム
    """
    return np.linalg.norm(x=(face_encoded_list - face_encoded_data), ord=None, axis=1)


def main(exec_times: int = 50) -> None:
    """
    このシンプルな例では、顔のエンコードデータの結果を表示します。

    Args:
        exec_times (int, optional): 処理を行うフレーム数。デフォルトは50回。

    Returns:
        None
    """
    # 初期化
    CONFIG: Dict = Initialize('DEFAULT', 'info').initialize()

    # フレーム生成オブジェクトを作成
    frame_generator_obj = VidCap().frame_generator(CONFIG)

    # ロガーを作成
    log = Logger().logger(__file__, dir)

    # Coreクラスのオブジェクトを作成
    core = Core()

    # 顔エンコードのリストを作成
    face_encoded_list = []

    # Dlib APIオブジェクトを作成
    Dlib_api_obj = Dlib_api()

    # 'exec_times'回ループを実行
    for i in range(0, exec_times):

        # ジェネレーターオブジェクトから__next__()を呼び出し、フレームを取得
        resized_frame = frame_generator_obj.__next__()

        # `resized_frame`を確認したい場合、以下の行をコメントアウト
        # VidCap().frame_imshow_for_debug(resized_frame)

        # `face_encoded_list`を取得
        frame_datas_array = core.frame_pre_processing(
            log, CONFIG, resized_frame)
        face_encodings, frame_datas_array = \
            core.face_encoding_process(log, CONFIG, frame_datas_array)

        if len(face_encodings) == 1:
            face_encoded_list.append(face_encodings[0])
        elif len(face_encodings) == 0:
            continue
        elif len(face_encodings) > 1:
            log.error(
                "この例は一人の人物に対して適用する必要があります。同じ入力に複数の人物が含まれないようにしてください。")
            exit()

    # Matplotlibの設定
    fig = plt.figure()
    # 引数は行、列、位置
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2, projection="3d")
    ax3 = fig.add_subplot(2, 2, 3, projection="3d")
    ax4 = fig.add_subplot(2, 2, 4)

    x = np.arange(0, 128)
    y = np.arange(0, exec_times)
    # メッシュグリッドを作成
    xv, yv = np.meshgrid(x, y)

    for j in range(0, exec_times):

        ax1.plot(x, face_encoded_list[j])

        z = face_encoded_list[j]
        zv = np.tile(z, (exec_times, 1))

        ax2.plot_surface(xv, yv, zv)

        ax3.scatter(xv, yv, zv)

        r = f_norm(face_encoded_list, face_encoded_list[j])
        # r = Dlib_api_obj.face_distance(face_encoded_list, face_encoded_list[j])  # 上記と同じ

        # 値が0.0の項目を削除
        r = np.delete(r, j)
        y_minus_one = np.delete(y, 1)
        ax4.plot(y_minus_one, r)

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    # メイン関数を呼び出し
    main(exec_times=4)
