"""
Summary:
    このスクリプトは、DAMO-YOLOを使用して画像内の物体を検出するプログラムです。
    指定された画像をモデルに入力し、検出された物体のクラス、スコア、バウンディングボックスを出力します。
    スコアが0.5以上の検出結果のみを表示します。
"""

import numpy as np
import torch
from face01lib.damo_yolo.damo_internal.config.base import parse_config
from face01lib.damo_yolo.damo_internal.detectors.detector import build_local_model
from face01lib.damo_yolo.damo_internal.structures.bounding_box import BoxList
from face01lib.damo_yolo.damo_internal.utils import postprocess
from face01lib.damo_yolo.damo_internal.utils.demo_utils import transform_img
from PIL import Image

# クラスIDからクラス名へのマッピング
COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light",
    "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
    "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
    "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed",
    "dining table", "toilet", "TV", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven",
    "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]


class Infer:
    """
    画像内の物体を検出するための推論クラス。

    Attributes:
        config: モデルの設定ファイル。
        ckpt_path: 学習済みモデルのチェックポイントのパス。
        infer_size: 推論時の画像サイズ（デフォルトは640x640）。
        device: 推論を行うデバイス（デフォルトはCUDA）。
        engine_type: 推論に使用するエンジンタイプ（torch、onnx、tensorRTのいずれか）。
    """
    def __init__(self, config, ckpt_path, infer_size=[640, 640], device='cuda', engine_type='torch'):
        """
        初期化メソッド。

        Args:
            config: モデルの設定ファイル。
            ckpt_path: 学習済みモデルのチェックポイントのパス。
            infer_size: 推論時の画像サイズ（デフォルトは640x640）。
            device: 推論を行うデバイス（デフォルトはCUDA）。
            engine_type: 推論に使用するエンジンタイプ（torch、onnx、tensorRTのいずれか）。
        """
        self.device = device if torch.cuda.is_available() else 'cpu'
        self.config = config
        self.infer_size = infer_size
        self.engine_type = engine_type
        self.model = self._build_model(ckpt_path)

    def _build_model(self, ckpt_path):
        """
        モデルを構築します。

        Args:
            ckpt_path: 学習済みモデルのチェックポイントのパス。

        Returns:
            構築されたモデル。
        """
        print(f'{self.engine_type}エンジンを使用してモデルを構築中...')
        if self.engine_type == 'torch':
            model = build_local_model(self.config, ckpt=ckpt_path, device=self.device)
            # ckpt = torch.load(ckpt_path, map_location=self.device)
            ckpt = torch.load(ckpt_path, map_location=self.device, weights_only=True)  # モデルの重み（パラメータ）のみを使用し、その他のオブジェクト（トレーニングの状態やカスタムクラスのインスタンスなど）は読み込まない。標準出力の警告文回避。
            model.load_state_dict(ckpt['model'], strict=True)
            model.eval()
        elif self.engine_type == 'onnx':
            raise NotImplementedError("この例ではONNXエンジンは未実装です。")
        elif self.engine_type == 'tensorRT':
            raise NotImplementedError("この例ではTensorRTエンジンは未実装です。")
        else:
            raise ValueError(f"サポートされていないエンジンタイプです: {self.engine_type}")
        return model

    def preprocess(self, image_path):
        """
        画像を前処理します。

        Args:
            image_path: 処理対象の画像ファイルのパス。

        Returns:
            前処理後の画像テンソルと元画像の形状。
        """
        origin_img = np.asarray(Image.open(image_path).convert('RGB'))
        img = transform_img(origin_img, 0, **self.config.test.augment.transform, infer_size=self.infer_size)
        img = img.tensors.to(self.device)
        return img, origin_img.shape[:2]

    def postprocess(self, preds, origin_shape):
        """
        推論結果を後処理します。

        Args:
            preds: モデルの推論結果。
            origin_shape: 元画像の形状。

        Returns:
            バウンディングボックス、スコア、クラスインデックスのリスト。
        """
        if self.engine_type == 'torch':
            output = preds
        elif self.engine_type == 'onnx':
            scores = torch.Tensor(preds[0])
            bboxes = torch.Tensor(preds[1])
            output = postprocess(scores, bboxes,
                                 self.config.model.head.num_classes,
                                 self.config.model.head.nms_conf_thre,
                                 self.config.model.head.nms_iou_thre)
        else:
            raise ValueError(f"サポートされていないエンジンタイプです: {self.engine_type}")

        if len(output) > 0:
            output = output[0].resize(origin_shape)
            bboxes = output.bbox.cpu().numpy()
            scores = output.get_field('scores').cpu().numpy()
            cls_inds = output.get_field('labels').cpu().numpy()
        else:
            bboxes, scores, cls_inds = [], [], []

        return bboxes, scores, cls_inds

    def forward(self, image):
        """
        画像を推論します。

        Args:
            image: 推論対象の画像（ファイルパスまたは numpy.ndarray）。

        Returns:
            推論後のバウンディングボックス、スコア、クラスインデックスのリスト。
        """
        with torch.no_grad():  # 推論時に勾配追跡を無効化
            if isinstance(image, str):  # ファイルパスの場合
                origin_img = np.asarray(Image.open(image).convert('RGB'))
            elif isinstance(image, np.ndarray):  # numpy.ndarray の場合
                origin_img = image
            else:
                raise ValueError("`image` はファイルパスまたは numpy.ndarray でなければなりません。")

            # 前処理
            img = transform_img(origin_img, 0, **self.config.test.augment.transform, infer_size=self.infer_size)
            img = img.tensors.to(self.device)

            # 推論
            preds = self.model(img)

            # 後処理
            return self.postprocess(preds, origin_img.shape[:2])



if __name__ == "__main__":
    # モジュールが直接実行された場合のみ以下を実行
    # モデルと設定のパス
    config_file = "configs/damoyolo_tinynasL20_T.py"
    ckpt_path = "pretrained_models/damoyolo_tinynasL20_T_420.pth"

    # 設定の読み込み
    config = parse_config(config_file)
    infer = Infer(config, ckpt_path)

    # 画像の推論
    # image_path = "assets/dog.jpg"
    image_path = "assets/input.png"
    bboxes, scores, cls_inds = infer.forward(image_path)

    # 出力結果をわかりやすく表示（スコアが0.5以上のもののみ出力）
    print("スコアが0.5以上の検出された物体:")
    for bbox, score, cls_ind in zip(bboxes, scores, cls_inds):
        if score >= 0.5:  # スコアが0.5以上の場合のみ表示
            class_name = COCO_CLASSES[int(cls_ind)]  # クラス名を取得
            print(f"物体: {class_name}, スコア: {score:.2f}, バウンディングボックス: {bbox}")
