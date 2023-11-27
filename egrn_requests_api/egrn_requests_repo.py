import httpx


class EGRNRequestsAPI:
    def __init__(self, host: str):
        self.host = host

    async def post_request(self, request_data: dict) -> dict:
        return {"id": 1}

    async def get_request(self, request_id: int):
        ...
