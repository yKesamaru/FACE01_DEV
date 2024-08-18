"""Data structure of FACE01.

Summary:
    In this example, you can learn data structure of FACE01.

Example:
    .. code-block:: bash
    
        python3 example data_structure.py
    
Config.ini setting:
    Data structure of FACE01 is closely related to what you set in config.ini.
    The contents of config.ini described below are the settings for face-detection and face-recognition. GUI windows are not displayed.

    .. code-block:: bash

        [DEFAULT]
        # [DEFAULT] section is for simple example.
        # This [DEFAULT] setting for only use CUI mode.
        # Also, This setting is for user who's PC is not installed Nvidia GPU card.
        # [DEFAULT] section is the inheritor of all sections.
        headless = True
        anti_spoof = False
        output_debug_log = False
        log_level = info
        set_width = 750
        similar_percentage = 99.1
        jitters = 0
        preset_face_images_jitters = 10
        upsampling = 0
        mode = hog
        frame_skip = 5
        number_of_people = 10
        use_pipe = True
        model_selection = 0
        min_detection_confidence = 0.6
        person_frame_face_encoding = False
        same_time_recognize = 2
        set_area = NONE
        movie = assets/test.mp4
        user = 
        passwd = 
        rectangle = False
        target_rectangle = False
        draw_telop_and_logo = False
        default_face_image_draw = False
        show_overlay = False
        alpha = 0.3
        show_percentage = False
        show_name = False
        crop_face_image = True
        frequency_crop_image = 5
        crop_with_multithreading = False
        Python_version = 3.8.10
        cpu_freq = 2.5
        cpu_count = 4
        memory = 4
        gpu_check = True
        calculate_time = False
        show_video = False
        number_of_crops = 0

Result:
    Executing this example script will output the following contents.
    (The output string has been formatted to make it easier to read.)

    .. code-block:: python

        frame_datas: 
        {
            'img': array([[[0, 0, 0], [0, 0, 0], ..., [0, 0, 0], dtype=uint8), 
            'face_location_list': [(165, 449, 287, 327), (240, 435, 391, 284)], 
            'overlay': array([[[  0,   0,  70],  ..., [ 88, 169, 127]], dtype=uint8), 
            'person_data_list': 
            [
                {
                    'name': '安倍晋三', 
                    'pict': 'output/安倍晋三_2022,10,08,19,17,41,346789_0.2.png', 
                    'date': '2022,10,08,19,17,41,344598', 
                    'location': (165, 449, 287, 327), 
                    'percentage_and_symbol': '99.7%'
                }, 
                {
                    'name': 'Unknown', 
                    'pict': 'output/安倍晋三_2022,10,08,19,17,41,346789_0.2.png', 
                    'date': '2022,10,08,19,17,41,344598', 
                    'location': (240, 435, 391, 284), 
                    'percentage_and_symbol': ''
                }
            ]
        }

Data structure:
    The `frame_datas_array` variable is a dictionary-like variable that contains the variables described below.
    
    * Dictionary

        * img: NDArray of a frame
        * face_location_list: List of face-coordinates
        * overlay: Shallow copy of img
        * person_data_list: List of person-coordinate which is included in `face_location_list`

    In addition, the `person_data_list` variable is an array that contains the variables described below.
    
    * List

        * Dictionary

            * name: name
            * pict: Saved image's file name which is cropped by face-coordinate in a frame
            * date: 
            * location: Face-coordinate
            * percentage_and_symbol: xx%
        
Source code:
    `data_structure.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/data_structure.py>`_
"""

# Operate directory: Common to all examples
import os.path
import sys
dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)


from typing import Dict

from face01lib.Core import Core
from face01lib.Initialize import Initialize


def main(exec_times: int = 50) -> None:
    """Output data structure.

    Data structure of FACE01 can be get as frame_datas_array variable.

    Args:
        exec_times (int, optional): Number of frames for process. Defaults to 50 times.

    Returns:
        None
    """    
    # Initialize
    CONFIG: Dict =  Initialize('DEFAULT', 'info').initialize()


    # Make generator
    gen = Core().common_process(CONFIG)


    # Repeat 'exec_times' times
    for i in range(0, exec_times):

        # Call __next__() from the generator object
        frame_datas_array = gen.__next__()

        for frame_datas in frame_datas_array:
            print(f"frame_datas: {frame_datas}\n")


if __name__ == '__main__':
    # Call main function.
    main(exec_times = 1)