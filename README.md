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

  comments {
    int comment_id PK
    int post_id FK
    int user_id FK
    string comments
  }
```
# ER図

```mermaid
erDiagram
  users ||--o{ posts : "1人のユーザーは複数の投稿を持つ"
  users ||--o{ commnets : "1人のユーザーは複数のコメントを投稿"
  posts ||--o{ commnets : "1つの投稿に複数のコメントがつく"
```

# Flow
## sign up
```mermaid
sequenceDiagram
    autonumber
    actor ユーザー
    participant /users
    ユーザー->>/users: postリクエスト
	Note left of /users: user_name, password
    /users->>ユーザー: Status Code 200
```

## login
```mermaid
sequenceDiagram
    autonumber
    actor ユーザー
    participant /token
    ユーザー->>/token: postリクエスト
	Note left of /token: user_name, password
    /token->>ユーザー: Status Code 200
	Note left of /token: access_token, token_type
```

# memo

```
docker compose run --rm --entrypoint "poetry run pytest" api
docker compose run --rm --entrypoint "poetry run black ." api
docker compose run --rm --entrypoint "poetry run isort ." api
docker compose run --rm --entrypoint "poetry run pylint api" api
```
