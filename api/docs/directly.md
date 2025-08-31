# ディレクトリ構成

- api/
  - docs/
    - hoge.md
  - src/
    - routers/
    - schemas/
    - cruds/
    - models/
  - pyproject.toml
  - README.md
  - uv.lock

# 説明

## /src以下

- routers/: APIのエンドポイントを定義
- schemas/: APIのリクエストとレスポンスの型を定義
- cruds/: DBのCRUD操作を定義
- models/: ORMライブラリにおけるDBモデル

