"""データ拡張をマルチプロセスで行うコード例.

Summary:
    このエグザンプルコードでは、時間のかかるデータ拡張においてマルチプロセス処理を行います。

Example:
    .. code-block:: bash

        python3 example/data_augmentation.py "/path/to/dir" "" "lens" 224 10 -0.1 0.1 0.01 4

Source code:
    `data_augmentation_mp.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/data_augmentation_mp.py>`_
"""
import concurrent.futures
# Operate directory: Common to all examples
import os.path
import sys
from concurrent.futures import ProcessPoolExecutor
from glob import glob

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

from typing import Dict, Optional

from face01lib.Initialize import Initialize
from face01lib.logger import Logger
from face01lib.utils import Utils

# Initialize
CONFIG: Dict = Initialize('DEFAULT', 'info').initialize()
# Set up logger
logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])
"""Initialize and Setup logger.
"""

utils = Utils(CONFIG['log_level'])


def _process_data(
    dir: str,
    size: int,
    initial_value: float,
    closing_value: float,
    step_value: float,
    num_jitters: int
):
    """_process_data 樽型歪みとジッター処理を行います

    Args:
        dir (str): ディレクトリパス
        size (int): 画像サイズ
        initial_value (float): 初期値
        closing_value (float): 最終値
        step_value (float): ステップ値
        num_jitters (int): ジッター回数
    """
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
    """main メインメソッド

    Args:
        dir_path (str): ディレクトリパス
        size (int, optional): 画像サイズ. Defaults to 224.
        num_jitters (int, optional): ジッター処理回数. Defaults to 10.
        initial_value (float, optional): 初期値. Defaults to -0.1.
        closing_value (float, optional): 最終値. Defaults to 0.1.
        step_value (float, optional): ステップ値. Defaults to 0.01.
        max_workers (Optional[int], optional): 並行処理値. Defaults to None.
    """
    data_dir = dir_path
    directory_list = []

    # Search recursively under the data directory
    for root, dirs, _ in os.walk(data_dir):
        for directory in dirs:
            directory_path = os.path.join(root, directory)
            # Get all files in directory_path and store them in files
            files = glob(os.path.join(directory_path, "*"))
            # skip the for statement if any element of the list files contains the string jitter
            if any('jitter' in file for file in files):
                continue
            else:
                directory_list.append(directory_path)

    # Execute data processing in parallel for each directory
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                _process_data,
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
