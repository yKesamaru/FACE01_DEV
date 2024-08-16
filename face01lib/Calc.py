"""A module that performs various calculations.

Calculation results are output to log
"""
from datetime import datetime
from functools import wraps
from time import perf_counter
from typing import Tuple

import numpy as np
import numpy.typing as npt
from PIL import Image, ImageDraw, ImageFile, ImageFont
from scipy.optimize import fsolve

from face01lib.logger import Logger

ImageFile.LOAD_TRUNCATED_IMAGES = True


class Cal:
    """Cal class include various calculation methods."""
    HANDLING_FRAME_TIME: float
    HANDLING_FRAME_TIME_FRONT: float
    HANDLING_FRAME_TIME_REAR: float
    x1: int
    y1: int
    x2: int
    y2: int

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

    @staticmethod
    def Measure_processing_time(
        HANDLING_FRAME_TIME_FRONT,
        HANDLING_FRAME_TIME_REAR
    ) -> float:
        """Measurement of processing time (calculation) and output to log.

        Args:
            HANDLING_FRAME_TIME_FRONT (float): First half point
            HANDLING_FRAME_TIME_REAR (float): Second half point
        """
        HANDLING_FRAME_TIME = \
            (HANDLING_FRAME_TIME_REAR - HANDLING_FRAME_TIME_FRONT)  # 小数点以下がミリ秒

        # logger.info(f'Processing time: {round(HANDLING_FRAME_TIME, 3)}[Sec]')

        return HANDLING_FRAME_TIME

    @staticmethod
    def Measure_processing_time_forward() -> float:
        """Measurement of processing time (first half).

        Returns:
            float: First half point
        """
        HANDLING_FRAME_TIME_FRONT = perf_counter()

        return HANDLING_FRAME_TIME_FRONT

    @staticmethod
    def Measure_processing_time_backward() -> float:
        """Measurement of processing time (second half).

        Returns:
            float: Second half point
        """
        HANDLING_FRAME_TIME_REAR: float = perf_counter()

        return HANDLING_FRAME_TIME_REAR

    def Measure_func(self, func):
        """Used as a decorator to time a function."""
        self.func = func

        @wraps(self.func)
        def wrapper(*args, **kargs):
            start: float = perf_counter()
            result = func(*args, **kargs)
            elapsed_time: float = round((perf_counter() - start) * 1000, 2)

            print(f"{func.__name__}.............{elapsed_time}[mSec]")

            return result
        return wrapper

    def cal_specify_date(self, logger) -> None:
        """廃止"""
        # self.logger = logger
        # limit_date = datetime(2025, 12, 1, 0, 0, 0)   # 指定日付
        # today = datetime.now()

        # if today >= limit_date:
        #     self.logger.warning("Trial period expired")
        #     self.logger.warning("If you wish to continue using FACE01, please contact us.")
        #     self.logger.warning("email: y.kesamaru@tokai-kaoninsho.com")
        #     exit(0)
        # elif today < limit_date:
        #     remaining_days = limit_date - today
        #     if remaining_days.days < 30:
        #         self.logger.info("Remaining days of use: ", str(remaining_days.days))
        #         self.logger.warning(
        #             "If you wish to continue using FACE01, please contact us.")
        #         self.logger.warning("email: y.kesamaru@tokai-kaoninsho.com")

    def cal_resized_telop_image(
        self,
        resized_telop_image: npt.NDArray[np.float64]
    ) -> Tuple[int, int, int, int, npt.NDArray[np.float64], npt.NDArray[np.float64]]:
        """Calculate telop image data.

        Args:
            resized_telop_image (npt.NDArray[np.float64]): Resized telop image data

        Returns:
            Tuple[int,int,int,int,npt.NDArray[np.float64],npt.NDArray[np.float64]]: Tuple

        Example:
            >>> cal_resized_telop_nums = Cal().cal_resized_telop_image(resized_telop_image)
        """
        self.resized_telop_image = resized_telop_image

        x1, y1, x2, y2 = 0, 0, resized_telop_image.shape[1], resized_telop_image.shape[0]
        a = (1 - resized_telop_image[:, :, 3:] / 255)
        b = resized_telop_image[:, :, :3] * \
            (resized_telop_image[:, :, 3:] / 255)
        cal_resized_telop_nums = (x1, y1, x2, y2, a, b)

        return cal_resized_telop_nums

    def cal_resized_logo_image(
        self,
        resized_logo_image: npt.NDArray[np.float64],
        set_height: int,
        set_width: int
    ) -> Tuple[int, int, int, int, npt.NDArray[np.float64], npt.NDArray[np.float64]]:
        """Calculate logo image data.

        Args:
            resized_logo_image (npt.NDArray[np.float64]): Resized logo image data
            set_height (int): Height
            set_width (int): Width

        Returns:
            Tuple[int,int,int,int,npt.NDArray[np.float64],npt.NDArray[np.float64]]: Return tuple

        Example:
            >>> cal_resized_logo_nums = Cal().cal_resized_logo_image(
                    resized_logo_image,
                    set_height,
                    set_width
                )
        """
        self.resized_logo_image: npt.NDArray[np.float64] = resized_logo_image
        self.set_height: int = set_height
        self.set_width: int = set_width

        x1, y1, x2, y2 = set_width - \
            resized_logo_image.shape[1], set_height - \
            resized_logo_image.shape[0], set_width, set_height
        a = (1 - resized_logo_image[:, :, 3:] / 255)
        b = resized_logo_image[:, :, :3] * (resized_logo_image[:, :, 3:] / 255)

        cal_resized_logo_nums: Tuple[int, int, int, int, npt.NDArray[np.float64], npt.NDArray[np.float64]] = \
            (x1, y1, x2, y2, a, b)

        return cal_resized_logo_nums

    def to_tolerance(
        self,
        similar_percentage: float,
        deep_learning_model: int,
    ) -> float:
        """similar_percentageを受け取ってtoleranceを返します.

        Args:
            similar_percentage (float): config.iniで設定されたProbability of similarityの値
            deep_learning_model (int): Deep learning modelを選びます.

        Returns:
            float: tolerance

        Note:
            deep_learning_model:
                0:dlib_face_recognition_resnet_model_v1.dat,
                1:JAPANESE_FACE_V1.onnx,
                2:mobilefacenet.onnx

        Example:
            >>> tolerance: float = Cal().to_tolerance(
                    self.CONFIG["similar_percentage"],
                    self.CONFIG["deep_learning_model"]
                )

        Dlib
            ## 算出式
            ## percentage = -4.76190475*(p*p)+(-0.380952375)*p+100
            ## percentage_example = -4.76190475*(0.45*0.45)+(-0.380952375)*0.45+100
            ## -4.76190475*(p*p)+(-0.380952375)*p+(100-similar_percentage) = 0
            # 式の変更: 2023年9月14日
            # # f(x) = 100 / (1 + exp(-10(x - 0.8)))
            # similar_percentage = 100 / (1 + np.exp(-10*(tolerance - 0.8)))

        JAPANESE_FACE_V1
            ## 算出式
            ## y=-23.71x2+49.98x+73.69
            ## See: https://zenn.dev/ykesamaru/articles/bc74ec27925896#%E9%96%BE%E5%80%A4%E3%81%A8%E7%99%BE%E5%88%86%E7%8E%87
            ## percentage = -23.71*(p*p)+49.98*p+73.69
            ## 0 = -23.71*(p*p)+49.98*p+(73.69-similar_percentage)
        """

        self.similar_percentage: float = similar_percentage
        tolerance: float = 0.0

        if deep_learning_model == 0:
            # 旧式 #########################################
            # tolerance_plus: float = (-1 * (-0.380952375) + np.sqrt((-0.380952375) * (-0.380952375) - 4 * (-4.76190475) * (100 - self.similar_percentage))) / (2 * (-4.76190475))
            # tolerance_minus: float = (-1 * (-0.380952375) - np.sqrt((-0.380952375) * (-0.380952375) - 4 * (-4.76190475) * (100 - self.similar_percentage))) / (2 * (-4.76190475))
            # if -5 < tolerance_plus < 0:
            #     tolerance = tolerance_plus
            # elif 0 < tolerance_minus < 5:
            #     tolerance = tolerance_minus
            # # toleranceの絶対値を得る
            # tolerance = abs(tolerance)
            # return tolerance
            # ##############################################

            # 新式 #########################################
            def equation(tolerance):
                return similar_percentage - 100 / (1 + np.exp(-10 * (tolerance - 0.8)))
            tolerance_solution = fsolve(equation, 0.5)
            return tolerance_solution[0]
            # ##############################################

        elif deep_learning_model == 1:
            tolerance_plus: float = (-1 * 49.98 + np.sqrt(49.98 * 49.98 - 4 * (-23.71) * (73.69 - self.similar_percentage))) / (2 * (-23.71))
            tolerance_minus: float = (-1 * 49.98 - np.sqrt(49.98 * 49.98 - 4 * (-23.71) * (73.69 - self.similar_percentage))) / (2 * (-23.71))
            if 0 < tolerance_plus < 1:
                tolerance = tolerance_plus
            elif 0 < tolerance_minus < 1:
                tolerance = tolerance_minus

        return tolerance

    def to_percentage(
        self,
        tolerance: float,
        deep_learning_model: int,
    ) -> float:
        """Receive 'tolerance' and return 'percentage'.

        Args:
            tolerance (float): tolerance

        Returns:
            float: percentage
        """
        percentage: float = 0.0
        self.tolerance: float = tolerance
        if deep_learning_model == 0:
            percentage: float = -4.76190475*(self.tolerance ** 2)+(-0.380952375) * self.tolerance +100
        elif deep_learning_model == 1:
            percentage: float = -23.71*(self.tolerance ** 2)+49.98*self.tolerance+73.69

        return percentage

    def decide_text_position(
        self,
        error_messg_rectangle_bottom,
        error_messg_rectangle_left,
        error_messg_rectangle_right,
        error_messg_rectangle_fontsize,
        error_messg_rectangle_messg
    ):
        """Not use."""
        self.error_messg_rectangle_bottom = error_messg_rectangle_bottom
        self.error_messg_rectangle_left = error_messg_rectangle_left
        self.error_messg_rectangle_right = error_messg_rectangle_right
        self.error_messg_rectangle_fontsize = error_messg_rectangle_fontsize
        self.error_messg_rectangle_messg = error_messg_rectangle_messg
        error_messg_rectangle_center = int((self.error_messg_rectangle_left + self.error_messg_rectangle_right)/2)
        error_messg_rectangle_chaCenter = int(len(self.error_messg_rectangle_messg)/2)
        error_messg_rectangle_pos = error_messg_rectangle_center - (error_messg_rectangle_chaCenter * self.error_messg_rectangle_fontsize) - int(self.error_messg_rectangle_fontsize / 2)
        error_messg_rectangle_position = (error_messg_rectangle_pos + self.error_messg_rectangle_fontsize, self.error_messg_rectangle_bottom - (self.error_messg_rectangle_fontsize * 2))

        return error_messg_rectangle_position

    def make_error_messg_rectangle_font(
        self,
        fontpath: str,
        error_messg_rectangle_fontsize: str,
        encoding='utf-8'
    ):
        """Not use."""
        self.fontpath = fontpath
        self.error_messg_rectangle_fontsize = error_messg_rectangle_fontsize

        error_messg_rectangle_font = ImageFont.truetype(
            self.fontpath, self.error_messg_rectangle_fontsize, encoding='utf-8')

        return error_messg_rectangle_font

    def return_percentage(
        self,
        distance: float,
        deep_learning_model: int
    ) -> float:  # python版
        """Receive 'distance' and return percentage.

        Args:
            distance (float): distance
            deep_learning_model (int): deep_learning_model

        Returns:
            float: percentage

        NOTE:
            deep_learning_model:
                0:dlib_face_recognition_resnet_model_v1.dat,
                1:JAPANESE_FACE_V1.onnx,
                2:mobilefacenet.onnx

        Example:
            >>> percentage = Cal().return_percentage(distance, deep_learning_model)
        """
        percentage: float = 0.0
        self.distance: float = distance
        if deep_learning_model == 0:
            percentage: float = -4.76190475 *(self.distance**2)-(0.380952375*self.distance)+100
        elif deep_learning_model == 1:
            percentage: float = -23.71*(self.distance**2)+(49.98*self.distance)+73.69

        return percentage

    def pil_img_instance(
        self,
        frame: npt.NDArray[np.uint8]
    ):
        """Generate pil_img object.

        Args:
            frame (npt.NDArray[np.uint8]): Image data

        Returns:
            object: PIL object
        """
        self.frame: npt.NDArray[np.uint8] = frame

        pil_img_obj = Image.fromarray(self.frame)

        return pil_img_obj

    def make_draw_rgb_object(
        self,
        pil_img_obj_rgb
    ):
        """Generate object.

        Args:
            pil_img_obj_rgb (object): object

        Returns:
            object: object
        """
        self.pil_img_obj_rgb = pil_img_obj_rgb

        draw_rgb = ImageDraw.Draw(self.pil_img_obj_rgb)

        return draw_rgb
