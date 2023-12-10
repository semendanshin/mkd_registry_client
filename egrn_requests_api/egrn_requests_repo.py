import httpx
import random


class EGRNRequestsAPI:
    def __init__(self, host: str):
        self.host = host
        self.base_url = f"http://{host}/api/v1/request"

    async def post_request(self, request_data: dict) -> dict:
        url = "/"
        return {"id": random.randint(1, 10000)}

    async def get_request(self, request_id: int):
        with open('test.xlsx', 'rb') as file:
            return file.read()

    async def send_order_to_work(self, cadnum: str, fio_is_provided: bool):
        return await self.post_request({
            "cadnum": cadnum,
            "fio_is_provided": fio_is_provided,
        })
