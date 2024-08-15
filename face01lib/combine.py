from itertools import chain
from typing import List, TypeVar

T = TypeVar('T')
import numpy as np

from face01lib.logger import Logger


class Comb:
    def __init__(self, log_level: str = 'info'):
        # Setup logger: common way
        self.log_level: str = log_level
        import os.path
        name: str = __name__
        dir: str = os.path.dirname(__file__)
        parent_dir, _ = os.path.split(dir)

        self.logger = Logger(self.log_level).logger(name, parent_dir)

    @staticmethod
    def comb(a: List[T], b: List[T]) -> List[T]:
        # 両方がnp.ndarrayの場合
        if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
            return list(np.concatenate((a, b)))

        # aがリストで、bがイテラブルなオブジェクト（文字列を除く）の場合
        elif isinstance(a, list) and hasattr(b, '__iter__') and not isinstance(b, str):
            if isinstance(b, np.ndarray):
                return list(chain(a, b.tolist()))  # bをリストに変換してから結合
            else:
                return list(chain(a, b))

        # bがリストで、aがイテラブルなオブジェクト（文字列を除く）の場合
        elif isinstance(b, list) and hasattr(a, '__iter__') and not isinstance(a, str):
            if isinstance(a, np.ndarray):
                return list(chain(b, a.tolist()))  # aをリストに変換してから結合
            else:
                return list(chain(b, a))

        # bがリストで、aが単一の要素の場合
        elif isinstance(b, list):
            if isinstance(a, np.ndarray):
                return list(chain(b, a.tolist()))  # aをリストに変換してから結合
            elif isinstance(a, list):
                return list(chain(b, a))  # aがリストの場合、そのまま結合
            else:
                return list(chain(b, [a]))  # aがリストでない場合、リストにしてから結合

        # それ以外の場合
        else:
            return list(chain(a, [b]))
