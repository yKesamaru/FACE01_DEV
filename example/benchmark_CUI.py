"""顔認識のベンチマークをとるエグザンプルコード例.

Summary:
    このコード例では、CUIモードでのベンチマークテストを行う方法を示します。
    このベンチマークテストを行うには開発用パッケージを追加インストールする必要があります。
    具体的にはrequirements_dev.txtをインストールしてください。

    .. code-block:: bash

        pip install -r requirements_dev.txt

    実行後、ベンチマークが自動的にブラウザで表示されます。
    終了するには、このエグザンプルが実行されているターミナル（またはコンソール）で「Ctrl + C」を押してください。

.. image:: ../docs/img/benchmark_CUI_restats.png
    :alt: SnakeVizによるベンチマークテスト画像
    :scale: 50%

Example:
    .. code-block:: bash

        python3 benchmark_CUI.py

Source code:
    `benchmark_CUI.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/benchmark_CUI.py>`_
"""
# Operate directory: Common to all examples
import os.path
import sys

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)


import cProfile as pr
import subprocess
from typing import Dict

from face01lib.Calc import Cal
from face01lib.Core import Core
from face01lib.Initialize import Initialize


def main(exec_times: int = 50) -> None:
    """Open automatically benchmark on you're own browser.

    Args:
        exec_times (int, optional): Number of frames for process. Defaults to 50 times.

    Returns:
        None
    """
    # Initialize
    CONFIG: Dict = Initialize().initialize()

    gen = Core().common_process(CONFIG)

    # Specify START point
    START: float = Cal.Measure_processing_time_forward()

    # Repeat 'exec_times' times
    for i in range(0, exec_times):

        # Call __next__() from the generator object
        frame_datas_array = gen.__next__()

        for frame_datas in frame_datas_array:

            for person_data in frame_datas['person_data_list']:
                if not person_data['name'] == 'Unknown':
                    # pass
                    print(
                        person_data['name'], "\n",
                        "\t", "similarity\t\t", person_data['percentage_and_symbol'], "\n",
                        "\t", "coordinate\t\t", person_data['location'], "\n",
                        "\t", "time\t\t\t", person_data['date'], "\n",
                        "\t", "output\t\t\t", person_data['pict'], "\n",
                        "-------\n"
                    )

    END = Cal.Measure_processing_time_backward()

    print(f'Total processing time: {round(Cal.Measure_processing_time(START, END) , 3)}[seconds]')
    print(f'Per frame: {round(Cal.Measure_processing_time(START, END) / ( exec_times), 3)}[seconds]')


if __name__ == '__main__':
    pr.run('main(exec_times = 1)', 'restats')
    subprocess.run(["snakeviz", "restats"])
