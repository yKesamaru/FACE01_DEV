"""Example of benchmark for face recognition.

Summary:
    In this example, you can learn about log functions.

    You can choose from two types of `log_level`,
        - info
        - debug
    in `CONFIG: Dict =  Initialize('DEFAULT', 'log_level').initialize()`.
    
Example:
    .. code-block:: python
    
        # Initialize
        CONFIG: Dict =  Initialize('DEFAULT', 'debug').initialize()
        # Set up logger
        logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])

Example:
    .. code-block:: bash
    
        python3 example/logging.py
        
Source code:
    `example_logging.py <../example/example_logging.py>`_
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
import os.path


name: str = __name__
dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)

# Initialize
CONFIG: Dict =  Initialize('DEFAULT', 'debug').initialize()
# Set up logger
logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])
"""Initialize and Setup logger.
When coding a program that uses FACE01, code `initialize` and `logger` first.
This will read the configuration file `config.ini` and log errors etc.
"""


def main(exec_times: int = 50) -> None:
    """Setup logger example.

    Output log with define log-level.

    Args:
        exec_times (int, optional): Number of frames for process. Defaults to 50 times.

    Returns:
        None

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
    main(exec_times = 10)
