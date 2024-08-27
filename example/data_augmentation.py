"""データセットのデータ拡張コード例.

Summary:
    このエグザンプルコードでは、データセットのデータ拡張する方法に
    ついて学びます。

Example:
    .. code-block:: bash

        python3 example/data_augmentation.py \
            "/path/to/dir" "" "lens" 224 10 -0.1 0.1 0.01

Result:
    .. image:: ../docs/img/data_augmentation.png
        :scale: 50%
        :alt: Image taken from https://tokai-kaoninsho.com

Source code:
    `data_augmentation.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/data_augmentation.py>`_
"""
# Operate directory: Common to all examples
import os.path
import sys
from glob import glob

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

from typing import Dict

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


def main(
    dir_path: str,
    size: int = 224,
    num_jitters: int = 10,
    initial_value: float = -0.1,
    closing_value: float = 0.1,
    step_value: float = 0.01,
):
    """
    この簡単なコード例では、与えられたディレクトリパスから再帰的に
    ファイルを読み込み、それらに対してデータ拡張を行います。
    この例でのデータ拡張は、FACE01のUtilsモジュールから、
    樽型歪みとジッターを呼び出します。

    Args:
        dir_path (str): ターゲットディレクトリの絶対パス.
        size (int, optional): 作成するイメージサイズ. Defaults to 224.
        num_jitters (int, optional): ジッター回数. Defaults to 10.
        initial_value (float, optional): 樽型歪みの初期値. Defaults to -0.1.
        closing_value (float, optional): 終わり値. Defaults to 0.1.
        step_value (float, optional): ステップ値. Defaults to 0.01.

    Return:
        ターゲットディレクトリから再帰的に読み込んだディレクトリごとに
        データ拡張したファイルを保存します。

    .. image:: ../assets/images/one_point_R.png
        :width: 70%
        :alt: one point

    樽型歪みをデータセットに加えることで、カメラのキャリブレーションが出来ない環境への耐性を高めます⭐️''
    `レンズの歪曲収差と対応方法 <https://tokai-kaoninsho.com/%e3%82%b3%e3%83%a9%e3%83%a0/%e3%83%ac%e3%83%b3%e3%82%ba%e3%81%ae%e6%ad%aa%e6%9b%b2%e5%8f%8e%e5%b7%ae%e3%81%a8%e5%af%be%e5%bf%9c%e6%96%b9%e6%b3%95/>`_
    をご参照ください。

    See Also:
        `dlib.jitter_image <http://dlib.net/python/index.html#dlib_pybind11.jitter_image>`_
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
