"""License for the Code.

Copyright Owner: Yoshitsugu Kesamaru
Please refer to the separate license file for the license of the code.
"""

"""Example of detect eye blinking.

Summary:
    In this example you can learn how to detect eye blinking.

Example:
    .. code-block:: bash
    
        python3 example/detect_eye_blink.py
        
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
import PySimpleGUI as sg

from face01lib.Core import Core
from face01lib.Initialize import Initialize
from face01lib.spoof import Spoof
from face01lib.logger import Logger

# Initialize
CONFIG: Dict =  Initialize('DETECT_EYE_BLINKS').initialize()

# Set up logger
logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])

def main(exec_times: int = 50) -> None:
    """Display window.

    Args:
        exec_times (int, optional): Receive value of number which is processed. Defaults to 50 times.

    Returns:
        None
    """

    # Make PySimpleGUI layout
    sg.theme('LightGray')
    layout = [
        [sg.Image(filename='', key='display', pad=(0,0))],
        [sg.Button('terminate', key='terminate', pad=(0,10), expand_x=True)]
    ]
    window = sg.Window(
        'FACE01 example with EfficientNetV2 ArcFace model',
        layout, alpha_channel = 1,
        margins=(10, 10),
        location=(0, 0),
        modal = True,
        titlebar_icon="./images/g1320.png",
        icon="./images/g1320.png"
    )


    # Make generator
    gen = Core().common_process(CONFIG)
    # Make Spoof object
    spoof = Spoof()

    # Repeat 'exec_times' times
    for i in range(0, exec_times):

        # Call __next__() from the generator object
        frame_datas_array = gen.__next__()
        bool = spoof.detect_eye_blinks(frame_datas_array, CONFIG)

        event, _ = window.read(timeout = 1)  # type: ignore

        if event == sg.WIN_CLOSED:
            print("The window was closed manually")
            break

        for frame_datas in frame_datas_array:
            if bool:
                logger.info('Blink')

            imgbytes = cv2.imencode(".png", frame_datas['img'])[1].tobytes()  # type: ignore
            window["display"].update(data = imgbytes)

        if event =='terminate':
            break
    window.close()


if __name__ == '__main__':
    main(exec_times = 200)
