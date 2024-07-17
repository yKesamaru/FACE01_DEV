"""Example of calculating similarity from two photos with JAPANESE_FACE_V1.onnx model.

Summary:
    This is a sample code that calculates the similarity between two given photos,
    using the JAPANESE_FACE_V1.onnx model, which is a Japanese-only learning model.

Example:
    .. code-block:: bash

        python3 example/similarity.py

Source code:
    `similarity.py <../example/similarity.py>`_

Copyright Owner: Yoshitsugu Kesamaru
Please refer to the separate license file for the license of the code.
"""
# Operate directory: Common to all examples
import os.path
import sys

import numpy as np

dir: str = os.path.dirname(__file__)
parent_dir, _ = os.path.split(dir)
sys.path.append(parent_dir)

from typing import Dict, List

import cv2
import dlib
import numpy.typing as npt

from face01lib.api import Dlib_api
from face01lib.Initialize import Initialize
from face01lib.logger import Logger

if __name__ == '__main__':
    api_obj = Dlib_api()

    # Initialize
    CONFIG: Dict = Initialize(
        'JAPANESE_FACE_V1_MODEL', 'info')._configure()
    # Set up logger
    logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])

    face_path_list = [
        'example/img/麻生太郎_default.png',
        'example/img/安倍晋三_default.png'
    ]

    encoding_list = []
    for face_path in face_path_list:
        img = dlib.load_rgb_image(face_path)  # type: ignore

        face_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        face_locations: List = api_obj.face_locations(img, mode="cnn")
        face_encodings: List[npt.NDArray] = api_obj.face_encodings(
            deep_learning_model=1,
            resized_frame=img,
            face_location_list=face_locations
        )
        encoding_list.append(face_encodings[0])

    emb0 = encoding_list[0].flatten()
    emb1 = encoding_list[1].flatten()
    cos_sim = np.dot(emb0, emb1) / \
        (np.linalg.norm(emb0) * np.linalg.norm(emb1))
    percentage = api_obj.percentage(cos_sim)
    print('---')
    print('類似度（％）')
    print(percentage)
