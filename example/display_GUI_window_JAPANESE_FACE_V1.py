"""顔画像を検出し、回転・クロップ・表示するウィンドウアプリケーション.

Summary:
    このプログラムは、顔認識モデルを使用して動画フレーム内の顔を検出し、
    データを解析、ウィンドウにリアルタイムで表示します。
    また、指定された回数分フレームを処理します。

Example:
    .. code-block:: bash

        python example/display_GUI_window_JAPANESE_FACE_V1.py <exec_times>

Features:
    - 顔認識モデルを使用して顔をリアルタイムで検出
    - 検出結果をターミナルに表示 (類似度、座標、時刻など)
    - 検出されたフレームをGUIウィンドウで表示
    - 処理回数または検出件数に応じて終了

Example:
    .. code-block:: bash

        python example/display_GUI_window_JAPANESE_FACE_V1.py

Result:
    - GUIウィンドウにリアルタイムで処理結果を表示
    - ターミナルに検出データを詳細表示
"""

import os.path
import sys

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


def main(exec_times: int = 50) -> None:
    """ウィンドウを表示するメイン関数.

    Args:
        exec_times (int, optional): 処理を実行する回数を受け取る. デフォルトは50回.

    Returns:
        None
    """
    # 初期化処理
    CONFIG: Dict = Initialize('JAPANESE_FACE_V1_MODEL_GUI').initialize()

    # tkinterウィンドウの作成
    root = tk.Tk()
    root.title('FACE01 example with JAPANESE_FACE_V1 model')
    root.geometry('800x600')

    # 画像を表示するためのラベル
    display_label = Label(root)
    display_label.pack()

    # 終了ボタンの設定
    def terminate():
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

                # フレーム内の各人物データを処理
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

                    if count >= max_count:  # カウントが200に達したらループを抜ける
                        raise StopIteration  # 外側のループも終了するために例外を送出

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
    main(exec_times=2000)
