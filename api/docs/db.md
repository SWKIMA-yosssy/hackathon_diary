# DB 設計

## users

- id
  - PK, SK, not null
  - ユーザーを一意に識別する ID
- auth_id
  - UK, not null
  - JWT に含まれるユーザー識別子
- name
  - not null
  - 表示名
- created_at
  - not null
  - アカウント作成日時

## posts

- id
  - PK, SK, not null
    - 投稿を一意に識別する ID
- user_id
  - FK, not null
    - usersテーブルのID
- content
  - not null
  - 日記の内容
- created_at
  - not null
  - 投稿日時
