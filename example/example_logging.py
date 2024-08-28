"""
Summary:
    このエグザンプルコードではログ機能について学びます。

    You can choose from two types of log_level:
        - info
        - debug
    in CONFIG: Dict = Initialize('DEFAULT', 'log_level').initialize().

Example:
    .. code-block:: python

        # Initialize
        CONFIG: Dict = Initialize('DEFAULT', 'debug').initialize()
        # Set up logger
        logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])

    .. code-block:: bash

        python3 example/logging.py

Source code:
    `example_logging.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/example_logging.py>`_
"""

# Operate directory: Common to all examples
import os.path
import sys

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)


import os.path
from typing import Dict

from face01lib.Core import Core
from face01lib.Initialize import Initialize
from face01lib.logger import Logger

name: str = __name__
dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)


def main(exec_times: int = 50) -> None:
    """Setup logger example.

    Output log with defined log-level.

    Args:
        exec_times (int, optional): Number of frames for process. Defaults to 50 times.

    Output example:

    .. code-block:: bash

        [2024-08-27 21:18:34,678] [/home/terms/bin/FACE01_DEV/example/example_logging.py] [example_logging.py] [DEBUG] 安倍晋三
        [2024-08-27 21:18:34,678] [/home/terms/bin/FACE01_DEV/example/example_logging.py] [example_logging.py] [DEBUG] 99.4%
        [2024-08-27 21:18:34,678] [/home/terms/bin/FACE01_DEV/example/example_logging.py] [example_logging.py] [DEBUG] (148, 342, 272, 217)
        [2024-08-27 21:18:34,678] [/home/terms/bin/FACE01_DEV/example/example_logging.py] [example_logging.py] [DEBUG] -----------------

    .. image:: ../assets/images/one_point_L.png
        :width: 70%
        :alt: one point

    ログとして出力させたい場合に使うと良いですね⭐️''

    ログとして出力すると、どのPythonファイルがどのログレベルで出力したのか一目瞭然です！💗
    """
    # Make generator
    gen = Core().common_process(CONFIG)

    # Repeat 'exec_times' times
    for i in range(0, exec_times):

        # Call __next__() from the generator object
        frame_datas_array = gen.__next__()

        for frame_datas in frame_datas_array:

            for person_data in frame_datas['person_data_list']:
                if not person_data['name'] == 'Unknown':
                    logger.debug(person_data['name'])
                    logger.debug(person_data['percentage_and_symbol'])
                    logger.debug(person_data['location'])
                    logger.debug("-----------------")


if __name__ == '__main__':
    # Initialize
    CONFIG: Dict = Initialize('DEFAULT', 'debug').initialize()
    # Set up logger
    logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])
    """Initialize and Setup logger.
    """

    main(exec_times=10)
