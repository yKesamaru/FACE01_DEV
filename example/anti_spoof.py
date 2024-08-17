import os.path
import sys

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

from face01lib.spoof import Spoof

""" アンチスプーフ機能を試すエグザンプルコード.

Summary:
    極めて簡単にマルチモーダルのためのQRコードを作成します。
    洗練されたQRコード作成を作成したい場合は
    'example/make_ID_card.py'を参照してください。

Example:
    .. code-block:: bash

        python3 example/anti_spoof.py

Results:
    スクリーンショットは作成されるQRコードを示しています。

    .. image:: ../example/img/anti_spoof.png
        :scale: 100%
        :alt: Screenshot of the lightweight GUI output
"""


if __name__ == '__main__':

    # Spoof().iris()
    # Spoof().obj_detect()
    Spoof().make_qr_code()
