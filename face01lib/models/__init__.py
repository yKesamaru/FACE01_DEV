__author__ = 'Original code written by Adam Geitgey, modified by YOSHITSUGU KESAMARU'
__email__ = 'y.kesamaru@tokai-kaoninsho.com'
__version__ = '2.2.02'

from pkg_resources import resource_filename


class Models:
    # DATA_PATH = pkg_resources.resource_filename('<package name>', 'data/')
    def pose_predictor_five_point_model_location(self):
        return resource_filename(__name__, "shape_predictor_5_face_landmarks.dat")

    def dlib_resnet_model_location(self):
        return resource_filename(__name__, "dlib_face_recognition_resnet_model_v1.dat")

    def cnn_face_detector_model_location(self):
        return resource_filename(__name__, "mmod_human_face_detector.dat")

    def anti_spoof_model_location(self):
        return resource_filename(__name__, "model_float32.onnx")

    def JAPANESE_FACE_V1_model_location(self):
        return resource_filename(__name__, "JAPANESE_FACE_V1.onnx")
