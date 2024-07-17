"""License for the Code.

Copyright Owner: Yoshitsugu Kesamaru
Please refer to the separate license file for the license of the code.
"""

"""Example of data augmentation for DNN.

Summary:
    In this example you can learn how to augment data for DNN.

Example:
    .. code-block:: bash
    
        python3 example/data_augmentation.py \
            "/path/to/dir" "" "lens" 224 10 -0.1 0.1 0.01
        
Source code:
    `data_augmentation.py <../example/data_augmentation.py>`_
"""
# Operate directory: Common to all examples
import os.path
import sys
from glob import glob
dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

from typing import Dict, List

from face01lib.Initialize import Initialize
from face01lib.logger import Logger
from face01lib.utils import Utils


# Initialize
CONFIG: Dict =  Initialize('DEFAULT', 'info').initialize()
# Set up logger
logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])
"""Initialize and Setup logger.
When coding a program that uses FACE01, code `initialize` and `logger` first.
This will read the configuration file `config.ini` and log errors etc.
"""

utils = Utils(CONFIG['log_level'])


def main(
        dir_path:str,
        size:int=224,
        num_jitters:int =10,
        initial_value: float = -0.1,
        closing_value: float = 0.1,
        step_value: float = 0.01,
    ):
    """Simple example.

        This simple example accepts a directory path and recursively loads
        the directories for data augmentation.

        Args:
            dir_path (str): target directory path.
            size (int, optional): image size. Defaults to 224.
            num_jitters (int, optional): number of jitters. Defaults to 10.
            initial_value (float, optional): initial value. Defaults to -0.1.
            closing_value (float, optional): closing value. Defaults to 0.1.
            step_value (float, optional): step value. Defaults to 0.01.

        Return:
            None

        See Also:
            `dlib.jitter_image <http://dlib.net/python/index.html#dlib_pybind11.jitter_image>`_
    """
    data_dir = dir_path
    directory_list = []

    # Search recursively under the data directory
    for root, dirs, _ in os.walk(data_dir):
        for directory in dirs:
            directory_path = os.path.join(root, directory)
            # Get all files in `directory_path` and store them in `files`
            files=glob(os.path.join(directory_path, "*"))
            # skip the `for` statement if any element of the list `files` contains the string `jitter`
            if any('jitter' in file for file in files):
                continue
            else:
                directory_list.append(directory_path)

    for dir in directory_list:
        logger.info(f"dir: {dir}")
        os.chdir(dir)
        utils.distort_barrel(
                dir,
                size=size,
                initial_value=initial_value,
                closing_value=closing_value,
                step_value=step_value,
                )
        utils.get_jitter_image(
                dir,
                num_jitters=num_jitters,
                size=size,
                disturb_color=True,
                )


if __name__ == '__main__':
    args: list = sys.argv
    main(
        args[1],
        int(args[2]),
        int(args[3]),
        float(args[4]),
        float(args[5]),
        float(args[6]),
        )