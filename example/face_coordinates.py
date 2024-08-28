"""
Summary:
    このエグザンプルコードでは、顔座標の取得と顔画像として保存する方法を学びます。

Example:
    .. code-block:: bash

        python3 example/face_coordinates.py

Config.ini setting:
    config.iniを以下のように記述して、顔座標と顔画像の保存を設定します。

    .. code-block:: bash

        [FACE-COORDINATE]
        headless = True
        crop_face_image = True
        frequency_crop_image = 5
        crop_with_multithreading = False
        number_of_crops = 0

Result:
    以下のような出力が得られます。

    .. code-block:: python

        face coordinates: [(156, 233, 304, 85), (114, 593, 276, 431), (130, 704, 349, 485), (319, 334, 449, 204), (281, 645, 405, 521), (23, 810, 313, 520), (349, 394, 573, 170), (244, 302, 408, 138), (344, 692, 514, 522), (21, 256, 215, 62)]
        }


.. image:: ../assets/images/one_point_R.png
    :width: 70%
    :alt: one point

顔画像の保存はデータセットを作成する時、役立ちます⭐️''

Source code:
    `face_coordinates.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/face_coordinates.py>`_

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
    # Initialize
    CONFIG: Dict = Initialize('FACE-COORDINATE', 'info').initialize()
    # Set up logger
    logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])

    # Call main function.
    main(exec_times=2)
