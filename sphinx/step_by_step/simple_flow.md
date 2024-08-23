# FACE01を使用するためのシンプルな流れ

<br />
<div style="display: flex; align-items: center;">
    <img src="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/00147-2005948782.png" alt="説明文" width="200" style="margin-right: 10px; border-radius: 50%; object-fit: cover;">
    <div style="background-color: white; padding: 10px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); position: relative;">
        <p style="margin: 10;">FACE01の豊富なクラスやメソッドを使って様々な機能を作ることが出来ますが、<span style="background-color: yellow;">基本的な使い方</span>が存在します。</p>
        <p style="margin: 10;">エグザンプルコードを参考にしながら一連の流れを確認しましょう⭐️''</p>
        <div style="position: absolute; top: 50%; left: -15px; width: 0; height: 0; border-top: 10px solid transparent; border-bottom: 10px solid transparent; border-right: 15px solid white; transform: translateY(-50%);"></div>
    </div>
</div>
<br />

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
