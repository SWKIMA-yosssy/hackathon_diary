# ディレクトリ構成

- docs/
  - hoge.md
- src/
  - routers/
  - cruds/
    - post.py
    - user.py
  - model.py
- db/
  - schema.sql
- pyproject.toml
- README.md

# 説明

## /src 以下

- routers/: API のエンドポイントを定義
- cruds/: DB の CRUD 操作を定義
- model.py: SQLModel を用いて ORM と Pydantic のモデルを定義

## /db 以下

- schema.sql でデータベースを起動した時用のスキーマを定義
