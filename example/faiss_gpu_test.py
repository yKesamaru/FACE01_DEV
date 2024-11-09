"""GPU上でFAISSを用いたベクトルインデックスの作成と動作確認.

Summary:
    このスクリプトは、FAISSライブラリを使用して512次元のランダムベクトルデータをGPU上でインデックス化し、
    ベクトルが正しくインデックスに追加されるかを確認します。FAISSの`GpuIndexFlatL2`インデックスを用いて
    L2距離に基づいた検索を行い、インデックスがGPU上で正常に機能しているかをテストします。

    FAISSには、インストール時に`faiss-gpu`と`faiss-cpu`の2種類があり、このうち`faiss-gpu`をインストールした際に
    GPU上での動作が正常に行われないことがあります。このコードを実行し、`faiss-gpu`が期待通りに動作しない場合には、
    `faiss-gpu`をアンインストールし、代わりに`faiss-cpu`をインストールすることが推奨されます。
    これにより、CPU上でのFAISSの動作を確認できます。

    実行には`faiss`および`numpy`ライブラリが必要です。

Output Verification:
    このスクリプトの実行時に "Index contains 10000 vectors." という出力が表示される場合、
    以下の処理が正常に動作していることが確認できます：

    1. **GPUリソースの確保**: `faiss.StandardGpuResources()` がエラーなく実行されています。
    2. **GPUインデックスの作成**: `faiss.GpuIndexFlatL2(res, d)` により、GPUインデックスが正常に構築されています。
    3. **ベクトルの追加**: `index.add(xb)` によって、ベクトルがインデックスに正常に追加されています。
    4. **インデックス内容の確認**: `index.ntotal` により、インデックスに追加されたベクトル数が正しく表示されています。

    この結果により、`faiss-gpu`はGPU上でのインデックス作成やデータ処理が期待通り動作していると判断できます。

Example:
    .. code-block:: python

        python3 example/faiss_gpu_test.py
Notes:
    - `faiss-gpu`が正常に動作しない場合の対処方法:
        1. `faiss-gpu`をアンインストール:
           pip uninstall faiss-gpu
        2. `faiss-cpu`をインストール:
           pip install faiss-cpu
        3. このスクリプトを再実行し、`faiss-cpu`がCPU上で正常に動作するか確認します。

.. image:: ../assets/images/one_point_L.png
    :width: 70%
    :alt: one point

このテストをパスしてもなお`faiss-gpu`が機能しない場合があります。その場合はfaiss-cpuを試してください。⭐️''

Source code:
    `faiss_gpu_test.py <https://github.com/yKesamaru/FACE01_DEV/blob/master/example/faiss_gpu_test.py>`__
"""


import faiss
import numpy as np

# ベクトル次元数とデータベースのベクトル数を定義
d = 512  # ベクトルの次元数
nb = 10000  # データベースのベクトル数

# ランダムなデータを生成し、インデックスに追加
np.random.seed(1234)
xb = np.random.random((nb, d)).astype('float32')
xb[:, 0] += np.arange(nb) / 1000.

# GPUインデックスを作成し、データをインデックスに追加
res = faiss.StandardGpuResources()  # GPUリソースの確保
index = faiss.GpuIndexFlatL2(res, d)  # L2距離でのGPUインデックスを作成
index.add(xb)  # データをインデックスに追加

# インデックスの内容を確認
print("Index contains", index.ntotal, "vectors.")
