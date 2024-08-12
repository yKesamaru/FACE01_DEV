"""config.ini を読み込み、CONFIG 辞書データを返します.

この関数は、ConfigParser モジュールを使用して 'config.ini' ファイルを読み込み、その内容を辞書として返します。

Returns:
    dict: 設定データを含む CONFIG 辞書。

Note:
    config.ini ファイルについては以下を参照してください:
    https://github.com/yKesamaru/FACE01_DEV/blob/master/docs/config_ini.md#about-configini-file

    詳細については `config_ini.md <..docs/config_ini.md>`_ を参照してください。

    'config.ini' は FACE01 の設定ファイルであり、Python の ConfigParser モジュールを使用しています。[DEFAULT] セクションは標準のデフォルト値を指定しており、この設定は例です。

    'config.ini' を修正する前に、ConfigParser モジュールに精通している必要があります。ConfigParser モジュールについては `ConfigParser module documentation <https://docs.python.org/3/library/configparser.html>`_ を参照してください。

    各セクションは [DEFAULT] セクションから継承されます。したがって、各セクションでは [DEFAULT] を上書きする項目（キーと値）のみを指定してください。

.. image:: ../docs/img/About_config_ini_file.png
    :scale: 50%
    :alt: config_ini.md

"""

import os
from configparser import ConfigParser
from datetime import datetime
from traceback import format_exc
from typing import Dict, List, Tuple

import numpy as np
import numpy.typing as npt

from face01lib.Calc import Cal
from face01lib.load_preset_image import LoadPresetImage
from face01lib.LoadImage import LoadImage
from face01lib.logger import Logger
from face01lib.video_capture import VidCap  # py

vid = VidCap()

# import .vidCap as video_capture  # so


class Initialize:
    """Initialize class.

    Load config.ini, return Dict style.
    """

    def __init__(
        self,
        section: str = 'DEFAULT',
        log_level: str = 'info'
    ) -> None:
        """init.

        Args:
            section (str, optional): Specify section which is defined in config.ini. Defaults to 'DEFAULT'.
            log_level (str, optional): Receive log level value. Defaults to 'info'.
        """
        self.section = section
        self.log_level: str = log_level

        # Setup logger: common way
        import os.path
        name: str = __name__
        dir: str = os.path.dirname(__file__)
        parent_dir, _ = os.path.split(dir)

        self.logger = Logger(self.log_level).logger(name, parent_dir)

        self.parent_dir: str = parent_dir

    def _configure(self) -> Dict:
        """Load conf.ini and return conf_dict dictionary.

        Args:
            self
        Returns:
            Dict: conf_dict
        NOTE:
            deep_learning_model:
                0:dlib_face_recognition_resnet_model_v1.dat,
                1:JAPANESE_FACE_V1.onnx,
                2:mobilefacenet.onnx
            Default: 0 (dlib_face_recognition_resnet_model_v1.dat)
        """
        preset_face_imagesDir: str = f'{self.parent_dir}/preset_face_images/'

        os.chdir(self.parent_dir)

        try:
            conf: ConfigParser = ConfigParser()
            success = conf.read('config.ini', 'utf-8')
            # dict作成
            conf_dict: Dict = {
                'headless': conf.getboolean(self.section, 'headless'),
                'deep_learning_model': int(conf.get(self.section, 'deep_learning_model')),
                'anti_spoof': conf.getboolean(self.section, 'anti_spoof'),
                'output_debug_log': conf.getboolean(self.section, 'output_debug_log'),
                'number_of_crops': int(conf.get(self.section, 'number_of_crops')),
                'log_level': conf.get(self.section, 'log_level'),
                'set_width': int(conf.get(self.section, 'set_width')),
                'similar_percentage': float(conf.get(self.section, 'similar_percentage')),
                'jitters': int(conf.get(self.section, 'jitters')),
                'preset_face_images_jitters': int(conf.get(self.section, 'preset_face_images_jitters')),
                'preset_face_imagesDir': preset_face_imagesDir,
                'upsampling': int(conf.get(self.section, 'upsampling')),
                'mode': conf.get(self.section, 'mode'),
                'frame_skip': int(conf.get(self.section, 'frame_skip')),
                'number_of_people': int(conf.get(self.section, 'number_of_people')),
                'use_pipe': conf.getboolean(self.section, 'use_pipe'),
                'model_selection': int(conf.get(self.section, 'model_selection')),
                'min_detection_confidence': float(conf.get(self.section, 'min_detection_confidence')),
                'person_frame_face_encoding': conf.getboolean(self.section, 'person_frame_face_encoding'),
                'same_time_recognize': int(conf.get(self.section, 'same_time_recognize')),
                'set_area': conf.get(self.section, 'set_area'),
                'movie': conf.get(self.section, 'movie'),
                'user': conf.get(self.section, 'user'),
                'passwd': conf.get(self.section, 'passwd'),
                'rectangle': conf.getboolean(self.section, 'rectangle'),
                'target_rectangle': conf.getboolean(self.section, 'target_rectangle'),
                'draw_telop_and_logo': conf.getboolean(self.section, 'draw_telop_and_logo'),
                'default_face_image_draw': conf.getboolean(self.section, 'default_face_image_draw'),
                'show_overlay': conf.getboolean(self.section, 'show_overlay'),
                'alpha': float(conf.get(self.section, 'alpha')),
                'show_percentage': conf.getboolean(self.section, 'show_percentage'),
                'show_name': conf.getboolean(self.section, 'show_name'),
                'crop_face_image': conf.getboolean(self.section, 'crop_face_image'),
                'frequency_crop_image': int(conf.get(self.section, 'frequency_crop_image')),
                'crop_with_multithreading': conf.getboolean(self.section, 'crop_with_multithreading'),
                'Python_version': conf.get(self.section, 'Python_version'),
                'cpu_freq': conf.get(self.section, 'cpu_freq'),
                'cpu_count': conf.get(self.section, 'cpu_count'),
                'memory': conf.get(self.section, 'memory'),
                'gpu_check': conf.getboolean(self.section, 'gpu_check'),
                'calculate_time': conf.getboolean(self.section, 'calculate_time'),
                'show_video': conf.getboolean(self.section, 'show_video'),
                'RootDir': self.parent_dir,
                'detect_eye_blinks': conf.getboolean(self.section, 'detect_eye_blinks'),
                'number_of_blinks': int(conf.get(self.section, 'number_of_blinks')),
                'EAR_THRESHOLD_CLOSE': float(conf.get(self.section, 'EAR_THRESHOLD_CLOSE')),
                'EAR_THRESHOLD_OPEN': float(conf.get(self.section, 'EAR_THRESHOLD_OPEN')),
            }
            return conf_dict
        except:
            self.logger.warning("config.ini 読み込み中にエラーが発生しました")
            self.logger.exception("conf_dictが正常に作成できませんでした")
            self.logger.warning("以下のエラーをシステム管理者様へお伝えください")
            self.logger.warning("-" * 20)
            self.logger.warning(format_exc(limit=None, chain=True))
            self.logger.warning("-" * 20)
            self.logger.warning("終了します")
            exit(1)

    # Initialize variables, load images
    def initialize(
        self,
    ) -> Dict:
        """Initialize values.

        Returns:
            Dict: CONFIG
            Dictionary of initialized preferences

        Example:
            .. code-block:: python

                CONFIG: Dict =  Initialize("SECTION").initialize()
        """
        self.conf_dict: Dict = self._configure()
        headless: bool = self.conf_dict["headless"]

        # overwrite `log_level`
        self.conf_dict['log_level'] = self.log_level

        known_face_encodings: List[np.ndarray]
        known_face_names: List[str]
        known_face_encodings, known_face_names = \
            LoadPresetImage().load_preset_image(
                self.conf_dict["deep_learning_model"],
                self.conf_dict["RootDir"],
                self.conf_dict["preset_face_imagesDir"]
            )
        # debug: 同一ファイルだった。
        # with open(f'{self.parent_dir}/npKnownなし.txt', 'w') as f:
        #     f.write(str(known_face_names))
        #     f.write(str(known_face_encodings))
        # print(f"known_face_names: {type(known_face_names)}")
        # print(f"known_face_encodings: {type(known_face_encodings)}")

        # set_width,fps,height,width,set_height
        set_width: int
        fps: int
        height: int
        width: int
        set_height: int
        set_width, fps, height, width, set_height = \
            vid.return_movie_property(
                self.conf_dict["set_width"],
                vid.return_vcap(self.conf_dict["movie"])
            )

        tolerance: float = Cal().to_tolerance(
            self.conf_dict["similar_percentage"],
            self.conf_dict["deep_learning_model"]
        )

        LoadImage_obj: LoadImage = LoadImage(
            headless,
            self.conf_dict
        )

        rect01_png: npt.NDArray[np.uint8]
        rect01_NG_png: List[npt.NDArray[np.uint8]]
        rect01_REAL_png: npt.NDArray[np.uint8]
        rect01_SPOOF_png: npt.NDArray[np.uint8]
        rect01_CANNOT_DISTINCTION_png: npt.NDArray[np.uint8]
        resized_telop_image: npt.NDArray[np.uint8]
        cal_resized_telop_nums: Tuple[int, int,
                                      int, int, np.ndarray, np.ndarray]
        resized_logo_image: npt.NDArray[np.uint8]
        cal_resized_logo_nums: Tuple[int, int,
                                     int, int, np.ndarray, np.ndarray]
        load_unregistered_face_image: bool
        telop_image: npt.NDArray[np.uint8]
        logo_image: npt.NDArray[np.uint8]
        unregistered_face_image: npt.NDArray[np.uint8]

        rect01_png, rect01_NG_png, rect01_REAL_png, rect01_SPOOF_png, rect01_CANNOT_DISTINCTION_png, resized_telop_image, cal_resized_telop_nums, resized_logo_image, \
            cal_resized_logo_nums, load_unregistered_face_image, telop_image, logo_image, unregistered_face_image = \
            LoadImage_obj.LI(set_height, set_width)

        # 日付時刻算出
        date = datetime.now().strftime("%Y,%m,%d,%H,%M,%S,%f")  # %f-> マイクロ秒

        # 辞書作成
        init_dict: Dict
        if headless is False:
            init_dict = {
                'known_face_encodings': known_face_encodings,
                'known_face_names': known_face_names,
                'date': date,
                'rect01_png': rect01_png,
                'rect01_NG_png': rect01_NG_png,
                'rect01_REAL_png': rect01_REAL_png,
                'rect01_SPOOF_png': rect01_SPOOF_png,
                'rect01_CANNOT_DISTINCTION_png': rect01_CANNOT_DISTINCTION_png,
                'telop_image': telop_image,
                'resized_telop_image': resized_telop_image,
                'cal_resized_telop_nums': cal_resized_telop_nums,
                'logo_image': logo_image,
                'cal_resized_logo_nums': cal_resized_logo_nums,
                'unregistered_face_image': unregistered_face_image,
                'height': height,
                'width': width,
                'set_height': set_height,
                'tolerance': tolerance,
                'default_face_image_dict': {}
            }
        elif headless is True:
            init_dict = {
                'known_face_encodings': known_face_encodings,
                'known_face_names': known_face_names,
                'date': date,
                'height': height,
                'width': width,
                'set_height': set_height,
                'tolerance': tolerance,
                'default_face_image_dict': {}
            }

        # 辞書結合
        CONFIG: Dict = {**init_dict, **self.conf_dict}

        # ヘッドレス実装
        # if headless == True:
        #     CONFIG['rectangle'] = False
        #     CONFIG['target_rectangle'] = False
        #     CONFIG['show_video'] = False
        #     CONFIG['default_face_image_draw'] = False
        #     CONFIG['show_overlay'] = False
        #     CONFIG['show_percentage'] = False
        #     CONFIG['show_name'] = False
        #     CONFIG['draw_telop_and_logo'] = False
        #     CONFIG['person_frame_face_encoding'] = False
        #     CONFIG['headless'] = True

        os.chdir(CONFIG["RootDir"])

        return CONFIG
