import httpx
import random


class EGRNRequestsAPI:
    """
    - post /api/v1/request/
        - cadnum: str
        - fio_is_provided: bool
        - order_id: int
    - post api/v1/request/{request_id: int}/startProduction
    - get /api/v1/request/{request_id: int}/r1r7
    - get /api/v1/request/{request_id: int}/registry
    """
    def __init__(self, host: str):
        self.host = host
        self.base_url = f"http://{host}/api/v1/request"

    async def _post(self, url: str, data: dict):
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.post(url, json=data)
            if not response.status_code == 200:
                raise RuntimeError(f"URL: {response.url}\nError: {response.text}")
            return response

    async def _get(self, url: str):
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url)
            if not response.status_code == 200:
                raise RuntimeError(f"URL: {response.url}\nError: {response.text}")
            return response

    async def create_request(self, cadnum: str, fio_is_provided: bool, order_id: int):
        url = self.base_url

        data = {
            "cadnum": cadnum,
            "fio_is_provided": fio_is_provided,
            "order_id": order_id,
        }

        response = await self._post(url, data)

        return response.json()

    async def reestr_to_production(self, request_id: int):
        url = f"{self.base_url}/{request_id}/startProduction"

        return await self._post(url, {})

    async def get_r1r7_file(self, request_id: int):
        url = f"{self.base_url}/{request_id}/r1r7/"

        response = await self._get(url)

        return response.content

    async def get_registry_file(self, order_id: int):
        url = f"{self.base_url}/{order_id}/registry/"

        response = await self._get(url)

        return response.content
