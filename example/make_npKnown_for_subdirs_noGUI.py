"""
このスクリプトは、指定したディレクトリ配下のサブディレクトリにnpKnown.npzファイルを作成します。

変更点:
    - GUIによるディレクトリ選択を廃止し、コード中で指定します。
    - 指定ディレクトリ: /media/terms/2TB_Movie/face_data_backup/data

ファイル名例: make_npKnown_for_subdirs_noGUI.py

実行方法:
    python3 make_npKnown_for_subdirs_noGUI.py

"""

import os  # osモジュールをインポート
import sys  # sysモジュールをインポート

# 現在のスクリプトファイルがあるディレクトリを取得
dir: str = os.path.dirname(__file__)  # 現在のファイルのディレクトリ
parent_dir, _ = os.path.split(dir)    # 親ディレクトリを取得
sys.path.append(parent_dir)           # 親ディレクトリをパスに追加

from face01lib.load_preset_image import LoadPresetImage  # LoadPresetImageクラスのインポート


def create_npz_for_all_subdirs(root_dir, load_preset_image_obj):
    """
    指定したディレクトリ以下の1階層目のサブディレクトリに対して、
    npKnown.npzファイルを作成します。

    Args:
        root_dir (str): ルートディレクトリのパス。
        load_preset_image_obj (LoadPresetImage): 画像読み込み用のオブジェクト。
    """
    # os.walkでディレクトリツリーを走査
    for dirpath, dirnames, filenames in os.walk(root_dir):          # ディレクトリを再帰的に探索
        # 各サブディレクトリに対して
        for subdir in dirnames:                                    # サブディレクトリごとに処理
            # 除外サブディレクトリ一覧
            if subdir in ["not_me", "multipleFaces", "noFace", "same_default_files", "same_face", "目視_not_me", "modified_faice"]:
                # このサブディレクトリはスキップ
                continue
            else:
                # npKnown.npz ファイルパスを生成
                npz_file_path = os.path.join(dirpath, subdir, 'npKnown.npz')  # npKnown.npzファイルのパス
                if os.path.exists(npz_file_path):                 # npKnown.npzが既に存在する場合
                    print(f"{npz_file_path} は既に存在します。処理をスキップします。")  # 存在する旨を表示
                    continue                                      # スキップ
                else:
                    # ディレクトリ内に画像ファイルが存在するか確認
                    image_dir = os.path.join(dirpath, subdir)  # subdir側を指定 # 追加; subdirを含めたパスを指定することで正しい場所にnpKnown.npzを作成する
                    image_files = [file for file in os.listdir(image_dir) if file.lower().endswith('.png')]  # subdir配下を確認

                    if image_files:
                        npz_file_path = os.path.join(dirpath, subdir, 'npKnown.npz')
                        print(f"{npz_file_path} を作成します...")
                        load_preset_image_obj.load_preset_image(
                            deep_learning_model=1,
                            RootDir=image_dir,                # subdir配下をRootDirとして指定 # 追加; 正しいディレクトリにnpKnown.npzが生成されるようにする
                            preset_face_imagesDir=image_dir   # 顔画像が含まれるsubdir配下を指定 # 追加; npKnown.npzと画像ファイルのディレクトリ整合性を確保
                        )
                        print(f"{npz_file_path} を作成しました。")
                    else:
                        print(f"{os.path.join(dirpath, subdir)} に画像ファイルが見つかりませんでした。処理をスキップします。")


if __name__ == '__main__':
    # LoadPresetImageオブジェクトを生成
    load_preset_image_obj = LoadPresetImage()  # 画像読み込みオブジェクト作成 # 追加; 画像読み込み処理用オブジェクト

    # GUIによるディレクトリ選択を廃止し、コード内で指定
    # root_dir = "/media/terms/2TB_Movie/face_data_backup/data"
    root_dir = "/media/terms/2TB_Movie/face_data_backup/woman2"

    # root_dirが存在するかチェック
    if not os.path.exists(root_dir):  # ディレクトリが存在しない場合
        print(f"指定されたディレクトリ {root_dir} が存在しません。プログラムを終了します。")  # エラーメッセージ表示
        sys.exit(1)  # スクリプト終了

    # サブディレクトリごとにnpKnown.npzを作成
    create_npz_for_all_subdirs(root_dir, load_preset_image_obj)  # npKnown.npzファイルを作成 # 追加; 指定ディレクトリ以下でnpKnown.npzを一括作成
