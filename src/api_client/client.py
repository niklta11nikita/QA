import requests
from src.url import base_url_1


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

    def get(self, endpoint: str):
        """Публичный метод — основной интерфейс"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url)
        return response.json()

    def __log_request(self, url: str):
        """Приватный метод — детали реализации"""
        print(f"Запрос к {url}")

    def post(self, endpoint: str, json: dict):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self.__log_request(url)

        response = self.session.post(
            url,
            json=json,
            timeout=10
        )
        response.raise_for_status()

        return response.json()


client = APIClient(base_url_1)

print(client.base_url)
data = client.get("/posts/1")
