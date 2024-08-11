"""顔認証におけるベンチマークコード例.

Summary:
    このエグザンプルコードでは、GUIウィンドウを作成したときの顔認証ベンチマークを取得する方法を学びます。
    このベンチマークテストを行うには開発用パッケージを追加インストールする必要があります。
    具体的にはrequirements_dev.txtをインストールしてください。

    .. code-block:: bash

        pip install -r requirements_dev.txt

    起動後、自動的にベンチマーク結果がブラウザ表示されます。
    終了するには、このエグザンプルが実行されているターミナル（またはコンソール）で「Ctrl + C」を押してください。

Example:
    .. code-block:: bash

        python3 example/benchmark_GUI_window.py

Result:
    .. image:: ../docs/img/benchmark_GUI_window.png
        :scale: 50%
        :alt: benchmark_GUI_window

    .. image:: ../docs/img/benchmark_GUI.png
        :scale: 50%
        :alt: benchmark_GUI

Source code:
    `benchmark_GUI_window.py <../example/benchmark_GUI_window.py>`_
"""
# Operate directory: Common to all examples
import os.path
import sys

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

import cProfile as pr
import subprocess
from typing import Dict

import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # tkinterで画像を扱うために必要
from face01lib.Calc import Cal
from face01lib.Core import Core
from face01lib.Initialize import Initialize
from face01lib.logger import Logger

# Initialize
CONFIG: Dict = Initialize('DEFAULT', 'info').initialize()
# Set up logger
logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])
"""Initialize and Setup logger.
When coding a program that uses FACE01, code `initialize` and `logger` first.
This will read the configuration file `config.ini` and log errors etc.
"""


def main(exec_times: int = 50) -> None:
    """Make GUI window and benchmark on your own browser.

    Args:
        exec_times (int, optional): Number of frames for process. Defaults to 50 times.

    Returns:
        None
    """

    # Create tkinter window
    root = tk.Tk()
    root.title('FACE01 EXAMPLE')
    root.geometry("800x600")  # ウィンドウサイズの設定
    root.iconphoto(False, tk.PhotoImage(file="assets/images/g1320.png"))

    # Create tkinter widgets
    display_label = ttk.Label(root)
    display_label.pack(padx=10, pady=10, expand=True)

    gen = Core().common_process(CONFIG)

    # Specify START point
    START: float = Cal.Measure_processing_time_forward()

    # Repeat 'exec_times' times
    for i in range(0, exec_times):
        # Call __next__() from the generator object
        frame_datas_array = gen.__next__()

        # Process events
        root.update_idletasks()
        root.update()

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
                else:
                    print("Unknown person", "\n",
                          "------\n"
                          )

                img = cv2.cvtColor(frame_datas['img'], cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)
                display_label.config(image=imgtk)
                display_label.image = imgtk  # 参照を保持するために必要

    # Close the tkinter window
    root.destroy()

    END = Cal.Measure_processing_time_backward()

    print(f'Total processing time: {round(Cal.Measure_processing_time(START, END), 3)}[seconds]')
    print(f'Per frame: {round(Cal.Measure_processing_time(START, END) / (exec_times), 3)}[seconds]')


if __name__ == '__main__':
    pr.run('main(exec_times = 30)', 'restats')
    subprocess.run(["snakeviz", "restats"])
