"""Manage log."""

import logging
import sys
from typing import Dict


class Logger:
    """Set log level."""
    def __init__(self, log_level: str = 'info') -> None:
        """init.

        Args:
            log_level(str): Set log level. Default to 'info'.
            Chose from bellow
            - 'debug'
            - 'info'

        You can pass value as CONFIG["set_level"]
        """
        self.log_level: str = log_level

    def logger(
        self,
        name: str,
        dir: str
    ):
        """Manage log.

        Args:
            name (str): File name
            dir (str): Directory name. (Usually the root directory of FACE01)

        Returns:
            Logger object: logger

        NOTE:
            | `parent_dir` in the above example refers to the root directory of FACE01.
            | i.e. `CONFIG['RootDir']` in the code below.

            .. code-block:: python

                # Initialize
                CONFIG: Dict =  Initialize('LIGHTWEIGHT_GUI', 'info').initialize()
                # Set up logger
                logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])


        """
        self.name = name
        self.dir = dir

        logger = logging.getLogger(self.name)

        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(filename)s] [%(levelname)s] %(message)s')

        log_file = dir + 'face01.log'
        file_handler = logging.FileHandler(log_file, mode='a')
        if self.log_level == 'debug':
            logger.setLevel(logging.DEBUG)
            file_handler.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
            file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler(stream=sys.stdout)
        if self.log_level == 'debug':
            logger.setLevel(logging.DEBUG)
            stream_handler.setLevel(logging.DEBUG)
        else:
            stream_handler.setLevel(logging.INFO)
            logger.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        return logger
