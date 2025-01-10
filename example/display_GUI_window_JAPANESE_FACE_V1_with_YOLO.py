"""
顔画像と物体を検出し、回転・クロップ・表示するウィンドウアプリケーション.

Summary:
    このプログラムは、顔認識モデルとDAMO-YOLO物体検出モデルを使用して、
    動画フレーム内の顔と物体を検出し、それらの情報をリアルタイムで表示します。
    GUIウィンドウ上に処理結果を表示し、詳細情報をターミナルに出力します。
    これにより、例えばスマートフォンに表示された顔の映像であることを識別したり出来ます。

Usage:
    .. code-block:: bash

        python display_GUI_window_JAPANESE_FACE_V1_with_YOLO.py <exec_times>

Features:
    - 顔認識と物体検出をリアルタイムで実行
    - 検出結果（類似度、座標、物体名など）をターミナルに表示
    - GUIウィンドウ上で処理結果を更新表示
    - 処理回数または検出件数に応じてプログラムを終了

Example:
    .. code-block:: bash

        python display_GUI_window_JAPANESE_FACE_V1_with_YOLO.py

Result:
    - GUIウィンドウで処理結果をリアルタイム表示
    - ターミナルに検出データの詳細を出力
"""
import sys
import os

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

import tkinter as tk
from tkinter import Button, Label
from typing import Dict

import cv2
from PIL import Image, ImageTk

from face01lib.Core import Core
from face01lib.Initialize import Initialize
from face01lib.damo_yolo.base import Infer, COCO_CLASSES  # base.pyをモジュールとして使用
from face01lib.damo_yolo.damo_internal.config.base import parse_config


def main(exec_times: int = 50) -> None:
    """
    ウィンドウを表示し、顔と物体を検出するメイン関数.

    Args:
        exec_times (int, optional): 処理を実行する回数. デフォルトは50回.

    Returns:
        None
    """
    # 初期化処理
    CONFIG: Dict = Initialize('JAPANESE_FACE_V1_MODEL_GUI').initialize()

    # DAMO-YOLOモデルの設定
    config_file = "face01lib/damo_yolo/configs/damoyolo_tinynasL20_T.py"
    ckpt_path = "face01lib/damo_yolo/pretrained_models/damoyolo_tinynasL20_T_420.pth"
    # 設定ファイルを解析してconfigを作成
    config = parse_config(config_file)
    damo_infer = Infer(config=config, ckpt_path=ckpt_path)

    # tkinterウィンドウの作成
    root = tk.Tk()
    root.title('FACE01 example with JAPANESE_FACE_V1 and DAMO-YOLO')
    root.geometry('800x600')

    # 画像を表示するためのラベル
    display_label = Label(root)
    display_label.pack()

    # 終了ボタンの設定
    def terminate():
        """ウィンドウを終了する関数."""
        root.destroy()

    terminate_button = Button(root, text="terminate", command=terminate)
    terminate_button.pack(pady=10)

    # ジェネレータを生成
    gen = Core().common_process(CONFIG)

    try:
        # カウント変数を初期化
        count = 0  # フレーム全体でカウントを維持
        max_count = 200  # 最大回数を設定

        # 'exec_times' 回処理を繰り返す
        for i in range(0, exec_times):
            # ジェネレータオブジェクトから次の値を取得
            frame_datas_array = gen.__next__()

            for frame_datas in frame_datas_array:
                # 顔認識結果をターミナルに出力
                for person_data in frame_datas['person_data_list']:
                    if not person_data['name'] == 'Unknown':
                        print(
                            person_data['name'], "\n",
                            "\t", "類似度\t\t", person_data['percentage_and_symbol'], "\n",
                            "\t", "座標\t\t", person_data['location'], "\n",
                            "\t", "時刻\t\t\t", person_data['date'], "\n",
                            "\t", "出力\t\t\t", person_data['pict'], "\n",
                            "-------\n"
                        )
                    count += 1  # カウントをインクリメント

                    if count >= max_count:  # カウントが最大に達したらループを抜ける
                        raise StopIteration  # 外側のループも終了するために例外を送出

                # DAMO-YOLOで物体検出を実行
                bboxes, scores, cls_inds = damo_infer.forward(frame_datas['img'])

                # 検出結果をターミナルに表示
                print("物体検出結果:")
                for bbox, score, cls_ind in zip(bboxes, scores, cls_inds):
                    if score >= 0.5:  # スコアが0.5以上の物体のみ出力
                        class_name = COCO_CLASSES[int(cls_ind)]  # クラス名を取得
                        print(f"物体: {class_name}, スコア: {score:.2f}, バウンディングボックス: {bbox}")

                # 画像をPIL形式に変換
                img = cv2.cvtColor(frame_datas['img'], cv2.COLOR_BGR2RGB)  # OpenCVのBGRをRGBに変換
                img = Image.fromarray(img)  # OpenCVの画像をPIL画像に変換
                img = ImageTk.PhotoImage(img)  # PIL画像をImageTkに変換

                # 新しい画像でラベルを更新
                display_label.config(image=img)
                display_label.image = img

            # ウィンドウを更新
            root.update_idletasks()
            root.update()

    except StopIteration:
        # 動画の供給が終了、またはカウントが最大に達した場合の処理
        print("処理が完了しました。プログラムを終了します。")
        root.destroy()  # ウィンドウを閉じる
    except Exception as e:
        # その他の予期しないエラーが発生した場合の処理
        print(f"予期しないエラーが発生しました: {e}")
        root.destroy()  # エラーが発生した場合もウィンドウを閉じる
    finally:
        # 終了処理
        print("終了処理を行っています...")


if __name__ == '__main__':
    # メイン関数を呼び出す
    main(exec_times=200)
