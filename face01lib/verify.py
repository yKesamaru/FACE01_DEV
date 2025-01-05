"""verify.py.

Summary:
    このスクリプトは、2枚の画像を読み込み、JAPANESE_FACE_V1モデルを用いて
    同一人物かどうかを判定するためのコマンドラインツールです。

Usage:
    $ python verify.py <image1> <image2> [--threshold THRESHOLD]

Options:
    -h, --help
        このヘルプメッセージを表示し、プログラムを終了します。
    --threshold THRESHOLD
        0以上1以下の範囲のfloat値。同一人物と判断するためのコサイン類似度のしきい値を指定します。
        指定しない場合のデフォルトは 0.25 です。
        例: --threshold 0.4

License:
    This script is licensed under the terms provided by yKesamaru, the original author.
"""

import argparse
import sys

from face01lib.api import Dlib_api


def check_image_path(path: str) -> str:
    """
    画像ファイルのパスがpng,jpg,jpegのいずれかであるかをチェックし、
    不適切な場合はエラーを投げる。

    Args:
        path (str): 画像ファイルのパス

    Raises:
        argparse.ArgumentTypeError: 拡張子がpng,jpg,jpeg以外の場合に発生

    Returns:
        str: 検証済みの画像パス
    """
    ext = path.split('.')[-1].lower()  # 拡張子を取得し、小文字化
    if ext not in ("png", "jpg", "jpeg"):
        raise argparse.ArgumentTypeError(
            f"拡張子が不正です。png, jpg, jpeg のいずれかを指定してください: '{path}'"
        )
    return path


def check_threshold(value: str) -> float:
    """
    0~1の範囲内のfloat値であるかをチェックし、範囲外の場合はエラーを投げる。

    Args:
        value (str): コマンドライン引数として入力された文字列

    Raises:
        argparse.ArgumentTypeError: floatに変換できない場合、または0~1の範囲外の場合に発生

    Returns:
        float: 0~1の範囲内のfloat値
    """
    try:
        val = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError("THRESHOLD は 0 以上 1 以下の float で指定してください。")
    if not (0.0 <= val <= 1.0):
        raise argparse.ArgumentTypeError("THRESHOLD は 0.0 以上 1.0 以下で指定してください。")
    return val


def main():
    """
    メイン関数。
    コマンドライン引数から画像ファイルのパス2つと、閾値を受け取り、
    Dlib_api().verify() メソッドを使って同一人物かを判定する。
    """
    parser = argparse.ArgumentParser(
        description="2枚の画像から同一人物かを判定します。"
    )
    parser.add_argument(
        'image1',
        type=check_image_path,
        help='1枚目の画像パス (png, jpg, jpeg)'
    )
    parser.add_argument(
        'image2',
        type=check_image_path,
        help='2枚目の画像パス (png, jpg, jpeg)'
    )
    parser.add_argument(
        '--threshold',
        type=check_threshold,
        default=0.25,
        help='同一人物判定のコサイン類似度のしきい値 (0~1, default=0.25)'
    )

    # コマンドライン引数が不足している場合は、ヘルプを表示して終了します
    # （python verify.py のように実行され、最低限の引数がない場合など）
    if len(sys.argv) < 3:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    dlib_api = Dlib_api()
    result = dlib_api.verify(args.image1, args.image2, threshold=args.threshold)
    print(f"結果: {result}")


if __name__ == '__main__':
    main()
