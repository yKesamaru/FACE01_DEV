"""顔エンコーディングデータの取得例.

Summary:
    In this example, you can learn how to get face encoded datas.
    標準出力に顔エンコーディングデータが出力されます。

Example:
    .. code-block:: bash

        python3 example/get_encoded_data.py

.. note::
    Make sure this example must be applied for 'one person'.
    Not more two persons in same input.

Source code:
    `get_encoded_data.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/get_encoded_data.py>`_
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
CONFIG: Dict = Initialize('FACE-COORDINATE', 'info').initialize()
# Set up logger
logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])
"""Initialize and Setup logger.
When coding a program that uses FACE01, code `initialize` and `logger` first.
This will read the configuration file `config.ini` and log errors etc.
"""


def main(exec_times: int = 50) -> None:
    """Simple example.

    This simple example script prints out results of face encoded datas.

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

        # VidCap().frame_imshow_for_debug(resized_frame)

        frame_datas_array = core.frame_pre_processing(logger, CONFIG, resized_frame)
        face_encodings, frame_datas_array = \
            core.face_encoding_process(logger, CONFIG, frame_datas_array)

        for encoded_data in face_encodings:
            print(f"face encoded data: {encoded_data}\n")


if __name__ == '__main__':
    # Call main function.
    main(exec_times=10)
