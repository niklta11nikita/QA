
from unittest.mock import patch

from src.url import base_url_1
from src.api_client.client import APIClient
from src.api_client.models import PostRequest, PostResponse


class TestAPIClient:

    # Проверяет, что GET возвращает валидированную Pydantic-модель
    @patch("client.requests.Session")
    def test_get_returns_json(self, mock_session_class):
        session = mock_session_class.return_value
        response = session.get.return_value
        response.json.return_value = {
            "userId": 1,
            "id": 1,
            "title": "Test post",
            "body": "Test body"
        }

        client = APIClient(base_url=base_url_1)

        result = client.get("/posts/1")

        assert isinstance(result, PostResponse)
        assert result.userId == 1
        assert result.id == 1
        assert result.title == "Test post"
        assert result.body == "Test body"

    # Проверяет правильный URL и timeout=10
    @patch("client.requests.Session")
    def test_get_calls_correct_url(self, mock_session_class):
        session = mock_session_class.return_value
        response = session.get.return_value
        response.json.return_value = {
            "userId": 1,
            "id": 1,
            "title": "Test post",
            "body": "Test body"
        }

        client = APIClient(base_url=base_url_1)

        client.get("/posts/1")

        session.get.assert_called_once_with(
            f"{base_url_1}/posts/1",
            timeout=10
        )

    # Проверяет повторное использование сессии
    @patch("client.requests.Session")
    def test_session_is_reused(self, mock_session_class):
        session = mock_session_class.return_value
        session.get.return_value.json.return_value = {
            "userId": 1,
            "id": 1,
            "title": "Test post",
            "body": "Test body"
        }

        client = APIClient(base_url=base_url_1)

        client.get("/posts/1")
        client.get("/posts/2")

        mock_session_class.assert_called_once_with()
        assert session.get.call_count == 2

    # Проверяет отправку Pydantic-модели и валидацию ответа POST
    @patch("client.requests.Session")
    def test_post_sends_pydantic_model(self, mock_session_class):
        session = mock_session_class.return_value
        response = session.post.return_value
        response.json.return_value = {
            "title": "foo",
            "body": "bar",
            "userId": 1,
            "id": 101
        }

        client = APIClient(base_url=base_url_1)

        payload = PostRequest(
            title="foo",
            body="bar",
            userId=1
        )

        result = client.post("/posts", request=payload)

        session.post.assert_called_once_with(
            f"{base_url_1}/posts",
            json=payload.model_dump(),
            timeout=10
        )

        assert isinstance(result, PostResponse)
        assert result.title == "foo"
        assert result.body == "bar"
        assert result.userId == 1
        assert result.id == 101
