"""顔認識モデルとしてJAPANESE FACE V1を使用したGUIアプリケーションのコード例.

Summary:
    In this example you can learn how to display GUI and output
    face recognition.

Example:
    .. code-block:: bash

        python3 example/display_GUI_window_JAPANESE_FACE_V1.py

Results:

.. image:: ../example/img/display_GUI_window_JAPANESE_FACE_V1.png
    :scale: 70%
    :alt: Screenshot of the GUI output

コンソール出力は以下のようになります。

.. code-block:: console

    岸田文雄
            similarity              94.1%
            coordinate              (161, 711, 376, 496)
            time                    2024,08,17,14,16,05,135247
            output                  output/岸田文雄_2024,08,17,14,16,05,141640_0.55.png
    -------


Source code:
    `display_GUI_window_JAPANESE_FACE_V1.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/display_GUI_window_JAPANESE_FACE_V1.py>`_
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


def main(exec_times: int = 50) -> None:
    """Display window.

    Args:
        exec_times (int, optional): Receive value of number which is processed. Defaults to 50 times.

    Returns:
        None
    """
    # Initialize
    CONFIG: Dict = Initialize('JAPANESE_FACE_V1_MODEL_GUI').initialize()

    # Create tkinter window
    root = tk.Tk()
    root.title('FACE01 example with JAPANESE_FACE_V1 model')
    root.geometry('800x600')

    # Label for displaying images
    display_label = Label(root)
    display_label.pack()

    # Terminate button
    def terminate():
        root.destroy()

    terminate_button = Button(root, text="terminate", command=terminate)
    terminate_button.pack(pady=10)

    # Make generator
    gen = Core().common_process(CONFIG)

    # Repeat 'exec_times' times
    for i in range(0, exec_times):

        # Call __next__() from the generator object
        frame_datas_array = gen.__next__()

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

            # Convert the image to PIL format
            img = cv2.cvtColor(frame_datas['img'], cv2.COLOR_BGR2RGB)  # OpenCVのBGRからRGBに変換
            img = Image.fromarray(img)  # OpenCVの画像をPIL画像に変換
            img = ImageTk.PhotoImage(img)  # PIL画像をImageTkに変換

            # Update the display label with the new image
            display_label.config(image=img)
            display_label.image = img

        # Update the window
        root.update_idletasks()
        root.update()

    root.mainloop()


if __name__ == '__main__':
    main(exec_times=2000)
