"""
Summary:
    このエグザンプルコードでは、顔の特徴量（エンコーディングされたデータ）を取得する方法を学びます。

Example:
    .. code-block:: bash

        python3 example/get_encoded_data.py

.. note::
    このコードでは、かならず一人が映っている映像を使用してください。

Results:

.. code-block:: bash

    face encoded data: [-0.01199415  0.01052003  0.07660526  0.06551921 -0.07496994 -0.12972911
    -0.05913385 -0.14237705  0.05547058 -0.13777749  0.13601969 -0.12244888
    -0.15050077  0.00519788 -0.03569282  0.17992854 -0.08323735 -0.08283503
    -0.10274227 -0.07727417  0.08088023  0.01752477 -0.05877539  0.02624322
    -0.0077478  -0.25635812 -0.13101193 -0.09281664  0.05218935 -0.04231806
    -0.06299889  0.04474396 -0.19532356 -0.12053486  0.02230695  0.06118448
    -0.06408831 -0.05561456  0.19666338 -0.00320839 -0.16399916  0.10793754
    0.09513831  0.19015315  0.1805291   0.06770462  0.04203921 -0.13319662
    0.14975622 -0.17903461 -0.0205469   0.12766521  0.23538746  0.1532644
    0.03183981 -0.04921352  0.12409633  0.0604726  -0.21282698  0.0895256
    0.1691601  -0.07778979  0.01881283  0.05160358  0.2315844   0.05034623
    -0.04736616 -0.10536997  0.15513012 -0.20276567 -0.11107794  0.02522913
    -0.07532144 -0.1432429  -0.28969032  0.03757014  0.41931418  0.1212881
    -0.1964694   0.06237716 -0.05123742 -0.04189032  0.14579299  0.06779657
    -0.04064779 -0.05232659 -0.07283606  0.02151246  0.25605643 -0.08359357
    0.03513885  0.15748617  0.05288177  0.03470919  0.0150839   0.04732724

.. image:: ../assets/images/one_point_R.png
    :width: 70%
    :alt: one point

dlibでは128次元、JAPANESE FACE V1では512次元のNDArrayデータが取得されます⭐️''

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
    # Initialize
    CONFIG: Dict = Initialize('FACE-COORDINATE', 'info').initialize()
    # Set up logger
    logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])
    # Call main function.
    main(exec_times=10)
