## [v3.04.01] - 2024-12-21
### 追加
- `tests`ディレクトリを作成し、`pytest`によるテストコードを追加
- テストのためのサンプルデータを追加（例: `tests/data`）
### 変更
- プロジェクト構造に`tests`ディレクトリを追加

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
