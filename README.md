# テーブル定義

```mermaid
erDiagram
  users {
    int user_id PK
    string user_name "ユーザー名"
	string password_hash "パスワードハッシュ"
  }

  posts {
	int post_id PK
	int user_id FK
	string contents
  }
```
# ER図

```mermaid
erDiagram
  users ||--o{ posts : "1人のユーザーは複数の投稿を持つ"
```

# Flow
## ユーザー作成

```mermaid
sequenceDiagram
    autonumber
    actor ユーザー
    participant /users
    ユーザー->>/users: postリクエスト
	Note left of /users: user_name
    /users->>ユーザー: Status Code 200
```

# memo

```
docker compose run --rm --entrypoint "poetry run pytest" api
docker compose run --rm --entrypoint "poetry run black ." api
docker compose run --rm --entrypoint "poetry run isort ." api
docker compose run --rm --entrypoint "poetry run pylint api" api
```
