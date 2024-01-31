import sqlite3

import pytest
import pytest_asyncio
import starlette.status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from api.db import Base, get_db
from api.main import app

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:  # Async用のengineとsessionを作成
    """
    テスト用の非同期HTTPクライアントを作成する fixture
    """
    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )

    # テスト用にオンメモリのSQLiteテーブルを初期化（関数ごとにリセット）
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # DIを使ってFastAPIのDBの向き先をテスト用DBに変更
    async def get_test_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    # テスト用に非同期HTTPクライアントを返却
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_user_unique_constraint(async_client):
    response = await async_client.post(
        "/users", json={"user_name": "anonymous", "password": "P@ssw0rd"}
    )

    response = await async_client.post(
        "/users", json={"user_name": "anonymous", "password": "P@ssw0rd"}
    )

    assert response.status_code == starlette.status.HTTP_400_BAD_REQUEST
    response_obj = response.json()

    # with pytest.raises(sqlite3.IntegrityError) as exc_info:
    #     response = await async_client.post(
    #         "/users", json={"user_name": "anonymous", "password": "P@ssw0rd"}
    #     )

    # assert "UNIQUE constraint failed: users.user_name" in str(exc_info.value)
    # assert resposen == "test"
    # assert response.status_code == starlette.status.HTTP_400_ERR
    # response_obj = response.json()
    # assert response_obj["user_name"] == "anonymous"
    # assert response_obj["password_hash"] == "b03ddf3ca2e714a6548e7495e2a03f5e824eaac9837cd7f159c67b90fb4b7342"


@pytest.mark.asyncio
async def test_update_user_invalid_token(async_client):
    await async_client.post(
        "/users", json={"user_name": "anonymous", "password": "P@ssw0rd"}
    )

    response = await async_client.get("/users")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["user_id"] == 1
    assert response_obj[0]["user_name"] == "anonymous"

    response = await async_client.post(
        "/token", json={"user_name": "anonymous", "password": "P@ssw0rd"}
    )

    response_obj = response.json()
    invalid_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJob2dlIiwiZXhwIjoxNzA2NTA4OTUxfQ.WG3V88hcyfuBq6Tgx01-6bumJK2QWZmO-r-mPecAgBs"
    response = await async_client.put(
        "/users/1",
        headers={"Authorization": f"Bearer {invalid_access_token}"},
        json={"user_name": "hoge", "password": "hoge"},
    )
    assert response.status_code == starlette.status.HTTP_401_UNAUTHORIZED

    response = await async_client.get("/users")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["user_id"] == 1
    assert response_obj[0]["user_name"] == "anonymous"


@pytest.mark.asyncio
async def test_delete_user_invalid_token(async_client):
    await async_client.post(
        "/users", json={"user_name": "anonymous", "password": "P@ssw0rd"}
    )
    await async_client.post("/users", json={"user_name": "hoge", "password": "hoge"})

    response = await async_client.get("/users")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 2
    assert response_obj[0]["user_id"] == 1
    assert response_obj[0]["user_name"] == "anonymous"
    assert response_obj[1]["user_id"] == 2
    assert response_obj[1]["user_name"] == "hoge"

    response = await async_client.post(
        "/token", json={"user_name": "anonymous", "password": "P@ssw0rd"}
    )

    response_obj = response.json()
    invalid_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJob2dlIiwiZXhwIjoxNzA2NTA4OTUxfQ.WG3V88hcyfuBq6Tgx01-6bumJK2QWZmO-r-mPecAgBs"
    response = await async_client.delete(
        "/users/1",
        headers={"Authorization": f"Bearer {invalid_access_token}"},
    )
    assert response.status_code == starlette.status.HTTP_401_UNAUTHORIZED

    response = await async_client.get("/users")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 2
    assert response_obj[0]["user_id"] == 1
    assert response_obj[0]["user_name"] == "anonymous"
    assert response_obj[1]["user_id"] == 2
    assert response_obj[1]["user_name"] == "hoge"
