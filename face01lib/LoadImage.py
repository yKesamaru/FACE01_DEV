"""Load image class."""
import cv2
import numpy as np
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
from typing import Dict, List, Tuple, Union

import numpy.typing as npt

from face01lib.Calc import Cal


class LoadImage:
    """This class include method to load images."""
    def __init__(self, headless: bool, conf_dict: Dict) -> None:
        """Initialize.

        Args:
            headless (bool): Default value (config.ini)
            conf_dict (Dict): Default values (Initialize.py)

        Return:
            None
        """
        self.headless: bool = headless
        self.conf_dict: Dict = conf_dict

        if self.headless is False:
            # それぞれの画像が1度だけしか読み込まれない仕組み
            self.load_telop_image: bool
            self.load_logo_image: bool
            self.load_unregistered_face_image: bool

            self.load_telop_image = False
            self.load_logo_image = False
            self.load_unregistered_face_image = False
        else:
            self.load_telop_image = True
            self.load_logo_image = True
            self.load_unregistered_face_image = True

    def LI(
        self,
        set_height: int,
        set_width: int
    ) -> Tuple[cv2.Mat, ...]:
        """Return values.

        Summary:
            Load images, and return all together in a tuple.

        Args:
            self: self
            set_height (int): Height described in config.ini
            set_width (int): Width described in config.ini

        Returns:
            Tuple.

            - rect01_png (cv2.Mat): Loaded image data as ndarray
            - rect01_NG_png (cv2.Mat): Loaded image data as ndarray
            - rect01_REAL_png (cv2.Mat): Loaded image data as ndarray
            - rect01_SPOOF_png (cv2.Mat): Loaded image data as ndarray
            - rect01_CANNOT_DISTINCTION_png (cv2.Mat): Loaded image data as ndarray
            - resized_telop_image (Union[cv2.Mat, None]): Loaded image data as ndarray
            - cal_resized_telop_nums : Return Tuple or None
            - resized_logo_image (Union[cv2.Mat, None]): Loaded image data as ndarray or None
            - cal_resized_logo_nums (Union[Tuple[int,int,int,int,npt.NDArray[np.float64],npt.NDArray[np.float64]], None]):
            - load_unregistered_face_image (bool): Bool
            - telop_image (Union[cv2.Mat, None]): Loaded image data as ndarray or None
            - logo_image (Union[cv2.Mat, None]): Loaded image data as ndarray or None
            - unregistered_face_image (Union[cv2.Mat, None]): Loaded image data as ndarray or None
        """
        rect01_png: cv2.Mat = cv2.imread("assets/images/rect01.png", cv2.IMREAD_UNCHANGED)
        rect01_NG_png: cv2.Mat = cv2.imread("assets/images/rect01_NG.png", cv2.IMREAD_UNCHANGED)
        rect01_REAL_png: cv2.Mat = cv2.imread("assets/images/rect01_REAL.png", cv2.IMREAD_UNCHANGED)
        rect01_SPOOF_png: cv2.Mat = cv2.imread("assets/images/rect01_SPOOF.png", cv2.IMREAD_UNCHANGED)
        rect01_CANNOT_DISTINCTION_png: cv2.Mat = cv2.imread("assets/images/rect01_CANNOT_DISTINCTION.png", cv2.IMREAD_UNCHANGED)

        # Load Telop image
        telop_image: Union[cv2.Mat, None]
        load_telop_image: bool = True
        orgWidth: int
        ratio: float
        resized_telop_image: Union[cv2.Mat, None]
        cal_resized_logo_nums: Union[Tuple[int,int,int,int,npt.NDArray[np.float64],npt.NDArray[np.float64]], None]
        logo_image: Union[cv2.Mat, None]
        resized_logo_image: Union[cv2.Mat, None]
        unregistered_face_image: Union[cv2.Mat, None]

        if not self.load_telop_image:
            telop_image = cv2.imread(
                "assets/images/telop.png", cv2.IMREAD_UNCHANGED)

            _, orgWidth = telop_image.shape[:2]
            ratio = self.conf_dict["set_width"] / \
                orgWidth / 3  # テロップ幅は横幅を分母として設定

            resized_telop_image = \
                cv2.resize(telop_image, None, fx=ratio, fy=ratio)

            cal_resized_telop_nums = \
                Cal().cal_resized_telop_image(resized_telop_image)
        else:
            resized_telop_image = None
            cal_resized_telop_nums = None
            telop_image = None

        # Load Logo image
        if not self.load_logo_image:
            logo_image = cv2.imread(
                "assets/images/Logo.png", cv2.IMREAD_UNCHANGED)
            load_logo_image = True
            _, logoWidth = logo_image.shape[:2]
            logoRatio = self.conf_dict["set_width"] / logoWidth / 15

            resized_logo_image = \
                cv2.resize(logo_image, None, fx=logoRatio, fy=logoRatio)

            cal_resized_logo_nums = \
                Cal().cal_resized_logo_image(
                    resized_logo_image,
                    set_height,
                    set_width
                )
        else:
            resized_logo_image = None
            cal_resized_logo_nums = None
            logo_image = None

        # Load unregistered_face_image
        if not self.load_unregistered_face_image:
            unregistered_face_image = np.array(Image.open('assets/images/顔画像未登録.png'))
            unregistered_face_image = cv2.cvtColor(unregistered_face_image, cv2.COLOR_BGR2RGBA)
            load_unregistered_face_image = True
        else:
            load_unregistered_face_image = False
            unregistered_face_image = None

        return \
            rect01_png, \
            rect01_NG_png, \
            rect01_REAL_png, \
            rect01_SPOOF_png, \
            rect01_CANNOT_DISTINCTION_png, \
            resized_telop_image, \
            cal_resized_telop_nums, \
            resized_logo_image, \
            cal_resized_logo_nums, \
            load_unregistered_face_image, \
            telop_image, \
            logo_image, \
            unregistered_face_image
