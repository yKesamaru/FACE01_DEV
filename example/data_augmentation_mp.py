"""License for the Code.

Copyright Owner: Yoshitsugu Kesamaru
Please refer to the separate license file for the license of the code.
"""

"""Example of data augmentation for DNN using multi process.

Summary:
    In this example you can learn how to augment data for DNN using multi process.

Example:
    .. code-block:: bash
    
        python3 example/data_augmentation.py \
            "/path/to/dir" "" "lens" 224 10 -0.1 0.1 0.01 4
        
Source code:
    `data_augmentation.py <../example/data_augmentation_mp.py>`_
"""
# Operate directory: Common to all examples
import os.path
import sys
from glob import glob
from concurrent.futures import ProcessPoolExecutor
import concurrent.futures

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

from typing import Dict, Optional

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

def process_data(
    dir: str,
    size: int,
    initial_value: float,
    closing_value: float,
    step_value: float,
    num_jitters: int
):
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

def main(
    dir_path: str,
    size: int = 224,
    num_jitters: int = 10,
    initial_value: float = -0.1,
    closing_value: float = 0.1,
    step_value: float = 0.01,
    max_workers: Optional[int] = None,
):
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

    # Execute data processing in parallel for each directory
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                process_data,
                dir,
                size,
                initial_value,
                closing_value,
                step_value,
                num_jitters,
            )
            for dir in directory_list
        ]

        # Wait until all processing is complete
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == '__main__':
    args: list = sys.argv
    main(
        args[1],
        int(args[2]),
        int(args[3]),
        float(args[4]),
        float(args[5]),
        float(args[6]),
        max_workers=4
    )

