"""License for the Code.

Copyright Owner: Yoshitsugu Kesamaru
Please refer to the separate license file for the license of the code.
"""

"""Load preset images."""
import os
from os.path import exists, isdir
from pathlib import Path
from shutil import move

from typing import List, Tuple

import numpy as np
import numpy.typing as npt
from face01lib.api import Dlib_api  # type: ignore
from face01lib.logger import Logger  # type: ignore
from face01lib.utils import Utils  # type: ignore
from face01lib.Calc import Cal


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
        Cal().cal_specify_date(self.logger)


    def load_preset_image(
            self,
            deep_learning_model: int,
            RootDir: str,
            preset_face_imagesDir: str,
            upsampling: int = 0,
            jitters:int = 100,
            mode: str = 'hog',
            model: str = 'small'
        ) -> Tuple[List, List]:
        """Load face image from preset_face_images folder.

        Args:
            deep_learning_model (int): You can select from 0 or 1. 0 is Dlib, 1 is Efficientnetv2_arcface.onnx.
            RootDir (str): Root directory. npKnown.npzが作成されるディレクトリ。
            preset_face_imagesDir (str): Path to preset_face_images folder. pngファイルが存在するディレクトリ。
            upsampling (int, optional): Value of upsampling. Defaults to 0.
            jitters (int, optional): Value of jitters. Defaults to 100.
            mode (str, optional): You can select from hog or cnn. Defaults to 'hog'.
            model (str, optional): You cannot modify this value.

        Returns:
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

        
        # Initialize
        known_face_names_list: List[str] = []
        known_face_encodings_list: List[np.ndarray] = []
        new_files: List = []
        cnt: int = 1  # cnt：何番目のファイルかを表す変数
        cd: bool = False

        if cd == False:
            os.chdir(self.RootDir)
            cd = True

        self.logger.info("Loading npKnown.npz")
        
        # npKnown.npzがdeep_learning_modelに合致しているかチェックする
        if exists("npKnown.npz"):
            if deep_learning_model == 1:
                # npKnown.npzファイルから配列をロード
                with np.load('npKnown.npz') as data:
                    keys = data.files  # 配列の名前のリストを取得
                # キーの存在をチェックする変数
                has_efficientnetv2_arcface = 'efficientnetv2_arcface.npy' in keys
                # has_name = 'name.npy' in keys

                # 条件をチェック
                if has_efficientnetv2_arcface == False:
                    self.logger.error('npKnown.npz file is corrupted. Create again.')
                    # npKnown.npzファイルを削除
                    os.remove('npKnown.npz')

        ###################### npKnown.npzの有る無しで処理を分岐させる ######################
        # ============= npKnown.npzファイルが存在する場合の処理 ===============
        if exists("npKnown.npz"):

            # npKnown.npzの読み込みを行い、今までの全てのデータを格納する
            npKnown = np.load('npKnown.npz', allow_pickle = True)
            if 'dlib' in npKnown:
                # deep_learning_modelが0の場合はdlibのデータを読み込むが、1の場合はエラーを表示する
                if self.deep_learning_model == 0:
                    known_face_names_ndarray = npKnown['name']
                    known_face_encodings_ndarray = npKnown['dlib']
                else:
                    self.logger.error("Mismatch between deep_learning_model and npKnown.npz content. The deep_learning_model is set to 0 (dlib model), but the npKnown.npz contains data for a different model.")
                    exit(1)
            elif 'efficientnetv2_arcface' in npKnown:
                # deep_learning_modelが1の場合はefficientnetv2_arcfaceのデータを読み込むが、0の場合はエラーを表示する
                if self.deep_learning_model == 1:
                    known_face_names_ndarray = npKnown['name']
                    known_face_encodings_ndarray = npKnown['efficientnetv2_arcface']
                else:
                    self.logger.error("Mismatch between deep_learning_model and npKnown.npz content. The deep_learning_model is set to 1 (efficientnetv2_arcface model), but the npKnown.npz contains data for a different model.")
                    exit(1)
            else:
                error_msg = "Unable to use npKnown.npz due to a mismatch between deep_learning_model and the file content. " \
                    "The deep_learning_model is set to a different value or the file contains data for a different model."
                self.logger.error(error_msg)

            # ############ 各配列の整形（ndarray型からリスト型へ変換する） ############
            known_face_names_list = known_face_names_ndarray.tolist()

            list = []
            for i in known_face_encodings_ndarray:
                list.append(i)
                # for x in i:
                #     list.append(x)
            known_face_encodings_list = list
            # #########################################################################

            # preset_face_imagesフォルダ内の全てのファイル名を読み込む
            os.chdir(self.preset_face_imagesDir)
            # まずself.preset_face_imagesDirのファイル名を全て得る
            for preset_face_image in os.listdir(self.preset_face_imagesDir):
                # <DEBUG>
                # if 'テスト' in preset_face_image:
                #     if not preset_face_image in known_face_names:
                #         print(preset_face_image)
                #     exit()
                # 関係ないファイルやフォルダは処理からとばす
                if preset_face_image == 'desktop.ini':
                    continue
                if isdir(preset_face_image):
                    continue
                if 'debug' in preset_face_image:
                    continue
                if 'npKnown.npz' in preset_face_image:
                    continue
                # もし画像ファイル以外だった場合、continueする
                if not preset_face_image.endswith('.jpg') and not preset_face_image.endswith('.jpeg') and not preset_face_image.endswith('.png'):
                    continue
                # all_preset_face_images.append(preset_face_image)

                # =============== file名がnpKnownのキーに存在していない場合の処理 ===============
                if not preset_face_image in known_face_names_list:
                    # preset_face_imageはknown_face_names配列にないから、new_fileに名前を変える
                    new_file: str = preset_face_image

                    new_file_face_image: npt.NDArray[np.uint8] = \
                        Dlib_api_obj.load_image_file(
                                new_file
                            )

                    new_file_face_locations: List[Tuple[int,int,int,int]] = \
                        Dlib_api_obj.face_locations(
                                new_file_face_image,
                                self.upsampling,
                                self.mode
                            )

                    # 顔検出できなかった場合hogからcnnへチェンジして再度顔検出する
                    if len(new_file_face_locations) == 0:
                        if self.mode == 'hog':
                            self.logger.info("Face could not be detected. Temporarily switch to 'cnn' mode")
                            new_file_face_locations = Dlib_api_obj.face_locations(
                                new_file_face_image, self.upsampling, 'cnn')
                            # cnnでも顔検出できない場合はnoFaceフォルダへファイルを移動する
                            self.logger.info(f"{cnt} No face detected in registered face image {new_file}(CNN mode).  Move it to the 'noFace' folder")
                            # `noFace`フォルダが存在しない場合は作成する
                            if not exists('../noFace'):
                                os.mkdir('../noFace')
                                self.logger.info("Create 'noFace' folder")
                            try:
                                move(new_file, '../noFace/')
                            except Exception as e:
                                # # 移動先のファイルが存在する場合は削除する
                                # if os.path.exists('../noFace/' + new_file):
                                #     os.remove('../noFace/' + new_file)
                                #     # ファイルを移動する
                                    # move(new_file, '../noFace/')
                                self.logger.error(e)
                                os.remove('../noFace/' + new_file)
                                move(new_file, '../noFace/')

                            self.mode = 'hog'
                            self.logger.info('Back to HOG mode')

                    # new_file顔画像のエンコーディング処理：array([encoding 配列])
                    self.logger.info(f"{cnt} Encoding {new_file}")

                    new_file_face_encodings: List[npt.NDArray] = []
                    # Dlib使用時の顔画像のエンコーディング処理
                    if self.deep_learning_model == 0:
                        new_file_face_encodings = Dlib_api_obj.face_encodings(
                            deep_learning_model=0,
                            resized_frame=new_file_face_image,
                            face_location_list=new_file_face_locations,
                            num_jitters=self.jitters,
                            model=self.model
                            )
                    # efficientnetv2_arcface.onnx使用時の顔画像のエンコーディング処理
                    elif self.deep_learning_model == 1:
                        new_file_face_encodings = Dlib_api_obj.face_encodings(
                            deep_learning_model=1,
                            resized_frame=new_file_face_image,
                            face_location_list=new_file_face_locations,
                            num_jitters=self.jitters,
                            model=self.model
                            )
                    
                    # CPU温度が設定温度を超過していたら待機
                    Utils_obj.temp_sleep()
                    
                    if len(new_file_face_encodings) > 1:  # 複数の顔が検出された時
                        self.logger.info(f"{cnt} Multiple faces detected in registered face image  {new_file}. Move it to noFace folder.")
                        # もしnoFaceフォルダに同じファイル名が存在したら削除する
                        if os.path.exists('../noFace/' + new_file):
                            os.remove('../noFace/' + new_file)
                        # もし`new_file`自体がカレントディレクトリに存在しない場合、`continue`する
                        if not os.path.exists(new_file):
                            self.logger.error(f"{new_file} does not exist in the current directory. Skip it.")
                            continue
                        move(new_file, '../noFace/')
                    elif len(new_file_face_encodings) == 0:  # 顔が検出されなかった時
                        self.logger.info(f"{cnt} No face detected in registered face image {new_files}. Move it to noFace folder.")
                        try:
                            move(new_file, '../noFace/' + new_file)
                        except:
                            pass

                    # エンコーディングした顔画像だけ新しい配列に入れる
                    if len(new_file_face_encodings) == 1:
                        known_face_names_list.append(new_file)
                        known_face_encodings_list.append(new_file_face_encodings[0])

                    cnt += 1

        # ============= npKnown.npzファイルが存在しない場合の処理 =============
        elif not exists("npKnown.npz"):
            # os.chdir(self.RootDir)
            os.chdir(self.preset_face_imagesDir)
            # os.chdir(os.path.join(self.RootDir, self.preset_face_imagesDir))
            # まずself.preset_face_imagesDirのファイル名を全て得る
            for preset_face_image_filename in os.listdir(self.preset_face_imagesDir):
                # # 関係ないファイルやフォルダは処理からとばす
                # if preset_face_image_filename == 'desktop.ini':  # desktop.iniは処理をとばす
                #     continue
                # if isdir(preset_face_image_filename):  # フォルダの場合は処理をとばす
                #     continue
                # if 'debug' in preset_face_image_filename:  # ファイル名にdebugを含む場合は処理をとばす
                #     continue
                # preset_face_image_filenameがpngファイル以外の場合は処理をとばす
                if not preset_face_image_filename.endswith("png"):
                    continue

                # それぞれの顔写真について顔認証データを作成する
                preset_face_img = \
                    Dlib_api_obj.load_image_file(
                            preset_face_image_filename
                        )

                preset_face_img_locations = \
                    Dlib_api_obj.face_locations(
                            preset_face_img,
                            self.upsampling,
                            self.mode
                        )
                
                # CPU温度が設定温度を超過していたら待機
                Utils_obj.temp_sleep()

                # 得られた顔データについて顔写真なのに顔が判別できない場合や複数の顔がある場合はcnnモードで再確認し、それでもな場合はnoFaceフォルダに移動する
                noFace_file = '../noFace/' + preset_face_image_filename

                if len(preset_face_img_locations) == 0 or len(preset_face_img_locations) > 1:
                    
                    if self.mode == 'hog':

                        self.logger.info('No face detected or multiple face detected. Temporarily switch to cnn mode')
                        
                        # CNNモードにて顔検出を行う
                        preset_face_img_locations = \
                            Dlib_api_obj.face_locations(
                                    preset_face_img, self.upsampling,
                                    'cnn'
                                )
                        # CPU温度が設定温度を超過していたら待機
                        Utils_obj.temp_sleep()

                        # cnnでも顔検出できない場合はnoFaceフォルダへファイルを移動する
                        if len(preset_face_img_locations) == 0 or len(preset_face_img_locations) > 1:
                            
                            self.logger.info(f"{cnt} (CNN mode) Registered face image {preset_face_image_filename}, No face detected or multiple face detected. Move it to noFace folder.")
                            
                            if exists(noFace_file):
                                os.remove(noFace_file)
                            
                            move(preset_face_image_filename, '../noFace/')
                            
                            self.mode = 'hog'
                            
                            self.logger.info('Back to HOG mode')

                # 得られた顔データ（この場合は顔ロケーション）を元にエンコーディングする：array([encoding 配列])
                self.logger.info(f"{cnt} Encoding {preset_face_image_filename}")

                preset_face_image_encodings = \
                    Dlib_api_obj.face_encodings(
                            self.deep_learning_model,
                            preset_face_img,
                            preset_face_img_locations,
                            self.jitters,
                            'small'
                        )
                # CPU温度が設定温度を超過していたら待機
                Utils_obj.temp_sleep()

                # エンコーディングした顔写真について複数顔や顔がない場合はnoFaceフォルダへ移動する
                if len(preset_face_image_encodings) > 1:  # 複数の顔が検出された時
                    
                    self.logger.info(f"{cnt} Multiple faces detected in registered face image {preset_face_image_filename}. Move it to noFace folder.")
                    if exists(noFace_file):
                        os.remove(noFace_file)
                    try:
                        move(preset_face_image_filename, '../noFace/')
                    except:
                        pass
                elif len(preset_face_image_encodings) == 0:  # 顔が検出されなかった時
                    self.logger.info(f"{cnt} No face detected in registered face image {preset_face_image_filename}. Move it to noFace folder.")
                    if exists(noFace_file):  # noFaceフォルダに同じ名前のファイルがある場合は削除する
                        os.remove(noFace_file)
                    try:
                        move(preset_face_image_filename, '../noFace/')
                    except:
                        """TODO"""
                        pass
                    continue

                # 配列に、名前やエンコーディングデータを要素として追加する
                # FACE01GRAPHICS本体の方では要素にndarrayを含むListを返り値として期待している(Dlib_api_obj APIにそう書いてある)
                known_face_names_list.append(preset_face_image_filename)
                known_face_encodings_list.extend(preset_face_image_encodings[0])
                # known_face_encodings_list.append(preset_face_image_encodings[0])

                cnt += 1

        ###################### savezで保存 ######################
        os.chdir(self.RootDir)
        # print('debug_npKnown.npzを作成します')
        if self.deep_learning_model == 0:
            np.savez(
                'npKnown',
                name=known_face_names_list,
                dlib=known_face_encodings_list
            )
        elif self.deep_learning_model == 1:
            np.savez(
                'npKnown',
                name=known_face_names_list,
                efficientnetv2_arcface=known_face_encodings_list
            )

        if known_face_encodings_list:
            print(type(known_face_encodings_list[0]))

        # ################### リスト型を返す ###################
        # <DEBUG>

        # list=[]
        # for i in known_face_encodings:  ## shape:(677, 1, 128)
        #     for x in i:
        #         list.append(x)
        # known_face_encodings = list
        return known_face_encodings_list, known_face_names_list

        # #################### 備考 ####################
        # 返り値のknown_face_encodingsと、npKnown.npzから読み込んだknown_face_encodingsとでは
        # もしかしたらデータ型とか？なにかが異なっているのかもしれない。

