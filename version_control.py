"""バージョンコントロールのためのスクリプト.

Summary:
    バージョンを上げる場合、FACE01_DEVフォルダからDISTフォルダへ必要なファイルだけをコピーしたり
    Dockerイメージを作ってDockerHubへアップロードしたりSphinxでドキュメントを生成してDISTフォルダへ
    コピーしたり煩雑な作業があり、その手順をすっかり忘れてしまいました。
    そこで上記工程をスクリプト化することにしました。

Args:
    None

Return:
    None

実行方法:
    python version_control.py

License for the Code.

Copyright Owner: Yoshitsugu Kesamaru
Please refer to the separate license file for the license of the code.
"""
import sphinx.ext.apidoc
import sphinx.cmd.build
import io
import os
import shutil
import subprocess
import sys
from glob import glob

# 標準出力と標準エラー出力をキャッチするためのバッファを作成
stdout_buffer = io.StringIO()
stderr_buffer = io.StringIO()

# # 標準出力と標準エラー出力をリダイレクト
# sys.stdout = stdout_buffer
# sys.stderr = stderr_buffer


"""作業ディレクトリを指定
"""
cwd = '/home/terms/bin/FACE01_DEV/'
os.chdir(cwd)
# subprocess.run(["play -v 1 -q 'voices/001これから自動バージ.wav'"], shell=True, check=True, cwd="/home/terms/bin/FACE01_DEV")


def main(dokokara):
    if dokokara == 1:
        rewrite_version()
        sphinx_function()
        # cython()
        copy_files()
        docker_image()
    elif dokokara == 2:
        sphinx_function()
        cython()
        copy_files()
        docker_image()
    elif dokokara == 3:
        cython()
        copy_files()
        docker_image()
    elif dokokara == 4:
        copy_files()
        docker_image()
    elif dokokara == 5:
        docker_image()


def rewrite_version():
    """バージョン情報の読み込み."""
    ver: str = ''
    with open('FACE01_DEV_VERSION') as f:
        lines = f.read()
        ver = lines.split('\n')[0]
        old_ver = lines.split('\n')[1]
        other = lines.split('\n')[2:]

    print("これから作るバージョンは", ver, "でよろしいですか？ [y/n]")
    subprocess.run(["play -v 1 -q voices/002これから作るバージ.wav"],
                   shell=True, check=True, cwd="/home/terms/bin/FACE01_DEV")

    if not 'y' == input():
        print("処理を終了します")
        exit(0)

    """①バージョン情報の書き換え
    """
    print("①バージョン情報の書き換え")
    subprocess.run(["play -v 1 -q voices/003それでは複数ある該.wav"],
                   shell=True, check=True, cwd="/home/terms/bin/FACE01_DEV")
    # sphinx_bk/origin/index.rst
    replacement_file_name: str = "/home/terms/bin/FACE01_DEV/sphinx_bk/origin/index.rst"
    with open(replacement_file_name) as r:
        lines: str = r.read()
    lines = lines.replace(old_ver, ver)
    with open(replacement_file_name, mode="w") as r:
        r.write(lines)

    # sphinx_bk/origin/conf.py
    replacement_file_name: str = "/home/terms/bin/FACE01_DEV/sphinx_bk/origin/conf.py"
    with open(replacement_file_name) as r:
        lines: str = r.read()
    lines = lines.replace(old_ver, ver)
    with open(replacement_file_name, mode="w") as r:
        r.write(lines)

    # README.md
    replacement_file_name: str = "/home/terms/bin/FACE01_DEV/README.md"
    with open(replacement_file_name) as r:
        lines: str = r.read()
    lines = lines.replace(old_ver, ver)
    with open(replacement_file_name, mode="w") as r:
        r.write(lines)

    # setup.py
    replacement_file_name: str = "/home/terms/bin/FACE01_DEV/setup.py"
    with open(replacement_file_name) as r:
        lines: str = r.read()
    lines = lines.replace(old_ver, ver)
    with open(replacement_file_name, mode="w") as r:
        r.write(lines)

    # make_DockerImages.sh
    replacement_file_name: str = "/home/terms/bin/FACE01_DEV/make_DockerImages.sh"
    with open(replacement_file_name) as r:
        lines: str = r.read()
    lines = lines.replace(old_ver, ver)
    with open(replacement_file_name, mode="w") as r:
        r.write(lines)

        subprocess.run(["play -v 1 -q voices/004書き換えが終わった.wav"],
                       shell=True, check=True, cwd="/home/terms/bin/FACE01_DEV")


def sphinx_function():
    """②SphinxによるDocファイルの自動生成.

    sphinxエラーまとめ.mdファイルを参照
    """
    print("②SphinxによるDocファイルの自動生成")

    # sphinx_bkフォルダからconf.pyとindex.rstを複製
    try:
        # ファイルのコピー
        shutil.copy2("/home/terms/bin/FACE01_DEV/sphinx_bk/origin/conf.py",
                     "/home/terms/bin/FACE01_DEV/sphinx/")
        shutil.copy2("/home/terms/bin/FACE01_DEV/sphinx_bk/origin/index.rst",
                     "/home/terms/bin/FACE01_DEV/sphinx/")
        print("sphinx_bkフォルダからconf.pyとindex.rstを複製しました")
    except Exception as e:
        print(e)
        # エラー処理
        exit(1)

    # sphinx-apidocの実行
    try:
        sphinx.ext.apidoc.main([
            "-f",
            "-o", "/home/terms/bin/FACE01_DEV/sphinx",
            "/home/terms/bin/FACE01_DEV/example",  # exampleディレクトリを追加
            "/home/terms/bin/FACE01_DEV/face01lib/"  # face01libディレクトリを追加
        ])
    except Exception as e:
        # エラーメッセージを出力
        print("エラーが発生しました:", e)
        print("標準出力:", stdout_buffer.getvalue())
        print("標準エラー出力:", stderr_buffer.getvalue())
        exit(1)
    except SystemExit:
        pass  # SystemExitの場合は何もしない

    # sphinx-buildの実行
    try:
        sphinx.cmd.build.main([
            "-b", "html",
            "-E",
            "/home/terms/bin/FACE01_DEV/sphinx",
            "/home/terms/bin/FACE01_DEV/docs"
        ])
    except Exception as e:
        print(e)
        # エラー処理
        exit(1)


def cython():
    """③Cython化.

    face01lib/compile.py, face01lib/arm_compile.py それぞれを参照
    """
    print("③Cython化")
    subprocess.run(["play -v 1 -q voices/006ライブラリファイル.wav"],
                   shell=True, check=True, cwd='/home/terms/bin/FACE01_DEV/')

    # 作業ディレクトリを移動
    try:
        os.chdir('/home/terms/bin/FACE01_DEV/face01lib/')
        print("作業ディレクトリを移動しました: ", os.getcwd())  # 現在の作業ディレクトリを出力
    except Exception as e:
        print(f"ディレクトリの移動に失敗しました: {e}")

    # 全ての.pyファイルを取得
    py_files = glob("*.py")
    # 除外するファイル名リスト
    excluded_files = ['compile.py', '__init__.py', 'arm_compile.py']
    # 除外ファイルを除くリストを作成
    py_files = [file for file in py_files if file not in excluded_files]
    # デバッグ用出力
    print(py_files)

    # pyファイルからpyxファイルを複製
    for py_file in py_files:
        shutil.copy(py_file, 'pyx/')

    try:
        # 作業ディレクトリをpyxディレクトリに移行
        os.chdir('/home/terms/bin/FACE01_DEV/face01lib/pyx')
        print("作業ディレクトリを移動しました: ", os.getcwd())  # 現在の作業ディレクトリを出力
    except Exception as e:
        print(f"ディレクトリの移動に失敗しました: {e}")
        print(cwd)

    # デバッグ用の出力
    print("現在の作業ディレクトリ: ", os.getcwd())
    print("CWDの内容: ", os.listdir(os.getcwd()))  # 現在のディレクトリの内容を出力

    # pyxフォルダの全ての.py拡張子を.pyxに変更
    for py_file in py_files:
        basename: str = py_file.split('.')[0]
        shutil.move(basename + '.py', basename + ".pyx")

    # Python仮想環境を起動
    # sourceコマンドは.でないとsubprocessで使用できない？
    activate_cmd: list = [". /home/terms/bin/FACE01_DEV/bin/activate"]
    try:
        ret = subprocess.run(activate_cmd, shell=True,
                             check=True, cwd="/home/terms/bin/FACE01_DEV")
    except subprocess.CalledProcessError as e:
        print(e)
        subprocess.run(["play -v 1 -q voices/error.wav"], shell=True,
                       check=True, cwd="/home/terms/bin/FACE01_DEV")

        exit(1)

    # compile.pyをpyxフォルダへ複製
    shutil.copy("/home/terms/bin/FACE01_DEV/face01lib/compile.py",
                "/home/terms/bin/FACE01_DEV/face01lib/pyx/")

    # arm_compile.pyをpyxフォルダへ複製
    # shutil.copy("/home/terms/bin/FACE01_DEV/face01lib/arm_compile.py", "/home/terms/bin/FACE01_DEV/face01lib/pyx/")

    # ###############################
    # pyxフォルダ内でコンパイル処理 -------------------
    # ###############################
    os.chdir('/home/terms/bin/FACE01_DEV/face01lib/pyx')
    print("作業ディレクトリを移動しました: ", os.getcwd())  # 現在の作業ディレクトリを出力

    # x86用バイナリ作成
    try:
        os.system("python compile.py build_ext --inplace")
    except Exception as e:  # エラーが発生した場合
        print(f"エラーが発生しました: {e}")
        # エラー音を再生
        os.system("play -v 1 -q /home/terms/bin/FACE01_DEV/voices/error.wav")
        exit(1)

    # ## arm用バイナリ作成
    # ### 参考：python3 setup.py build_ext --compiler=arm-linux-gnueabihf-gcc
    # arm_compile_cmd: list = ["python /home/terms/bin/FACE01_DEV/face01lib/pyx/arm_compile.py build_ext --compiler=arm-linux-gnueabihf-gcc --inplace"]
    # try:
    #     ret = subprocess.run(arm_compile_cmd, shell=True, check=True)
    # except subprocess.CalledProcessError as e:
    #     print(e)
    #     exit(1)
    # ---------------------------------------------------------------------
    try:
        # subprocess.run(["play -v 1 -q voices/error.wav"], shell=True, check=True, cwd="/home/terms/bin/FACE01_DEV")
        print("コンパイル完了。")
    except subprocess.CalledProcessError as e:
        print(e)
        subprocess.run(["play -v 1 -q voices/error.wav"], shell=True,
                       check=True, cwd="/home/terms/bin/FACE01_DEV")
        exit(1)

    os.chdir('/home/terms/bin/FACE01_DEV/face01lib/')
    # compile.pyと_init_.pyを除く
    py_files: list = glob("*[!'compile'|!'__init__']*.py")
    # FACE01_DEV/face01lib/のpyファイルはpy_filesフォルダへ移動
    for py_file in py_files:
        try:
            shutil.move(
                py_file, "/home/terms/bin/FACE01_DEV/face01lib/py_files/")
        except:
            continue


def copy_files():
    """④必要なファイルをFACE01_DEVからDISTフォルダに上書き複製."""
    print("④必要なファイルをFACE01_DEVからDISTフォルダに上書き複製")
    os.chdir('/home/terms/bin/FACE01_DEV/')
    subprocess.run(["play -v 1 -q voices/007必要なファイルをF.wav"],
                   shell=True, check=True, cwd="/home/terms/bin/FACE01_DEV")

    # .soファイルをDISTディレクトリに移動する
    so_files: list = glob("/home/terms/bin/FACE01_DEV/face01lib/*.so")
    for so_file in so_files:
        # file_name: str = so_file.split('/')[-1]
        # shutil.copy(so_file, "/home/terms/bin/FACE01_DEV/face01lib/" + file_name)
        shutil.copy(so_file, "/home/terms/bin/DIST/face01lib/")

    # 各フォルダ内を素の状態に戻す
    # pyxフォルダ
    shutil.rmtree("/home/terms/bin/FACE01_DEV/face01lib/pyx")
    os.mkdir("/home/terms/bin/FACE01_DEV/face01lib/pyx")

    # docsフォルダ
    shutil.copytree('/home/terms/bin/FACE01_DEV/docs/',
                    '/home/terms/bin/DIST/docs/', dirs_exist_ok=True)

    # exampleフォルダのpyファイル
    py_files: list = glob("/home/terms/bin/FACE01_DEV/example/*.py")
    for py_file in py_files:
        shutil.copy(py_file, '/home/terms/bin/DIST/example/')

    # imgフォルダ
    shutil.copytree('/home/terms/bin/FACE01_DEV/img/',
                    '/home/terms/bin/DIST/img/', dirs_exist_ok=True)

    # README.mdファイル
    shutil.copy("/home/terms/bin/FACE01_DEV/README.md",
                "/home/terms/bin/DIST/README.md")

    # imagesフォルダ
    shutil.copytree('/home/terms/bin/FACE01_DEV/images/',
                    '/home/terms/bin/DIST/images/', dirs_exist_ok=True)

    # dockerフォルダ
    shutil.copytree('/home/terms/bin/FACE01_DEV/docker/',
                    '/home/terms/bin/DIST/docker/', dirs_exist_ok=True)

    # assetsフォルダ
    shutil.copytree('/home/terms/bin/FACE01_DEV/assets/',
                    '/home/terms/bin/DIST/assets/', dirs_exist_ok=True)

    # config.iniファイル
    shutil.copy("/home/terms/bin/FACE01_DEV/config.ini",
                "/home/terms/bin/DIST/config.ini")

    # requirements.txtファイル
    shutil.copy("/home/terms/bin/FACE01_DEV/requirements.txt",
                "/home/terms/bin/DIST/requirements.txt")

    # make_DockerImages.shファイル
    shutil.copy("/home/terms/bin/FACE01_DEV/make_DockerImages.sh",
                "/home/terms/bin/DIST/make_DockerImages.sh")

    # INSTALL_FACE01_DEVファイル
    shutil.copy("/home/terms/bin/FACE01_DEV/INSTALL_FACE01_DEV.sh",
                "/home/terms/bin/DIST/INSTALL_FACE01_DEV.sh")


def docker_image():
    """⑤Docker image作成とpush.

    make_DockerImage.sh参照
    """
    print("⑤Docker image作成とpush")
    subprocess.run(["play -v 1 -q voices/008DISTフォルダに.wav"],
                   shell=True, check=True, cwd="/home/terms/bin/FACE01_DEV")
    subprocess.run(["play -v 1 -q voices/009ちなみにCPUやメ.wav"],
                   shell=True, check=True, cwd="/home/terms/bin/FACE01_DEV")

    cwd: str = "/home/terms/bin/DIST/"
    os.chdir(cwd)

    try:
        ret = subprocess.run("/home/terms/bin/DIST/make_DockerImages.sh",
                             shell=True, check=True, cwd="/home/terms/bin/DIST")
    except subprocess.CalledProcessError as e:
        print(e)
        subprocess.run(["play -v 1 -q voices/error.wav"], shell=True,
                       check=True, cwd="/home/terms/bin/FACE01_DEV")
        exit(1)


if __name__ == "__main__":
    # 変数`dokokara`の説明
    # 1: 最初から処理する
    # 2: sphinxから処理する
    # 3: Cythonから処理する
    # 4: 必要なファイルをFACE01_DEVからDISTフォルダに上書き複製から始める
    # 5: Docker image作成とpushから始める
    dokokara: int = 1

    main(dokokara)

    # rewrite_version()
    # sphinx_function()
    # cython()
    # copy_files()
    # docker_image()

    # subprocess.run(["play -v 1 -q voices/001全ての作業が滞りな….wav"], shell=True, check=True, cwd="/home/terms/bin/FACE01_DEV")
    # subprocess.run(["play -v 1 -q voices/002DISTフォルダを….wav"], shell=True, check=True, cwd="/home/terms/bin/FACE01_DEV")
