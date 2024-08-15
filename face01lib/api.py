"""Summary.

COPYRIGHT:
    This code is based on 'face_recognition' written by Adam Geitgey (ageitgey),
    and modified by Yoshitsugu Kesamaru (yKesamaru).

ORIGINAL AUTHOR:
    - Dlib
        - davisking
    - face_recognition
        - ageitgey
    - FACE01, and api.py
        - yKesamaru

References:
    - Dlib:
        - https://github.com/davisking/dlib
    - Dlib Python API:
        - http://dlib.net/python/index.html
    - dlib/python_example/face_recognition.py:
        - https://github.com/davisking/dlib/blob/master/python_examples/face_recognition.py
    - Dlib Face Recognition Model:
        - https://github.com/davisking/dlib-models
    - Face Recognition:
        - https://github.com/ageitgey/face_recognition
    - Max-Margin Object Detection(MMOD):
        - [Ja] https://blog.chowagiken.co.jp/entry/2019/06/28/OpenCV%E3%81%A8dlib%E3%81%AE%E9%A1%94%E6%A4%9C%E5%87%BA%E6%A9%9F%E8%83%BD%E3%81%AE%E6%AF%94%E8%BC%83
        - https://github.com/davisking/dlib-models
    - Typing (numpy.typing):
        - https://numpy.org/doc/stable/reference/typing.html#typing-numpy-typing
    - EfficientNetV2:
        - https://arxiv.org/pdf/2104.00298.pdf
        - https://github.com/huggingface/pytorch-image-models
    - ArcFace:
        - https://arxiv.org/pdf/1801.07698.pdf
    - MobileFaceNets:
        - https://arxiv.org/ftp/arxiv/papers/1804/1804.07573.pdf

NOTE:
    About coordinate order...

    - dlib: (Left, Top, Right, Bottom), called 'rect'.
    - face_recognition: (top, right, bottom, left), called 'css'.

    See bellow
    https://github.com/davisking/dlib/blob/master/python_examples/face_recognition.py

DEBUG: MEMORY LEAK
    .. code-block:: python

        from .memory_leak import Memory_leak
        m = Memory_leak(limit=2, key_type='traceback', nframe=20)
        m.memory_leak_analyze_start()

See bellow:
    [Ja] https://zenn.dev/ykesamaru/articles/bd403aa6d03100
"""


from typing import List, Tuple

import dlib
import numpy as np
import numpy.typing as npt  # See [Typing (numpy.typing)](https://numpy.org/doc/stable/reference/typing.html#typing-numpy-typing)
from PIL import ImageFile
from PIL import Image
import cv2

ImageFile.LOAD_TRUNCATED_IMAGES = True
from sys import exit
from traceback import format_exc

from face01lib.Calc import Cal
from face01lib.logger import Logger
# from face01lib.video_capture import VidCap
import onnx
import onnxruntime as ort
import torchvision.transforms as transforms


class Dlib_api:
    """Dlib api.

    Author: Original code written by Adam Geitgey, modified by YOSHITSUGU KESAMARU

    Email: y.kesamaru@tokai-kaoninsho.com
    """

    def __init__(
        self,
        # log_level: str = 'info'
        log_level: str = 'error'
    ) -> None:
        """init.

        Args:
            log_level (str, optional): Receive log level value. Defaults to 'info'.
        """
        # Setup logger: common way
        self.log_level: str = log_level
        import os.path
        name: str = __name__
        dir: str = os.path.dirname(__file__)
        parent_dir, _ = os.path.split(dir)

        # self.logger = Logger(self.log_level).logger(name, parent_dir)
        # self.logger.info("COPYRIGHT: TOKAI-KAONINSHO, yKesamaru")
        # self.logger.info("FACE01: 商用利用にはライセンスが必要です")

        # DEBUG: ログ抑制 #################################################
        # Loggerクラスの初期化
        self.logger = Logger('error').logger(name, parent_dir)  # ログレベルを'error'に設定
        # ONNX Runtimeのログ抑制 (例)
        os.environ['ORT_LOGGING_LEVEL'] = 'ERROR'
        # #################################################################

        # cv2のスパムログ出力を抑制 ####################
        import logging
        logging.getLogger('cv2').setLevel(logging.ERROR)
        os.environ['OPENCV_LOG_LEVEL'] = 'ERROR'
        # ##############################################

        try:
            from .models import Models
            Models_obj = Models()
        except Exception:
            self.logger.error("Failed to import dlib model")
            self.logger.error("-" * 20)
            self.logger.error(format_exc(limit=None, chain=True))
            self.logger.error("-" * 20)
            exit(0)

        # Cal().cal_specify_date(self.logger)  # 日付による使用停止処理は廃止

        self.face_detector = dlib.get_frontal_face_detector()  # type: ignore

        self.predictor_5_point_model = Models_obj.pose_predictor_five_point_model_location()
        self.pose_predictor_5_point = dlib.shape_predictor(
            self.predictor_5_point_model)  # type: ignore

        self.cnn_face_detection_model = Models_obj.cnn_face_detector_model_location()
        self.cnn_face_detector = dlib.cnn_face_detection_model_v1(
            self.cnn_face_detection_model)  # type: ignore

        self.dlib_resnet_model = Models_obj.dlib_resnet_model_location()
        self.dlib_resnet_face_encoder = dlib.face_recognition_model_v1(
            self.dlib_resnet_model)  # type: ignore

        self.JAPANESE_FACE_V1 = Models_obj.JAPANESE_FACE_V1_model_location()
        self.JAPANESE_FACE_V1_model = onnx.load(self.JAPANESE_FACE_V1)
        # self.ort_session = ort.InferenceSession(self.JAPANESE_FACE_V1)
        self.ort_session = ort.InferenceSession(self.JAPANESE_FACE_V1, providers=[
                                                'CUDAExecutionProvider', 'CPUExecutionProvider'])

        # 署名表示
        for prop in self.JAPANESE_FACE_V1_model.metadata_props:
            if prop.key == "signature":
                print(prop.value)

    def JAPANESE_FACE_V1_model_compute_face_descriptor(
        self,
        resized_frame: npt.NDArray[np.uint8],
        raw_face_landmark,  # dlib.rectangle type.
        size: int = 224,
        _PADDING: float = 0.1
    ) -> npt.NDArray[np.float32]:
        """EfficientNetV2とArcFaceモデルを使用して顔の特徴量を計算します。

        この関数は、与えられた顔の画像データから、EfficientNetV2とArcFaceモデルを使用して顔の特徴量（embedding）を計算します。

        Args:
            resized_frame (npt.NDArray[np.uint8]): リサイズされたフレームの画像データ。
            raw_face_landmark (dlib.rectangle): 顔のランドマーク情報。
            size (int, optional): 顔のチップのサイズ。デフォルトは224。
            _PADDING (float, optional): 顔のチップを取得する際のパディング。デフォルトは0.1。

        Returns:
            npt.NDArray[np.float32]: 顔の特徴量（embedding）。
        """
        self.resized_frame: npt.NDArray[np.uint8] = resized_frame
        # VidCap().frame_imshow_for_debug(self.resized_frame)

        self.raw_face_landmark = raw_face_landmark  # dlib.rectangle type.
        # print(self.raw_face_landmark)

        self.size: int = size
        self._PADDING: float = _PADDING

        face_image_np: npt.NDArray = dlib.get_face_chip(
            self.resized_frame, self.raw_face_landmark, size=self.size, padding=self._PADDING)  # type: ignore
        # face_imageをBGRからRGBに変換する
        face_image_rgb = cv2.cvtColor(
            face_image_np, cv2.COLOR_BGR2RGB)  # type: ignore
        # VidCap().frame_imshow_for_debug(face_image_rgb)

        # 入力名を取得
        input_name: str = self.JAPANESE_FACE_V1_model.graph.input[0].name

        # 画像の前処理を定義
        mean_value = [0.485, 0.456, 0.406]
        std_value = [0.229, 0.224, 0.225]
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=mean_value,
                std=std_value
            )
        ])

        # numpy配列からPIL Imageに変換
        face_image_pil: Image.Image = Image.fromarray(face_image_rgb)

        image = transform(face_image_pil)
        image = image.unsqueeze(0)  # バッチ次元を追加  # type: ignore
        image = image.numpy()
        embedding: npt.NDArray[np.float32] = self.ort_session.run(
            None, {input_name: image})[0]  # 'input'をinput_nameに変更
        return embedding

    # type: ignore
    def _rect_to_css(self, rect: dlib.rectangle) -> Tuple[int, int, int, int]:
        """Convert a dlib 'rect' object to a plain tuple in (top, right, bottom, left) order.

        This method used only 'use_pipe = False'.

        Args:
            dlib.rectangle: dlib rect object

        Returns:
            Tuple[int,int,int,int]: Plain tuple representation of the rect in (top, right, bottom, left) order
        """
        self.rect: dlib.rectangle = rect  # type: ignore
        return self.rect.top(), self.rect.right(), self.rect.bottom(), self.rect.left()

    # type: ignore
    def _css_to_rect(self, css: Tuple[int, int, int, int]) -> dlib.rectangle:
        self.css: Tuple[int, int, int, int] = css
        """Convert a tuple in (top, right, bottom, left) order to a dlib 'rect' object

        Args:
            Tuple[int,int,int,int]: css
            - Plain tuple representation of the rect in (top, right, bottom, left) order

        Returns:
            dlib.rectangle: <class '_dlib_pybind11.rectangle'>
        """
        return dlib.rectangle(self.css[3], self.css[0], self.css[1], self.css[2])  # type: ignore

    def _trim_css_to_bounds(
        self,
        css: Tuple[int, int, int, int],
        image_shape: Tuple[int, int, int]
    ) -> Tuple[int, int, int, int]:
        self._trim_css_to_bounds_css: Tuple[int, int, int, int] = css
        self.image_shape: Tuple[int, int, int] = image_shape
        """Trim 'css' along with border.

        Make sure a tuple in (top, right, bottom, left) order is within the bounds of the image.
        This method used only 'use_pipe = False'.

        Args:
            Tuple[int,int,int,int]: css
            - Plain tuple representation of the rect in (top, right, bottom, left) order

            Tuple[int,int,int]: image_shape
            - numpy shape of the image array

        Returns:
            Tuple[int,int,int,int]:  a trimmed plain tuple representation of the rect in (top, right, bottom, left) order
        """
        return (
            max(self._trim_css_to_bounds_css[0], 0),
            min(self._trim_css_to_bounds_css[1], self.image_shape[1]),
            min(self._trim_css_to_bounds_css[2], self.image_shape[0]),
            max(self._trim_css_to_bounds_css[3], 0)
        )

    def load_image_file(
        self,
        file: str,
        mode: str = 'RGB'
    ) -> npt.NDArray[np.uint8]:
        """Loads an image file (.jpg, .png, etc) into a numpy array.

        Args:
            file (str): image file name or file object to load
            mode (str): format to convert the image to. Only 'RGB' (8-bit RGB, 3 channels) and 'L' (black and white) are supported.

        Returns:
            npt.NDArray[np.uint8]: image contents as numpy array
        """
        self.file = file
        self.mode = mode
        im = Image.open(self.file)

        if self.mode:
            im = im.convert(self.mode)

        return np.array(im)

    def _raw_face_locations(
        self,
        resized_frame: npt.NDArray[np.uint8],
        number_of_times_to_upsample: int = 0,
        mode: str = "cnn"
    ) -> List[dlib.rectangle]:  # type: ignore
        """Returns an array of bounding boxes of human faces in a image.

        This method used only 'use_pipe = False'.

        Args:
            npt.NDArray[np.uint8]: resized_frame: An image
            int: number_of_times_to_upsample
            - How many times to upsample the image looking for faces. Higher numbers find smaller faces.

            str: mode
            - Which face detection mode to use. "hog" is less accurate but faster on CPUs. "cnn" is a more accurate deep-learning mode which is GPU/CUDA accelerated (if available). The default is "hog".

        Returns:
            List[dlib.rectangle]: a list of dlib 'rect' objects of found face locations
        """
        self.resized_frame: npt.NDArray[np.uint8] = resized_frame
        self.number_of_times_to_upsample: int = number_of_times_to_upsample
        self.mode: str = mode
        if self.mode == "cnn":
            return self.cnn_face_detector(self.resized_frame, self.number_of_times_to_upsample)
        else:
            return self.face_detector(self.resized_frame, self.number_of_times_to_upsample)

    def face_locations(
        self,
        resized_frame: npt.NDArray[np.uint8],
        number_of_times_to_upsample: int = 0,
        mode: str = "hog"
    ) -> List[Tuple[int, int, int, int]]:
        """Returns an array of bounding boxes of human faces in a image.

        This method used only 'use_pipe = False'.

        Args:
            resized_frame (npt.NDArray[np.uint8]): Resized image
            number_of_times_to_upsample (int): How many times to upsample the image looking for faces. Higher numbers find smaller faces.
            mode (str): Which face detection mode to use. "hog" is less accurate but faster on CPUs. "cnn" is a more accurate deep-learning mode which is GPU/CUDA accelerated (if available). The default is "hog".

        Returns:
            A list of tuples of found face locations in css (top, right, bottom, left) order
        """
        self.resized_frame: npt.NDArray[np.uint8] = resized_frame
        self.number_of_times_to_upsample: int = number_of_times_to_upsample
        self.mode: str = mode
        face_locations: List[Tuple[int, int, int, int]] = []

        if self.mode == 'cnn':
            for face in self._raw_face_locations(
                self.resized_frame,
                self.number_of_times_to_upsample,
                self.mode
            ):
                face_locations.append(
                    self._trim_css_to_bounds(
                        self._rect_to_css(face.rect),
                        self.resized_frame.shape
                    )
                )
        else:
            for face in self._raw_face_locations(
                self.resized_frame,
                self.number_of_times_to_upsample,
                self.mode
            ):
                face_locations.append(
                    self._trim_css_to_bounds(
                        self._rect_to_css(face),
                        self.resized_frame.shape
                    )
                )

        return face_locations

    def _return_raw_face_landmarks(
        self,
        resized_frame: npt.NDArray[np.uint8],
        face_location_list: List[Tuple[int, int, int, int]],
        model: str = "small"
    ) -> List[dlib.rectangle]:  # type: ignore

        # type: ignore
        new_face_location_list: List[dlib.rectangle[Tuple[int, int, int, int]]] = [
        ]
        raw_face_location: Tuple[int, int, int, int]

        for raw_face_location in face_location_list:
            new_face_location_list.append(self._css_to_rect(raw_face_location))

        # type: ignore
        raw_face_landmarks: List[dlib.rectangle[Tuple[int, int, int, int]]] = [
        ]
        # type: ignore
        new_face_location: dlib.rectangle[Tuple[int, int, int, int]]

        for new_face_location in new_face_location_list:
            raw_face_landmarks.append(
                self.pose_predictor_5_point(resized_frame, new_face_location)
            )

        return raw_face_landmarks

    def face_encodings(
        self,
        deep_learning_model: int,
        resized_frame: npt.NDArray[np.uint8],
        # Initial value of 'face_location_list' is '[]'.
        face_location_list: List = [],
        num_jitters: int = 0,
        model: str = "small"
    ) -> List[np.ndarray]:
        """Given an image, return the 128-dimension face encoding for each face in the image.

        Args:
            resized_frame (npt.NDArray[np.uint8]): The image that contains one or more faces (=small_frame)
            face_location_list (List): Optional - the bounding boxes of each face if you already know them. (=face_location_list)
            num_jitters (int): How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
            model (str): Do not modify.

        Returns:
            List[npt.NDArray[np.float64]]: A list of 128-dimensional face encodings (one for each face in the image).

            If `deep_learning_model == 1`, the returned list contains 512-dimensional face encodings, with the type
            `List[npt.NDArray[np.float32]]`.

            Image size: The image should be of size 150x150. Also, cropping must be done as `dlib.get_face_chip` would do it.
            That is, centered and scaled essentially the same way.

        See also:
            `class dlib.face_recognition_model_v1: compute_face_descriptor(*args, **kwargs)`:
            http://dlib.net/python/index.html#dlib_pybind11.face_recognition_model_v1

            `compute_face_descriptor(*args, **kwargs)`:
            http://dlib.net/python/index.html#dlib_pybind11.face_recognition_model_v1.compute_face_descriptor
        """
        self.deep_learning_model: int = deep_learning_model
        self.face_encodings_resized_frame: npt.NDArray[np.uint8] = resized_frame
        self.face_location_list: List = face_location_list
        self.num_jitters: int = num_jitters
        self.face_encodings_model: str = model
        _PADDING: float = 0.25  # dlib学習モデル用
        face_encodings: List[npt.NDArray[np.float64]] = []

        if len(self.face_location_list) > 0:
            raw_face_landmarks: List = self._return_raw_face_landmarks(
                self.face_encodings_resized_frame,
                self.face_location_list,
                self.face_encodings_model
            )

            raw_face_landmark: dlib.full_object_detection  # type: ignore
            face_landmark_ndarray: npt.NDArray[np.float64] = np.array([])
            if self.deep_learning_model == 0:
                for raw_face_landmark in raw_face_landmarks:
                    # face_landmark_ndarray: npt.NDArray[np.float64] = []
                    face_landmark_ndarray: npt.NDArray[np.float64] = np.array(
                        # Make 128 dimensional vector
                        self.dlib_resnet_face_encoder.compute_face_descriptor(
                            self.face_encodings_resized_frame,
                            raw_face_landmark,
                            self.num_jitters,
                            _PADDING
                        )
                    )
                    face_encodings.append(face_landmark_ndarray)
            elif self.deep_learning_model == 1:
                for raw_face_landmark in raw_face_landmarks:
                    # faces = dlib.full_object_detections()  # type: ignore
                    # Make 512 dimensional vector
                    face_landmark_ndarray: npt.NDArray[np.float64] = np.array(
                        self.JAPANESE_FACE_V1_model_compute_face_descriptor(
                            self.face_encodings_resized_frame,
                            raw_face_landmark,
                            size=224,
                            _PADDING=0.1
                        )
                    )
                face_encodings.append(face_landmark_ndarray)

        return face_encodings
        """
        [compute_face_descriptor](https://blog.dlib.net/2017/02/high-quality-face-recognition-with-deep.html?m=0&commentPage=2)
        Davis King said...
        The landmarks are only used to align the face before the DNN extracts
        the face descriptor. How many landmarks you use doesn't really matter.
        """

        # TODO: #27 Padding around faces, 0.25
        # return [np.array(self.dlib_resnet_face_encoder.compute_face_descriptor(self.face_encodings_resized_frame, raw_landmark_set, self.num_jitters, 0.25)) for raw_landmark_set in raw_landmarks]
        # 4th value (0.25) is padding around the face. If padding == 0 then the chip will
        # be closely cropped around the face. Setting larger padding values will result a looser cropping.
        # In particular, a padding of 0.5 would double the width of the cropped area, a value of 1.
        # would triple it, and so forth.
        # see bellow
        # http://dlib.net/face_recognition.py.html
        """マルチスレッド化
        pool = ThreadPoolExecutor()
        # pool = ProcessPoolExecutor(max_workers=1)  # Error while calling cudaGetDevice(&the_device_id) in file /tmp/pip-install-983gqknr/dlib_66282e4ffadf4aa6965801c6f7ff7671/dlib/cuda/gpu_data.cpp:204. code: 3, reason: initialization error
        return [pool.submit(multithread, raw_landmark_set, self.face_encodings_resized_frame, self.num_jitters).result() for raw_landmark_set in raw_landmarks]
        """

    def face_distance(
        self,
        face_encodings: List[npt.NDArray[np.float64]],
        face_to_compare: npt.NDArray[np.float64]
        # face_encodings: List[np.ndarray],
        # face_to_compare: np.ndarray
    ) -> npt.NDArray[np.float64]:
        """与えられた顔エンコーディングのリストを既知の顔エンコーディングと比較し、各比較顔のユークリッド距離を返します.

        距離が近ければ、顔がどれだけ似ているかが分かります。

        Args:
            face_encodings (List[npt.NDArray[np.float64]]): List of face encodings to compare (=small_frame)
            face_to_compare (npt.NDArray[np.float64]): A face encoding to compare against (=face_location_list)

        Returns:
            npt.NDArray[np.float64]: 顔（名前）配列と同じ順序の、顔同士の距離である numpy ndarray を返します
        """
        # self.face_encodings = face_encodings
        # self.face_to_compare = face_to_compare

        if len(face_encodings) == 0:
            # return `dummy data`
            return np.empty((2, 2, 3), dtype=np.float64)

        # ord = None -> Frobenius norm. norm for vectors is '2-norm'.
        # See:
        # document: https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html
        # [全成分の二乗和のルートをフロベニウスノルムと言います。](https://manabitimes.jp/math/1284)
        # > フロベニウスノルムは，行列の全成分を一列に並べてベクトルとみなしたときのベクトルの長さ（2ノルム）と考えることもできます。
        return np.linalg.norm(x=(face_encodings - face_to_compare), axis=1)

    def cosine_similarity(self, embedding1, embedding2, threshold=0.4):
        """
        cosine_similarity 特徴量ベクトルを受け取り、類似度を計算し、閾値を超えているかどうかを返す

        Args:
            embedding1 (npt.NDArray): feature vector
            embedding2 (npt.NDArray): feature vector
            threshold (float, optional): threshold. Defaults to 0.4.

        Returns:
            Tuple[np.array, float]: Returns a tuple of a numpy array of booleans and the minimum cos_sim
        """
        results: List[Tuple[bool, float]] = []
        max_cos_sim = float(0.0)
        embedding2 = embedding2.flatten()
        for emb1 in embedding1:
            emb1 = emb1.flatten()
            cos_sim: float = np.dot(
                emb1, embedding2) / (np.linalg.norm(emb1) * np.linalg.norm(embedding2))
            if cos_sim >= threshold:
                results.append((True, cos_sim))
            else:
                results.append((False, cos_sim))
            max_cos_sim = max(max_cos_sim, cos_sim)
        return results, max_cos_sim
        # for emb1 in embedding1:
        #     emb1 = emb1.flatten()
        #     cos_sim = np.dot(emb1, embedding2) / (np.linalg.norm(emb1) * np.linalg.norm(embedding2))
        #     results.append(cos_sim >= threshold)
        #     max_cos_sim= max(max_cos_sim, cos_sim)
        # return np.array(results), max_cos_sim

    # Percentage calculation

    def percentage(self, cos_sim):
        """
        percentage 与えられた cos_sim から類似度を計算する

        Args:
            cos_sim (float): cosine similarity

        Returns:
            float: percentage of similarity
        """
        # BUG: Issue #25
        return round(-23.71 * cos_sim ** 2 + 49.98 * cos_sim + 73.69, 2)

    def compare_faces(
        self,
        deep_learning_model: int,
        known_face_encodings: List[npt.NDArray[np.float64]],
        face_encoding_to_check: npt.NDArray[np.float64],
        tolerance: float = 0.6,
        threshold: float = 0.4
    ) -> Tuple[np.ndarray, float]:
        """顔エンコーディングのリストを候補エンコーディングと比較して、それらが一致するかどうかを確認します。

        Args:
            deep_learning_model (int): 0: dlib cnn model, 1: JAPANESE_FACE_V1.onnx
            known_face_encodings (List[npt.NDArray[np.float64]]): known face encodingsのリスト
            face_encoding_to_check (npt.NDArray[np.float64]): リストに対して比較する、単一の顔エンコーディング
            tolerance (float): 顔間の距離がどのくらいあれば一致するとみなされるか。dlibの場合、低いほど厳密で、0.6 が一般的な値です。
            threshold (float): 閾値

        Returns:
            どの known_face_encoding がチェック対象の顔エンコーディングに一致するか、およびそれらの間の最小距離を示す True/False 値のタプル。
        """
        self.deep_learning_model: int = deep_learning_model
        self.known_face_encodings: List[npt.NDArray[np.float64]] = known_face_encodings
        self.face_encoding_to_check: npt.NDArray[np.float64] = face_encoding_to_check
        self.tolerance: float = tolerance
        self.threshold: float = threshold

        if self.deep_learning_model == 0:
            face_distance_list: List[float] = list(
                self.face_distance(
                    self.known_face_encodings,
                    self.face_encoding_to_check
                )
            )

            self.min_distance: float = min(face_distance_list)

            if self.min_distance > self.tolerance:
                # All elements are 'False' if 'self.min_distance' is greater than 'self.tolerance'.
                # return [False] * len(face_distance_list)
                return np.full(len(face_distance_list), False), self.min_distance
            else:
                bool_list: List[Tuple[bool, float]] = []
                for face_distance in face_distance_list:
                    if self.tolerance >= face_distance:
                        bool_list.append((True, face_distance))
                    else:
                        bool_list.append((False, face_distance))
                return np.array(bool_list), self.min_distance
                # bool_list: List[bool] = []
                #     if self.tolerance >= face_distance:
                #         bool_list.append(True)
                #     else:
                #         bool_list.append(False)
                # return np.array(bool_list), self.min_distance

        elif self.deep_learning_model == 1:
            results: List[Tuple[bool, float]] = []
            results, max_cos_sim = \
                self.cosine_similarity(
                    self.known_face_encodings, self.face_encoding_to_check, self.threshold)
            return np.array(results), max_cos_sim
