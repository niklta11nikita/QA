from unittest.mock import patch
from src.url import base_url_1
from client import APIClient


@patch("client.requests.Session")
#Проверяет, что метод get() возвращает данные из response.json()
def test_get_returns_json(mock_session_class):
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

    assert result["userId"] == 1
    assert result["id"] == 1
    assert result["title"] == "Test post"
    assert result["body"] == "Test body"


@patch("client.requests.Session")
#Проверяет, что клиент правильно собирает URL и передаёт timeout=10.
def test_get_calls_correct_url(mock_session_class):
    session = mock_session_class.return_value
    response = session.get.return_value
    response.json.return_value = {"id": 1}

    client = APIClient(base_url=base_url_1)

    client.get("/posts/1")

    session.get.assert_called_once_with(
        f"{base_url_1}/posts/1",
        timeout=10
    )


@patch("client.requests.Session")
#Проверяет, что при двух GET-запросах создаётся только одна сессия, а запросы выполняются дважды.
def test_session_is_reused(mock_session_class):
    session = mock_session_class.return_value
    session.get.return_value.json.return_value = {"id": 1}

    client = APIClient(base_url=base_url_1)

    client.get("/posts/1")
    client.get("/posts/2")

    mock_session_class.assert_called_once_with()
    assert session.get.call_count == 2

