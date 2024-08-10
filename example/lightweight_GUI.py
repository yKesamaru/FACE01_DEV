"""シンプルで軽量なGUIアプリケーションの作成例.

Summary:
    この例では、シンプルで軽量なGUIアプリケーションの作成方法を学びます。

Example:
    .. code-block:: bash

        python3 example/lightweight_GUI.py

Results:
    スクリーンショットは作成されるウィンドウを示しています。

    .. image:: ../example/img/lightweight_GUI.png
        :scale: 50%
        :alt: Screenshot of the lightweight GUI output

    コンソール出力は以下のようになります。

    .. code-block:: console

        [2023-01-23 22:33:18,752] [face01lib.load_preset_image] [load_preset_image.py] [INFO] Loading npKnown.npz
        安倍晋三
                similarity              99.7%
                coordinate              (134, 431, 248, 317)
                time                    2023,01,23,22,33,23,445574
                output                  output/安倍晋三_2023,01,23,22,33,23,446640_0.19.png
        -------

Source code:
    `lightweight_GUI.py <../example/lightweight_GUI.py>`_
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
from PIL import Image, ImageTk  # Pillowライブラリをインポート

from face01lib.Core import Core
from face01lib.Initialize import Initialize
from face01lib.logger import Logger

# Initialize
CONFIG: Dict = Initialize('LIGHTWEIGHT_GUI', 'info').initialize()
# Set up logger
logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])


class App:
    def __init__(self, root, exec_times=500):
        self.root = root
        self.exec_times = exec_times
        self.root.title('LIGHTWEIGHT GUI APP')

        # ラベルとボタンを配置
        self.label = Label(root, text='LIGHTWEIGHT GUI app sample')
        self.label.pack()

        self.display = Label(root)
        self.display.pack()

        self.terminate_button = Button(root, text='TERMINATE', command=self.terminate, width=50, bg='red')
        self.terminate_button.pack()

        # 画像表示用のインスタンス変数
        self.img_tk = None
        self.current_frame_datas_array = None  # 現在のフレームデータを保持するための変数

        # ジェネレータを作成
        self.gen = Core().common_process(CONFIG)

        # GUIを更新する
        self.update_image()

    def update_image(self):
        self.current_frame_datas_array = self.gen.__next__()

        for frame_datas in self.current_frame_datas_array:
            img = Image.fromarray(cv2.cvtColor(frame_datas['img'], cv2.COLOR_BGR2RGB))
            self.img_tk = ImageTk.PhotoImage(image=img)  # 画像をインスタンス変数に保持
            self.display.config(image=self.img_tk)

        # 100ミリ秒ごとにウィンドウを更新
        self.root.after(100, self.update_image)

    def terminate(self):
        self.root.quit()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root, exec_times=500)
    root.mainloop()
