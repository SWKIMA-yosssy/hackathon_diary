-- users テーブル
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,                   -- 自動採番のID（整数）
    auth_id VARCHAR(255) UNIQUE NOT NULL,    -- JWTに含まれるユーザー識別子（ユニーク制約）
    name VARCHAR(100) NOT NULL,              -- 表示名
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()  -- 作成日時（タイムゾーン付き）
);

-- posts テーブル
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,                   -- 投稿ID（自動採番）
    user_id INTEGER NOT NULL,                   -- usersテーブルのID (FK)
    content TEXT NOT NULL,                   -- 投稿内容
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), -- 投稿日時

    CONSTRAINT fk_user
        FOREIGN KEY(user_id) 
        REFERENCES users(id)
        ON DELETE CASCADE -- ユーザーが削除されたら、そのユーザーの投稿も全て削除する
);
