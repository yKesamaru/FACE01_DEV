"""まばたきを検出するコード例.

Summary:
    このエグザンプルでは、目の瞬き検出を扱うコード例を示します。

Example:
    .. code-block:: bash

        python3 example/detect_eye_blink.py

Note:
    このコードを実行する際、以下のような大量のスパム出力が標準出力に表示されることがあります。
    これは、OpenGLやEGLの初期化、および推論処理に関連する内部ログの出力が原因です。
    これらの出力はプログラムの動作に影響を与えませんが、ログのフィルタリングやリダイレクトが必要な場合があります。

    .. code-block:: text

        I0000 00:00:1723262233.064390   20773 gl_context_egl.cc:85] Successfully initialized EGL. Major : 1 Minor: 5
        I0000 00:00:1723262233.148223   21035 gl_context.cc:357] GL version: 3.2 (OpenGL ES 3.2 NVIDIA 555.42.06), renderer: NVIDIA GeForce GTX 1660 Ti/PCIe/SSE2
        W0000 00:00:1723262233.150802   21030 inference_feedback_manager.cc:114] Feedback manager requires a model with a single signature inference. Disabling support for feedback tensors.

Source code:
    `detect_eye_blink.py <../example/detect_eye_blink.py>`_
"""

# Operate directory: Common to all examples
import os.path
import sys

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

from typing import Dict

import cv2
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk

from face01lib.Core import Core
from face01lib.Initialize import Initialize
from face01lib.spoof import Spoof
from face01lib.logger import Logger

# 出力ログの抑制 #################################
# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0 = DEBUG, 1 = INFO, 2 = WARNING, 3 = ERROR

# os.environ['GLOG_minloglevel'] = '2'  # INFOレベル以下のログを抑制
# os.environ['GLOG_logtostderr'] = '1'  # 標準エラーに出力

# # 標準出力をファイルにリダイレクト
# sys.stdout = open('output.log', 'w')

# # 標準エラーをファイルにリダイレクト
# sys.stderr = open('error.log', 'w')

# import os
# import onnxruntime as ort

# # 現在のスクリプトのディレクトリを基準にして、モデルファイルへのパスを設定
# model_path = os.path.join(os.path.dirname(__file__), "../face01lib/models/JAPANESE_FACE_V1.onnx")

# # ログレベルの設定
# sess_options = ort.SessionOptions()
# sess_options.log_severity_level = 3  # ログレベルをERRORに設定

# # ONNXモデルのセッションを作成
# session = ort.InferenceSession(model_path, sess_options, providers=['CPUExecutionProvider'])

# sys.stderr = open('error.log', 'w')
# #################################################


# Operate directory: Common to all examples
dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

# Initialize
CONFIG: Dict = Initialize('DETECT_EYE_BLINKS').initialize()

# Set up logger
logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])


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
    root = tk.Tk()
    app = App(root, exec_times=200)
    root.mainloop()
