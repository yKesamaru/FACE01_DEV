"""樽型歪み画像をシミュレートするコード例.

Summary:
    In this example, you can learn how to get distorted images.

Args:
    path (str): Directory path where images containing faces exist
    size (int, optional): Specify the number of px for the extracted face image with an integer. Default is 200px.

Example:
    .. code-block:: bash

        python3 example/distort_barrel.py path size

Source code:
    `distort_barrel.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/distort_barrel.py>`_
"""
import os
import sys

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

from typing import Dict

from tqdm import tqdm

from face01lib.Initialize import Initialize
from face01lib.logger import Logger
# Operate directory: Common to all examples
from face01lib.utils import Utils

# Initialize
CONFIG: Dict = Initialize(
    'JAPANESE_FACE_V1_MODEL_GUI', 'info').initialize()
# Set up logger
logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])
"""Initialize and Setup logger.
When coding a program that uses FACE01, code `initialize` and `logger` first.
This will read the configuration file `config.ini` and log errors etc.
"""

utils = Utils(CONFIG['log_level'])


def main(
    dir_path: str,
    align_and_resize_bool: bool = False,
    size: int=224,
    padding: float=0.1,
    initial_value: float = -0.1,
    closing_value: float = 0.1,
    step_value: float = 0.1
) -> None:
    """Simple example.

    このシンプルなコード例では、拡張子がpng, jpg, jpeg画像を含むディレクトリのパスを受け取り、樽型歪み処理をして、それらを保存します。

    See `Tokai-kaoninsho:レンズの歪曲収差と対応方法(6) <https://tokai-kaoninsho.com/%e3%82%b3%e3%83%a9%e3%83%a0/%e3%83%ac%e3%83%b3%e3%82%ba%e3%81%ae%e6%ad%aa%e6%9b%b2%e5%8f%8e%e5%b7%ae%e3%81%a8%e5%af%be%e5%bf%9c%e6%96%b9%e6%b3%956/>`_

    Args:
        path (str): 絶対パス: 例えば"~/bin/FACE01_DEV/assets/data"
        align_and_resize_bool (bool, optional): Whether to align and resize. Defaults to False.
        size (int, optional): Width and height. Defaults to 224.
        initial_value (float): Initial value. Default is -0.05.
        closing_value (float): Closing value. Default is 0.05.
        step_value (float): Step value. Default is 0.05.

    Returns:
        None

    .. note::

        システムにImageMagickがインストールされていなければ正常動作しません。

        - See `ImageMagick <https://imagemagick.org/script/download.php>`_

    Result:
        .. image:: ../docs/img/distort_barrel.png
            :scale: 100%
            :alt: distort_barrel

    Image:
        `Pakutasoハート型のチョコと指ハートの無料写真素材 <https://www.pakutaso.com/20220158028post-38602.html>`_
    """
    os.chdir(dir_path)
    # pathディレクトリをrootとして、pathディレクトリ以下のディレクトリを取得
    dir_list = os.listdir(dir_path)
    for dir in tqdm(dir_list):
        utils.distort_barrel(
            dir,
            align_and_resize_bool,
            size,
            padding,
            initial_value,
            closing_value,
            step_value
        )


if __name__ == '__main__':
    args: list = sys.argv
    os.chdir(args[1])
    main(
        dir_path=args[1],
        align_and_resize_bool=False,
        size=512,
        padding=0.1,
        initial_value=-0.1,
        closing_value=0.1,
        step_value=0.1
    )
