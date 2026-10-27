import requests
from src.api_client.models import PostResponse, PostRequest


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self._session = None

    @property
    def session(self):
        """Публичный геттер для сессии"""
        if self._session is None:
            self._session = requests.Session()
        return self._session

    def get(self, endpoint: str) -> PostResponse:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self.__log_request(url)
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return PostResponse.model_validate(response.json())

    def __log_request(self, url: str):
        """Приватный метод — детали реализации"""
        print(f"Запрос к {url}")

    def post(self, endpoint: str, request: PostRequest) -> PostResponse:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self.__log_request(url)

        response = self.session.post(
            url,
            json=request.model_dump(),
            timeout=10
        )
        response.raise_for_status()
        return PostResponse.model_validate(response.json())
