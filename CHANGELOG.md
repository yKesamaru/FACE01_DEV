## [v3.04.02] - 2025-01-03
### 追加
- `verify`コマンド: face01libディレクトリ内
### 変更
- pyproject.toml: verifyコマンドのため。
- ~~Python仮想環境作成を廃止: 煩雑なため。~~
  - INSTALL_FACE01.sh
  - ~~Docker_INSTALL_FACE01.sh~~
  - ~~Docker_INSTALL_FACE01_CPU.sh~~
- Docker_INSTALL_FACE01.sh
  - GPU用の設定のところ。
- README.md
- MANIFEST.in

---

## [v3.04.01] - 2024-12-21
### 追加
- `tests`ディレクトリを作成し、`pytest`によるテストコードを追加
- テストのためのサンプルデータを追加（例: `tests/data`）
### 変更
- プロジェクト構造に`tests`ディレクトリを追加
- `face01lib.models.__init__.py`
  - `pkg_resources.resource_filename`は非推奨な為、`importlib.resources`へ変更
- `pip install git+https://github.com/yKesamaru/FACE01_DEV.git`
  - `pyproject.toml`を修正
  - `MANIFEST.ini`を修正

---

## [v3.03.04] - 2024-11-19
### 追加
- `CHANGELOG.md`
### 削除
- `FACE01_VERSION`
### 変更
- `make_DockerImages.sh`
- `Dockerfile_gpu`, `Dockerfile_no_gpu`
  - 作成されるdocker imageの軽量化
