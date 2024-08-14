"""License for the Code.

Copyright Owner: Yoshitsugu Kesamaru
Please refer to the separate license file for the license of the code.

The utils class.

When creating a deep learning model, we usually perform data augmentation processing to increase the base data.
In general, multiple aberrations that occur are mainly corrected by calibration. However, as far as I have seen, heard and experienced, it is "common way" that it is not calibrated (except for strong face recognition). As long as we use the normal model, this leads to a large accuracy loss.

    .. image:: ../docs/img/face_distortion.gif
        :scale: 50%
        :alt: Face distortion. Image taken from https://imgur.com/VdKIQqF

    .. image:: ../docs/img/face_distort_and_model.png
        :scale: 50%
        :alt: Image taken from https://tokai-kaoninsho.com

By using the utils.distort_barrel() method, we believe that we can greatly ensure the robustness of distortion caused by the camera lens.

    .. image:: ../docs/img/woman-1.gif
        :scale: 50%
        :alt: Image taken from https://tokai-kaoninsho.com

    .. image:: ../docs/img/distort_barrel.png
        :scale: 50%
        :alt: Image taken from https://tokai-kaoninsho.com

Note:
    **ImageMagick must be installed on your system.**
    - See ImageMagick https://imagemagick.org/script/download.php
"""

import os
import pathlib
import re
import shutil
import subprocess
import time
from glob import glob
from os import environ
from sys import exit
from traceback import format_exc
from typing import List, Tuple

import cv2
import dlib
import numpy as np
import numpy.typing as npt
from PIL import ImageFile
from tqdm import tqdm

from face01lib.api import Dlib_api
from face01lib.Calc import Cal
from face01lib.logger import Logger
from face01lib.video_capture import VidCap

from .models import Models

VidCap_obj = VidCap()


ImageFile.LOAD_TRUNCATED_IMAGES = True
"""TODO #18 opencvの環境変数変更 要調査"""
# environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"


class Utils:
    """Utils class.

    contains convenience methods
    """
    def __init__(self, log_level: str = 'info') -> None:
        """init.

        Args:
            log_level (str, optional): Receive log level value. Defaults to 'info'.

        Return:
                None
        """
        # Setup logger: common way
        self.log_level: str = log_level
        import os.path
        name: str = __name__
        dir: str = os.path.dirname(__file__)
        parent_dir, _ = os.path.split(dir)

        self.logger = Logger(self.log_level).logger(name, parent_dir)

        Cal().cal_specify_date(self.logger)

        # Dlib
        try:
            from .models import Models
            models_obj = Models()
        except Exception:
            self.logger.error("Failed to import dlib model")
            self.logger.error("-" * 20)
            self.logger.error(format_exc(limit=None, chain=True))
            self.logger.error("-" * 20)
            exit(0)
        self.face_detector = dlib.get_frontal_face_detector()  # type: ignore
        self.predictor_5_point_model = models_obj.pose_predictor_five_point_model_location()
        self.pose_predictor_5_point = dlib.shape_predictor(self.predictor_5_point_model)  # type: ignore

    def get_files_from_path(self, path: str, contain: str = "resize") -> list:
        """Receive path, return files.

        Args:
            path (str): Directory path
            contain (str): Contain word. If you want to get all files, set `*`. Default is `resize`.

        Returns:
            list: Files in received path (absolute path)
        """
        self.path: str = path
        self.contain: str = contain
        if self.contain == '*':
            self.contain = ''

        files: list = []
        files_png: list = []
        files_jpg: list = []
        files_jpeg: list = []
        files_png.append(glob(self.path + "/*" + self.contain + "*" + "*.png"))
        files_jpg.append(glob(self.path + "/*" + self.contain + "*" + "*.jpg"))
        files_jpeg.append(
            glob(self.path + "/*" + self.contain + "*" + "*.jpeg"))
        files = files_png[0] + files_jpg[0] + files_jpeg[0]
        return files

    # Resize to specified size while maintaining aspect ratio
    def align_and_resize_maintain_aspect_ratio(
        self,
        path: str,
        upper_limit_length: int = 1024,
        padding: float = 0.4,
        size: int = 224,
        contain: str = ''
    ) -> List[str]:
        """入力画像をアラインメントしてリサイズ（アスペクト比を維持）.

        Args:
            path (str): ファイル名を含むファイルパス。('.jpg' または '.jpeg' または '.png'。これらは小文字でなければなりません。) パスがディレクトリの場合、そのディレクトリに含まれるすべてのファイルが対象です。
            upper_limit_length (int, optional): 幅の上限長さ。デフォルトは1024。
            padding (float, optional): 顔の周りのパディング。大 = 0.8、中 = 0.4、小 = 0.25、非常に小さい = 0.1。デフォルトは0.4。
            size (int, optional): 画像データのリサイズ後のサイズ。デフォルトは224。
            contain (str, optional): ディレクトリ内のファイル名に含まれる単語。

        Return:
            error_files (list): アラインメントとリサイズに失敗したファイルのリスト。

        Result:
            .. image:: ../docs/img/face_alignment.png
                :scale: 50%
                :alt: Image taken from https://tokai-kaoninsho.com

        Note:
            入力画像ファイルの幅が'1024px'を超える場合、アスペクト比を維持しながら'1024px'にリサイズされます。

        """
        self.path: str = path
        self.upper_limit_length: int = upper_limit_length
        self.padding: float = padding
        self.size: int = size
        self.contain: str = contain

        files: list = []
        error_files: list = []
        if '.jpg' in self.path:
            files.append(self.path)
        elif '.jpeg' in self.path:
            files.append(self.path)
        elif '.png' in self.path:
            files.append(self.path)
        else:
            files: list = self.get_files_from_path(self.path, self.contain)

        for file_path in files:
            # file_name = file_path.split('/')[-1]
            # count faces
            face_cnt: int = 0

            # Load image
            # img: npt.NDArray[np.uint8] = Dlib_api().load_image_file(file_path, mode='RGB')
            try:
                img: npt.NDArray[np.uint8] = dlib.load_rgb_image(
                    file_path)  # type: ignore
            except:
                self.logger.error(file_path + ": cannot load image")
                error_files.append(file_path)
                continue

            # ISSUE #3: Resize input image to 1024px while maintaining aspect ratio.
            if img.shape[0] > self.upper_limit_length or img.shape[1] > self.upper_limit_length:
                img = self.resize_image(img, self.upper_limit_length)
            # DEBUG
            # VidCap_obj.frame_imshow_for_debug(img)

            dets = self.face_detector(img, 1)
            num_faces = len(dets)
            if num_faces == 0:
                # Flip image horizontally
                horizontal_flip_img: np.ndarray = cv2.flip(img, 1)
                if len(self.face_detector(horizontal_flip_img, 1)) == 0:
                    self.logger.error(file_path + ": no face")
                    error_files.append(file_path)
                    # DEBUG
                    # VidCap_obj.frame_imshow_for_debug(horizontal_flip_img)
                    continue

            faces = dlib.full_object_detections()  # type: ignore

            for detection in dets:
                landmark = self.pose_predictor_5_point(img, detection)
                faces.append(landmark)

            # Get a calibrated image
            try:
                images = dlib.get_face_chips(img, faces, self.size, self.padding)  # type: ignore
                # [get_face_chip](http://dlib.net/python/index.html#dlib_pybind11.get_face_chip) about padding.
            except:
                continue

            # img = images[0]
            for img in images:
                img = img[:, :, ::-1]  # bgr to rgb
                cv2.imwrite(file_path + "_" + str(face_cnt) +
                            "_align_resize.png", img)
                face_cnt += 1
        return error_files

    def create_concat_images(
        self,
        img: str,
        size: int = 224
    ) -> None:
        """Create tile images.

        Args:
            img (str): absolute file path
            size (int): image size. Default is 224.

        Result:
            .. image:: ../docs/img/make_concat_image.png
                    :scale: 50%
                    :alt: Image taken from https://tokai-kaoninsho.com

            .. image:: ../docs/img/distort_concat_images.png
                    :scale: 50%
                    :alt: Image taken from https://tokai-kaoninsho.com
        """
        self.img: str = img

        path, file_name = os.path.split(self.img)

        p_append: str = "convert +append"
        m_append: str = "convert -append"
        sp: str = " "
        bk_png: str = "assets/images/224x224.png"
        concat_png: str = "concat.png"
        bb_png: str = "bb.png"

        # pwd = os.getcwd()

        # top-left
        subprocess.run([p_append + sp + self.img + sp + bk_png + sp + concat_png], shell=True)
        subprocess.run([p_append + sp + bk_png + sp + bk_png + sp + bb_png], shell=True)
        subprocess.run([m_append + sp + concat_png + sp + bb_png + sp + path + "/concat_images/" + file_name + "_top_left.png"], shell=True)

        # top_right
        subprocess.run([p_append + sp + bk_png + sp + self.img + sp + concat_png], shell=True)
        subprocess.run([p_append + sp + bk_png + sp + bk_png + sp + bb_png], shell=True)
        subprocess.run([m_append + sp + concat_png + sp + bb_png + sp + path + "/concat_images/" + file_name + "_top_right.png"], shell=True)

        # bottom_left
        subprocess.run([p_append + sp + bk_png + sp + bk_png + sp + bb_png], shell=True)
        subprocess.run([p_append + sp + self.img + sp + bk_png + sp + concat_png], shell=True)
        subprocess.run([m_append + sp + bb_png + sp + concat_png + sp + path + "/concat_images/" + file_name + "_bottom_left.png"], shell=True)

        # bottom_right
        subprocess.run([p_append + sp + bk_png + sp + bk_png + sp + bb_png], shell=True)
        subprocess.run([p_append + sp + bk_png + sp + self.img + sp + concat_png], shell=True)
        subprocess.run([m_append + sp + bb_png + sp + concat_png + sp + path + "/concat_images/" + file_name + "_bottom_right.png"], shell=True)

        # remove
        subprocess.run(["rm" + sp + concat_png + sp + bb_png], shell=True)

    def distort_barrel(
        self,
        dir_path: str,
        align_and_resize_bool: bool = False,
        size: int = 224,
        padding: float = 0.1,
        initial_value: float = -0.1,
        closing_value: float = 0.1,
        step_value: float = 0.1
    ) -> List[str]:
        """Distort barrel.

        Takes a path which contained png, jpg, jpeg files in the directory,
        distort barrel and saves them.

        Args:
            dir_path (str): absolute path of target directory.
            align_and_resize_bool (bool, optional): Whether to align and resize. Defaults to False.
            size (int, optional): Width and height. Defaults to 224.
            padding (float, optional): Padding. Defaults to 0.1.
            initial_value (float): Initial value. Default is -0.1.
            closing_value (float): Closing value. Default is 0.1.
            step_value (float): Step value. Default is 0.1.

        Return:
            Path list of processed files.

        Note:
            **ImageMagick must be installed on your system.**
            - See ImageMagick https://imagemagick.org/script/download.php

        Result:
            .. image:: ../docs/img/distort_barrel.png
                :scale: 50%
                :alt: Image taken from https://tokai-kaoninsho.com
        """
        self.path: str = dir_path
        self.align_and_resize_bool = align_and_resize_bool
        self.size: int = size
        self.padding: float = padding
        self.initial_value: float = initial_value
        self.closing_value: float = closing_value
        self.step_value: float = step_value

        if self.align_and_resize_bool == True:
            self.align_and_resize_maintain_aspect_ratio(
                path=self.path,
                padding=self.padding,
                size=self.size,
            )

        # Create tile images
        os.mkdir(os.path.join(self.path, "concat_images"))

        files: list = []
        files = self.get_files_from_path(self.path, contain='resize')

        for file_path in tqdm(files):
            self.create_concat_images(file_path)

        # Make float list
        value_list = [initial_value]
        while True:
            # Increment value by distortion_value
            self.initial_value += self.step_value
            if self.initial_value == 0.0:
                continue
            if self.initial_value > self.closing_value:
                break
            value_list.append(self.initial_value)

        # Make barrel images
        files = files + \
            self.get_files_from_path(os.path.join(self.path, "concat_images"))

        for file_path in tqdm(files):
            for value in value_list:
                cmd = "convert {} ".format(file_path) + ' -rotate -0'
                barrel_value = " -distort barrel '0.0 0.0 {}'".format(value)
                output_image = ' ' + file_path + \
                    "_lensD_{}".format(value) + ".png"
                cmd = cmd + barrel_value + output_image
                res = subprocess.run([cmd], shell=True)

        self.align_and_resize_maintain_aspect_ratio(
            path=self.path,
            padding=self.padding,
            size=self.size,
            contain='_top_'
        )
        self.align_and_resize_maintain_aspect_ratio(
            path=self.path,
            padding=self.padding,
            size=self.size,
            contain='_bottom_'
        )

        cwp = pathlib.Path(self.path)
        parent_dir = cwp.parent
        face_images: list = glob(self.path + "/*_lensD_*.png_align_resize.png")
        for face_image in face_images:
            shutil.move(face_image, parent_dir)

        # Remove trash files
        shutil.rmtree(self.path)

        # Return file list
        return glob(os.path.join(parent_dir, '*_lensD_*_align_resize.png'))

    def get_jitter_image(
        self,
        dir_path: str,
        num_jitters: int = 10,
        size: int = 224,
        disturb_color: bool = True
    ):
        """Jitter images at the specified path.

        Args:
            dir_path (str): path of target directory.
            num_jitters (int, optional): Number of jitters. Defaults to 10.
            size (int, optional): Resize image to size(px). Defaults to 224px.
            disturb_color (bool, optional): Disturb color. Defaults to True.

        Note:
        This method is based on davisking/dlib/python_example/face_jitter.py.
        https://github.com/davisking/dlib/blob/master/python_examples/face_jitter.py
        """
        self.path = dir_path
        self.num_jitters = num_jitters
        self.size = size
        self.disturb_color = disturb_color
        try:
            models_obj = Models()
        except Exception:
            self.logger.error("Failed to import dlib model")
            self.logger.error("-" * 20)
            self.logger.error(format_exc(limit=None, chain=True))
            self.logger.error("-" * 20)
            exit(0)
        self.face_detector = dlib.get_frontal_face_detector()  # type: ignore
        self.pose_predictor_5_point = dlib.shape_predictor(self.predictor_5_point_model)  # type: ignore
        face_list: list = self.get_files_from_path(self.path, contain='*')
        faces: list = []
        for file_name in tqdm(face_list):
            # Load the image using dlib
            img = dlib.load_rgb_image(file_name)  # type: ignore
            # Ask the detector to find the bounding boxes of each face.
            dets = self.face_detector(img)
            num_faces = len(dets)
            if num_faces == 0:
                continue
            # Find the 5 face landmarks we need to do the alignment.
            faces = dlib.full_object_detections()  # type: ignore
            for detection in dets:
                faces.append(self.pose_predictor_5_point(img, detection))
            # Get the aligned face image and show it
            image = dlib.get_face_chip(img, faces[0], size=self.size, padding=0.4)  # type: ignore
            # Jitter images with data augmentation
            jittered_images = dlib.jitter_image(image, num_jitters=self.num_jitters, disturb_colors=self.disturb_color)  # type: ignore
            # Save jittered images
            for i, jittered_image in (enumerate(jittered_images)):
                # save image
                cv2.imwrite(file_name + "_jitter_{}.png".format(i), jittered_image)

    def get_face_encoding(
        self,
        deep_learning_model: int,
        image_path: str,
        num_jitters: int = 0,
        number_of_times_to_upsample: int = 0,
        mode: str = 'cnn',
        model: str = 'small'
    ):
        # ) -> npt.NDArray[np.float32] or None:
        """get_face_encoding : get face encoding from image file.

        Args:
            deep_learning_model (int): dli model: 0, efficientnetv2_arcface model: 1
            image_path (str): image file path.
            num_jitters (int, optional): Number of jitters. Defaults to 0.
            number_of_times_to_upsample (int, optional): Number of times to upsample the image looking for faces. Defaults to 0.
            mode (str, optional): cnn or hog. Defaults to 'cnn'.
            model (str, optional): small or large. Defaults to 'small'.

        Returns:
            NDArray data (npt.NDArray[np.float32]): face encoding data or None if not detected face.
        """
        self.deep_learning_model: int = deep_learning_model
        self.image_path: str = image_path
        self.num_jitters: int = num_jitters
        self.number_of_times_to_upsample: int = number_of_times_to_upsample
        self.mode: str = mode
        self.model: str = model

        Dlib_api_obj = Dlib_api()

        dir_file_ndarray = Dlib_api_obj.load_image_file(self.image_path)
        face_locations = Dlib_api_obj.face_locations(
            resized_frame=dir_file_ndarray,
            number_of_times_to_upsample=self.number_of_times_to_upsample,
            mode=self.mode  # default is cnn.
        )
        default_file_data_list: List[npt.NDArray[np.float64]] = Dlib_api_obj.face_encodings(
            deep_learning_model=self.deep_learning_model,
            resized_frame=dir_file_ndarray,
            face_location_list=face_locations,
            num_jitters=self.num_jitters,  # default is 0.
            model=self.model  # default is small.
        )
        # Returns None if no faces are detected.
        if len(default_file_data_list) == 0:
            return None
        return default_file_data_list[0]

    def _get_cpu_temp(self) -> float:
        """Get cpu temperature.

        This method tries to get the temperature of the CPU by running the command 'sensors -u' and using regular expressions to extract the value of 'temp1_input'.
        If it is successful, the temperature is returned, otherwise 0.0 is returned and an error message is output to the log.
        """
        temperature: str
        cmd = ['sensors', '-u']
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        pattern = r'Tctl:\n\s+temp1_input:\s+(\d+\.\d+)'
        match = re.search(pattern, result.stdout.decode())
        if match:
            temperature = match.group(1)
            return float(temperature)
        else:
            self.logger.error("Failed to get cpu temperature")
            cnt: int = 0
            while cnt < 3:
                cnt += 1
                subprocess.run(['notify-send', 'Failed to get cpu temperature'])
                time.sleep(1)
            else:
                return 0.0

    def temp_sleep(
        self,
        temp: float = 80.0,
        sleep_time: int = 60
    ):
        """temp_sleep : sleep time for cpu temperature.

        If the CPU temperature exceeds the value specified by the argument `temp`, it sleeps for the time specified by `sleep_time`.
        If the `sensors` command fails to get the CPU temperature, it will try to execute it 3 times at 1 second intervals. If it still can't get it, exit the program.

        Args:
            temp (float, optional): cpu temperature. Defaults to 80.0.
            sleep_time (int, optional): sleep time. Defaults to 60.

        Returns:
            None

        Note:
            The `sensors` and `notify-send` commands are required to use this method.
            The `sensors` command is included in the `lm-sensors` package.
            The `notify-send` command is included in the `libnotify-bin` package.
        """
        self.temp: float = temp
        self.sleep_time: int = sleep_time
        temperature: float = self._get_cpu_temp()
        if temperature == 0.0:
            exit(0)
        while temperature > self.temp:
            self.logger.info(f"The temperature has exceeded {self.temp} degrees.")
            # print('The temperature has exceeded 80 degrees.')
            subprocess.run(['notify-send', f'The temperature has exceeded {self.temp} degrees.'])
            try:
                subprocess.run(['play', '-q', '-v 1', 'assets/voices/CPU_temp.wav'])
            except:
                pass
            time.sleep(self.sleep_time)
            temperature = self._get_cpu_temp()

    def resize_image(
        self,
        img: np.ndarray,
        upper_limit_length: int = 1024,
    ) -> np.ndarray:
        """resize_image : resize image.

        The input `np.ndarray` format image data is resized to fit the specified width or height. In this process, the aspect ratio is maintained by resizing based on the longer side of the width and height. The default maximum values for width and height are 1024px.

        Args:
            img (np.ndarray): image data.
            upper_limit_length (int, optional): upper limit length. Defaults to 1024.

        Returns:
            np.ndarray: resized image data.
        """
        self.img: np.ndarray = img
        self.upper_limit_length: int = upper_limit_length
        height: int
        width: int
        resized_height: int
        resized_width: int

        from math import gcd

        height, width = self.img.shape[:2]

        if height < upper_limit_length and width < upper_limit_length:
            return self.img

        gcd_value = gcd(height, width)
        aspect_ratio_height: int = height // gcd_value
        aspect_ratio_width: int = width // gcd_value

        if height > width:
            if height > self.upper_limit_length:
                resized_height = self.upper_limit_length
                resized_width = int(resized_height * aspect_ratio_width / aspect_ratio_height)
        else:
            if width > self.upper_limit_length:
                resized_width = self.upper_limit_length
                resized_height = int(resized_width * aspect_ratio_height / aspect_ratio_width)

        return cv2.resize(self.img, (resized_width, resized_height), interpolation=cv2.INTER_AREA)

    # def data_augmentation(
    #         self,
    #         dir_path:str,
    #         size:int=224,
    #         num_jitters:int =10,
    #         initial_value: float = -0.1,
    #         closing_value: float = 0.1,
    #         step_value: float = 0.01,
    #     ):
    #     """Data augmentation.

    #     This method accepts a directory path and recursively loads
    #     the images in that directory for data augmentation.

    #     Args:
    #         dir_path (str): directory path.
    #         size (int, optional): image size. Defaults to 224.
    #         num_jitters (int, optional): number of jitters. Defaults to 10.
    #         initial_value (float, optional): initial value. Defaults to -0.1.
    #         closing_value (float, optional): closing value. Defaults to 0.1.
    #         step_value (float, optional): step value. Defaults to 0.01.

    #     Return:
    #         None

    #     See Also:
    #         `dlib.jitter_image <http://dlib.net/python/index.html#dlib_pybind11.jitter_image>`_
    #     """
    #     self.dir_path: str = dir_path
    #     self.size: int = size
    #     self.num_jitters: int = num_jitters
    #     self.initial_value: float = initial_value
    #     self.closing_value: float = closing_value
    #     self.step_value: float = step_value

    #     self.distort_barrel(
    #             dir_path=self.dir_path,
    #             size=self.size,
    #             initial_value=self.initial_value,
    #             closing_value=self.closing_value,
    #             step_value=self.step_value,
    #         )
    #     self.get_jitter_image(
    #         dir_path=self.dir_path,
    #         num_jitters=self.num_jitters,
    #         size=self.size,
    #         disturb_color=True,
    #         )

    def return_qr_code(self, face_encodings) -> List[np.ndarray]:
        """return_qr_code : return qr code.

        Summary:
            This method returns a QR code based on the face encoding list.

        Args:
            face_encodings (List): face encoding list.

        Returns:
            List: qr code.

        See Also:
            example/make_ID_card.py

        Results:
            .. image:: ../docs/img/ID_card_sample.png
                :scale: 50%
        """
        import qrcode
        import base64
        import pickle
        import lzma
        qr_img_list = []
        for face_encoding in face_encodings:
            self.face_encoding: np.ndarray = face_encodings
            # 配列とそのメタデータ（形状とデータ型）を辞書にパック
            data = {
                'array': face_encoding.tolist(),
                'shape': face_encoding.shape,
                'dtype': str(face_encoding.dtype),
            }

            # データをバイト文字列に変換
            byte_array = base64.b64encode(pickle.dumps(data))
            # 圧縮されたデータのバイト数を表示
            print(f"byte_array data size: {len(byte_array)} bytes")

            # データをlzmaで圧縮
            compressed_data = lzma.compress(byte_array)
            # 圧縮されたデータのバイト数を表示
            print(f"Compressed data size: {len(compressed_data)} bytes")

            # QRコード生成
            qr = qrcode.QRCode(
                version=40,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            qr.add_data(compressed_data)
            qr.make(fit=True)

            qr_img = qr.make_image(fill='black', back_color='white')
            qr_img_list.append(qr_img)

        return qr_img_list
