"""Reference.

- Data structure:
    - Definition of person_data_list and frame_datas_array:
        - overlay (npt.NDArray[np.uint8]): Copy of frame
        - face_location_list (List[Tuple[int,int,int,int]]): List of face_location
        - name (str): Each of person's name
        - filename (str): File name
        - percentage_and_symbol (str): Concatenate of digit of percentage and '%' symbol
        - person_data_list (List): List of person_data
        - frame_datas_array (List[Dict]): Array of frame_datas
        - resized_frame (npt.NDArray[np.uint8]): Numpy array of frame

        >>> person_data = {
                'name': name,
                'pict':filename,
                'date': date,
                'location': (top,right,bottom,left),
                'percentage_and_symbol': percentage_and_symbol
            }
        >>> person_data_list.append(person_data)

        >>> frame_datas = {
                'img': resized_frame,
                'face_location_list': face_location_list,
                'overlay': overlay,
                'person_data_list': person_data_list
            }
        >>> frame_datas_array.append(frame_datas)

- About coordinate order:
    - dlib: (Left, Top, Right, Bottom,)
    - Dlib_api(): (top, right, bottom, left)
    - see bellow
        - https://github.com/davisking/dlib/blob/master/python_examples/faceapi.py

- References:
    - About usage of 'cython':
        - see bellow
            - https://www.youtube.com/watch?app=desktop&v=sGggkVaRMzY

    - About mediapipe for python:
        - see bellow
            - https://github.com/google/mediapipe/tree/master/mediapipe/python
            - https://solutions.mediapipe.dev/face_detection#python-solution-api

    - About anti spoof function:
        - model
            - Original model create by Prokofev Kirill, modified by PINT
        - URL
            - https://github.com/PINTO0309/PINTO_model_zoo/tree/main/191_anti-spoof-mn3

"""


# from __future__ import annotations


import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from os.path import exists
from platform import system
from shutil import move
from traceback import format_exc
from typing import Dict, Generator, List, Tuple, Union

import cv2
import mediapipe as mp
import mojimoji
import numpy as np
import numpy.typing as npt  # See [](https://discuss.python.org/t/how-to-type-annotate-mathematical-operations-that-supports-built-in-numerics-collections-and-numpy-arrays/13509)
import onnxruntime as ort
# from memory_profiler import profile  # @profile()
from PIL import Image, ImageDraw, ImageFile, ImageFont

from face01lib.api import Dlib_api
from face01lib.Calc import Cal
from face01lib.logger import Logger
from face01lib.models import Models
from face01lib.return_face_image import Return_face_image
from face01lib.video_capture import VidCap

Cal_obj = Cal()
VidCap_obj = VidCap()
Dlib_api_obj = Dlib_api()
Return_face_image_obj = Return_face_image()

ImageFile.LOAD_TRUNCATED_IMAGES = True


anti_spoof_model: str = Models().anti_spoof_model_location()

# mediapipeのスパムログ出力を抑制 ####################
os.environ['GLOG_minloglevel'] = '3'  # 3: FATAL (致命的なエラー)
# ログレベルをERRORに設定 (INFOやDEBUGより低いレベルのログが出力されなくなる)
# mp.logging_util.set_verbosity(mp.logging_util.ERROR)  # mediapipe v0.10.14では未対応
# ####################################################


class Core:
    """Coreクラス.

    このクラスは多くの有用なメソッドを含みます。
    """

    def __init__(self, log_level: str = 'info') -> None:
        """init.

        Args:
            log_level (str, optional): ログレベルを受け取ります。デフォルトは`info`です。
        """
        # Setup logger: common way
        self.log_level: str = log_level
        import os.path
        name: str = __name__
        dir: str = os.path.dirname(__file__)
        parent_dir, _ = os.path.split(dir)
        self.logger = Logger(self.log_level).logger(name, parent_dir)

        # Cal_obj.cal_specify_date(self.logger)  # 日付による動作停止処理は廃止

    # @profile()
    def mp_face_detection_func(
        self,
        resized_frame: npt.NDArray[np.uint8],
        model_selection: int = 0,
        min_detection_confidence: float = 0.4
    ):
        """RGBイメージを処理し、mediapipeを使って算出したface locationデータを返します.

        Args:
            resized_frame (npt.NDArray[np.uint8]): Resized image frame
            model_selection (int, optional): Value set in config.ini.  Defaults to 0.
            min_detection_confidence (float, optional): Value set in config.ini. Defaults to 0.4.

        Returns:
            A NamedTuple object with a "detections" field that contains a list of the
            detected face location data.

        Refer:
            https://solutions.mediapipe.dev/face_detection#python-solution-api

        Note:
            number_of_people and same_time_recognize in config.ini are disabled when using mp_face_detection_func.
        """
        self.resized_frame: npt.NDArray[np.uint8] = resized_frame
        self.model_selection: Tuple[int] = model_selection,
        self.min_detection_confidence: float = min_detection_confidence

        """DEBUG
        VidCap().frame_imshow_for_debug(self.resized_frame)
        print(type(self.resized_frame))
        """

        # method 1
        # mp_face_detection = mp.solutions.face_detection
        # with mp_face_detection.FaceDetection(
        #     self.model_selection[0],
        #     self.min_detection_confidence
        # ) as face_detection:
        #     results = face_detection.process(self.resized_frame)

        # method 2
        f = mp.solutions.face_detection.FaceDetection(
            self.model_selection[0],
            self.min_detection_confidence
        )

        results = f.process(self.resized_frame)
        f.close()

        """DEBUG
        if not results.detections:
            exit(0)
        """

        """リファレンス

        https://solutions.mediapipe.dev/face_detection#python-solution-api

        Processes an RGB image and returns a list of the detected face location data.

        Args:
            image: An RGB image represented as a numpy ndarray.
        Raises:
            RuntimeError: If the underlying graph throws any error.
        ValueError:
            If the input image is not three channel RGB.
        Returns:
            A NamedTuple object with a "detections" field that contains a list of the
            detected face location data.'
        """
        return results

    # @profile()
    def _return_face_location_list(
        self,
        resized_frame: npt.NDArray[np.uint8],
        set_width: int,
        set_height: int,
        model_selection: int,
        min_detection_confidence: float,
        same_time_recognize: int = 2
    ) -> List[Tuple[int, int, int, int]]:
        self.face_location_list_resized_frame: npt.NDArray[np.uint8] = resized_frame
        self.set_width: int = set_width
        self.set_height: int = set_height
        self.face_location_list_model_selection: int = model_selection
        self.min_detection_confidence = min_detection_confidence
        self.same_time_recognize: int = same_time_recognize

        self.face_location_list_resized_frame.flags.writeable = False
        face_location_list: List = []
        # person_frame = np.empty((2,0), dtype = np.float64)
        # date = datetime.now().strftime("%Y,%m,%d,%H,%M,%S,%f")

        # VidCap().frame_imshow_for_debug(self.face_location_list_resized_frame)

        results = \
            self.mp_face_detection_func(
                self.face_location_list_resized_frame,
                self.face_location_list_model_selection,
                self.min_detection_confidence
            )
        if not results.detections:
            return []  # face_location_list
        else:
            # n: int = 0
            """TODO:
            なぜresults.detectionsは大きな数なのか？
            results.detectionは顔パーツそれぞれのデータを持つ可能性
            →use_pipe = Trueの時はperson_frame_face_encodingとnumber_of_peopleは無効になる旨、ドキュメントに書いておきます。
            """

            for detection in results.detections:
                # if n >= 1:
                # # if n >= self.same_time_recognize:
                #     break
                xleft: int = int(
                    detection.location_data.relative_bounding_box.xmin * self.set_width)
                xtop: int = int(
                    detection.location_data.relative_bounding_box.ymin * self.set_height)
                xright: int = int(
                    detection.location_data.relative_bounding_box.width * self.set_width + xleft)
                xbottom: int = int(
                    detection.location_data.relative_bounding_box.height * self.set_height + xtop)
                # see bellow
                # https://stackoverflow.com/questions/71094744/how-to-crop-face-detected-via-mediapipe-in-python

                if xleft <= 0 or xtop <= 0:  # xleft or xtop がマイナスになる場合があるとバグる
                    continue
                face_location_list.append(
                    (xtop, xright, xbottom, xleft))  # Dlib_api() order
                # n += 1

        self.resized_frame.flags.writeable = True
        return face_location_list

    # @profile()

    def _draw_telop(
        self,
        logger,
        cal_resized_telop_nums: Tuple[int, int, int, int, npt.NDArray[np.float64], npt.NDArray[np.float64]],
        frame: npt.NDArray[np.uint8]
    ) -> npt.NDArray[np.uint8]:
        self.logger = logger
        self.cal_resized_telop_nums: Tuple[int, int, int, int,
                                           npt.NDArray[np.float64], npt.NDArray[np.float64]] = cal_resized_telop_nums
        self.frame: npt.NDArray[np.uint8] = frame
        x1: int
        y1: int
        x2: int
        y2: int
        a: npt.NDArray[np.float64]
        b: npt.NDArray[np.float64]
        x1, y1, x2, y2, a, b = self.cal_resized_telop_nums
        frame_view: npt.NDArray[np.uint8] = self.frame.view(
            dtype=np.uint8, type=np.ndarray)
        try:
            # TODO: #21 numpyのfunctionを探す
            # https://numpy.org/devdocs/reference/arrays.indexing.html
            frame[y1:y2, x1:x2] = self.frame[y1:y2, x1:x2] * a + b
            # frame[:,y1:y2, x1:x2] = frame_view[:,y1:y2, x1:x2] * a + b

        except:
            self.logger.debug("cannot draw telop image")
            # TODO np.clip
        return frame

    # @profile()

    def _draw_logo(
        self,
        logger,
        cal_resized_logo_nums: Tuple[int, int, int, int, npt.NDArray[np.float64], npt.NDArray[np.float64]],
        frame: npt.NDArray[np.uint8]
    ) -> npt.NDArray[np.uint8]:
        self.logger = logger
        self.cal_resized_logo_nums: Tuple[int, int, int, int,
                                          npt.NDArray[np.float64], npt.NDArray[np.float64]] = cal_resized_logo_nums
        self.frame: npt.NDArray[np.uint8] = frame
        x1: int
        y1: int
        x2: int
        y2: int
        a: npt.NDArray[np.float64]
        b: npt.NDArray[np.float64]
        x1, y1, x2, y2, a, b = self.cal_resized_logo_nums
        try:
            frame[y1:y2, x1:x2] = self.frame[y1:y2, x1:x2] * a + b
        except:
            self.logger.debug("logoが描画できません")
            # TODO np.clip
        return frame

    # @profile()

    def _check_compare_faces(
        self,
        logger,
        deep_learning_model: int,
        known_face_encodings: List[npt.NDArray[np.float64]],
        face_encoding: npt.NDArray[np.float64],
        tolerance: float
    ) -> Tuple[npt.NDArray[np.bool8], float]:
        """dlib_apiを用いてmatchリストとmin valueを返します.

        Args:
            logger (_type_): logger
            known_face_encodings (List[npt.NDArray[np.float64]]): known face encodesリスト
            face_encoding (npt.NDArray[np.float64]): 比較されるFace encoding data
            tolerance (float): tolerance値

        Returns:
            Tuple[npt.NDArray[np.bool8], float]: match list, min value
        """
        self.logger = logger
        self.deep_learning_model: int = deep_learning_model
        self.known_face_encodings: List[npt.NDArray[np.float64]
                                        ] = known_face_encodings
        self.face_encoding: npt.NDArray[np.float64] = face_encoding
        self.tolerance: float = tolerance
        self.threshold: float = Cal_obj.to_tolerance(
            self.CONFIG["similar_percentage"], self.CONFIG["deep_learning_model"])
        try:
            matches: npt.NDArray[np.bool8]
            min_distance: float
            matches, min_distance =\
                Dlib_api_obj.compare_faces(
                    self.deep_learning_model,
                    self.known_face_encodings,
                    self.face_encoding,
                    self.tolerance,
                    self.threshold
                )
            return matches, min_distance
        except:
            self.logger.error("DEBUG: npKnown.npzが壊れているか予期しないエラーが発生しました。")
            self.logger.error(
                "npKnown.npzの自動削除は行われません。原因を特定の上、必要な場合npKnown.npzを削除して下さい。")
            self.logger.error("処理を終了します。FACE01を再起動して下さい。")
            self.logger.error("以下のエラーをシステム管理者様へお伝えください")
            self.logger.error("-" * 20)
            self.logger.error(format_exc(limit=None, chain=True))
            self.logger.error("-" * 20)
            exit(0)

    # @profile()

    def make_frame_datas_array(
        self,
        overlay: npt.NDArray[np.uint8],
        face_location_list: List[Tuple[int, int, int, int]],
        name: str,
        filename: str,
        percentage_and_symbol: str,
        person_data_list: List,
        frame_datas_array: List[Dict],
        resized_frame: npt.NDArray[np.uint8]
    ) -> List[Dict]:
        """Method to make frame_datas_array.

        Return the data structure of frame_datas_list.

        Args:
            overlay (npt.NDArray[np.uint8]): Copy of frame
            face_location_list (List[Tuple[int,int,int,int]]): List of face_location
            name (str): Each of person's name
            filename (str): File name
            percentage_and_symbol (str): Concatenate of digit of percentage and '%' symbol
            person_data_list (List): List of person_data
            frame_datas_array (List[Dict]): Array of frame_datas
            resized_frame (npt.NDArray[np.uint8]): Numpy array of frame

        Returns:
            List[Dict]: List of frame_datas_array

        Example:
            person_data

            >>> {
                'name': name,
                'pict': filename,
                'date': date,
                'location': (top,right,bottom,left),
                'percentage_and_symbol': percentage_and_symbol
            }

            person_data_list

            >>> person_data_list.append(person_data)

            frame_datas

            >>> {
                'img': resized_frame,
                'face_location_list': face_location_list,
                'overlay': overlay,
                'person_data_list': person_data_list
            }

            frame_datas_list

            >>> frame_datas_array.append(frame_datas)
        """
        self.overlay: npt.NDArray[np.uint8] = overlay
        self.face_location_list: List[Tuple[int,
                                            int, int, int]] = face_location_list
        self.name: str = name
        self.filename: str = filename
        self.percentage_and_symbol: str = percentage_and_symbol
        self.person_data_list: List = person_data_list
        self.frame_datas_array: List[Dict] = frame_datas_array

        self.make_frame_datas_array_resized_frame: npt.NDArray[np.uint8] = resized_frame
        if len(face_location_list) > 0:
            for face_location in face_location_list:
                # person_data = {'spoof_dict':{}, 'name': self.name, 'pict':self.filename,  'date':date, 'location':face_location, 'percentage_and_symbol': self.percentage_and_symbol}
                # self.person_data_list.append(person_data)
                frame_datas = {
                    'img': self.make_frame_datas_array_resized_frame,
                    'face_location_list': self.face_location_list,
                    'overlay': self.overlay,
                    'person_data_list': self.person_data_list
                }
                self.frame_datas_array.append(frame_datas)
        else:
            frame_datas = {
                'img': self.make_frame_datas_array_resized_frame,
                'face_location_list': self.face_location_list,
                'overlay': self.overlay,
                'person_data_list': self.person_data_list
            }
            self.frame_datas_array.append(frame_datas)

        """DEBUG
        logger.debug(f'frame_datas_array size: {len(self.frame_datas_array)}')
        logger.debug(inspect.currentframe().f_back.f_code.co_filename)
        logger.debug(inspect.currentframe().f_back.f_lineno)
        """

        return self.frame_datas_array

    # pil_img_rgbオブジェクトを生成
    # @profile()

    def _pil_img_rgb_instance(self, frame):
        self.frame = frame
        pil_img_obj_rgb = Image.fromarray(
            cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA))
        return pil_img_obj_rgb

    # 顔部分の領域をクロップ画像ファイルとして出力
    # @profile()
    def _make_crop_face_image(
        self,
        anti_spoof,
        name,
        dis,
        pil_img_obj_rgb,
        top,
        left,
        right,
        bottom,
        number_of_crops,
        frequency_crop_image
    ):
        self.anti_spoof = anti_spoof
        self.name = name
        self.dis = dis
        self.pil_img_obj_rgb = pil_img_obj_rgb
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom
        self.number_of_crops = number_of_crops
        self.frequency_crop_image = frequency_crop_image
        date = datetime.now().strftime("%Y,%m,%d,%H,%M,%S,%f")
        # TODO: CROPする時の余白を設定可能にする
        margin = 50
        imgCroped = \
            self.pil_img_obj_rgb.crop(
                (self.left - margin, self.top - margin, self.right + margin, self.bottom + margin)).resize((400, 400)
                                                                                                           )
        # TODO: outputのファイル名にanti_spoof結果を入れる
        if self.anti_spoof is True:
            filename = "output/%s_%s_%s.png" % (self.name, date, self.dis)
        else:
            filename = "output/%s_%s_%s.png" % (self.name, date, self.dis)
        imgCroped.save(filename)
        return filename, self.number_of_crops, self.frequency_crop_image

    # @profile()

    def _return_face_name(
        self,
        CONFIG: Dict,
        matches: npt.NDArray[np.bool8],
        min_distance: float
    ) -> str:
        """Get face_name.

        Args:
            CONFIG (Dict): CONFIG
            matches (npt.NDArray[np.bool8]): List of bool value
            min_distance (float): min value

        Returns:
            str: Name who is.
        """
        self.CONFIG = CONFIG
        self.matches = matches
        self.min_distance = min_distance

        if self.CONFIG["deep_learning_model"] == 0:
            # アレイ中のインデックスからknown_face_names中の同インデックスの要素を算出
            # index: int = np.where(matches is True)[0][0]  # bug: Trueが複数ある場合、最初の要素が取得されてしまう。
            #
            # matches配列において、最初の列が1である行の中から、2番目の列の値が最も小さい行を見つける
            # 最小値のインデックスを取得
            min_index = np.argmin(matches[matches[:, 0] == 1, 1])
            # 最小値を持つ行のインデックスを求める
            rows_with_1 = np.where(matches[:, 0] == 1)[0]
            index = rows_with_1[min_index]
            file_name: str = str(
                CONFIG["known_face_names"][index]) + ':' + str(min_distance)

            return file_name
        elif self.CONFIG["deep_learning_model"] == 1:
            # matches配列において、最初の列が1である行の中から、2番目の列の値が最も大きい行を見つける
            # 最大値のインデックスを取得
            max_index = np.argmax(matches[matches[:, 0] == 1, 1])
            # 最大値を持つ行のインデックスを求める
            rows_with_1 = np.where(matches[:, 0] == 1)[0]
            index = rows_with_1[max_index]
            file_name: str = str(
                CONFIG["known_face_names"][index]) + ':' + str(min_distance)
            return file_name

    # @profile()
    def return_concatenate_location_and_frame(
        self,
        resized_frame: npt.NDArray[np.uint8],
        face_location_list: List[Tuple[int, int, int, int]]
    ) -> Tuple[List[Tuple[int, int, int, int]], npt.NDArray[np.uint8]]:
        """Return tuple.

        - concatenate_face_location_list
        - concatenate_person_frame

        Args:
            resized_frame (npt.NDArray[np.uint8]): Resized frame
            face_location_list (List[Tuple[int,int,int,int]]): Face location list

        Returns:
            concatenate_face_location_list (Tuple[List[Tuple[int,int,int,int]])
                List of concatenated coordinates
            concatenate_person_frame (npt.NDArray[np.uint8]])
                Image data of concatenated person image data
        """
        self.return_concatenate_location_and_frame_resized_frame: npt.NDArray[
            np.uint8] = resized_frame
        self.face_location_list = face_location_list

        """face_location_listはresized_frame上の顔座標"""
        finally_height_size: int = 150
        concatenate_face_location_list: List[Tuple[int, int, int, int]] = []
        detection_counter: int = 0
        person_frame_list: List[npt.NDArray[np.uint8]] = []

        concatenate_person_frame: npt.NDArray[np.uint8] = np.empty(
            (2, 2, 3), dtype=np.uint8)

        for xtop, xright, xbottom, xleft in self.face_location_list:
            person_frame: npt.NDArray[np.uint8] = \
                self.return_concatenate_location_and_frame_resized_frame[xtop:xbottom, xleft:xright]

            # person_frameをリサイズする
            height: int = xbottom - xtop
            width: int = xright - xleft
            # 拡大・縮小率を算出
            fy: float = finally_height_size / height
            finally_width_size: int = int(width * fy)

            resized_person_frame: cv2.Mat = \
                cv2.resize(person_frame, dsize=(finally_width_size, finally_height_size))
            person_frame_list.append(resized_person_frame)  # type: ignore
            """DEBUG
            cv2.imshow("DEBUG", person_frame)
            cv2.waitKey(5000)
            cv2.destroyAllWindows()
            """

            # 拡大率に合わせて各座標を再計算する
            # person_frame上の各座標
            person_frame_xtop: int = 0
            person_frame_xright: int = finally_width_size
            person_frame_xbottom: int = finally_height_size
            person_frame_xleft: int = 0
            # 連結されたperson_frame上の各座標
            concatenated_xtop: int = person_frame_xtop
            concatenated_xright: int = person_frame_xright + \
                (finally_width_size * detection_counter)
            concatenated_xbottom: int = person_frame_xbottom
            concatenated_xleft: int = person_frame_xleft + \
                (finally_width_size * detection_counter)

            concatenate_face_location_list.append(
                (concatenated_xtop, concatenated_xright, concatenated_xbottom, concatenated_xleft))  # Dlib_api() order
            detection_counter += 1
            """about coordinate order
            dlib: (Left, Top, Right, Bottom,)
            Dlib_api(): (top, right, bottom, left)
            see bellow
            https://github.com/davisking/dlib/blob/master/python_examples/faceapi.py
            """

            concatenate_person_frame = np.hstack(person_frame_list)
            """DEBUG
            cv2.imshow("face_encodings", concatenate_person_frame)
            cv2.moveWindow("face_encodings", 800,600)
            cv2.waitKey(500)
            cv2.destroyAllWindows()
            exit(0)
            print("---------------------------------")
            print(f'concatenate_face_location_list: {concatenate_face_location_list}')
            print("---------------------------------")
            """
        return concatenate_face_location_list, concatenate_person_frame

    # フレーム前処理
    # @profile()
    def frame_pre_processing(
        self,
        logger,
        CONFIG: Dict,
        resized_frame: npt.NDArray[np.uint8]
    ) -> List[Dict]:
        """Return `frame_datas_array`.

        Args:
            logger (_type_): logger
            CONFIG (Dict): Dict of Initial settings
            resized_frame (npt.NDArray[np.uint8]): Resized frame

        Returns:
            List[Dict]: `frame_datas_array`

        Processing:
            - If CONFIG["headless"] is False
                - copy frame data for `overlay`
                - composite `telop` and `logo`
            - Compute face coordinates
            - Make `frame_datas`
                - `img`
                - `face_location_list`
                - `overlay`
                    - If `CONFIG["headless"] is True`, insert `dummy data`
                        -  np.empty((2,2,3), dtype=np.uint8)
                - `person_data_list`
            - Make `frame_datas_array`
                - frame_datas_array.append(frame_datas)

        Data structure of `frame_datas_array`:
            - `overlay` (npt.NDArray[np.uint8])
            - `face_location_list` (List[Tuple[int,int,int,int]])
            - `name` (str)
            - `filename` (str)
            - `percentage_and_symbol` (str)
            - `person_data_list` (List)
            - `frame_datas_array` (List[Dict])
            - `resized_frame` (npt.NDArray[np.uint8])

            See `Core.make_frame_datas_array()`

        Example:
            >>> exec_times = 2
            # Initialize
            CONFIG: Dict =  Initialize('FACE-COORDINATE', 'info').initialize()
            # Make generator
            frame_generator_obj = VidCap().frame_generator(CONFIG)
            # Make logger
            import os.path
            dir: str = os.path.dirname(__file__)
            log = Logger().logger(__file__, dir)
            # Make generator
            core = Core()
            # Repeat 'exec_times' times
            for i in range(0, exec_times):
                # Call __next__() from the generator object
                resized_frame = frame_generator_obj.__next__()
                frame_datas_array = core.frame_pre_processing(log, CONFIG,resized_frame)
        """
        self.logger = logger
        self.CONFIG: Dict = CONFIG
        self.resized_frame: npt.NDArray[np.uint8] = resized_frame

        person_data_list: List[Dict] = []
        name: str = 'Unknown'
        filename: str = ''
        frame_datas_array: List[Dict] = []
        face_location_list: List[Tuple[int, int, int, int]] = []
        percentage_and_symbol: str = ''
        overlay: npt.NDArray[np.uint8] = np.empty(
            (2, 2, 3), dtype=np.uint8)  # Dummy data

        # 描画系（bottom area, 半透明, telop, logo）
        if self.CONFIG["headless"] is False:
            # 半透明処理（前半）
            if self.CONFIG["show_overlay"] is True:
                overlay = self.resized_frame.copy()
                """DEBUG: Memory leak"""

            # テロップとロゴマークの合成
            if self.CONFIG["draw_telop_and_logo"] is True:

                self.resized_frame = \
                    self._draw_telop(
                        self.logger,
                        self.CONFIG["cal_resized_telop_nums"],
                        self.resized_frame
                    )

                self.resized_frame = \
                    self._draw_logo(
                        self.logger,
                        self.CONFIG["cal_resized_logo_nums"],
                        self.resized_frame
                    )

        # 顔座標算出
        if self.CONFIG["use_pipe"] is True:
            face_location_list = \
                self._return_face_location_list(
                    self.resized_frame,
                    self.CONFIG["set_width"],
                    self.CONFIG["set_height"],
                    self.CONFIG["model_selection"],
                    self.CONFIG["min_detection_confidence"],
                    self.CONFIG["same_time_recognize"]
                )
        else:
            # date: str = datetime.now().strftime("%Y,%m,%d,%H,%M,%S,%f")  # Not use
            face_location_list: List[Tuple[int, int, int, int]] = \
                Dlib_api_obj.face_locations(
                # Dlib_api_obj.face_locations(
                    self.resized_frame,
                    self.CONFIG["upsampling"],
                    self.CONFIG["mode"]
            )

        # 顔がなかったら以降のエンコード処理を行わない
        if len(face_location_list) == 0:
            frame_datas_array: List[Dict] = \
                self.make_frame_datas_array(
                    overlay,
                    face_location_list,
                    name,
                    filename,
                    percentage_and_symbol,
                    person_data_list,
                    frame_datas_array,
                    self.resized_frame
            )
            return frame_datas_array

        # 顔が一定数以上なら以降の処理を行わない
        if len(face_location_list) >= self.CONFIG["number_of_people"]:
            self.logger.info(f'{self.CONFIG["number_of_people"]}人以上を検出しました')
            frame_datas_array = \
                self.make_frame_datas_array(
                    overlay,
                    face_location_list,
                    name,
                    filename,
                    percentage_and_symbol,
                    person_data_list,
                    frame_datas_array,
                    self.resized_frame
                )
            return frame_datas_array

        frame_datas: Dict = {
            'img': self.resized_frame,
            'face_location_list': face_location_list,
            'overlay': overlay,
            'person_data_list': person_data_list
        }

        # frame_datas_array.extend(frame_datas)
        frame_datas_array.append(frame_datas)

        return frame_datas_array

    # 顔のエンコーディング
    # @profile()
    # @Cal_obj.Measure_func

    def face_encoding_process(
        self,
        logger,
        CONFIG: Dict,
        frame_datas_array: List[Dict]
    ) -> Tuple[List[npt.NDArray[np.float64]], List[Dict]]:
        """Encode face data and Return bellow.

        - list of encoded data
        - frame_datas_array

        Args:
            logger (_type_): logger
            CONFIG (Dict): Dict including initial setting
            frame_datas_array (List[Dict]): frame datas

        Returns:
            - list of encoded data
                - Tuple[List[npt.NDArray[np.float64]]
            - frame_datas_array
                - List[Dict]]

        Definition of person_data_list and frame_datas_array:
            >>> person_data = {
                    'name': name,
                    'pict':filename,
                    'date':date,
                    'location':(top,right,bottom,left),
                    'percentage_and_symbol': percentage_and_symbol
                }
            >>> person_data_list.append(person_data)

            >>> frame_datas = {
                    'img': resized_frame,
                    'face_location_list': face_location_list,
                    'overlay': overlay,
                    'person_data_list': person_data_list
                }
            >>> frame_datas_array.append(frame_datas)
        """
        self.logger = logger
        self.CONFIG: Dict = CONFIG
        self.frame_datas_array: List[Dict] = frame_datas_array

        face_encodings: List[npt.NDArray[np.float64]] = []
        # face_encodings_list = []  # Not used.

        for frame_data in self.frame_datas_array:
            resized_frame: npt.NDArray[np.uint8] = frame_data["img"]
            # [(139, 190, 257, 72)]
            face_location_list = frame_data["face_location_list"]

            if len(face_location_list) == 0:  # 顔がない場合
                return face_encodings, self.frame_datas_array
            elif len(face_location_list) > 0:  # 顔がある場合

                # 顔ロケーションからエンコーディングを求める
                if self.CONFIG["use_pipe"] is True and self.CONFIG["person_frame_face_encoding"] is True:
                    """FIX
                    人数分を繰り返し処理しているので時間がかかる。
                    dlibは一つの画像に複数の座標を与えて一度に処理をする。
                    なので各person_frameをくっつけて一つの画像にすれば処理時間は短くなる。
                        numpy.hstack(tup)[source]
                        Stack arrays in sequence horizontally (column wise).
                        https://numpy.org/doc/stable/reference/generated/numpy.hstack.html
                    """

                    concatenate_face_location_list: List[Tuple[int, int, int, int]]
                    concatenate_person_frame: npt.NDArray[np.uint8]

                    concatenate_face_location_list, concatenate_person_frame = \
                        self.return_concatenate_location_and_frame(
                            resized_frame,
                            face_location_list
                        )
                    face_encodings = \
                        Dlib_api_obj.face_encodings(
                            self.CONFIG["deep_learning_model"],
                            concatenate_person_frame,
                            concatenate_face_location_list,
                            self.CONFIG["jitters"],
                            "small"
                        )
                elif self.CONFIG["use_pipe"] is True and self.CONFIG["person_frame_face_encoding"] is False:
                    try:
                        face_encodings = \
                            Dlib_api_obj.face_encodings(
                                self.CONFIG["deep_learning_model"],
                                resized_frame,
                                face_location_list,
                                self.CONFIG["jitters"],
                                "small"
                            )
                        # TODO: #34 use_pipe = TrueとFalseによる'face_encodings'の処理速度の違いを究明する
                        # if face_encodings == []:
                        #     return face_encodings, self.frame_datas_array
                    except Exception as e:
                        self.logger.warning(
                            f'resized_frame: {resized_frame}\nface_location_list:  {face_location_list}')
                        self.logger.warning(f'ERROR: {e}')
                        self.logger.warning(format_exc())
                        exit(0)
                elif self.CONFIG["use_pipe"] is False and self.CONFIG["person_frame_face_encoding"] is True:
                    self.logger.warning("config.ini:")
                    self.logger.warning(
                        "You cannot set person_frame_face_encoding = True if use_pipe = False")
                    self.logger.warning("Change the settings appropriately")
                    self.logger.warning("-" * 20)
                    self.logger.warning(format_exc(limit=None, chain=True))
                    self.logger.warning("-" * 20)
                    exit(0)
                elif self.CONFIG["use_pipe"] is False and self.CONFIG["person_frame_face_encoding"] is False:
                    face_encodings = \
                        Dlib_api_obj.face_encodings(
                            self.CONFIG["deep_learning_model"],
                            resized_frame,
                            face_location_list,
                            self.CONFIG["jitters"],
                            "small"
                        )

                # face_encodings_list = face_encodings_list.append(face_encodings)
        # yield face_encodings, self.frame_datas_array
        return face_encodings, self.frame_datas_array

    # 顔の生データ(np.ndarray)を返す
    """How to slice
    face_location order: top, right, bottom, left
    how to slice: img[top:bottom, left:right]
    """
    # def return_face_image(
    #     self,
    #     resized_frame,
    #     face_location
    # ):
    #     self.resized_frame = resized_frame
    #     empty_ndarray = np.empty(shape=(0,0,0), dtype=np.uint8)

    #     if len(self.face_location) > 0:
    #         top = face_location[0]
    #         right = face_location[1]
    #         bottom = face_location[2]
    #         left = face_location[3]
    #         face_image = self.resized_frame[top:bottom, left:right]
    #         """DEBUG
    #         from .video_capture import VidCap
    #         VidCap().frame_imshow_for_debug(face_image)
    #         VidCap().frame_imshow_for_debug(self.resized_frame)
    #         """
    #         return face_image
    #     else:
    #         return empty_ndarray

    # フレーム後処理
    # @profile()
    def frame_post_processing(
        self,
        logger,
        CONFIG: Dict,
        face_encodings: List[npt.NDArray[np.float64]],
        frame_datas_array: List[Dict]
    ) -> List[Dict]:
        """Modify each frame's datas.

        Args:
            logger (_type_): logger
            CONFIG (Dict): Dict of initial settings
            face_encodings (List[npt.NDArray[np.float64]]): List of encoded face datas
            frame_datas_array (List[Dict]): List of datas

        Returns:
            List[Dict]: List of modified datas

        Modify:
            - Composite images
                - Default face image
                - Rectangle
                - Percentage
                - Name
            - Percentage calculation
            - Save cropped face images
            - Make person_data_list
            - Make frame_datas_list
        """
        self.logger = logger
        self.CONFIG: Dict = CONFIG
        self.face_encodings: List[npt.NDArray[np.float64]] = face_encodings
        self.frame_datas_array: List[Dict] = frame_datas_array
        face_names: List[str] = []
        face_location_list: List[Tuple[int, int, int, int]] = []
        filename: str = ''
        # debug_frame_turn_count = 0  # Not use
        modified_frame_list = []

        # frame_datas_arrayについて一度づつ回す
        for frame_data in self.frame_datas_array:

            # frame_dataにface_location_listがなければ処理をとばす
            if "face_location_list" not in frame_data:
                if self.CONFIG["headless"] is False:
                    # 半透明処理（後半）_1frameに対して1回
                    if self.CONFIG["show_overlay"] is True:
                        cv2.addWeighted(
                            frame_data["overlay"],
                            self.CONFIG["alpha"],
                            frame_data["img"],
                            1 - self.CONFIG["alpha"],
                            0,
                            frame_data["img"]
                        )
                continue

            resized_frame: npt.NDArray[np.uint8] = frame_data["img"]
            face_location_list = frame_data["face_location_list"]
            overlay: npt.NDArray[np.uint8] = frame_data["overlay"]
            # person_data_listが変数に格納される
            person_data_list = frame_data["person_data_list"]
            date = datetime.now().strftime("%Y,%m,%d,%H,%M,%S,%f")

            face_encoding: npt.NDArray[np.float64]
            matches: npt.NDArray[np.bool8]
            min_distance: float

            # 名前リスト作成
            for face_encoding in self.face_encodings:
                # Initialize name, matches (Inner frame)
                name: str = "Unknown"

                matches, min_distance = \
                    self._check_compare_faces(
                        self.logger,
                        self.CONFIG["deep_learning_model"],
                        self.CONFIG["known_face_encodings"],
                        face_encoding,
                        self.CONFIG["tolerance"]
                    )

                # if not np.any(matches is True):  # If there is no such person
                if not np.any(matches == 1):  # If there is no such person
                    face_names.append(name)  # Set "Unknown"
                    continue
                else:  # If there is an applicable person
                    face_name: str = self._return_face_name(
                        self.CONFIG,
                        matches,
                        min_distance
                    )
                face_names.append(face_name)  # set the person's name

            if len(face_names) == 0:
                continue

            # face_location_listについて繰り返し処理 → **frame_datas_array**作成
            # つまり人が写っているframeだけに対して以降の処理を行う、ということ。
            number_of_people = 0  # 人数。計算上0人から始める。draw_default_face()で使用する
            for (top, right, bottom, left), name in zip(face_location_list, face_names):
                # person_data = defaultdict(int)  # defaultdict(): k(eyの存在チェックが不要)[https://qiita.com/xza/items/72a1b07fcf64d1f4bdb7]
                # person_data = {}
                if name == 'Unknown':
                    percentage_and_symbol: str = ''
                    dis: str = ''
                    p: float = 1.0
                # nameが誰かの名前の場合、以下の処理を行う。
                else:
                    distance: str
                    name, distance = name.split(':')
                    # パーセンテージの算出
                    dis = str(round(float(distance), 2))
                    p = float(distance)
                    # return_percentage(p)
                    percentage = Cal_obj.return_percentage(
                        p, self.CONFIG["deep_learning_model"])
                    percentage = round(percentage, 1)
                    percentage_and_symbol = str(percentage) + '%'
                    # ファイル名を最初のアンダーバーで区切る（アンダーバーは複数なのでmaxsplit = 1）
                    try:
                        name, _ = name.split('_', maxsplit=1)
                    except:
                        self.logger.warning(
                            'ファイル名に異常が見つかりました', name, 'NAME_default.png あるいはNAME_001.png (001部分は001からはじまる連番)にしてください', 'noFaceフォルダに移動します')
                        move(name, './noFace/')
                        # return
                        continue

                # nameがUnknownであってもなくても以降の処理を行う。
                # クロップ画像保存
                if self.CONFIG["crop_face_image"] is True:
                    if self.CONFIG["frequency_crop_image"] < self.CONFIG["number_of_crops"]:
                        pil_img_obj_rgb = self._pil_img_rgb_instance(
                            resized_frame)
                        if self.CONFIG["crop_with_multithreading"] is True:
                            # """1.3.08 multithreading 9.05s
                            with ThreadPoolExecutor() as executor:
                                future = executor.submit(self._make_crop_face_image,
                                                         CONFIG["anti_spoof"],
                                                         name,
                                                         dis,
                                                         pil_img_obj_rgb,
                                                         top,
                                                         left,
                                                         right,
                                                         bottom,
                                                         self.CONFIG["number_of_crops"],
                                                         self.CONFIG["frequency_crop_image"]
                                                         )
                                filename, number_of_crops, frequency_crop_image = future.result()
                            # """
                        else:
                            # """ORIGINAL: 1.3.08で変更 8.69s
                            filename, number_of_crops, frequency_crop_image = \
                                self._make_crop_face_image(
                                    CONFIG["anti_spoof"],
                                    name,
                                    dis,
                                    pil_img_obj_rgb,
                                    top,
                                    left,
                                    right,
                                    bottom,
                                    self.CONFIG["number_of_crops"],
                                    self.CONFIG["frequency_crop_image"]
                                )
                            # """
                        self.CONFIG["number_of_crops"] = 0
                    else:
                        self.CONFIG["number_of_crops"] += 1

                # 描画系
                if self.CONFIG["headless"] is False:

                    # デフォルト顔画像の描画
                    if self.deep_learning_model == 0:
                        if p <= self.CONFIG["tolerance"]:  # ディスタンスpがtolerance以下の場合
                            if self.CONFIG["default_face_image_draw"] is True:
                                resized_frame: npt.NDArray[np.uint8] = \
                                    self._draw_default_face(
                                        self.logger,
                                        self.CONFIG,
                                        name,
                                        resized_frame,
                                        number_of_people
                                )
                                number_of_people += 1  # 何人目か
                                """DEBUG"""
                                # frame_imshow_for_debug(resized_frame)
                    elif self.deep_learning_model == 1:
                        percentage = Cal_obj.to_percentage(
                            self.CONFIG["tolerance"], self.CONFIG["deep_learning_model"])
                        if p <= percentage:  # ディスタンスpがtolerance以下の場合
                            if self.CONFIG["default_face_image_draw"] is True:
                                resized_frame: npt.NDArray[np.uint8] = \
                                    self._draw_default_face(
                                        self.logger,
                                        self.CONFIG,
                                        name,
                                        resized_frame,
                                        number_of_people
                                )
                                number_of_people += 1

                    # ピンクまたは白の四角形描画
                    if self.CONFIG["rectangle"] is True:
                        if name == 'Unknown':  # プリセット顔画像に対応する顔画像がなかった場合
                            resized_frame: npt.NDArray[np.uint8] = self._draw_pink_rectangle(
                                resized_frame, top, bottom, left, right)
                        else:  # プリセット顔画像に対応する顔画像があった場合
                            resized_frame: npt.NDArray[np.uint8] = \
                                self._draw_white_rectangle(
                                    self.CONFIG["rectangle"],
                                    resized_frame,
                                    top,
                                    left,
                                    right,
                                    bottom
                            )

                    # パーセンテージ描画
                    if self.CONFIG["show_percentage"] is True:
                        resized_frame: npt.NDArray[np.uint8] = \
                            self._display_percentage(
                                self.CONFIG["deep_learning_model"],
                                percentage_and_symbol,
                                resized_frame,
                                p,
                                left,
                                right,
                                bottom,
                                self.CONFIG["tolerance"]
                        )
                        """DEBUG"""
                        # frame_imshow_for_debug(resized_frame)

                    # 名前表示と名前用四角形の描画
                    if self.CONFIG["show_name"] is True:
                        resized_frame: npt.NDArray[np.uint8] = \
                            self._draw_rectangle_for_name(
                                name,
                                resized_frame,
                                left,
                                right, bottom
                        )
                        pil_img_obj = Image.fromarray(resized_frame)
                        resized_frame: npt.NDArray[np.uint8] = \
                            self._draw_text_for_name(
                            self.CONFIG["deep_learning_model"],
                            self.logger,
                            left,
                            right,
                            bottom,
                            name,
                            p,
                            self.CONFIG["tolerance"],
                            pil_img_obj
                        )
                        """DEBUG"""
                        # frame_imshow_for_debug(resized_frame)

                    # target_rectangleの描画
                    if self.CONFIG["target_rectangle"] is True:
                        resized_frame: npt.NDArray[np.uint8] = \
                            self._draw_target_rectangle(
                            person_data_list,
                            self.CONFIG,
                            resized_frame,
                            top,
                            bottom,
                            left,
                            right,
                            name
                        )
                        """DEBUG
                        frame_imshow_for_debug(resized_frame)
                        """

                person_data = {
                    'name': name,
                    'pict': filename,
                    'date': date,
                    'location': (top, right, bottom, left),
                    'percentage_and_symbol': percentage_and_symbol
                }
                person_data_list.append(person_data)

                # self.frame_datas_array = \
                #     self.make_frame_datas_array(
                #         overlay,
                #         face_location_list,
                #         name,
                #         filename,
                #         percentage_and_symbol,
                #         person_data_list,
                #         frame_datas_array,
                #         resized_frame
                #     )
            # End for (top, right, bottom, left), name in zip(face_location_list, face_names)

            # _1frameに対して1回 <- ?
            # 人が写っているframeをforで回している途中です。
            if self.CONFIG["headless"] is False:
                frame_datas = {
                    'img': resized_frame,
                    'face_location_list': face_location_list,
                    'overlay': overlay,
                    'person_data_list': person_data_list
                }
                """DEBUG
                frame_imshow_for_debug(resized_frame)
                self.frame_datas_array.append(frame_datas)
                """
                modified_frame_list.append(frame_datas)

            elif self.CONFIG["headless"] is True:
                frame_datas = {
                    'img': resized_frame,
                    'face_location_list': face_location_list,
                    'overlay': overlay,
                    'person_data_list': person_data_list
                }
                # self.frame_datas_array.append(frame_datas)
                modified_frame_list.append(frame_datas)
            # else:  # この処理はどうして書いたのか？不明。
            #     frame_datas = {'img':resized_frame, 'face_location_list':face_location_list, 'overlay': overlay, 'person_data_list': 'no-data_person_data_list'}
            #     # self.frame_datas_array.append(frame_datas)
            #     modified_frame_list.append(frame_datas)

            if self.CONFIG["headless"] is False:
                # 半透明処理（後半）_1frameに対して1回
                if self.CONFIG["show_overlay"] is True:
                    # cv2.addWeighted(overlay, self.CONFIG["alpha"], resized_frame, 1-self.CONFIG["alpha"], 0, resized_frame)
                    for modified_frame in modified_frame_list:
                        cv2.addWeighted(
                            modified_frame["overlay"], self.CONFIG["alpha"], modified_frame["img"], 1 -
                            self.CONFIG["alpha"], 0, modified_frame["img"]
                        )
                    # """DEBUG"""
                    # frame_imshow_for_debug(resized_frame)

        # return frame_datas
        """DEBUG
        print(f"modified_frame_list.__sizeof__(): {modified_frame_list.__sizeof__()}MB")
        """
        return modified_frame_list

    # @profile()

    def r_face_image(
        self,
        frame: npt.NDArray[np.uint8],
        face_location: Tuple[int, int, int, int]
    ) -> npt.NDArray[np.uint8]:
        """Return face image which expressed for ndarray.

        Args:
            frame (npt.NDArray[np.uint8]): Frame image
            face_location (Tuple[int,int,int,int]): Face location (coordinate)

        Returns:
            npt.NDArray[np.uint8]: Face image which expressed for ndarray
        """
        self.frame: npt.NDArray[np.uint8] = frame
        self.face_location: Tuple[int, int, int, int] = face_location
        face_image: npt.NDArray[np.uint8] = \
            Return_face_image_obj.return_face_image(
                self.frame, self.face_location)
        return face_image

    # @profile()

    def return_anti_spoof(
        self,
        frame: npt.NDArray[np.uint8],
        face_location: Tuple[int, int, int, int]
    ) -> Tuple[str, float, bool]:
        """Return result of anti spoof.

        Note:
            This function is EXPERIMENTAL!
            It might occur side effects.

        Args:
            frame (npt.NDArray[np.uint8]): Each of frame
            face_location (Tuple[int,int,int,int]): Face location

        Returns:
            Tuple[str, float, bool]:
            - spoof_or_real
            - score
            - ELE
                - Equally Likely Events
        """
        self.frame: npt.NDArray[np.uint8] = frame
        self.face_location: Tuple[int, int, int, int] = face_location
        face_image: npt.NDArray[np.uint8] = self.r_face_image(
            self.frame, self.face_location)
        # face_image = Return_face_image_obj.return_face_image(self.frame, self.face_location)
        # face_image = self.return_face_image(self.frame, self.face_location)
        # VidCap_obj.frame_imshow_for_debug(face_image)  # DEBUG

        """ DEBUG: face_image確認 -> 正方形であることを確認した
        print(self.face_location)
        cv2.imshow('Core: DEBUG', face_image)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()
        """

        # 定形処理:リサイズ, 標準化, 成形, float32キャスト, 推論, 後処理
        input_image: cv2.Mat = \
            cv2.resize(face_image, dsize=(128, 128))
        """DEBUG"""
        # VidCap_obj.frame_imshow_for_debug(input_image)

        input_image = input_image.transpose(2, 0, 1).astype('float32')
        input_image = input_image.reshape(-1, 3, 128, 128)

        # 推論
        input_name: str = onnx_session.get_inputs()[0].name
        result: List[npt.NDArray[np.float32]] = \
            onnx_session.run(None, {input_name: input_image})    # type: ignore

        # 後処理
        result_ndarray: npt.NDArray[np.float32] = np.array(result)
        result_squeeze: npt.NDArray[np.float32] = np.squeeze(result_ndarray)

        as_index: np.int64 = np.argmax(result_squeeze)

        score: float = 0.0
        if result_squeeze[0] > result_squeeze[1]:
            score = result_squeeze[0] - result_squeeze[1]
        else:
            score = result_squeeze[1] - result_squeeze[0]
        score = round(score, 2)

        ELE: bool = False
        if score < 0.4:
            ELE = True

        spoof_or_real: str = ''
        if as_index == 0 and score >= 0.8:  # (255, 0, 0)
            # spoof_or_real = 'real'
            spoof_or_real = 'spoof'
            return spoof_or_real, score, ELE
        if as_index == 1 and score >= 0.8:
            # else:
            # spoof_or_real = 'spoof'
            spoof_or_real = 'real'
            return spoof_or_real, score, ELE
        else:
            spoof_or_real = 'cannot_distinction'
            return spoof_or_real, score, ELE

# 以下、元libdraw.LibDraw
    # @profile()
    def _draw_pink_rectangle(
        self,
        resized_frame: npt.NDArray[np.uint8],
        top,
        bottom,
        left,
        right
    ) -> np.ndarray:
        self.resized_frame: npt.NDArray[np.uint8] = resized_frame
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        cv2.rectangle(
            self.resized_frame,
            (self.left, self.top),
            (self.right, self.bottom),
            (255, 87, 243),
            2
        )  # pink
        return self.resized_frame

    # @profile()
    def _draw_white_rectangle(
        self,
        rectangle,
        resized_frame: npt.NDArray[np.uint8],
        top,
        left,
        right,
        bottom
    ) -> np.ndarray:
        self.rectangle = rectangle
        self.resized_frame: npt.NDArray[np.uint8] = resized_frame
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom
        cv2.rectangle(self.resized_frame, (self.left-18, self.top-18),
                      (self.right+18, self.bottom+18), (175, 175, 175), 2)  # 灰色内枠
        cv2.rectangle(self.resized_frame, (self.left-20, self.top-20),
                      (self.right+20, self.bottom+20), (255, 255, 255), 2)  # 白色外枠
        return self.resized_frame

    # パーセンテージ表示
    # @profile()

    def _display_percentage(
        self,
        deep_learning_model,
        percentage_and_symbol, resized_frame: npt.NDArray[np.uint8],
        p,
        left,
        right,
        bottom,
        tolerance
    ) -> np.ndarray:
        self.deep_learning_model = deep_learning_model
        self.percentage_and_symbol = percentage_and_symbol
        self.resized_frame: npt.NDArray[np.uint8] = resized_frame
        self.p = p
        self.left = left
        self.right = right
        self.bottom = bottom
        self.tolerance = tolerance
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        # パーセンテージ表示用の灰色に塗りつぶされた四角形の描画
        cv2.rectangle(self.resized_frame, (self.left-25, self.bottom + 75),
                      (self.right+25, self.bottom+50), (30, 30, 30), cv2.FILLED)  # 灰色
        # テキスト表示位置
        fontsize = 14
        putText_center = int((self.left-25 + self.right+25)/2)
        putText_chaCenter = int(5/2)
        putText_pos = putText_center - \
            (putText_chaCenter*fontsize) - int(fontsize/2)
        putText_position = (putText_pos, self.bottom + 75 - int(fontsize / 2))

        # toleranceの値によってフォント色を変える
        if deep_learning_model == 0:
            if self.p < self.tolerance:
                # パーセンテージを白文字表示
                self.resized_frame: npt.NDArray[np.uint8] = cv2.putText(
                    self.resized_frame, self.percentage_and_symbol, putText_position, font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            else:
                # パーセンテージをピンク表示
                self.resized_frame: npt.NDArray[np.uint8] = cv2.putText(
                    self.resized_frame, self.percentage_and_symbol, putText_position, font, 1, (255, 87, 243), 1, cv2.LINE_AA)
        elif deep_learning_model == 1:
            percentage = Cal_obj.to_percentage(
                self.tolerance, deep_learning_model)
            if self.p < percentage:
                # パーセンテージを白文字表示
                self.resized_frame: npt.NDArray[np.uint8] = cv2.putText(
                    self.resized_frame, self.percentage_and_symbol, putText_position, font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            else:
                # パーセンテージをピンク表示
                self.resized_frame: npt.NDArray[np.uint8] = cv2.putText(
                    self.resized_frame, self.percentage_and_symbol, putText_position, font, 1, (255, 87, 243), 1, cv2.LINE_AA)

        return self.resized_frame

    # デフォルト顔画像の描画処理
    # @profile()
    def _draw_default_face_image(
        self,
        logger,
        resized_frame: npt.NDArray[np.uint8],
        default_face_small_image,
        x1,
        y1,
        x2,
        y2,
        number_of_people,
        face_image_width
    ):
        self.resized_frame: npt.NDArray[np.uint8] = resized_frame
        self.default_face_small_image = default_face_small_image
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.number_of_people = number_of_people
        self.face_image_width = face_image_width
        try:
            self.x1 = self.x1 + (self.number_of_people * self.face_image_width)
            self.x2 = self.x2 + (self.number_of_people * self.face_image_width)
            self.resized_frame[self.y1:self.y2, self.x1:self.x2] = self.resized_frame[self.y1:self.y2, self.x1:self.x2] * (
                1 - self.default_face_small_image[:, :, 3:] / 255) + self.default_face_small_image[:, :, :3] * (default_face_small_image[:, :, 3:] / 255)
            # resized_frame[y1:y2, x1:x2] = resized_frame[y1:y2, x1:x2] * a + b  # ValueError: assignment destination is read-only
            """DEBUG"""
            # frame_imshow_for_debug(resized_frame)
        except:
            logger.info('デフォルト顔画像の描画が出来ません')
            logger.info('描画面積が足りないか他に問題があります')
        return self.resized_frame

    # デフォルト顔画像の表示面積調整
    # @profile()
    def _adjust_display_area(
        self,
        CONFIG,
        default_face_image
    ) -> tuple:
        self.CONFIG = CONFIG
        self.default_face_image = default_face_image
        """TODO: 繰り返し計算させないようリファクタリング"""
        face_image_width = int(self.CONFIG["set_width"] / 15)
        default_face_small_image = cv2.resize(self.default_face_image, dsize=(
            face_image_width, face_image_width))  # 幅・高さともに同じとする
        # 高さ = face_image_width
        x1, y1, x2, y2 = 0, self.CONFIG["set_height"] - face_image_width - \
            10, face_image_width, self.CONFIG["set_height"] - 10
        return x1, y1, x2, y2, default_face_small_image, face_image_width

    # @profile()
    def _draw_default_face(
        self,
        logger,
        CONFIG,
        name,
        resized_frame: npt.NDArray[np.uint8],
        number_of_people
    ):
        self.logger = logger
        self.CONFIG = CONFIG
        self.name = name
        self.resized_frame: npt.NDArray[np.uint8] = resized_frame
        self.number_of_people = number_of_people
        default_face_image_dict = self.CONFIG["default_face_image_dict"]

        default_name_png = self.name + '_default.png'
        default_face_image_name_png = './preset_face_images/' + default_name_png
        if not self.name in default_face_image_dict:  # default_face_image_dictにnameが存在しなかった場合
            # 各人物のデフォルト顔画像ファイルの読み込み
            if exists(default_face_image_name_png):
                # WINDOWSのopencv-python4.2.0.32ではcv2.imread()でpng画像を読み込めないバグが
                # 存在する可能性があると思う。そこでPNG画像の読み込みにはpillowを用いることにする
                default_face_image = np.array(
                    Image.open(default_face_image_name_png))
                """DEBUG
                frame_imshow_for_debug(default_face_image)
                """
                # BGAをRGBへ変換
                default_face_image = cv2.cvtColor(
                    default_face_image, cv2.COLOR_BGR2RGBA)
                """DEBUG
                frame_imshow_for_debug(default_face_image)
                """
                # if default_face_image.ndim == 3:  # RGBならアルファチャンネル追加 resized_frameがアルファチャンネルを持っているから。
                # default_face_imageをメモリに保持
                # キーnameと値default_face_imageの組み合わせを挿入する
                default_face_image_dict[self.name] = default_face_image
            else:
                if self.name != 'Unknown':
                    self.logger.info(
                        f'{self.name}さんのデフォルト顔画像ファイルがpreset_face_imagesフォルダに存在しません')
                    self.logger.info(
                        f'{self.name}さんのデフォルト顔画像ファイルをpreset_face_imagesフォルダに用意してください')
        else:  # default_face_image_dictにnameが存在した場合
            # キーnameに対応する値をdefault_face_imageへ格納する
            default_face_image = default_face_image_dict[self.name]
            """DEBUG
            frame_imshow_for_debug(default_face_image)  # OK
            """
            x1, y1, x2, y2, default_face_small_image, face_image_width = self._adjust_display_area(
                CONFIG, default_face_image)
            resized_frame: npt.NDArray[np.uint8] = self._draw_default_face_image(
                logger, resized_frame, default_face_small_image, x1, y1, x2, y2, number_of_people, face_image_width)
        return resized_frame

    # @profile()
    def _draw_rectangle_for_name(
        self,
        name,
        resized_frame: npt.NDArray[np.uint8],
        left,
        right, bottom
    ):
        self.name = name
        self.resized_frame: npt.NDArray[np.uint8] = resized_frame
        self.left = left
        self.right = right
        self.bottom = bottom
        if self.name == 'Unknown':   # nameがUnknownだった場合
            self.resized_frame = cv2.rectangle(self.resized_frame, (
                self.left-25, self.bottom + 25), (self.right+25, self.bottom+50), (255, 87, 243), cv2.FILLED)  # pink
        else:                   # nameが既知だった場合
            # cv2.rectangle(resized_frame, (left-25, bottom + 25), (right+25, bottom+50), (211, 173, 54), thickness = 1) # 濃い水色の線
            self.resized_frame = cv2.rectangle(self.resized_frame, (
                self.left-25, self.bottom + 25), (self.right+25, self.bottom+50), (211, 173, 54), cv2.FILLED)  # 濃い水色
        return self.resized_frame

    # 帯状四角形（ピンク）の描画
    # @profile()
    def _draw_error_messg_rectangle(
        self,
        resized_frame: npt.NDArray[np.uint8],
        set_height,
        set_width
    ):
        """Deprecated."""
        self.resized_frame: npt.NDArray[np.uint8] = resized_frame
        self.set_height = set_height
        self.set_width = set_width
        error_messg_rectangle_top: int = int((self.set_height + 20) / 2)
        error_messg_rectangle_bottom: int = int((self.set_height + 120) / 2)
        error_messg_rectangle_left: int = 0
        error_messg_rectangle_right: int = self.set_width
        cv2.rectangle(self.resized_frame, (error_messg_rectangle_left, error_messg_rectangle_top), (
            error_messg_rectangle_right, error_messg_rectangle_bottom), (255, 87, 243), cv2.FILLED)  # pink
        return error_messg_rectangle_left, error_messg_rectangle_right, error_messg_rectangle_bottom

    # drawオブジェクトを生成
    # @profile()
    def _make_draw_object(self, frame):
        self.frame = frame
        draw = ImageDraw.Draw(Image.fromarray(self.frame))
        return draw

    # @profile()
    def _draw_error_messg_rectangle_messg(
        self,
        draw,
        error_messg_rectangle_position,
        error_messg_rectangle_messg,
        error_messg_rectangle_font
    ):
        """Deprecated."""
        self.draw = draw
        self.error_messg_rectangle_position = error_messg_rectangle_position
        self.error_messg_rectangle_messg = error_messg_rectangle_messg
        self.error_messg_rectangle_font = error_messg_rectangle_font
        draw.text(self.error_messg_rectangle_position, self.error_messg_rectangle_messg, fill=(
            255, 255, 255, 255), font=self.error_messg_rectangle_font)

    # @profile()
    def _return_fontpath(self, logger):
        # フォントの設定(フォントファイルのパスと文字の大きさ)
        operating_system: str = system()
        fontpath: str = ''
        if (operating_system == 'Linux'):
            # fontpath = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
            fontpath = "/usr/share/fonts/truetype/mplus/mplus-1mn-bold.ttf"

        elif (operating_system == 'Windows'):
            # fontpath = "C:/WINDOWS/FONTS/BIZ-UDGOTHICR.TTC"
            fontpath = "C:/WINDOWS/FONTS/BIZ-UDGOTHICB.TTC"  # bold体
        else:
            logger.info('オペレーティングシステムの確認が出来ません。システム管理者にご連絡ください')
        return fontpath

    # @profile()
    def _calculate_text_position(
        self,
        left,
        right,
        name,
        fontsize,
        bottom
    ):
        # TODO: #17 英数字のみの場合の位置決定バグ
        self.left = left
        self.right = right
        self.name = name
        self.fontsize = fontsize
        self.bottom = bottom

        center = int((self.left + self.right)/2)
        chaCenter = int(len(self.name)/2)
        pos = center - (chaCenter * self.fontsize) - int(self.fontsize/2)
        position = (pos, self.bottom + (self.fontsize * 2))
        Unknown_position = (pos + self.fontsize,
                            self.bottom + (self.fontsize * 2))
        return position, Unknown_position

    # @profile()
    def _draw_name(
        self,
        deep_learning_model,
        name,
        pil_img_obj,
        Unknown_position,
        font,
        p,
        tolerance,
        position
    ):
        self.deep_learning_model = deep_learning_model
        self.name = name
        self.pil_img_obj = pil_img_obj
        self.Unknown_position = Unknown_position
        self.font = font
        self.p = p
        self.tolerance = tolerance
        self.position = position

        local_draw_obj = ImageDraw.Draw(self.pil_img_obj)
        if self.name == 'Unknown':  # nameがUnknownだった場合
            # draw.text(Unknown_position, '照合不一致', fill=(255, 255, 255, 255), font = font)
            # unregistered = mojimoji.han_to_zen('UNREGISTERED')
            # local_draw_obj.text(self.Unknown_position, unregistered, fill=(255, 255, 255, 255), font = self.font)
            local_draw_obj.text(self.Unknown_position, 'UNREGISTERED', fill=(
                255, 255, 255, 255), font=self.font)
            # local_draw_obj.text(self.Unknown_position, '　未登録', fill=(255, 255, 255, 255), font = self.font)
        else:  # nameが既知の場合
            if deep_learning_model == 0:
                # if percentage > 99.0:
                if self.p < self.tolerance:
                    # nameの描画
                    local_draw_obj.text(self.position, self.name, fill=(
                        255, 255, 255, 255), font=self.font)
                else:
                    local_draw_obj.text(self.position, self.name, fill=(
                        255, 87, 243, 255), font=self.font)
            elif deep_learning_model == 1:
                percentage = Cal_obj.to_percentage(
                    self.tolerance, deep_learning_model)
                if self.p < percentage:
                    # nameの描画
                    local_draw_obj.text(self.position, self.name, fill=(
                        255, 255, 255, 255), font=self.font)
                else:
                    local_draw_obj.text(self.position, self.name, fill=(
                        255, 87, 243, 255), font=self.font)

        return self.pil_img_obj

    # pil_img_objをnumpy配列に変換
    # @profile()
    def _convert_pil_img_to_ndarray(
        self,
        pil_img_obj
    ):
        self.pil_img_obj = pil_img_obj
        frame = np.array(self.pil_img_obj)
        """DEBUG: Memory leak
        del pil_img_obj
        gc.collect()
        """
        return frame

    # @profile()
    def _draw_text_for_name(
        self,
        deep_learning_model,
        logger,
        left,
        right,
        bottom,
        name,
        p,
        tolerance,
        pil_img_obj
    ):
        self.deep_learning_model = deep_learning_model
        self.logger = logger
        self.left = left
        self.right = right
        self.bottom = bottom
        self.name = name
        self.p = p
        self.tolerance = tolerance
        self.pil_img_obj = pil_img_obj

        # すべての文字を全角変換する
        self.name = mojimoji.han_to_zen(
            self.name, ascii=True, kana=True, digit=True)

        fontpath = self._return_fontpath(logger)
        """TODO #16 FONTSIZEハードコーティング訂正"""
        fontsize = 14
        font = ImageFont.truetype(fontpath, fontsize, encoding='utf-8')
        # テキスト表示位置決定
        position, Unknown_position = \
            self._calculate_text_position(
                self.left,
                self.right,
                self.name,
                fontsize,
                self.bottom
            )
        # nameの描画
        self.pil_img_obj = \
            self._draw_name(
                self.deep_learning_model,
                self.name,
                self.pil_img_obj,
                Unknown_position,
                font,
                self.p,
                self.tolerance,
                position
            )
        # pil_img_objをnumpy配列に変換
        resized_frame: npt.NDArray[np.uint8] = self._convert_pil_img_to_ndarray(
            self.pil_img_obj)
        # del self.pil_img_obj
        return resized_frame

    # target_rectangleの描画
    # @profile()
    def _draw_target_rectangle(
        self,
        person_data_list,
        CONFIG,
        resized_frame: npt.NDArray[np.uint8],
        top,
        bottom,
        left,
        right,
        name
    ):
        self.person_data_list = person_data_list,
        self.anti_spoof = CONFIG["anti_spoof"],
        self.rect01_png = CONFIG["rect01_png"]
        self.rect01_NG_png = CONFIG["rect01_NG_png"]
        self.rect01_REAL_png = CONFIG["rect01_REAL_png"]
        self.rect01_SPOOF_png = CONFIG["rect01_SPOOF_png"]
        self.rect01_CANNOT_DISTINCTION_png = CONFIG["rect01_CANNOT_DISTINCTION_png"]
        self.resized_frame: npt.NDArray[np.uint8] = resized_frame
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.name = name
        face_location = (self.top, self.right, self.bottom, self.left)

        width_ratio: float
        height_ratio: float
        face_width: int
        face_height: int
        result = None

        spoof_or_real = None
        score = 0.0
        ELE = True

        if self.anti_spoof[0] is True:
            # Fix: TODO: この箇所でreturn_anti_spoof()を呼び出すのは重複になる
            # for person_data in self.person_data_list:
            #     for person_data_element in person_data:
            #         if person_data_element == {}:
            #             continue
            #         spoof_or_real = person_data_element["spoof_dict"]["spoof_or_real"]
            #         score = person_data_element["spoof_dict"]["score"]
            #         ELE = person_data_element["spoof_dict"]["ELE"]
            # ELE: Equally Likely Events
            spoof_or_real, score, ELE = self.return_anti_spoof(
                self.resized_frame, face_location)

            if spoof_or_real == 'spoof' and ELE is False:
                face_width: int = self.right - self.left
                face_height: int = self.bottom - self.top
                orgHeight, orgWidth = self.rect01_SPOOF_png.shape[:2]
                width_ratio = 1.0 * (face_width / orgWidth)
                height_ratio = 1.0 * (face_height / orgHeight)
                self.rect01_SPOOF_png = cv2.resize(
                    self.rect01_SPOOF_png, None, fx=width_ratio, fy=height_ratio)
                x1, y1, x2, y2 = self.left, self.top, self.left + \
                    self.rect01_SPOOF_png.shape[1], self.top + \
                    self.rect01_SPOOF_png.shape[0]
                try:
                    self.resized_frame[y1:y2, x1:x2] = self.resized_frame[y1:y2, x1:x2] * (1 - self.rect01_SPOOF_png[:, :, 3:] / 255) + \
                        self.rect01_SPOOF_png[:, :, :3] * \
                        (self.rect01_SPOOF_png[:, :, 3:] / 255)
                except:
                    # TODO: np.clip
                    pass
            elif spoof_or_real == 'cannot_distinction' and ELE is False:
                face_width: int = self.right - self.left
                face_height: int = self.bottom - self.top
                orgHeight, orgWidth = self.rect01_CANNOT_DISTINCTION_png.shape[:2]
                width_ratio = 1.0 * (face_width / orgWidth)
                height_ratio = 1.0 * (face_height / orgHeight)
                self.rect01_CANNOT_DISTINCTION_png = cv2.resize(
                    self.rect01_CANNOT_DISTINCTION_png, None, fx=width_ratio, fy=height_ratio)
                x1, y1, x2, y2 = self.left, self.top, self.left + \
                    self.rect01_CANNOT_DISTINCTION_png.shape[1], self.top + \
                    self.rect01_CANNOT_DISTINCTION_png.shape[0]
                try:
                    self.resized_frame[y1:y2, x1:x2] = self.resized_frame[y1:y2, x1:x2] * (1 - self.rect01_CANNOT_DISTINCTION_png[:, :, 3:] / 255) + \
                        self.rect01_CANNOT_DISTINCTION_png[:, :, :3] * (
                            self.rect01_CANNOT_DISTINCTION_png[:, :, 3:] / 255)
                except:
                    # TODO: np.clip
                    pass
            elif self.name != 'Unknown' and spoof_or_real == 'real' and ELE is False:  # self.nameが既知の場合
                face_width: int = self.right - self.left
                face_height: int = self.bottom - self.top
                orgHeight, orgWidth = self.rect01_REAL_png.shape[:2]
                width_ratio = 1.0 * (face_width / orgWidth)
                height_ratio = 1.0 * (face_height / orgHeight)
                self.rect01_REAL_png = cv2.resize(
                    self.rect01_REAL_png, None, fx=width_ratio, fy=height_ratio)
                x1, y1, x2, y2 = self.left, self.top, self.left + \
                    self.rect01_REAL_png.shape[1], self.top + \
                    self.rect01_REAL_png.shape[0]
                try:
                    self.resized_frame[y1:y2, x1:x2] = self.resized_frame[y1:y2, x1:x2] * (1 - self.rect01_REAL_png[:, :, 3:] / 255) + \
                        self.rect01_REAL_png[:, :, :3] * \
                        (self.rect01_REAL_png[:, :, 3:] / 255)
                except:
                    # TODO: np.clip
                    pass
            elif self.name == 'Unknown' and spoof_or_real == 'real' and ELE is False:  # self.nameがUnknownだった場合
                fx: float = 0.0
                face_width = self.right - self.left
                face_height = self.bottom - self.top
                # rect01_NG_png←ピンクのtarget_rectangle
                # rect01_NG_png: cv2.Mat = cv2.imread("images/rect01_NG.png", cv2.IMREAD_UNCHANGED)
                orgHeight, orgWidth = self.rect01_NG_png.shape[:2]
                width_ratio = float(1.0 * (face_width / orgWidth))
                height_ratio = 1.0 * (face_height / orgHeight)
                self.rect01_NG_png = cv2.resize(
                    self.rect01_NG_png, None, fx=width_ratio, fy=height_ratio)
                x1, y1, x2, y2 = self.left, self.top, self.left + \
                    self.rect01_NG_png.shape[1], self.top + \
                    self.rect01_NG_png.shape[0]
                try:
                    self.resized_frame[y1:y2, x1:x2] = self.resized_frame[y1:y2, x1:x2] * (1 - self.rect01_NG_png[:, :, 3:] / 255) + \
                        self.rect01_NG_png[:, :, :3] * \
                        (self.rect01_NG_png[:, :, 3:] / int(255))
                except:
                    # TODO: np.clip
                    pass
        elif self.anti_spoof[0] is False:
            # BUG FIX: v1.4.04
            ELE = False
            if self.name != 'Unknown':  # self.nameが既知の場合
                face_width: int = self.right - self.left
                face_height: int = self.bottom - self.top
                orgHeight, orgWidth = self.rect01_png.shape[:2]
                width_ratio = 1.0 * (face_width / orgWidth)
                height_ratio = 1.0 * (face_height / orgHeight)
                self.rect01_png = cv2.resize(
                    self.rect01_png, None, fx=width_ratio, fy=height_ratio)
                x1, y1, x2, y2 = self.left, self.top, self.left + \
                    self.rect01_png.shape[1], self.top + \
                    self.rect01_png.shape[0]
                try:
                    self.resized_frame[y1:y2, x1:x2] = self.resized_frame[y1:y2, x1:x2] * (1 - self.rect01_png[:, :, 3:] / 255) + \
                        self.rect01_png[:, :, :3] * \
                        (self.rect01_png[:, :, 3:] / 255)
                except:
                    # TODO: np.clip
                    pass
            elif self.name == 'Unknown':  # self.nameがUnknownだった場合
                fx: float = 0.0
                face_width = self.right - self.left
                face_height = self.bottom - self.top
                # rect01_NG_png←ピンクのtarget_rectangle
                # rect01_NG_png: cv2.Mat = cv2.imread("images/rect01_NG.png", cv2.IMREAD_UNCHANGED)
                orgHeight, orgWidth = self.rect01_NG_png.shape[:2]
                width_ratio = float(1.0 * (face_width / orgWidth))
                height_ratio = 1.0 * (face_height / orgHeight)
                self.rect01_NG_png = cv2.resize(
                    self.rect01_NG_png, None, fx=width_ratio, fy=height_ratio)
                x1, y1, x2, y2 = self.left, self.top, self.left + \
                    self.rect01_NG_png.shape[1], self.top + \
                    self.rect01_NG_png.shape[0]
                try:
                    self.resized_frame[y1:y2, x1:x2] = self.resized_frame[y1:y2, x1:x2] * (1 - self.rect01_NG_png[:, :, 3:] / 255) + \
                        self.rect01_NG_png[:, :, :3] * \
                        (self.rect01_NG_png[:, :, 3:] / int(255))
                except:
                    # TODO: np.clip
                    pass

        return self.resized_frame

    def common_process(
        self,
        CONFIG: Dict
    ) -> Generator:
        """Generator of frame_datas_array.

        common_process function consists 3 part of Core() methods.

        1. Core().frame_pre_processing
        2. Core().face_encoding_process
        3. Core().frame_post_processing

        Yields:
            Generator: frame_datas_array
                - frame_datas_array: List[Dict]

        Example:
            Make generator object

            >>> obj = Core().common_process(CONFIG)

            Call '__next__()' method

            >>> while True:
                frame_datas_array = obj.__next__()
        """
        self.CONFIG: Dict = CONFIG

        frame_generator_obj = VidCap_obj.frame_generator(self.CONFIG)
        while True:
            try:

                frame_datas_array: List[Dict] = \
                    self.frame_pre_processing(
                        self.logger,
                        CONFIG,
                        frame_generator_obj.__next__()
                )

                """DEBUG
                self.logger.debug(inspect.currentframe().f_back.f_code.co_filename)
                self.logger.debug(inspect.currentframe().f_back.f_lineno)
                self.logger.debug(f'frame_datas_array size: {len(frame_datas_array), getsizeof(frame_datas_array)}')
                self.logger.debug(inspect.currentframe().f_back.f_code.co_filename)
                self.logger.debug(inspect.currentframe().f_back.f_lineno)
                self.logger.debug(f'CONFIG size: {len(CONFIG), getsizeof(CONFIG)}')
                """

                face_encodings, frame_datas_array = \
                    self.face_encoding_process(
                        self.logger,
                        CONFIG,
                        frame_datas_array
                    )

                # FIXED: ISSUE: #1 Awai_diff
                if len(face_encodings) == 0:
                    # DEBUG:
                    # VidCap_obj.frame_imshow_for_debug(frame_datas_array[0]['img'])
                    yield frame_datas_array
                    continue

                frame_datas_array = \
                    self.frame_post_processing(
                        self.logger,
                        CONFIG,
                        face_encodings,
                        frame_datas_array
                    )

                yield frame_datas_array

            except StopIteration:
                self.logger.warning("DATA RECEPTION HAS ENDED")
                exit(0)
            except Exception as e:
                self.logger.warning("ERROR OCURRED")
                self.logger.warning("-" * 20)
                self.logger.warning(f"ERROR TYPE: {e}")
                self.logger.warning(format_exc(limit=None, chain=True))
                self.logger.warning("-" * 20)
                exit(0)

    def override_args_dict(
        self,
        CONFIG: Dict,
        override_list: List[Tuple]
    ) -> Dict:
        """Override CONFIG for example.

        Args:
            Dict: CONFIG
            List[Tuple]: override_list

        Returns:
            Dict: CONFIG

        Example:
            >>> CONFIG = Core.override_args_dict(
                CONFIG,
                [
                    ('crop_face_image', False),
                    ('output_debug_log', True)
                ]
            )

        Note:
            - *THIS METHOD IS EXPERIMENTAL*
                - Unexpected side effects may occur.
            - If you specified key is not exist, application will fail down
                with print out log 'warning'.
            - You cannot change key 'headless'. If override it, application will fall down.
        """
        self.logger.warning("'override' method is EXPERIMENTAL")
        self.logger.warning("Unexpected side effects may occur")

        element: Tuple
        for element in override_list:
            key, value = element

            if not key in CONFIG:
                self.logger.error(f"{key} dose not exist")
                exit()

            if key == 'headless':
                self.logger.warning(
                    "You cannot change key 'headless' from True to False.")
                self.logger.warning("exit")
                exit()

            CONFIG[key] = value

        return CONFIG
