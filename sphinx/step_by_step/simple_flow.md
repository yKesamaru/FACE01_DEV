# FACE01を使用するためのシンプルな流れ

`FACE01`を使用するプログラムをコーディングする際には、最初に`initialize`および`logger`をコードします。

これにより、設定ファイル`config.ini`が読み込まれ、エラーなどがログに記録されます。

使用目的に応じて`config.ini`のセクションを選択するか、`DEFAULT`を継承して新しいセクションを追加してください。

```python
# Initializeクラスをインポート
from face01lib.Initialize import Initialize
from face01lib.logger import Logger

# 初期化
CONFIG: Dict =  Initialize('DEFAULT').initialize()
# Loggerの設定
logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])
```

次に、連続するフレームデータを読み込むために`generator`を作成する必要があります。
```python
# Coreクラスをインポート
from face01lib.Core import Core

# ジェネレータの作成
gen = Core().common_process(CONFIG)
```

`Core`クラスの`common_processメソッド`を使用することで、顔検出から顔認識までの一連の流れをスムーズに実行できます。

データを取得するには、`__next__`を呼び出す必要があります。
```python
while True:

    # ジェネレータオブジェクトから__next__()を呼び出す
    frame_datas_array = gen.__next__()
```

`frame_datas_array`にはさまざまなデータが含まれています。取得するデータの種類や内容を`config.ini`に設定してください。
