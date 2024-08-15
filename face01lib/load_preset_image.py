"""顔画像ファイルから`npKnown.npz`ファイルを作成する.

Summary:
    `preset_face_images`ディレクトリを捜査して、`npKnown.npz`ファイルを作成します。
"""

import os
import shutil
import sys
from os.path import exists
from typing import List, Tuple

import numpy as np
import numpy.typing as npt

from face01lib.api import Dlib_api
from face01lib.Calc import Cal
from face01lib.combine import Comb as C
from face01lib.logger import Logger
from face01lib.utils import Utils

# グローバルオブジェクトの初期化
Dlib_api_obj = Dlib_api()
Utils_obj = Utils()


class LoadPresetImage:
    def __init__(
        self,
        log_level: str = "info"
    ) -> None:
        self.log_level = log_level
        # Setup logger
        name: str = __name__
        dir: str = os.path.dirname(__file__)
        parent_dir, _ = os.path.split(dir)

        self.logger = Logger(self.log_level).logger(name, parent_dir)

        # Cal().cal_specify_date(self.logger)  # 廃止

    def _save_as_noKnown(self, known_face_encodings, known_face_names):
        """_save_as_noKnown エンコードされた顔のデータと名前のリストを、npKnown.npzファイルとして保存するメソッド.

        Args:
            known_face_encodings (_type_): エンコードされた顔のデータ
            known_face_names (_type_): 名前のリスト
        """
        if self.deep_learning_model == 0:
            np.savez(
                os.path.join(self.RootDir, 'npKnown'),
                name=known_face_names,
                dlib=known_face_encodings
            )
        elif self.deep_learning_model == 1:
            np.savez(
                os.path.join(self.RootDir, 'npKnown'),
                name=known_face_names,
                efficientnetv2_arcface=known_face_encodings
            )

    # フォルダーの作成
    def _make_folder(self) -> None:
        # `noFace`フォルダが存在しない場合は作成する
        if not exists(os.path.join(self.RootDir, 'noFace')):
            os.mkdir(os.path.join(self.RootDir, 'noFace'))
            self.logger.info("Create 'noFace' folder")
        # `multipleFaces`フォルダが存在しない場合は作成する
        if not exists(os.path.join(self.RootDir, 'multipleFaces')):
            os.mkdir(os.path.join(self.RootDir, 'multipleFaces'))
            self.logger.info("Create 'multipleFaces' folder")

    def _get_known_face_data(self) -> Tuple[List[np.ndarray], List[str]]:
        """既知の顔データをnpKnown.npzからロードするメソッド
        Returns:
            エンコードされた顔の情報と名前のリスト
        """
        known_face_encodings_list: List[np.ndarray] = []
        known_face_names_list: List[str] = []

        # npKnown.npzファイルが存在する場合の処理
        if exists(os.path.join(self.RootDir, "npKnown.npz")):
            npKnown = np.load(
                os.path.join(self.RootDir, 'npKnown.npz'),
                allow_pickle=True
            )
            # npKnown.npzファイルのdeep_learning_modelとself.deep_learning_modelが一致するか確認
            if 'dlib' in npKnown and self.deep_learning_model == 0:
                known_face_encodings_ndarray = npKnown['dlib']
                known_face_names_ndarray = npKnown['name']
            elif 'efficientnetv2_arcface' in npKnown and self.deep_learning_model == 1:
                known_face_encodings_ndarray = npKnown['efficientnetv2_arcface']
                known_face_names_ndarray = npKnown['name']
            else:
                self.logger.error("npKnown.npzとdeep_learning_modelが一致しません。")
                self.logger.error("config.iniのdeep_learning_modelの値を変更し、再度起動して下さい。")
                self.logger.error("終了します。")
                # npKnown.npzファイルを削除する
                os.remove(os.path.join(self.RootDir, 'npKnown.npz'))
                sys.exit(0)
            # ndarrayをlistに変換
            known_face_encodings_list = [i for i in known_face_encodings_ndarray]
            known_face_names_list = known_face_names_ndarray.tolist()
        # npKnown.npzファイルが存在しない場合の処理
        elif not exists("npKnown.npz"):
            face_images_list = self._get_face_images(self.preset_face_imagesDir)
            known_face_encodings_list, known_face_names_list = \
                self._encode_face_images(face_images_list)
        return known_face_encodings_list, known_face_names_list

    def _update_known_face_data(self) -> Tuple[List[np.ndarray], List[str]]:
        """
        npKnown.npzファイルに存在するデータ名リストと顔画像ファイル名リストが異なる場合に
        顔画像ファイルを追加してnpKnown.npzファイルを更新するメソッド
        """
        known_face_encodings: List[np.ndarray] = []
        known_face_names: List[str] = []
        known_face_encodings, known_face_names = self._get_known_face_data()
        face_image_filename_list = self._get_face_images(self.preset_face_imagesDir)
        # known_face_namesをアルファベット順にソート
        known_face_names.sort()
        # face_image_filename_listをアルファベット順にソート
        face_image_filename_list.sort()
        # known_face_namesとface_image_filename_listを比較して、
        # 内容が異なる場合には、npKnown.npzファイルを更新する
        if known_face_names != face_image_filename_list:
            # npKnown.npzファイルを削除する
            os.remove(os.path.join(self.RootDir, 'npKnown.npz'))
            # 顔画像ファイルから顔画像のエンコードリストと顔画像名リストを取得する
            face_encoding_list, face_file_name_list = \
                self._encode_face_images(face_image_filename_list)
            # npKnown.npzファイルとして保存する
            self._save_as_noKnown(face_encoding_list, face_file_name_list)
        else:
            # npKnown.npzファイルに変更はないので、npKnown.npzファイルをロードする
            face_encoding_list, face_file_name_list = self._get_known_face_data()
        return face_encoding_list, face_file_name_list

    # ディレクトリから顔画像ファイルを取得するメソッド
    def _get_face_images(self, dir: str) -> List[str]:
        # 拡張子がpng, jpeg, jpg, webpの場合のみface_images_listに追加
        face_image_filename_list = []  # 顔画像のリストを初期化
        # preset_face_imagesDir内のファイルを一つずつ確認
        for filename in os.listdir(dir):
            # ファイルの拡張子を取得
            extension = os.path.splitext(filename)[1].lower()  # 拡張子を小文字に変換
            # 拡張子がpng, jpeg, jpg, webpのいずれかの場合、リストに追加
            if extension in ['.png', '.jpeg', '.jpg', '.webp']:
                face_image_filename_list = C.comb(
                    face_image_filename_list, [filename])
                # face_image_filename_list.append(filename)
        return face_image_filename_list

    def _encode_face_images(self, face_images_list: List[str]) -> Tuple[List[np.ndarray], List[str]]:
        """_encode_face_images 顔画像エンコードリストと顔画像名リストを返すメソッド

        Args:
            face_images_list (List[str]): ファイルリスト

        Returns:
            Tuple[List[np.ndarray], List[str]]: face_encoding_list, face_image_filename_list
        """
        # フォルダー存在の確認と作成
        self._make_folder()
        # 変数の初期化
        face_encoding_list: List[np.ndarray] = []
        face_file_name_list: List[str] = []
        face_location_list: List[Tuple[int, int, int, int]] = []
        for face_image in face_images_list:
            # 顔画像ファイルを読み込む
            face_image_ndarray: npt.NDArray[np.uint8] = \
                Dlib_api_obj.load_image_file(
                    os.path.join(self.preset_face_imagesDir, face_image)
            )
            # 顔画像ファイルから顔の位置を検出
            face_location_list = Dlib_api_obj.face_locations(
                face_image_ndarray,
                self.upsampling,
                self.mode
            )
            # 顔検出できなかった場合hogからcnnへチェンジして再度顔検出する
            if len(face_location_list) == 0:
                if self.mode == 'hog':
                    self.logger.info(
                        "Face could not be detected. Temporarily switch to 'cnn' mode")
                    face_location_list = Dlib_api_obj.face_locations(
                        face_image_ndarray, self.upsampling, 'cnn')
                    # modeをhogに戻す
                    self.mode = 'hog'
                    self.logger.info('Back to HOG mode')
                    # cnnでも顔検出できない場合はnoFaceフォルダへファイルを移動して次のファイルへ。
                    # ファイルをnoFaceフォルダへ移動
                    if len(face_location_list) == 0:
                        try:
                            shutil.move(face_image, os.path.join(
                                self.RootDir, 'noFace'))  # 既にファイルが存在する場合は上書きされる
                        except:
                            pass
                        self.logger.info(
                            f"No face detected in registered face image {face_image}(CNN mode).  Move it to the 'noFace' folder")
                        continue
                    # ファイルをmultipleFacesフォルダへ移動
                    elif len(face_location_list) > 1:
                        self.logger.info(
                            f"Multiple faces detected in registered face image {face_image}(CNN mode).  Move it to the 'multipleFaces' folder")
                        shutil.move(face_image, os.path.join(
                            self.RootDir, 'multipleFaces'))
                        continue
            # 複数の顔が検出された場合はmultipleFacesフォルダへファイルを移動する
            elif len(face_location_list) > 1:
                self.logger.info(f"Multiple faces detected in registered face image {face_image}.  Move it to the 'multipleFaces' folder")
                shutil.move(face_image, os.path.join(self.RootDir, 'multipleFaces'))  # 既にファイルが存在する場合は上書きされる
                continue
            elif len(face_location_list) == 1:
                # ログ出力
                self.logger.info(f"Encoding {face_image}")
                # Dlib使用時の顔画像のエンコーディング処理
                if self.deep_learning_model == 0:
                    face_encode_data: List[np.ndarray] = Dlib_api_obj.face_encodings(
                        deep_learning_model=0,
                        resized_frame=face_image_ndarray,
                        face_location_list=face_location_list,
                        num_jitters=self.jitters,
                        model=self.model
                    )
                # JAPANESE_FACE_V1.onnx使用時の顔画像のエンコーディング処理
                elif self.deep_learning_model == 1:
                    face_encode_data: List[np.ndarray] = Dlib_api_obj.face_encodings(
                        deep_learning_model=1,
                        resized_frame=face_image_ndarray,
                        face_location_list=face_location_list,
                        num_jitters=self.jitters,
                        model=self.model
                    )
                # self.deep_learning_modelの値が不正な場合
                else:
                    face_encode_data = []
                    # ログ出力
                    self.logger.error("deep_learning_modelの値が不正です。")
                    self.logger.error("Now deep_learning_model: {self.deep_learning_model}}")
                    sys.exit(1)
                face_encoding_list = C.comb(face_encoding_list, face_encode_data)
                face_file_name_list = C.comb(face_file_name_list, [face_image])
            else:
                self.logger.error("face_location_listの値が不正です。")
                self.logger.error("Now face_location_list: {face_location_list}")
                sys.exit(1)
        return face_encoding_list, face_file_name_list

    def load_preset_image(
        self,
        deep_learning_model: int,
        RootDir: str,
        preset_face_imagesDir: str,
        upsampling: int = 0,
        jitters: int = 100,
        mode: str = 'hog',
        model: str = 'small'
    ) -> Tuple[List[np.ndarray], List[str]]:
        """load_preset_image npKnown.npzを作成する.

        Args:
            deep_learning_model (int): 0または1.  0: dlib, 1: JAPANESE FACE V1
            RootDir (str): npKnown.npzを作成するディレクトリ
            preset_face_imagesDir (str): 顔画像が格納されているディレクトリ
            upsampling (int, optional): upsampling値. Defaults to 0.
            jitters (int, optional): jitter値. Defaults to 100.
            mode (str, optional): HOG OR CNN. Defaults to 'hog'.
            model (str, optional): Defaults to 'small'.

        Returns:
            Tuple[List[np.ndarray], List[str]]: npKnown.npzを作成する
            Tuple[List, List]: known_face_encodings_list, known_face_names_list

            - known_face_encodings_list
                - List of encoded many face images as ndarray

            - known_face_names_list
                - List of name which encoded as ndarray

        Example:
            >>> known_face_encodings, known_face_names = LoadPresetImage().load_preset_image(
                    self,
                    self.conf_dict["RootDir"],
                    self.conf_dict["preset_face_imagesDir"]
                )
        """
        self.deep_learning_model = deep_learning_model
        self.RootDir = RootDir
        self.preset_face_imagesDir = preset_face_imagesDir
        self.upsampling = upsampling
        self.jitters = jitters
        self.mode = mode
        self.model = model
        self.logger.info("Loading npKnown.npz")
        self._make_folder()
        # 初期化
        face_encoding_list: List[np.ndarray] = []
        face_image_filename_list: List[str] = []
        if exists(os.path.join(self.RootDir, "npKnown.npz")):
            face_encoding_list, face_image_filename_list = self._update_known_face_data()
        else:
            file_list = self._get_face_images(self.preset_face_imagesDir)
            face_encoding_list, face_image_filename_list = self._encode_face_images(
                file_list)
            self._save_as_noKnown(face_encoding_list, face_image_filename_list)
        return face_encoding_list, face_image_filename_list
