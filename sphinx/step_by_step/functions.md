# 関数のチュートリアル
このセクションでは、`main_process`関数について説明します。
他の関数の情報は[こちら](more_functions.md)で説明されています。
FACE01を使用するためには、このチュートリアルを読むだけで十分です。

まず、FACE01をインポートする必要があります。
```python
import FACE01 as fg
```

## `main_process`
`FACE01.py`ファイル内で以下のように定義されています。
```python
Core_obj= Core()
def main_process():
    frame_datas_array = Core_obj.frame_pre_processing(logger, args_dict, frame_generator_obj.__next__())
    face_encodings, frame_datas_array = Core_obj.face_encoding_process(logger, args_dict, frame_datas_array)
    frame_datas_array = Core_obj.frame_post_processing(logger, args_dict, face_encodings, frame_datas_array, GLOBAL_MEMORY)
    yield frame_datas_array
```
この関数は3つの部分に分かれています。
1.  `Core_obj.frame_pre_processing(logger, args_dict, frame_generator_obj.__next__())`
2.  `Core_obj.face_encoding_process(logger, args_dict, frame_datas_array)`
3.  `Core_obj.frame_post_processing(logger, args_dict, face_encodings, frame_datas_array, GLOBAL_MEMORY)`

`Core`は`face01lib.Core`内で宣言されたクラスです。
`Core`クラスをインポートするには、`frame_pre_processing`セクションを参照してください。

`main_process`メソッドはジェネレータであり、配列を返します。
```python
frame_datas_array = fg.main_process().__next__()
```
```python
while True:
    try:
        frame_datas_array = main_process().__next__()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        exit(0)
    exec_times = exec_times - 1
    if  exec_times <= 0:
        break
    else:
        print(f'exec_times: {exec_times}')
        if args_dict["headless"] == False:
            event, _ = window.read(timeout = 1)
            if event == sg.WIN_CLOSED:
                print("The window was closed manually")
                break
        for frame_datas in frame_datas_array:
            if "face_location_list" in frame_datas:
                img = frame_datas['img']
                person_data_list = frame_datas['person_data_list']

                for person_data in person_data_list:
                    if person_data == {}:
                        continue

                    name = person_data['name']
                    pict = person_data['pict']
                    date = person_data['date']
                    location = person_data['location']
                    percentage_and_symbol = person_data['percentage_and_symbol']
```

### `frame_pre_processing`
```python
fg.Core().frame_pre_processing(fg.logger, fg.args_dict,next_frame)
```
は、`img`、`face_location_list`、`overlay`、`person_data_list`の変数を含む`Dict`を返します。
- `img`
  - `numpy.ndarray`
- `face_location_list`
  -  `List[tuple]`
- `overlay`
  - `numpy.ndarray`
- `person_data_list`
  - `List[Dict{name:'', pict: '', date: '', location: tuple, percentage_and_symbol: ''}]`

`face_location_list`には顔の座標が含まれています。顔の座標のみが必要な場合、この関数は便利です。

### `face_encoding_process`
映像のフレーム内にいる人物の名前を取得したい場合、`frame_pre_processing`、`face_encoding_process`、および`frame_post_processing`メソッドを呼び出す必要があります。
これら3つのメソッドは`main_process`内にグループ化されています。
`face_encoding_process`と`frame_post_processing`は、単独で使用される機会は少ないです。
```python
fg.Core().face_encoding_process(fg.logger, fg.args_dict, fg.frame_datas_array)
```
は、`face_encodings`、`frame_datas_array`を返します。
- `face_encodings`
  - `numpy.ndarray[list, ...]`
- `frame_datas_array`
  - `[{'img': 'no-data_img', 'face_location_list': [...], 'overlay': array([], dtype=float64), 'person_data_list': [...]}]`

### `frame_post_processing`
```python
 fg.Core().frame_post_processing(fg.logger,fg.args_dict, face_encodings, frame_datas_array, fg.GLOBAL_MEMORY)
 ```
は、`frame_datas_array`を返します。
- `[{'img': 'no-data_img', 'face_location_list': [...], 'overlay': array([], dtype=float64), 'person_data_list': [...]}]`

## `person_data_list`
上記の例では、返された値`person_data_list`が非常に重要です。
`person_data_list`には、以下の値が含まれています。
- `name`
- `pict`
  - 保存された顔画像ファイルのパス
- `date`
- `location`
  - Tuple: フレーム内の顔の座標
  - (top, right, bottom, left)
- `percentage_and_symbol`
  - フレーム内の顔の類似度を'%'で表したもの

### 例
```python
for person_data in person_data_list:
    name, pict, date,  location, percentage_and_symbol = \
        person_data['name'], person_data['pict'], person_data['date'],  person_data['location'], person_data['percentage_and_symbol']
    if not name == 'Unknown':
        print(
            name, "\n",
            "\t", "similarity\t", percentage_and_symbol, "\n",
            "\t", "coordinate\t", location, "\n",
            "\t", "time\t", date, "\n",
            "\t", "output\t", pict, "\n",
            "-------\n"
        )
```
結果は以下のようになります。
```bash
菅義偉
         similarity      99.3%
         coordinate      (127, 182, 276, 33)
         time    2022,07,22,11,05,01,426742
         output  output/菅義偉_2022,07,22,11,05,01,459014_0.34.png
 -------

麻生太郎
         similarity      99.4%
         coordinate      (122, 535, 281, 376)
         time    2022,07,22,11,05,01,426742
         output  output/菅義偉_2022,07,22,11,05,01,459014_0.34.png
 -------
```
