__author__ = 'Original code written by Adam Geitgey, modified by YOSHITSUGU KESAMARU'
__email__ = 'y.kesamaru@tokai-kaoninsho.com'
__version__ = '3.04.01'

import importlib.resources


class Models:
    def pose_predictor_five_point_model_location(self):
        with importlib.resources.path(__name__, "shape_predictor_5_face_landmarks.dat") as file_path:
            return str(file_path)

    def dlib_resnet_model_location(self):
        with importlib.resources.path(__name__, "dlib_face_recognition_resnet_model_v1.dat") as file_path:
            return str(file_path)

    def cnn_face_detector_model_location(self):
        with importlib.resources.path(__name__, "mmod_human_face_detector.dat") as file_path:
            return str(file_path)

    def anti_spoof_model_location(self):
        with importlib.resources.path(__name__, "model_float32.onnx") as file_path:
            return str(file_path)

    def JAPANESE_FACE_V1_model_location(self):
        with importlib.resources.path(__name__, "JAPANESE_FACE_V1.onnx") as file_path:
            return str(file_path)
