"""Example of simple face recognition script with EfficientNetV2 Arcface model.

Summary:
    In this example, you can learn how to execute FACE01 as simple.

Example:
    .. code-block:: bash
    
        python3 example/simple_efficientnetv2_arcface.py
        
Source code:
    `simple_efficientnetv2_arcface.py <../example/simple_efficientnetv2_arcface.py>`_
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

# Initialize
CONFIG: Dict =  Initialize('JAPANESE_FACE_V1_MODEL', 'info').initialize()
# Set up logger
logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])
"""Initialize and Setup logger.
When coding a program that uses FACE01, code `initialize` and `logger` first.
This will read the configuration file `config.ini` and log errors etc.
"""

# Make generator
gen = Core().common_process(CONFIG)

def main(exec_times: int = 50) -> None:
    """Simple example.

    This simple example script prints out results of face recognition process.

    Args:
        exec_times (int, optional): Number of frames for process. Defaults to 50 times.

    Returns:
        None

    """    
    # Repeat 'exec_times' times
    for i in range(0, exec_times):

        # Call __next__() from the generator object
        frame_datas_array = gen.__next__()

        for frame_datas in frame_datas_array:
            
            for person_data in frame_datas['person_data_list']:
                if not person_data['name'] == 'Unknown':
                    print(
                        person_data['name'], "\n",
                        "\t", "similarity\t\t", person_data['percentage_and_symbol'], "\n",
                        "\t", "coordinate\t\t", person_data['location'], "\n",
                        "\t", "time\t\t\t", person_data['date'], "\n",
                        "\t", "output\t\t\t", person_data['pict'], "\n",
                        "-------\n"
                    )


if __name__ == '__main__':
    main(exec_times = 100)