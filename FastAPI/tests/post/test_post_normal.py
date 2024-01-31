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
async def test_create_post(async_client):
    """
    /users/{user_id}/posts エンドポイントの POST リクエストをテストする。

    - ポストが正常に作成された場合、ステータスコードは 200 OK になる。
    - 作成されたポストの内容とユーザー情報が期待通りであることを確認する。
    """
    await async_client.post(
        "/users", json={"user_name": "anonymous", "password": "P@ssw0rd"}
    )
    response = await async_client.post(
        "/token", json={"user_name": "anonymous", "password": "P@ssw0rd"}
    )

    response_obj = response.json()
    access_token = response_obj["access_token"]
    response = await async_client.post(
        "/users/1/posts",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"contents": "ContentsTest"},
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["contents"] == "ContentsTest"
    assert response_obj["user_id"] == 1
    assert response_obj["post_id"] == 1


@pytest.mark.asyncio
async def test_read_post(async_client):
    """
    /users/{user_id}/posts エンドポイントの GET リクエストをテストする。

    - ユーザーが複数のポストを作成した場合、正しい数のポストが取得されることを確認する。
    - 取得されたポストの内容が期待通りであることを確認する。
    """
    await async_client.post(
        "/users", json={"user_name": "anonymous", "password": "P@ssw0rd"}
    )
    response = await async_client.post(
        "/token", json={"user_name": "anonymous", "password": "P@ssw0rd"}
    )

    response_obj = response.json()
    access_token = response_obj["access_token"]
    await async_client.post(
        "/users/1/posts",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"contents": "ContentsTest1"},
    )

    await async_client.post(
        "/users/1/posts",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"contents": "ContentsTest2"},
    )

    response = await async_client.get(
        "/users/1/posts",
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 2
    assert response_obj[0]["contents"] == "ContentsTest1"
    assert response_obj[1]["contents"] == "ContentsTest2"


@pytest.mark.asyncio
async def test_update_post(async_client):
    await async_client.post(
        "/users", json={"user_name": "anonymous", "password": "P@ssw0rd"}
    )
    response = await async_client.post(
        "/token", json={"user_name": "anonymous", "password": "P@ssw0rd"}
    )

    response_obj = response.json()
    access_token = response_obj["access_token"]
    await async_client.post(
        "/users/1/posts",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"contents": "ContentsTest1"},
    )

    response = await async_client.get(
        "/users/1/posts",
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["contents"] == "ContentsTest1"

    response = await async_client.put(
        "/users/1/posts/1",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"contents": "ContentsPutTest1"},
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["user_id"] == 1
    assert response_obj["post_id"] == 1
    assert response_obj["contents"] == "ContentsPutTest1"

    response = await async_client.get(
        "/users/1/posts",
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["contents"] == "ContentsPutTest1"


@pytest.mark.asyncio
async def test_delete_post(async_client):
    await async_client.post(
        "/users", json={"user_name": "anonymous", "password": "P@ssw0rd"}
    )
    response = await async_client.post(
        "/token", json={"user_name": "anonymous", "password": "P@ssw0rd"}
    )

    response_obj = response.json()
    access_token = response_obj["access_token"]
    await async_client.post(
        "/users/1/posts",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"contents": "ContentsTest1"},
    )
    await async_client.post(
        "/users/1/posts",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"contents": "ContentsTest2"},
    )

    response = await async_client.get(
        "/users/1/posts",
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 2
    assert response_obj[0]["contents"] == "ContentsTest1"

    response = await async_client.delete(
        "/users/1/posts/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj is None

    response = await async_client.get(
        "/users/1/posts",
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["contents"] == "ContentsTest2"
