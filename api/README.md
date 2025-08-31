## API Server

FAST API を利用した API サーバーです。

### Usage

```bash
$ uv sync  # Install dependencies
$ uv run src/main.py
```

## 認証

1. Google ID トークン検証: `/auth/exchange` エンドポイントで Google ID トークンを検証
2. アプリ用 JWT 発行: 検証成功後、アプリ専用の JWT トークンを発行
3. BFF からの Bearer 認証: 各 API エンドポイントで Bearer トークンを検証

### Dependencies

- [**uv**](https://docs.astral.sh/uv/)
- [**ruff**](https://docs.astral.sh/ruff/)
