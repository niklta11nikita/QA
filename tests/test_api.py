import pytest

from src.api_client.client import ApiClient


BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.mark.asyncio
async def test_get_post():
    async with ApiClient(BASE_URL) as client:
        response = await client.get("/posts/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert isinstance(data["title"], str)
    assert isinstance(data["body"], str)
    assert isinstance(data["userId"], int)


@pytest.mark.asyncio
async def test_get_all_posts():
    async with ApiClient(BASE_URL) as client:
        response = await client.get("/posts")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_create_post():
    payload = {
        "title": "Test title",
        "body": "Test body",
        "userId": 1,
    }

    async with ApiClient(BASE_URL) as client:
        response = await client.post("/posts", payload)

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]
    assert "id" in data