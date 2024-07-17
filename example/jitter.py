"""Example of to jitter images.

Summary:
    In this example, you can learn how to get jittered images.

Args:
    path (str): Directory path where images containing faces exist.
        num_jitters (int, optional): Number of jitters. Defaults to 5.
        size (int, optional): Resize the image to the specified size. Defaults to 200.
        disturb_color (bool, optional): Disturb the color. Defaults to True.

Returns:
    None

Example:
    .. code-block:: bash
    
        python example/jitter.py path 100 200 True

Result:
    .. image:: ../docs/img/jitter.png
        :scale: 100 %
        :alt: jitter_image

Source code:
    `jitter.py <../example/jitter.py>`_
"""
# Operate directory: Common to all examples
import os.path
import sys

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

from typing import Dict

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
    path: str,
    num_jitters: int=5,
    size: int = 200,
    disturb_color: bool = True
    ) -> None:
    """Simple example.
    
    This simple example script takes a path which contained png, jpg, jpeg files in the directory,
    jitter and saves them.

    Args:
        path (str): absolute path
        num_jitters (int, optional): Number of jitters. Defaults to 5.
        size (int, optional): Resize the image to the specified size. Defaults to 200.
        disturb_color (bool, optional): Disturb the color. Defaults to True.
    """    
    utils.get_jitter_image(path, num_jitters, size, disturb_color)


if __name__ == '__main__':
    args: list = sys.argv
    main(args[1], num_jitters=5, size=200, disturb_color=False)
    # OR, you can use like this:
    # main(args[1], int(args[2]), int(args[3]), bool(args[4]))
