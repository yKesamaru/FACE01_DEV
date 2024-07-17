"""Example of benchmark for face recognition.

Summary:
    In this example, you can test benchmark for create GUI window.

    After running, it will automatically display the benchmark in your browser.
    To quite, press "Cnt + c" in terminal(or console) where this example is running.

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
import PySimpleGUI as sg

from face01lib.Calc import Cal
from face01lib.Core import Core
from face01lib.Initialize import Initialize
from face01lib.logger import Logger

# Initialize
CONFIG: Dict =  Initialize('DEFAULT', 'info').initialize()
# Set up logger
logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])
"""Initialize and Setup logger.
When coding a program that uses FACE01, code `initialize` and `logger` first.
This will read the configuration file `config.ini` and log errors etc.
"""


def main(exec_times: int = 50) -> None:
    """Make GUI window and benchmark on you're own browser.

    Args:
        exec_times (int, optional): Number of frames for process. Defaults to 50 times.

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
        'FACE01 EXAMPLE',
        layout, alpha_channel = 1,
        margins=(10, 10),
        location=(0, 0),
        modal = True,
        titlebar_icon="./images/g1320.png",
        icon="./images/g1320.png"
    )


    gen = Core().common_process(CONFIG)
    

    # Specify START point
    START: float = Cal.Measure_processing_time_forward()


    # Repeat 'exec_times' times
    for i in range(0, exec_times):

        # Call __next__() from the generator object
        frame_datas_array = gen.__next__()

        event, _ = window.read(timeout = 1)  # type: ignore
        if event == sg.WIN_CLOSED:
            print("The window was closed manually")
            break

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
            
                imgbytes = cv2.imencode(".png", frame_datas['img'])[1].tobytes()
                window["display"].update(data = imgbytes)
            
        if event =='terminate':
            break
    window.close()

    
    END = Cal.Measure_processing_time_backward()

    print(f'Total processing time: {round(Cal.Measure_processing_time(START, END) , 3)}[seconds]')
    print(f'Per frame: {round(Cal.Measure_processing_time(START, END) / ( exec_times), 3)}[seconds]')


if __name__ == '__main__':
    pr.run('main(exec_times = 30)', 'restats')
    subprocess.run(["snakeviz", "restats"])