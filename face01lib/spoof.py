"""Spoof Module.

NOTE:
    This module is experimental.

このモジュールは、顔の特徴点の検出、オブジェクトの検出、およびQRコードの生成に関連する機能を提供します。

主なクラス:
    - Spoof: 顔の特徴点の検出、オブジェクトの検出、およびQRコードの生成を行うメソッドを持つクラス。

主なメソッド:
    - iris: 顔の虹彩を検出し、その特徴点を描画します。
    - obj_detect: オブジェクトを検出し、その特徴点を描画します。
    - make_qr_code: QRコードを生成します。

使用例:
    spoof_obj = Spoof()
    spoof_obj.iris()
    spoof_obj.obj_detect()
    spoof_obj.make_qr_code()

注意:
    - このモジュールは、実験的なものです。

License:
    Copyright Owner: Yoshitsugu Kesamaru
    Please refer to the separate license file for the license of the code.
"""


from enum import Enum

import cv2
import mediapipe as mp
import numpy as np
import pyqrcode
from PIL import ImageFile

# from face01lib.api import Dlib_api
from face01lib.Calc import Cal
from face01lib.Core import Core
from face01lib.Initialize import Initialize
from face01lib.logger import Logger
# from face01lib.models import Dlib_models
from face01lib.return_face_image import Return_face_image
from face01lib.video_capture import VidCap

Cal_obj = Cal()
VidCap_obj = VidCap()
Core_obj = Core()
# Dlib_api_obj = Dlib_api()
Return_face_image_obj = Return_face_image()

ImageFile.LOAD_TRUNCATED_IMAGES = True


# anti_spoof_model: str = Dlib_models().anti_spoof_model_location()
# onnx_session = onnxruntime.InferenceSession(anti_spoof_model)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_objectron = mp.solutions.objectron



class Spoof():
    # 目の状態を表す列挙型
    class EyeState(Enum):
        OPEN = 1
        CLOSED = 2
        BLINKING = 3

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

        Cal_obj.cal_specify_date(self.logger)
        # 顔のランドマークを検出するためのモデルをロード
        mp_face_mesh = mp.solutions.face_mesh  # type: ignore
        self.face_mesh = mp_face_mesh.FaceMesh()

        # 初期状態は目が開いているとする
        self.current_state = self.EyeState.OPEN
        self.previous_state = self.EyeState.OPEN

        # 最初のフレームを処理したかどうかを追跡するフラグ
        self.first_frame_processed = False
        self.blink_counter = 0  # この変数で瞬きの回数をカウント


    # 眼のアスペクト比を計算するプライベート関数
    def _calculate_eye_ratio(self, face_landmarks, eye_landmarks):
        eye_points = np.array([[face_landmarks.landmark[i].x, face_landmarks.landmark[i].y] for i in eye_landmarks])
        # EAR計算
        A = np.linalg.norm(eye_points[1] - eye_points[5])
        B = np.linalg.norm(eye_points[2] - eye_points[4])
        C = np.linalg.norm(eye_points[0] - eye_points[3])
        eye_ratio = (A + B) / (2.0 * C)
        return eye_ratio

    def detect_eye_blinks(self, frame_datas_array, CONFIG) -> bool:
        """Return True if eye blink is detected.

        Args:
            frame_datas_array (array[Dict]): frame_datas_array

        Returns:
            bool: If eye blink is detected, return True. Otherwise, return False.
        """        
        self.frame_datas_array = frame_datas_array
        self.CONFIG = CONFIG
        
        if self.CONFIG["detect_eye_blinks"] == False:
            return False

        # EARの閾値
        EAR_THRESHOLD_CLOSE = self.CONFIG["EAR_THRESHOLD_CLOSE"]  # 目が閉じていると判断する閾値
        EAR_THRESHOLD_OPEN = self.CONFIG["EAR_THRESHOLD_OPEN"]   # 目が開いていると判断する閾値
        # 顔のランドマークを検出
        results = self.face_mesh.process(self.frame_datas_array[0]["img"])

        # 瞬きを検出
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                self.left_eye_ratio = self._calculate_eye_ratio(face_landmarks, [33, 246, 161, 160, 159, 158, 157, 173])
                self.right_eye_ratio = self._calculate_eye_ratio(face_landmarks, [263, 466, 388, 387, 386, 385, 384, 398])

            # 前回の状態を保存
            self.previous_state = self.current_state

            # 状態遷移マトリックスに基づいて目の状態を更新
            if self.left_eye_ratio < EAR_THRESHOLD_CLOSE or self.right_eye_ratio < EAR_THRESHOLD_CLOSE:
                self.current_state = self.EyeState.CLOSED
            elif self.left_eye_ratio > EAR_THRESHOLD_OPEN or self.right_eye_ratio > EAR_THRESHOLD_OPEN:
                self.current_state = self.EyeState.OPEN

            # 最初のフレームの場合、瞬きのカウントをスキップ
            if not self.first_frame_processed:
                self.first_frame_processed = True
                return False

            if self.previous_state == self.EyeState.OPEN and self.current_state == self.EyeState.CLOSED:
                self.blink_counter += 1  # 瞬きを検出したらカウンタを増やす

            if self.blink_counter == self.CONFIG["number_of_blinks"]:  # カウンタが指定数になったらTrueを返す
                self.blink_counter = 0  # カウンタをリセット
                return True

        return False  # それ以外の場合はFalseを返す


    
    def obj_detect(self):
        # For webcam input:
        cap = cv2.VideoCapture(0)
        with mp_objectron.Objectron(static_image_mode=False,
                                    max_num_objects=5,
                                    min_detection_confidence=0.5,
                                    min_tracking_confidence=0.99,
                                    model_name='Shoe') as objectron:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = objectron.process(image)

                # Draw the box landmarks on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.detected_objects:
                    for detected_object in results.detected_objects:
                        mp_drawing.draw_landmarks(
                        image, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
                        mp_drawing.draw_axis(image, detected_object.rotation,
                                            detected_object.translation)
                # Flip the image horizontally for a selfie-view display.
                cv2.imshow('MediaPipe Objectron', cv2.flip(image, 1))
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        cap.release()


    def make_qr_code(self):
        # Get CONFIG
        CONFIG = Initialize("MAKE_QR_CODE").initialize()
        
        # Make generator
        gen = VidCap_obj.frame_generator(CONFIG)
        
        for _ in range(0, 50):
            resized_frame = VidCap().frame_generator(CONFIG).__next__()
            VidCap_obj.frame_imshow_for_debug(resized_frame)
            frame_datas_array = Core_obj.frame_pre_processing(self.logger, CONFIG, resized_frame)
            encoded_list, frame_datas_array = Core_obj.face_encoding_process(self.logger, CONFIG, frame_datas_array)
            datas_list = Core_obj.frame_post_processing(self.logger, CONFIG, encoded_list, frame_datas_array)
            VidCap_obj.frame_imshow_for_debug(datas_list[0]["img"])
        pass
        url = pyqrcode.create('http://uca.edu')
        url.svg('uca-url.svg', scale=8)
        print(url.terminal(quiet_zone=1))





if __name__ == '__main__':
    # Call main function.
    # Spoof().main()
    pass
