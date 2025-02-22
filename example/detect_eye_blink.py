"""まばたきを検出するコード例.

Summary:
    このエグザンプルでは、目の瞬き検出を扱うコード例を示します。

Example:
    .. code-block:: bash

        python3 example/detect_eye_blink.py

Note:
    このコードを実行する際、入力されるソースには必ず1人だけのものを選ばなくてはいけません。
    複数人を対象とすることはできません。

.. image:: ../assets/images/2024-08-27_20-02.png
    :width: 100%
    :alt: eye blink

.. image:: ../assets/images/one_point_L.png
    :width: 70%
    :alt: one point

注目すべきは瞬きの検出が1行で済んでいるところです！⭐️''

.. code-block:: python

    blink_detected: bool = self.spoof.detect_eye_blinks(self.current_frame_datas_array, CONFIG)

Source code:
    `detect_eye_blink.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/detect_eye_blink.py>`_
"""

# Operate directory: Common to all examples
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
from face01lib.logger import Logger
from face01lib.spoof import Spoof

# Operate directory: Common to all examples
dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)


class App:
    def __init__(self, root, exec_times=50):
        self.root = root
        self.exec_times = exec_times
        self.root.title('FACE01 example with EfficientNetV2 ArcFace model')

        # Window icon
        self.root.iconphoto(True, tk.PhotoImage(file="assets/images/g1320.png"))

        # Label for displaying image
        self.display = Label(root)
        self.display.pack()

        # Terminate button
        self.terminate_button = Button(root, text='terminate', command=self.terminate, width=50)
        self.terminate_button.pack(pady=10)

        # 画像表示用のインスタンス変数
        self.img_tk = None
        self.current_frame_datas_array = None  # 現在のフレームデータを保持するための変数

        # ジェネレータを作成
        self.gen = Core().common_process(CONFIG)

        # Spoofオブジェクトを作成
        self.spoof = Spoof()

        # GUIを更新する
        self.update_image()

    def update_image(self):
        self.current_frame_datas_array = self.gen.__next__()
        blink_detected: bool = self.spoof.detect_eye_blinks(self.current_frame_datas_array, CONFIG)

        for frame_datas in self.current_frame_datas_array:
            if blink_detected:
                # logger.info('Blink')
                print('BLINK')

            img = Image.fromarray(cv2.cvtColor(frame_datas['img'], cv2.COLOR_BGR2RGB))
            self.img_tk = ImageTk.PhotoImage(image=img)  # 画像をインスタンス変数に保持
            self.display.config(image=self.img_tk)

        # 100ミリ秒ごとにウィンドウを更新
        self.root.after(100, self.update_image)

    def terminate(self):
        self.root.quit()


if __name__ == '__main__':
    # Initialize
    CONFIG: Dict = Initialize('DETECT_EYE_BLINKS').initialize()
    # Set up logger
    logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])

    root = tk.Tk()
    app = App(root, exec_times=200)
    root.mainloop()
