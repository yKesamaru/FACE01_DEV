"""GUI表示と顔認識データ出力の例。

Summary:
    In this example you can learn how to display GUI and output
    face recognition.

Example:
    .. code-block:: bash

        python3 example/display_GUI_window.py

Results:

.. image:: ../assets/images/2024-08-27_20-16.png
    :scale: 70%
    :alt: Screenshot of the GUI output

.. image:: ../assets/images/one_point_L.png
    :width: 70%
    :alt: one point

'Core().common_process(self.CONFIG)'で得られたジェネレーターを'for'で回すだけで全ての情報が取得できるんです！⭐️''

Source code:
    `display_GUI_window.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/display_GUI_window.py>`_

See also:
    ttkbootstrap
    https://ttkbootstrap.readthedocs.io/en/version-0.5/themes.html

"""
# Operate directory: Common to all examples
import os.path
import sys

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

import tkinter as tk

import cv2
from PIL import Image, ImageTk
from ttkbootstrap import Style

from face01lib.Core import Core
from face01lib.Initialize import Initialize


class App:
    def __init__(self, root, exec_times):
        self.root = root
        self.exec_times = exec_times
        self.root.title("FACE01 EXAMPLE")
        self.root.geometry("800x700")

        self.style = Style(theme='minty')  # ttkbootstrapでmintyテーマを使用する

        self.image_label = tk.Label(self.root)  # ttkbootstrapのスタイルインスタンスを使用
        self.image_label.pack(padx=10, pady=10)

        self.terminate_button = tk.Button(self.root, text="terminate", command=self.terminate, bg='blue', fg='white')
        self.terminate_button.pack(fill=tk.X, padx=10, pady=10)  # 横幅をウィンドウ全体に広げる

        self.running = True
        self.gen = None
        self.CONFIG = Initialize('DISPLAY_GUI').initialize()

    def start(self):
        self.gen = Core().common_process(self.CONFIG)
        self.update_image()

    def update_image(self):
        if not self.running:
            return

        try:
            frame_datas_array = next(self.gen)

            for frame_datas in frame_datas_array:
                for person_data in frame_datas['person_data_list']:
                    if not person_data['name'] == 'Unknown':
                        print(
                            person_data['name'], "\n",
                            "\t", "similarity\t\t", person_data['percentage_and_symbol'], "\n",
                            "\t", "coordinate\t\t", person_data['location'], "\n",
                            "\t", "time\t\t\t", person_data['date'], "\n",
                            "\t", "output\t\t\t", person_data['pict'], "\n",
                            "-------\n"
                        )

                img = cv2.cvtColor(frame_datas['img'], cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                img_tk = ImageTk.PhotoImage(img)
                self.image_label.config(image=img_tk)
                self.image_label.image = img_tk

            self.root.after(1, self.update_image)
        except StopIteration:
            pass

    def terminate(self):
        self.running = False
        self.root.destroy()


def main(exec_times: int = 50) -> None:
    """Display window.

    Args:
        exec_times (int, optional): Receive value of number which is processed. Defaults to 50 times.

    Returns:
        None
    """
    root = tk.Tk()
    app = App(root, exec_times)
    app.start()
    root.mainloop()


if __name__ == '__main__':
    main(exec_times=200)
