"""Example of to draw datas using matplotlib.

Summary:
    In this example, you can learn how to draw datas.

Example:
    .. code-block:: bash
    
        python3 example/draw_datas.py

Result:
    .. image:: ../docs/img/4_times.png
        :scale: 50%
        :alt: 4 times

    .. image:: ../docs/img/20_times.png
        :scale: 50%
        :alt: 20 times

Source code:
    `draw_datas.py <../example/draw_datas.py>`_
"""

# Operate directory: Common to all examples
import os.path
import sys

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)


from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
from face01lib.api import Dlib_api
from face01lib.Core import Core
from face01lib.Initialize import Initialize
from face01lib.logger import Logger
from face01lib.video_capture import VidCap


def f_norm(face_encoded_list, face_encoded_data):
    """Return `Frobenius norm`.

    Args:
        face_encoded_list (List): Face encoded list
        face_encoded_data (np.NDArray): Face encoded data as np.ndarray

    Returns:
        Any: Frobenius norm
    """    
    return np.linalg.norm(x=(face_encoded_list - face_encoded_data), ord=None, axis=1)


def main(exec_times: int = 50) -> None:
    """Simple example.

    This simple example script prints out results of face encoded datas.

    Args:
        exec_times (int, optional): Number of frames for process. Defaults to 50 times.

    Returns:
        None
    """    
    # Initialize
    CONFIG: Dict =  Initialize('DEFAULT', 'info').initialize()

    # Make generator
    frame_generator_obj = VidCap().frame_generator(CONFIG)

    # Make logger
    log = Logger().logger(__file__, dir)

    # Make generator
    core = Core()

    # Make list
    face_encoded_list = []

    # Make obj
    Dlib_api_obj = Dlib_api()


    # Repeat 'exec_times' times
    for i in range(0, exec_times):

        # Call __next__() from the generator object
        resized_frame = frame_generator_obj.__next__()

        # If you want check `resized_frame`, comment out bellow.
        # VidCap().frame_imshow_for_debug(resized_frame)

        # Get `face_encoded_list`
        frame_datas_array = core.frame_pre_processing(log, CONFIG, resized_frame)
        face_encodings, frame_datas_array = \
            core.face_encoding_process(log, CONFIG, frame_datas_array)

        if len(face_encodings) == 1:
            face_encoded_list.append(face_encodings[0])
        elif len(face_encodings) == 0:
            continue
        elif len(face_encodings) > 1:
            log.error("Make sure this example must be applied for 'one person'. Not more two persons in same input.")
            exit()


    # Matplotlib configure
    fig = plt.figure()
    # Arguments are row, column, location
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2, projection="3d")
    ax3 = fig.add_subplot(2, 2, 3, projection="3d")
    ax4 = fig.add_subplot(2, 2, 4)

    x = np.arange(0, 128)
    y = np.arange(0, exec_times)
    # Make `meshgrid`
    xv, yv = np.meshgrid(x, y)

    for j in range(0, exec_times):

        ax1.plot(x, face_encoded_list[j])

        z = face_encoded_list[j]
        zv = np.tile(z, (exec_times, 1))

        ax2.plot_surface(xv, yv, zv)

        ax3.scatter(xv, yv, zv)

        r = f_norm(face_encoded_list, face_encoded_list[j])
        # r = Dlib_api_obj.face_distance(face_encoded_list, face_encoded_list[j])  # Same above

        # Delete item which is 0.0
        r = np.delete(r, j)
        y_minus_one = np.delete(y, 1)
        ax4.plot(y_minus_one, r)


    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    # Call main function.
    main(exec_times = 4)
