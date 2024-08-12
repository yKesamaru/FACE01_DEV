"""Get only face coordinates.

Summary:
    In this example, you can learn how to get face coordinates and cropped face images.

Example:
    .. code-block:: bash

        python3 example/face_coordinates.py

Config.ini setting:
    Set config.ini as described below as an example to get face-coordinate and get cropped face images.

    .. code-block:: bash

        [FACE-COORDINATE]
        headless = True
        anti_spoof = False
        output_debug_log = False
        log_level = info
        set_width = 750
        similar_percentage = 99.1
        jitters = 0
        preset_face_images_jitters = 100
        upsampling = 0
        frame_skip = 5
        number_of_people = 10
        use_pipe = True
        model_selection = 0
        min_detection_confidence = 0.4
        person_frame_face_encoding = False
        same_time_recognize = 10
        set_area = NONE
        movie = assets/some_people.mp4
        crop_face_image = True
        frequency_crop_image = 5
        crop_with_multithreading = False
        number_of_crops = 0
        show_overlay = True

Result:
    Executing this example script will output the following contents.

    .. code-block:: python

        face coordinates: [(156, 233, 304, 85), (114, 593, 276, 431), (130, 704, 349, 485), (319, 334, 449, 204), (281, 645, 405, 521), (23, 810, 313, 520), (349, 394, 573, 170), (244, 302, 408, 138), (344, 692, 514, 522), (21, 256, 215, 62)]
        }

Source code:
    `face_coordinates.py <../example/face_coordinates.py>`_

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
from face01lib.logger import Logger
from face01lib.video_capture import VidCap

# Initialize
CONFIG: Dict =  Initialize('FACE-COORDINATE', 'info').initialize()
# Set up logger
logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])
"""Initialize and Setup logger.
When coding a program that uses FACE01, code initialize and logger first.
This will read the configuration file config.ini and log errors etc.
"""


def main(exec_times: int = 50) -> None:
    """Output face coordinates.

    Args:
        exec_times (int, optional): Number of frames for process. Defaults to 50 times.

    Returns:
        None

    """
    # Make generator
    frame_generator_obj = VidCap().frame_generator(CONFIG)

    # Make generator
    core = Core()

    # Repeat 'exec_times' times
    for i in range(0, exec_times):

        # Call __next__() from the generator object
        resized_frame = frame_generator_obj.__next__()

        VidCap().frame_imshow_for_debug(resized_frame)

        frame_datas_array = core.frame_pre_processing(logger, CONFIG,resized_frame)

        for frame_datas in frame_datas_array:
            print(f"face coordinates: {frame_datas['face_location_list']}\n")


if __name__ == '__main__':
    # Call main function.
    main(exec_times = 2)