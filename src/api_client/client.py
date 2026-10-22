import httpx


class ApiClient:
    def __init__(self, base_url: str):
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=10.0,
        )

    async def get(self, endpoint: str) -> httpx.Response:
        return await self._client.get(endpoint)

    async def post(
        self,
        endpoint: str,
        data: dict,
    ) -> httpx.Response:
        return await self._client.post(endpoint, json=data)

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()