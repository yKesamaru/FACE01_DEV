"""シンプルな顔認識のコード例.

Summary:
    このコード例では、FACE01がどれほど簡単に実行できるのかを学びます。

Example:
    .. code-block:: bash

        python3 example/simple.py

Source code:
    `simple.py <../example/simple.py>`_
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
CONFIG: Dict = Initialize('DEFAULT', 'info').initialize()
# Set up logger
logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])
"""初期化とロガーの設定.

FACE01を使ったコードでは、まず`initialize`と`logger`をコードしなくてはいけません。
これらは`config.ini`設定ファイルを読み込んだり`log`の設定を行います。
"""

# Make generator
gen = Core().common_process(CONFIG)


def main(exec_times: int = 50) -> None:
    """Simple example.

    This simple example script prints out results of face recognition process.

    Args:
        exec_times (int, optional): 何回フレームを処理するかを決定します。 Defaults to 50 times.

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
                else:
                    print(
                        "Unknown person", "\n",
                        "-------\n"
                    )


if __name__ == '__main__':
    # Call main function. Pass 5.
    main(exec_times=100)
