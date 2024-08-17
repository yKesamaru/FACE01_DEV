"""JAPANESE FACE V1モデルを使用したQR顔エンコードの例.

Summary:
    この例では、マルチモーダル認証のためのQRコード付きIDカードサンプルの作成方法を学ぶことができます。
    作成された画像ファイルは'example/img/'ディレクトリに保存されます。
    この例ではより洗練されたQRコード付きIDカードサンプルを作成していますが、QRコードだけの作成ならば
    Spoof().make_qr_code()
    で作成できます。'example/anti_spoof.py'を参照してください。

Example:
    .. code-block:: bash

        python3 example/make_ID_card.py

Results:
    .. image:: ../docs/img/ID_card_sample.png
        :scale: 50%

Source code:
    `make_ID_card.py <../example/make_ID_card.py>`_
"""

# Operate directory: Common to all examples
import os.path
import sys

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

from typing import Dict, List

import cv2
import dlib
import numpy.typing as npt
from PIL import Image, ImageDraw, ImageFont

from face01lib.api import Dlib_api
from face01lib.Initialize import Initialize
from face01lib.logger import Logger
from face01lib.utils import Utils

api_obj = Dlib_api()
utils_obj = Utils()

if __name__ == '__main__':
    # Initialize
    CONFIG: Dict = Initialize('JAPANESE_FACE_V1_MODEL', 'info')._configure()
    # Set up logger
    logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])
    """Initialize and Setup logger.
    When coding a program that uses FACE01, code `initialize` and `logger` first.
    This will read the configuration file `config.ini` and log errors etc.
    """

    # 各画像のpath
    base_path = "example/img/base.png"
    # qr_path = 'example/img/qrcode.png'
    face_path = 'example/img/麻生太郎_default.png'
    # 適切なフォントパスを指定してください
    font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc'

    # Load '麻生.png' in the example/img folder
    img = dlib.load_rgb_image(face_path)  # type: ignore

    # Convert face_image from BGR to RGB
    face_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    face_locations: List = api_obj.face_locations(img, mode="cnn")
    face_encodings: List[npt.NDArray] = api_obj.face_encodings(
        deep_learning_model=1,
        resized_frame=img,
        face_location_list=face_locations
    )

    # QRコードを作成
    qr_img_list = utils_obj.return_qr_code(face_encodings[0])

    # 各画像を開く
    base_img = Image.open(base_path)
    face_img = Image.open(face_path)
    # 顔写真のファイル名を取得し、最初の"_"で区切る
    face_name = os.path.basename(face_path).split("_")[0]

    # 各画像を適切なサイズにリサイズ
    qr_img_resized = qr_img_list[0].resize((480, 480))  # QRコードのサイズを調整
    face_img_resized = face_img.resize((150, 150))  # 顔写真のサイズを調整
    # 文字を追加
    draw = ImageDraw.Draw(base_img)
    font = ImageFont.truetype(font_path, 25)  # フォントとサイズを指定

    # 各画像をベース画像に貼り付け
    base_img.paste(qr_img_resized, (10, 70))  # QRコードを貼り付け # type: ignore
    base_img.paste(face_img_resized, (80, 600))  # 顔写真を貼り付け
    draw.text((280, 700), face_name, fill='black', font=font)

    # 画像を保存
    base_img.save(os.path.join("example/img", 'ID_card_sample.png'))
