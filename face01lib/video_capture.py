"""The VidCap class."""

import inspect
from io import BytesIO
from os import environ
from sys import exit
from traceback import format_exc
from typing import Dict, Generator, List, Tuple

import cv2
import numpy as np
import numpy.typing as npt
import requests
from PIL import Image, ImageFile
from requests.auth import HTTPDigestAuth

from face01lib.Calc import Cal
from face01lib.logger import Logger

ImageFile.LOAD_TRUNCATED_IMAGES = True
"""TODO #18 opencvの環境変数変更 要調査"""
# environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"


class VidCap:
    """VidCap class.

    contains methods that initially process the input video data
    """
    def __init__(self, log_level: str = 'info') -> None:
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

        self.logger = Logger(self.log_level).logger(name, parent_dir)

        Cal().cal_specify_date(self.logger)

    # デバッグ用imshow()
    def frame_imshow_for_debug(
        self,
        frame: npt.NDArray[np.uint8]
    ) -> None:
        """Used for debugging.

        Display the given frame data in a GUI window for 3 seconds.

        Args:
            frame (npt.NDArray[np.uint8]): Image data called 'frame'

        Return:
            None
        """
        self.frame_maybe: npt.NDArray[np.uint8] = frame

        if isinstance(self.frame_maybe, np.ndarray):
            cv2.imshow("DEBUG", self.frame_maybe)
            self.logger.debug(inspect.currentframe().f_back.f_code.co_filename)
            self.logger.debug(inspect.currentframe().f_back.f_lineno)
            cv2.moveWindow('window DEBUG', 0, 0)
            cv2.waitKey(3000)
            cv2.destroyAllWindows()
        else:
            for fra in self.frame_maybe:
                fr: npt.NDArray[np.uint8] = fra["img"]
                cv2.imshow("DEBUG", fr)
                cv2.moveWindow('window DEBUG', 0, 0)
                self.logger.debug(inspect.currentframe().f_back.f_code.co_filename)
                self.logger.debug(inspect.currentframe().f_back.f_lineno)
                cv2.waitKey(3000)
                cv2.destroyAllWindows()

    def resize_frame(
        self,
        set_width: int,
        set_height: int,
        frame: npt.NDArray[np.uint8]
    ) -> npt.NDArray[np.uint8]:
        """Return resized frame data.

        Args:
            set_width (int): Width described in config.ini
            set_height (int): Height described in config.ini
            frame (npt.NDArray[np.uint8]): Image data

        Returns:
            npt.NDArray[np.uint8]: small_frame
        """
        self.set_width: int = set_width
        self.set_height: int = set_height
        self.frame: npt.NDArray[np.uint8] = frame

        small_frame: npt.NDArray[np.uint8] = \
            cv2.resize(self.frame, (self.set_width, self.set_height))  # cv2.Mat
        return small_frame

    def return_movie_property(
        self,
        set_width: int,
        vcap
    ) -> Tuple[int, ...]:
        """Return input movie file's property.

        Args:
            set_width (int): Width which set in config.ini
            vcap (cv2.VideoCapture): Handle of input movie processing

        Returns:
            Tuple[int,...]: self.set_width, fps, height, width, set_height
        """
        self.set_width: int = set_width
        self.vcap = vcap
        # # debug
        # if vcap.isOpened():
        #     print("VideoCaptureオブジェクトが正しく開かれています。")
        # else:
        #     print("VideoCaptureオブジェクトが開かれていません。")

        fps: int = self.vcap.get(cv2.CAP_PROP_FPS)
        height: int = self.vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width: int = self.vcap.get(cv2.CAP_PROP_FRAME_WIDTH)

        fps: int = int(fps)
        height: int = int(height)
        width: int = int(width)

        if width <= 0:
            self.logger.warning("Can't receive input data")
            self.logger.warning("-" * 20)
            self.logger.warning(format_exc(limit=None, chain=True))
            self.logger.warning("-" * 20)
            self.logger.warning("exit")
            exit(0)

        # BUGFIX: vcapを閉じておく
        self.finalize(self.vcap)
        # # debug
        # if vcap.isOpened():
        #     print("VideoCaptureオブジェクトが正しく開かれています。")
        # else:
        #     print("VideoCaptureオブジェクトが開かれていません。")
        set_height: int = int((self.set_width * height) / width)

        return self.set_width,fps,height,width,set_height

    # cdef, python版
    def _cal_angle_coordinate(self, height: int, width: int) -> Tuple[Tuple[int,int,int,int], ...]:
        self.height: int = height
        self.width: int = width
        """Pre-calculate the angle of view (TOP_LEFT, TOP_RIGHT).

        Args:
            height (int)
            width (int)

        Returns:
            Tuple[int,int,int,int]: TOP_LEFT,TOP_RIGHT,BOTTOM_LEFT,BOTTOM_RIGHT,CENTER
        """
        # order: (top, bottom, left, right)
        TOP_LEFT: Tuple[int,int,int,int] = (0,int(self.height/2), 0, int(self.width/2))
        TOP_RIGHT: Tuple[int,int,int,int] = (0,int( self.height/2),int(self.width/2),self.width)
        BOTTOM_LEFT: Tuple[int,int,int,int] = (int(self.height/2),self.height,0,int(self.width/2))
        BOTTOM_RIGHT: Tuple[int,int,int,int] = (int(self.height/2),self.height,int(self.width/2),self.width)
        CENTER: Tuple[int,int,int,int] = (int(self.height/4),int(self.height/4)*3,int(self.width/4),int(self.width/4)*3)
        return TOP_LEFT,TOP_RIGHT,BOTTOM_LEFT,BOTTOM_RIGHT,CENTER

    def _angle_of_view_specification(
        self,
        set_area: str,
        frame: npt.NDArray[np.uint8],
        TOP_LEFT: Tuple[int, int, int, int],
        TOP_RIGHT: Tuple[int, int, int, int],
        BOTTOM_LEFT: Tuple[int, int, int, int],
        BOTTOM_RIGHT: Tuple[int, int, int, int],
        CENTER: Tuple[int, int, int, int]
    ) -> npt.NDArray[np.uint8]:
        """Return ndarray data which area specification coordinates for frame.

        Args:
            set_area (str): Described in config.ini
            frame (npt.NDArray[np.uint8]): Image data which described ndarray
            TOP_LEFT (Tuple[int,int,int,int]): Top-left coordinate
            TOP_RIGHT (Tuple[int,int,int,int]): Top-right coordinate
            BOTTOM_LEFT (Tuple[int,int,int,int]): Bottom-left coordinate
            BOTTOM_RIGHT (Tuple[int,int,int,int]): Bottom-right coordinate
            CENTER (Tuple[int,int,int,int]): Coordinates to keep the angle of view in the center of the screen

        Returns:
            npt.NDArray[np.uint8]: self.frame

        Note:
            Face_location order: top, right, bottom, left
            TOP_LEFT order: (top, bottom, left, right)
            How to slice: img[top: bottom, left: right]
        """
        self.set_area: str = set_area
        self.frame: npt.NDArray[np.uint8] = frame
        self.TOP_LEFT: Tuple[int, int, int, int] = TOP_LEFT
        self.TOP_RIGHT: Tuple[int, int, int, int] = TOP_RIGHT
        self.BOTTOM_LEFT: Tuple[int, int, int, int] = BOTTOM_LEFT
        self.BOTTOM_RIGHT: Tuple[int, int, int, int] = BOTTOM_RIGHT
        self.CENTER: Tuple[int, int, int, int] = CENTER

        # VidCap().frame_imshow_for_debug(self.frame)

        if self.set_area=='NONE':
            return self.frame
        elif self.set_area=='TOP_LEFT':
            self.frame = self.frame[self.TOP_LEFT[0]:self.TOP_LEFT[1],self.TOP_LEFT[2]:self.TOP_LEFT[3]]
        elif self.set_area=='TOP_RIGHT':
            self.frame = self.frame[self.TOP_RIGHT[0]:self.TOP_RIGHT[1],self.TOP_RIGHT[2]:self.TOP_RIGHT[3]]
        elif self.set_area=='BOTTOM_LEFT':
            self.frame = self.frame[self.BOTTOM_LEFT[0]:self.BOTTOM_LEFT[1],self.BOTTOM_LEFT[2]:self.BOTTOM_LEFT[3]]
        elif self.set_area=='BOTTOM_RIGHT':
            self.frame = self.frame[self.BOTTOM_RIGHT[0]:self.BOTTOM_RIGHT[1],self.BOTTOM_RIGHT[2]:self.BOTTOM_RIGHT[3]]
        elif self.set_area=='CENTER':
            self.frame = self.frame[self.CENTER[0]:self.CENTER[1],self.CENTER[2]:self.CENTER[3]]
        # VidCap().frame_imshow_for_debug(self.frame)
        return self.frame

    def return_vcap(self, movie: str) -> cv2.VideoCapture:
        """Return vcap object.

        Args:
            movie (str): movie

        Returns:
            object: cv2.VideoCapture
        """
        self.movie: str = movie
        # movie=movie
        if self.movie == 'usb' or self.movie == 'USB':   # USB カメラ読み込み時使用
            live_camera_number: int = 0
            for camera_number in range(0, 5):
                vcap = cv2.VideoCapture(camera_number)
                # BUG: cv2.CAP_FFMPEG
                # vcap = cv2.VideoCapture(camera_number, cv2.CAP_FFMPEG)
                # vcap = cv2.VideoCapture(camera_number, cv2.CAP_DSHOW)
                ret: bool
                frame: npt.NDArray[np.uint8]
                ret, frame = vcap.read()
                if ret:
                    """DEBUG
                    self.frame_imshow_for_debug(frame)
                    """
                if ret:
                    live_camera_number = camera_number
                    self.finalize(vcap)
                    break
                if camera_number == 4 and ret is False:
                    self.logger.warning("USBカメラの受信が出来ません")
                    self.logger.warning("以下のエラーをシステム管理者へお伝えください")
                    self.logger.warning("-" * 20)
                    self.logger.warning(format_exc(limit=None, chain=True))
                    self.logger.exception("USBカメラとの通信に異常が発生しました")
                    self.logger.warning("-" * 20)
                    self.logger.warning("終了します")
                    self.finalize(vcap)
                    exit(0)
            # print(f'live_camera_number: {live_camera_number}')
            vcap = cv2.VideoCapture(live_camera_number)
            return vcap
        else:
            vcap = cv2.VideoCapture(self.movie)
            # # debug
            # if vcap.isOpened():
            #     print("VideoCaptureオブジェクトが正しく開かれています。")
            # else:
            #     print("VideoCaptureオブジェクトが開かれていません。")
            # import os
            # current_directory = os.getcwd()
            # print("現在の作業ディレクトリ:", current_directory)
            return vcap

    def finalize(self, vcap) -> None:
        """Release vcap and Destroy window.

        Args:
            vcap (cv2.VideoCapture): vcap which is handle of input video process
        """
        self.vcap = vcap
        self.vcap.release()
        cv2.destroyAllWindows()

    # @lru_cache(maxsize=None)
    def frame_generator(
        self,
        CONFIG: Dict
    ) -> Generator:
        """Generator: Return resized frame data.

        Args:
            CONFIG (Dict): CONFIG

        Raises:
            StopIteration: `ret` == False, then raise `StopIteration`

        Yields:
            Generator: Resized frame data (npt.NDArray[np.uint8])
        """
        self.CONFIG: Dict = CONFIG

        """Initial values"""
        frame_skip_counter: int
        set_width: int = self.CONFIG["set_width"]
        set_height: int = self.CONFIG["set_height"]
        movie: str = self.CONFIG["movie"]
        set_area: str = self.CONFIG["set_area"]

        ret: bool
        # vcap
        frame: npt.NDArray[np.uint8]

        # RootDir: str = self.CONFIG["RootDir"]
        # chdir(RootDir)  # Not use

        # Calculate coordinates of corners: Tuple[int,int,int,int] for 'angle of view'.
        TOP_LEFT: Tuple[int, int, int, int]
        TOP_RIGHT: Tuple[int, int, int, int]
        BOTTOM_LEFT: Tuple[int, int, int, int]
        BOTTOM_RIGHT: Tuple[int, int, int, int]
        CENTER: Tuple[int, int, int, int]

        TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT, CENTER = \
            self._cal_angle_coordinate(
                self.CONFIG["height"],
                self.CONFIG["width"]
            )

        if (movie == 'usb' or movie == 'USB'):   # USB カメラ読み込み時使用
            camera_number: int = 0
            live_camera_number: int = 0
            for camera_number in range(-1, 5):
                vcap = cv2.VideoCapture(camera_number)
                ret, frame = vcap.read()
                if ret:
                    live_camera_number = camera_number
                    break
            # TODO: #39 変数camera_numberの挙動が奇妙。-1は本当か、なぜログ出力が5行もでる？
            self.logger.info(f'CAMERA DEVICE NUMBER: {camera_number}')
            while vcap.isOpened():
                # frame_skipの数値に満たない場合は処理をスキップ
                for frame_skip_counter in range(1, self.CONFIG["frame_skip"]):
                    ret, frame = vcap.read()
                    if frame_skip_counter < self.CONFIG["frame_skip"]:
                        continue
                    if ret == False:
                        self.logger.warning("ERROR OCURRED\nREPORTED BY FACE01")
                        self.logger.warning("-" * 20)
                        self.logger.warning(format_exc(limit=None, chain=True))
                        self.logger.warning("-" * 20)
                        self.finalize(vcap)
                    break
                else:
                    # 画角値をもとに各frameを縮小
                    # python版
                    frame = self._angle_of_view_specification(set_area, frame, TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT, CENTER)  # type: ignore
                    # 各frameリサイズ
                    resized_frame = self.resize_frame(set_width, set_height, frame)
                    """DEBUG
                    self.frame_imshow_for_debug(resized_frame)
                    """
                    yield resized_frame

        elif 'http' in movie:  # http通信を行う場合
            """see bellow
            [Panasonic製ネットワークカメラの画像を取得して顔検出をしてみる](https://qiita.com/mix_dvd/items/a0bdbe0ba628d5282639)
            [Python, Requestsの使い方](https://note.nkmk.me/python-requests-usage/)
            """
            url = movie
            # 画像の取得
            try:
                # responseの内容について分岐
                while True:
                    # frame_skipの数値に満たない場合は処理をスキップ
                    for frame_skip_counter in range(1, self.CONFIG["frame_skip"]):
                        response = requests.get(url, auth = HTTPDigestAuth(self.CONFIG["user"], self.CONFIG["passwd"]))
                        # print(f'response: {response}')
                        if frame_skip_counter < self.CONFIG["frame_skip"]:
                            continue
                    # {'Status': '200', 'Connection': 'Close', 'Set-Cookie': 'Session=0', 'Accept-Ranges': 'bytes',
                    #  'Cache-Control': 'no-cache', 'Content-length': '40140', 'Content-type': 'image/jpeg'}
                    # if response.headers['Status'] == '200' and response.headers['Content-type'] == 'image/jpeg':
                    if response.headers['Content-type'] == 'image/jpeg':
                        # 取得した画像データをOpenCVで扱う形式に変換
                        img_bin = BytesIO(response.content)
                        img_pil = Image.open(img_bin)
                        img_np  = np.asarray(img_pil)
                        frame  = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGR)
                        """DEBUG
                        cv2.imshow("video_capture_DEBUG", frame)
                        cv2.moveWindow("video_capture_DEBUG", 0,0)
                        cv2.waitKey(5000)
                        cv2.destroyAllWindows()
                        exit(0)
                        """
                        # 画角値をもとに各frameを縮小
                        # python版
                        frame = self._angle_of_view_specification(set_area, frame, TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT, CENTER)
                        # 各frameリサイズ
                        resized_frame = self.resize_frame(set_width, set_height, frame)
                        """DEBUG
                        cv2.imshow("video_capture_DEBUG", frame)
                        cv2.moveWindow("video_capture_DEBUG", 0,0)
                        cv2.waitKey(500)
                        cv2.destroyAllWindows()
                        """
                        try:
                            yield resized_frame
                        except TypeError as e:
                            self.logger.warning(e)
                        except Exception as e:
                            self.logger.warning(e)
                        finally:
                            yield resized_frame
                    else:
                        self.logger.warning("以下のエラーをシステム管理者へお伝えください")
                        self.logger.warning(f"ステータスコード: {response.headers['Status']}")
                        self.logger.warning(f"コンテントタイプ: {response.headers['Content-type']}")
                        self.logger.warning("-" * 20)
                        self.logger.warning(format_exc(limit=None, chain=True))
                        self.logger.warning("-" * 20)
                        exit(0)
            except:
                self.logger.warning("以下のエラーをシステム管理者へお伝えください")
                self.logger.warning("-" * 20)
                self.logger.warning(format_exc(limit=None, chain=True))
                self.logger.exception("通信に異常が発生しました")
                self.logger.warning("-" * 20)
                self.logger.warning("終了します")
                exit(0)

        else:  # RTSPの場合は通常のテスト動画と同じ
            vcap = cv2.VideoCapture(movie)
            # vcap = cv2.VideoCapture(movie, cv2.CAP_FFMPEG)

            cnt: int = 1
            debug_num:int = 1
            while vcap.isOpened():

                ret, frame = vcap.read()
                """DEBUG"""
                # self.frame_imshow_for_debug(frame)

                # frame_skipの数値に満たない場合は処理をスキップ
                if cnt < self.CONFIG["frame_skip"]:
                    cnt += 1
                    continue
                cnt = 0

                if ret == False:
                    self.logger.warning("ERROR OCURRED")
                    self.logger.warning("DATA RECEPTION HAS ENDED")
                    self.logger.warning("-" * 20)
                    self.logger.warning(format_exc(limit=None, chain=True))
                    self.logger.warning("-" * 20)
                    self.finalize(vcap)
                    raise StopIteration()
            # else:
                if ret == True:
                    """C++実装試験
                    # frame = frame.astype(dtype='float64')
                    size(frame.shape, frame.strides, set_area, frame, TOP_LEFT)
                    """
                    # 画角値をもとに各frameを縮小
                    # python版
                    angle_frame = self._angle_of_view_specification(
                            set_area,
                            frame,
                            TOP_LEFT,
                            TOP_RIGHT,
                            BOTTOM_LEFT,
                            BOTTOM_RIGHT,
                            CENTER
                        )

                    # 各frameリサイズ
                    resized_frame = self.resize_frame(set_width, set_height, angle_frame)
                    """DEBUG"""
                    # self.frame_imshow_for_debug(resized_frame)

                    yield resized_frame

                elif ret == False:
                    self.finalize(vcap)


"""Reference
- [imreadで返される配列について](https://qiita.com/Castiel/items/53ecbee3c06b9d92759e)
    cv2.imreadで読み込んだframe変数について。
    > 3次元配列が出力されていることがわかる．この配列をA×B×3次元配列とする．
    > Aは画素の行数であり，Bは画素の列数である
    > (読み込む画像のサイズによって，行列のサイズは変わるため変数A，Bとした)．3は，RGBの輝度である．
    > 上の画像において，輝度が縦に大量に並んでいるが，これは
    > [[[0行0列目の輝度]~[0行B列目の輝度]]~[[A行0列目の輝度]~[A行B列目の輝度]]]の順に並んでいる．
    > (画像において0行0列目は，左上)
    > よって，imreadで返される配列とは，画素の輝度を行列の順に格納したものである

    > imreadで返された配列の顔画像の部分(顔画像の左上の行列から，右下の行列までの**区分行列**（ブロック行列）の輝度)
    > だけを取り出すことで，切り取ることができた．

- [NumPyの軸(axis)と次元数(ndim)とは何を意味するのか](https://deepage.net/features/numpy-axis.html)
"""
